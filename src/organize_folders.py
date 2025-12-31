#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
import shutil

DEFAULT_MAP = {
    "images": {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".bmp", ".gif"},
    "documents": {".pdf", ".doc", ".docx", ".txt", ".md", ".rtf"},
    "spreadsheets": {".csv", ".xls", ".xlsx"},
    "archives": {".zip", ".rar", ".7z", ".tar", ".gz"},
    "code": {".py", ".js", ".ts", ".json", ".yaml", ".yml"},
}

def organize(folder: Path, dry_run: bool) -> list[tuple[Path, Path]]:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")

    moves: list[tuple[Path, Path]] = []
    for item in sorted(folder.iterdir()):
        if not item.is_file():
            continue
        ext = item.suffix.lower()

        target_dir = None
        for group, exts in DEFAULT_MAP.items():
            if ext in exts:
                target_dir = folder / group
                break

        if target_dir is None:
            target_dir = folder / "other"

        target_dir.mkdir(parents=True, exist_ok=True)
        target_path = target_dir / item.name
        if target_path.exists():
            target_path = target_dir / f"{item.stem}_{item.stat().st_mtime_ns}{item.suffix}"

        moves.append((item, target_path))

    if dry_run:
        return moves

    for src, dst in moves:
        shutil.move(str(src), str(dst))
    return moves

def main() -> int:
    parser = argparse.ArgumentParser(description="Organize files by extension into subfolders.")
    parser.add_argument("folder", type=str, help="Target folder")
    parser.add_argument("--dry-run", action="store_true", help="Show plan only")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    moves = organize(folder, args.dry_run)

    for src, dst in moves:
        print(f"{src.name}  ->  {dst.relative_to(folder)}")

    if args.dry_run:
        print("\n(Dry run only — no files were moved.)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
