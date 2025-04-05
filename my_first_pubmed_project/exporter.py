# exporter.py

import csv
from typing import List, Dict

def export_to_csv(data: List[Dict], filename: str = "pubmed_output.csv") -> None:
    """Export list of dictionaries to a CSV file."""
    if not data:
        print("No data to export.")
        return

    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

    print(f"✅ Data exported successfully to '{filename}'")
