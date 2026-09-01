"""Convert dish photos to WebP at two sizes and losslessly recompress the hero PNG.

For every *.png in img/dish/ (skipping any with real alpha transparency):
  - <name>.webp        max width 800px,  quality 82  (menu card thumbnail)
  - <name>-large.webp  max width 1400px, quality 85  (lightbox / zoomed view)
Aspect ratio is preserved and images are never upscaled. Original PNGs are kept.

img/hero-food.png has real transparency and is never converted to WebP; it is
only re-saved in place with lossless PNG recompression (alpha untouched).

Usage:
    pip install Pillow
    python optimize-images.py
"""
from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parent
DISH_DIR = ROOT / "dish"
HERO_FILE = ROOT / "hero-food.png"

THUMB_MAX_W = 800
THUMB_QUALITY = 82
LARGE_MAX_W = 1400
LARGE_QUALITY = 85


def has_real_alpha(im: Image.Image) -> bool:
    if im.mode not in ("RGBA", "LA"):
        return False
    lo, _hi = im.getchannel("A").getextrema()
    return lo < 255


def resized(im: Image.Image, max_w: int) -> Image.Image:
    if im.width <= max_w:
        return im
    new_h = round(im.height * max_w / im.width)
    return im.resize((max_w, new_h), Image.LANCZOS)


def convert_dish_photos():
    rows = []
    for png_path in sorted(DISH_DIR.glob("*.png")):
        with Image.open(png_path) as im:
            if has_real_alpha(im):
                print(f"SKIP (real alpha): {png_path.name}")
                continue
            rgb = im.convert("RGB")

            before_kb = png_path.stat().st_size / 1024

            thumb = resized(rgb, THUMB_MAX_W)
            thumb_path = png_path.with_suffix(".webp")
            thumb.save(thumb_path, "WEBP", quality=THUMB_QUALITY)

            large = resized(rgb, LARGE_MAX_W)
            large_path = png_path.with_name(png_path.stem + "-large.webp")
            large.save(large_path, "WEBP", quality=LARGE_QUALITY)

            thumb_kb = thumb_path.stat().st_size / 1024
            large_kb = large_path.stat().st_size / 1024

            rows.append((png_path.name, before_kb, thumb_path.name, thumb.width, thumb.height, thumb_kb,
                         large_path.name, large.width, large.height, large_kb))
    return rows


def recompress_hero():
    with Image.open(HERO_FILE) as im:
        before_kb = HERO_FILE.stat().st_size / 1024
        im.save(HERO_FILE, "PNG", optimize=True, compress_level=9)
    after_kb = HERO_FILE.stat().st_size / 1024
    return before_kb, after_kb


def main():
    rows = convert_dish_photos()

    print(f"\n{'ORIGINAL':45} {'BEFORE KB':>10}  {'THUMBNAIL':30} {'WxH':10} {'KB':>8}  {'LARGE':35} {'WxH':10} {'KB':>8}")
    total_before = total_thumb = total_large = 0.0
    for (orig, before_kb, tname, tw, th, tkb, lname, lw, lh, lkb) in rows:
        print(f"{orig:45} {before_kb:10.1f}  {tname:30} {str(tw)+'x'+str(th):10} {tkb:8.1f}  {lname:35} {str(lw)+'x'+str(lh):10} {lkb:8.1f}")
        total_before += before_kb
        total_thumb += tkb
        total_large += lkb

    print(f"\nDish photos: {len(rows)} converted")
    print(f"  Original PNGs total:   {total_before:9.1f} KB")
    print(f"  Thumbnails total:      {total_thumb:9.1f} KB")
    print(f"  Large versions total:  {total_large:9.1f} KB")
    print(f"  Thumb+large total:     {total_thumb+total_large:9.1f} KB  (vs {total_before:.1f} KB originals)")

    hero_before, hero_after = recompress_hero()
    print(f"\nHero PNG recompressed: {hero_before:.1f} KB -> {hero_after:.1f} KB")


if __name__ == "__main__":
    main()
