"""Profile CSV data quality without third-party packages.

Usage: python python/csv_profiler.py data.csv
Prints JSON with row counts, null percentages, and duplicate counts.
"""
import argparse
from collections import Counter
import csv
import json
from pathlib import Path


def profile_csv(path: Path, key_columns: list[str] | None = None) -> dict:
    """Read a UTF-8 CSV file and report basic column quality metrics."""
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        reader = csv.DictReader(handle)
        columns = reader.fieldnames
        if not columns:
            raise ValueError("CSV has no header")
        if len(set(columns)) != len(columns):
            raise ValueError("CSV has duplicate header names")
        if any(not col for col in columns):
            raise ValueError("CSV has an empty header name")
        keys = key_columns or columns
        missing_keys = set(keys) - set(columns)
        if missing_keys:
            raise ValueError(f"Unknown key columns: {sorted(missing_keys)}")
        blanks = Counter({col: 0 for col in columns})
        seen = set()
        duplicates = 0
        count = 0
        for row in reader:
            if None in row:
                raise ValueError(f"Row {count + 2} contains extra fields")
            count += 1
            for col in columns:
                if row[col] is None or not row[col].strip():
                    blanks[col] += 1
            key = tuple(row[col] for col in keys)
            if key in seen:
                duplicates += 1
            else:
                seen.add(key)
    return {
        "file": path.name,
        "rows": count,
        "key_columns": keys,
        "duplicate_keys": duplicates,
        "columns": {
            col: {"blank_count": blanks[col],
                  "blank_pct": round(100 * blanks[col] / count, 2) if count else 0.0}
            for col in columns
        },
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("csv_file", type=Path)
    parser.add_argument("--keys", nargs="+", help="Columns defining a unique record")
    args = parser.parse_args()
    try:
        report = profile_csv(args.csv_file, args.keys)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
