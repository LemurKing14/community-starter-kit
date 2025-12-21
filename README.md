# Pokemon Trading Card Cataloger

A lightweight command-line tool that scans Pokemon trading card images, extracts identifying
information, and looks up current market prices from the [Pokemon TCG API](https://pokemontcg.io/).
It can process a single image or a directory of card photos, then save the catalog as JSON.

## Features

- Optional OCR (via Tesseract) to detect the card name and collector number from the image.
- Fallback filename parsing so you can catalog cards even without OCR (e.g., `Pikachu-58-102.jpg`).
- Automatic price lookup using the public Pokemon TCG API with support for API keys.
- JSON export of cataloged cards, including set name, rarity, and market price when available.

## Installation

1. Install Python 3.9+.
2. (Optional) Install [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) if you want OCR-based scanning.
3. Install Python dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Catalog a single image and write `catalog.json`:

```bash
python card_catalog.py path/to/Pikachu-58-102.jpg
```

Catalog all images in a directory and write to a custom file:

```bash
python card_catalog.py /path/to/images --output my_cards.json
```

Provide an API key (otherwise uses the `POKEMON_TCG_API_KEY` environment variable):

```bash
python card_catalog.py /path/to/images --api-key YOUR_KEY
```

The script prints a summary for each card and saves the full catalog to JSON.

## Output example

```json
[
  {
    "name": "Pikachu",
    "number": "58/102",
    "set_name": "Base Set",
    "rarity": "Common",
    "price": 5.25,
    "currency": "USD",
    "image_path": "./images/Pikachu-58-102.jpg",
    "api_id": "base1-58"
  }
]
```

## Notes

- OCR is optional; the script will try OCR first and fall back to parsing the filename.
- Prices come from the `tcgplayer` market price reported by the Pokemon TCG API when available.
- Only `.png`, `.jpg`, and `.jpeg` files are scanned when pointing to a directory.

## License

This project is available under the [MIT License](LICENSE.md).
