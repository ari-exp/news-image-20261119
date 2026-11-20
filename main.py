"""Copy the rendered poster into the directory selected by MAKEFUN_OUTPUT_DIR."""

import os
import shutil
from pathlib import Path


def main():
    output_dir = Path(os.environ["MAKEFUN_OUTPUT_DIR"])
    output_dir.mkdir(parents=True, exist_ok=True)
    source = Path(__file__).resolve().parent / "entry.png"
    shutil.copy2(source, output_dir / "entry.png")


if __name__ == "__main__":
    main()
