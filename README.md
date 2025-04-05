# 📘 my-first-pubmed-project

A command-line tool that fetches and extracts non-academic papers from PubMed, and optionally saves them to a CSV file.  
This project is built using Python Typer BeautifulSoup, and managed using Poetry.

---

## 🔍 What It Does

- Lets you search PubMed using a keyword or phrase.
- Fetches relevant paper titles, links, and summaries.
- Optionally saves the results to a `.csv` file.
- Provides a clean command-line interface (CLI).

---

## 📦 Installation

### ✅ Install from Test PyPI:

You can install the package from Test PyPI using below cmd from command prompt:

pip install -i https://test.pypi.org/simple/ my-first-pubmed-project

🛠️ Usage
After installation, run the CLI command:

get-papers-list "your search query here" --output results.csv
📌 Options
QUERY (required): Keyword or topic to search on PubMed.

--output/-o: CSV file to store the extracted papers (optional).

--debug/-d: Print detailed debug output (optional).

✅ Example
"get-papers-list "AI in Healthcare" --output ai_healthcare_results.csv"
🧾 Output
A CSV file containing:
PubmedID	
Title	
Publication Date	
Non-academicAuthor(s)	
CompanyAffiliation(s)	
Corresponding Author Email




