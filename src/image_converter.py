#!/usr/bin/env python3
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image

def convert_images(folder: Path, to_format: str, out_dir: Path | None, dry_run: bool) -> list[tuple[Path, Path]]:
    if not folder.exists() or not folder.is_dir():
        raise FileNotFoundError(f"Folder not found: {folder}")

    to_format = to_format.lower().lstrip(".")
    if to_format not in {"png", "jpg", "jpeg", "webp"}:
        raise ValueError("to_format must be one of: png, jpg, jpeg, webp")

    if out_dir is None:
        out_dir = folder / "converted"
    out_dir.mkdir(parents=True, exist_ok=True)

    supported = {".png", ".jpg", ".jpeg", ".webp", ".tiff", ".bmp"}
    plan: list[tuple[Path, Path]] = []

    for p in sorted(folder.iterdir()):
        if not p.is_file() or p.suffix.lower() not in supported:
            continue
        target = out_dir / f"{p.stem}.{to_format}"
        plan.append((p, target))

    if dry_run:
        return plan

    for src, dst in plan:
        with Image.open(src) as im:
            if to_format in {"jpg", "jpeg"}:
                im = im.convert("RGB")
                im.save(dst, quality=92, optimize=True)
            else:
                im.save(dst)
    return plan

def main() -> int:
    parser = argparse.ArgumentParser(description="Convert image formats in a folder using Pillow.")
    parser.add_argument("folder", type=str, help="Folder containing images")
    parser.add_argument("--to", type=str, required=True, help="Output format: png/jpg/jpeg/webp")
    parser.add_argument("--out", type=str, default="", help="Output directory (default: <folder>/converted)")
    parser.add_argument("--dry-run", action="store_true", help="Show plan only")
    args = parser.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    out_dir = Path(args.out).expanduser().resolve() if args.out else None

    plan = convert_images(folder, args.to, out_dir, args.dry_run)
    for src, dst in plan:
        print(f"{src.name}  ->  {dst.name}")

    if args.dry_run:
        print("\n(Dry run only — no images converted.)")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
