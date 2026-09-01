# QR codes

Generates one QR PNG per dish, each pointing to `https://orale-authentic-mexican-flavor.github.io/dish.html?id=<dish-id>`.

## Usage

```
pip install qrcode[pil]
python generate_qr.py
```

Dish ids are read directly from `../dishes-data.js`, so the codes always match whatever dishes are currently in the menu — no list to keep in sync by hand. Re-run the script any time dishes are added, removed, or renamed, and commit the updated PNGs.

QR codes are generated for every dish id found in `dishes-data.js`, including dishes marked `active:false` (hidden from the menu). This is intentional so a printed QR is never orphaned. If a dish is deactivated, scanning its QR still works but `dish.html` shows a bilingual "not available" message instead of the dish details.
