# main.py

import typer
from typing import Optional
from api import search_pubmed, fetch_details


app = typer.Typer()

@app.command()
def fetch(
    query: str = typer.Argument(..., help="Search query for PubMed"),
    max_results: int = typer.Option(10, "--max", "-m", help="Maximum number of results to fetch"),
    output_file: Optional[str] = typer.Option(None, "--output", "-o", help="Save results to CSV")
):
    """
    Fetch and display research papers from PubMed matching the query.
    """
    typer.echo(f"🔍 Searching PubMed for: {query}")
    ids = search_pubmed(query, max_results)

    if not ids:
        typer.echo("❌ No results found.")
        raise typer.Exit()

    typer.echo(f"✅ Found {len(ids)} result(s). Fetching details...")
    papers = fetch_details(ids)

    if not papers:
        typer.echo("⚠️ No paper details could be fetched.")
        raise typer.Exit()

    for i, paper in enumerate(papers, start=1):
        typer.echo(f"\n--- Result {i} ---")
        for key, value in paper.items():
            typer.echo(f"{key}: {value}")

    if output_file:
        import csv
        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=papers[0].keys())
            writer.writeheader()
            writer.writerows(papers)
        typer.echo(f"\n📁 Results saved to {output_file}")


if __name__ == "__main__":
    app()
