# Will contain filtering heuristics for non-academic authors
import re

# Common non-academic organization indicators
NON_ACADEMIC_KEYWORDS = [
    "inc", "ltd", "llc", "corp", "company", "co.", "gmbh", "technologies", "solutions",
    "pharma", "industries", "pvt", "private limited", "startup", "consulting"
]

# Common academic indicators to filter out
ACADEMIC_KEYWORDS = [
    "university", "college", "institute", "school", "hospital", "center", "centre", "faculty"
]


def is_non_academic(affiliation: str) -> bool:
    """Check if an affiliation is likely non-academic."""
    affiliation = affiliation.lower()
    return any(keyword in affiliation for keyword in NON_ACADEMIC_KEYWORDS) and not any(
        keyword in affiliation for keyword in ACADEMIC_KEYWORDS
    )


def extract_non_academic_authors(authors: list, affiliations: list) -> list:
    """Return list of author names that are likely non-academic."""
    non_academic_authors = []
    for author, aff in zip(authors, affiliations):
        if aff and is_non_academic(aff):
            non_academic_authors.append(author)
    return non_academic_authors


def extract_company_affiliations(affiliations: list) -> list:
    """Return affiliations that appear to be companies."""
    return [aff for aff in affiliations if aff and is_non_academic(aff)]


def extract_emails(text: str) -> list:
    """Extract all valid email addresses from given text."""
    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    return re.findall(email_pattern, text)
