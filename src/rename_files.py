#!/usr/bin/env python3
from __future__ import annotations
import argparse
import re
from pathlib import Path


def safe_stem(name: str) -> str:
    stem = name.strip().lower().replace(" ", "_")
    stem = re.sub(r"[^a-z0-9_\-]+", "", stem)
    stem = re.sub(r"_+", "_", stem)
    return stem or "file"


def rename_files(folder: Path, prefix: str, start: int, dry_run: bool) -> list[tuple[Path, Path]]:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")

    files = [p for p in sorted(folder.iterdir()) if p.is_file()]
    plan: list[tuple[Path, Path]] = []
    counter = start

    for p in files:
        new_name = f"{prefix}{counter:03d}_{safe_stem(p.stem)}{p.suffix.lower()}"
        target = p.with_name(new_name)
        if target.exists() and target != p:
            target = p.with_name(f"{prefix}{counter:03d}_{safe_stem(p.stem)}_{p.stat().st_mtime_ns}{p.suffix.lower()}")
        plan.append((p, target))
        counter += 1

    if dry_run:
        return plan

    for src, dst in plan:
        src.rename(dst)
    return plan


def main() -> int:
    parser = argparse.ArgumentParser(description="Rename files in a folder with prefix + numbering + clean names.")
    parser.add_argument("folder", type=str, help="Target folder containing files")
    parser.add_argument("--prefix", type=str, default="item_", help="Prefix for renamed files (default: item_)")
    parser.add_argument("--start", type=int, default=1, help="Start number (default: 1)")
    parser.add_argument("--dry-run", action="store_true", help="Show rename plan without making changes")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    plan = rename_files(folder, args.prefix, args.start, args.dry_run)

    for src, dst in plan:
        print(f"{src.name}  ->  {dst.name}")

    if args.dry_run:
        print("\n(Dry run only — no files were renamed.)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
