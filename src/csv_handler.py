#!/usr/bin/env python3
from __future__ import annotations
import argparse
import csv
from pathlib import Path

def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)

def clean_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    cleaned: list[dict[str, str]] = []
    for r in rows:
        new = {k: (v or "").strip() for k, v in r.items()}
        if any(val != "" for val in new.values()):
            cleaned.append(new)
    return cleaned

def main() -> int:
    parser = argparse.ArgumentParser(description="Read, clean, and write CSV using Python's csv module.")
    parser.add_argument("input_csv", type=str, help="Input CSV path")
    parser.add_argument("--output", type=str, default="output/cleaned.csv", help="Output CSV path")
    args = parser.parse_args()

    inp = Path(args.input_csv).expanduser().resolve()
    out = Path(args.output).expanduser().resolve()
    out.parent.mkdir(parents=True, exist_ok=True)

    rows = read_csv(inp)
    if not rows:
        print("No rows found.")
        return 0

    cleaned = clean_rows(rows)
    fieldnames = list(rows[0].keys())
    write_csv(out, cleaned, fieldnames)

    print(f"Input rows: {len(rows)}")
    print(f"Cleaned rows: {len(cleaned)}")
    print(f"Saved: {out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
