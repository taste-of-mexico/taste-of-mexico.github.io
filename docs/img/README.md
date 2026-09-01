# Image optimization

Dish photos in `dish/` are large PNG exports (~2 MB each). `optimize-images.py` converts each one to two WebP versions:

- `<name>.webp` — max 800px wide, quality 82 — used as the menu card thumbnail.
- `<name>-large.webp` — max 1400px wide, quality 85 — used by the lightbox when a photo is tapped/clicked to zoom.

Original PNGs are kept (not deleted). `hero-food.png` has real transparency and is never converted — it's only re-saved with lossless PNG recompression.

## Usage

```
pip install Pillow
python optimize-images.py
```

Re-run whenever a dish photo is added or replaced in `dish/`, then update the corresponding `img` path (and `imgW`/`imgH`) in `../dishes-data.js` to point at the new `.webp` thumbnail.
