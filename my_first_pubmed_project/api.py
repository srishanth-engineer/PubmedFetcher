from typing import List, Dict, Tuple, Optional
import requests
from bs4 import BeautifulSoup

from my_first_pubmed_project.exporter import export_to_csv

from my_first_pubmed_project.utils import (
    extract_emails,
    extract_company_affiliations,
    extract_non_academic_authors
)

import typer

BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"


def search_pubmed(query: str, max_results: int = 20) -> List[str]:
    """Search PubMed for a query and return a list of PubMed IDs."""
    url = f"{BASE_URL}/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "retmode": "json"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    return data.get("esearchresult", {}).get("idlist", [])


def fetch_details(pubmed_ids: List[str]) -> List[Dict]:
    """Fetch details for each PubMed ID using efetch and parse paper information."""
    if not pubmed_ids:
        return []

    url = f"{BASE_URL}/efetch.fcgi"
    params = {
        "db": "pubmed",
        "id": ",".join(pubmed_ids),
        "retmode": "xml"
    }

    response = requests.get(url, params=params)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, features="xml")
    articles = soup.find_all("PubmedArticle")
    results = []

    for article in articles:
        try:
            pmid = article.PubmedData.ArticleIdList.find("ArticleId", {"IdType": "pubmed"}).text
            title = article.MedlineCitation.Article.ArticleTitle.text
            pub_date = extract_publication_date(article)

            authors, affiliations, companies = extract_authors(article)
            affiliations_text = " ".join(filter(None, affiliations))
            emails = extract_emails(affiliations_text)
            corresponding_email = emails[0] if emails else "Not Found"

            non_academic_authors = extract_non_academic_authors(authors, affiliations)
            company_affiliations = extract_company_affiliations(affiliations)

            results.append({
                "PubmedID": pmid,
                "Title": title,
                "Publication Date": pub_date,
                "Non-academicAuthor(s)": "; ".join(non_academic_authors),
                "CompanyAffiliation(s)": "; ".join(company_affiliations),
                "Corresponding Author Email": corresponding_email
            })
        except Exception as e:
            typer.echo(f"⚠️ Error parsing article: {e}")
            continue

    return results


def extract_publication_date(article) -> str:
    """Extract publication date from article."""
    try:
        date_elem = article.MedlineCitation.Article.Journal.JournalIssue.PubDate
        year = date_elem.Year.text if date_elem.Year else "Unknown"
        month = date_elem.Month.text if hasattr(date_elem, 'Month') else ""
        day = date_elem.Day.text if hasattr(date_elem, 'Day') else ""
        return f"{year}-{month}-{day}".strip("-")
    except Exception:
        return "Unknown"


def extract_authors(article) -> Tuple[List[str], List[str], List[str]]:
    """Extract author affiliations, companies, and non-academic authors."""
    affiliations = []
    companies = []
    non_academic = []

    author_list = article.MedlineCitation.Article.find_all("Author")
    for author in author_list:
        affiliation = author.find("AffiliationInfo")
        if affiliation and affiliation.Affiliation:
            aff_text = affiliation.Affiliation.text
            affiliations.append(aff_text)

            if is_non_academic(aff_text):
                if author.LastName:
                    non_academic.append(author.LastName.text)
                companies.append(aff_text)

    return affiliations, list(set(companies)), non_academic


def is_non_academic(affiliation: str) -> bool:
    """Heuristic to determine if an affiliation is non-academic."""
    academic_keywords = [
        "university", "institute", "college", "hospital",
        "school", "laboratory", "centre", "center"
    ]
    return not any(keyword in affiliation.lower() for keyword in academic_keywords)


def fetch_and_process_papers(query: str, file: str = None, debug: bool = False, max_results: int = 100):
    """Main orchestrator function to search, fetch, process, and save results."""
    if debug:
        typer.echo(f"🔍 Searching PubMed for: '{query}'")

    ids = search_pubmed(query)
    if not ids:
        typer.echo("⚠️ No results found for the given query.")
        raise typer.Exit()

    if debug:
        typer.echo(f"✅ Found {len(ids)} articles. Fetching details...")

    try:
        papers = fetch_details(ids)
    except Exception as e:
        typer.echo(f"❌ Error while fetching details: {e}")
        raise typer.Exit(code=1)

    if not papers:
        typer.echo("⚠️ No paper details could be parsed.")
        raise typer.Exit()

    if file:
        export_to_csv(papers, file)
        typer.echo(f"📁 Results saved to '{file}'")
    else:
        for paper in papers:
            typer.echo(paper)
