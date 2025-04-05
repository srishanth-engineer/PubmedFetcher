import typer
from my_first_pubmed_project.api import fetch_and_process_papers

app = typer.Typer()

@app.command()
def get_papers_list(
    query: str,
    file: str = typer.Option(None, "--file", "-f", help="Filename to save results as CSV."),
    debug: bool = typer.Option(False, "--debug", "-d", help="Print debug output."),
    max_results: int = typer.Option(100, "--max", "-m", help="Maximum number of results to fetch."),
):
    fetch_and_process_papers(query, file, debug, max_results)
