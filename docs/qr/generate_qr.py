"""Generate a QR code PNG per dish, pointing to its dish.html detail page.

Reads dish ids straight out of ../dishes-data.js (regex-extracted, so this
script never needs its own copy of the dish list) and writes one PNG per
dish into this folder, named <id>.png.
"""
import re
from pathlib import Path

import qrcode

BASE_URL = "https://orale-authentic-mexican-flavor.github.io/dish.html?id="
DATA_FILE = Path(__file__).resolve().parent.parent / "dishes-data.js"
OUTPUT_DIR = Path(__file__).resolve().parent


def get_dish_ids():
    text = DATA_FILE.read_text(encoding="utf-8")
    return re.findall(r'\{id:"([a-z0-9-]+)"', text)


def main():
    ids = get_dish_ids()
    if not ids:
        raise SystemExit(f"No dish ids found in {DATA_FILE}")

    for dish_id in ids:
        url = BASE_URL + dish_id
        img = qrcode.make(url)
        out_path = OUTPUT_DIR / f"{dish_id}.png"
        img.save(out_path)
        print(f"{dish_id}.png  ->  {url}")

    print(f"\nGenerated {len(ids)} QR codes in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
