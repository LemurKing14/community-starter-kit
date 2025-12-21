"""
Pokemon trading card scanner and cataloger.

This script can scan card images, try to extract identifying data (name, number, set),
and look up current market values from the Pokemon TCG API.
"""
from __future__ import annotations

import argparse
import json
import os
import re
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Iterable, List, Optional

import requests

try:  # Optional dependency, so keep import local and guarded
    from PIL import Image
    import pytesseract
except Exception:  # pragma: no cover - best effort import for optional features
    Image = None
    pytesseract = None


@dataclass
class CardRecord:
    name: str
    number: Optional[str]
    set_name: Optional[str]
    rarity: Optional[str]
    price: Optional[float]
    currency: Optional[str]
    image_path: str
    api_id: Optional[str]


class PokemonTCGClient:
    """Minimal client for the Pokemon TCG API.

    Prices are pulled from the tcgplayer market price when available.
    """

    BASE_URL = "https://api.pokemontcg.io/v2"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("POKEMON_TCG_API_KEY")

    def search_card(self, name: str, number: Optional[str], set_name: Optional[str]) -> Optional[dict]:
        query_parts = [f'name:"{name}"']
        if number:
            query_parts.append(f"number:{number}")
        if set_name:
            query_parts.append(f'set.name:"{set_name}"')
        params = {"q": " ".join(query_parts), "orderBy": "-set.releaseDate"}
        headers = {"User-Agent": "card-catalog-script/1.0"}
        if self.api_key:
            headers["X-Api-Key"] = self.api_key

        response = requests.get(f"{self.BASE_URL}/cards", params=params, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json().get("data", [])
        return data[0] if data else None

    @staticmethod
    def parse_price(card_data: dict) -> tuple[Optional[float], Optional[str]]:
        tcgplayer = card_data.get("tcgplayer") or {}
        prices = tcgplayer.get("prices") or {}
        for variant in ("holofoil", "reverseHolofoil", "normal", "1stEditionHolofoil", "unlimitedHolofoil"):
            price_info = prices.get(variant)
            if price_info and "market" in price_info:
                return price_info["market"], tcgplayer.get("currency", "USD")
        return None, None


class ImageScanner:
    """Extract metadata from card images.

    The scanner uses Tesseract OCR when available and falls back to file naming
    conventions if OCR fails. OCR is optional to keep the script lightweight.
    """

    number_pattern = re.compile(r"(\d{1,3})\s*/\s*(\d{1,3})")

    def __init__(self) -> None:
        self.ocr_available = Image is not None and pytesseract is not None

    def scan(self, image_path: Path) -> tuple[Optional[str], Optional[str]]:
        """Return a tuple of (name, number) detected for the image."""
        if self.ocr_available:
            name, number = self._scan_with_ocr(image_path)
            if name or number:
                return name, number
        return self._scan_from_filename(image_path)

    def _scan_with_ocr(self, image_path: Path) -> tuple[Optional[str], Optional[str]]:
        try:
            with Image.open(image_path) as img:
                text = pytesseract.image_to_string(img)
        except Exception:
            return None, None
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        name = self._extract_probable_name(lines)
        number = self._extract_number(lines)
        return name, number

    def _scan_from_filename(self, image_path: Path) -> tuple[Optional[str], Optional[str]]:
        stem = image_path.stem.replace("_", " ")
        parts = stem.split("-")
        name = parts[0].strip().title() if parts else None
        number = None
        match = self.number_pattern.search(stem)
        if match:
            number = f"{match.group(1)}/{match.group(2)}"
        return name, number

    def _extract_number(self, lines: Iterable[str]) -> Optional[str]:
        for line in lines:
            match = self.number_pattern.search(line)
            if match:
                return f"{match.group(1)}/{match.group(2)}"
        return None

    def _extract_probable_name(self, lines: List[str]) -> Optional[str]:
        for line in lines:
            clean = re.sub(r"[^A-Za-z'\s-]", "", line).strip()
            if not clean:
                continue
            if len(clean.split()) <= 3 and any(ch.isalpha() for ch in clean):
                return clean
        return None


class CardCataloger:
    def __init__(self, api_key: Optional[str]):
        self.scanner = ImageScanner()
        self.client = PokemonTCGClient(api_key)

    def catalog_path(self, target: Path) -> List[CardRecord]:
        paths = self._collect_image_paths(target)
        catalog = []
        for path in paths:
            name, number = self.scanner.scan(path)
            card_data = self.client.search_card(name or "", number, None) if name else None
            price, currency = (None, None)
            set_name = rarity = api_id = None
            if card_data:
                price, currency = PokemonTCGClient.parse_price(card_data)
                set_name = card_data.get("set", {}).get("name")
                rarity = card_data.get("rarity")
                api_id = card_data.get("id")
            record = CardRecord(
                name=name or "Unknown",
                number=number,
                set_name=set_name,
                rarity=rarity,
                price=price,
                currency=currency,
                image_path=str(path),
                api_id=api_id,
            )
            catalog.append(record)
        return catalog

    def _collect_image_paths(self, target: Path) -> List[Path]:
        if target.is_file():
            return [target]
        supported = {".png", ".jpg", ".jpeg"}
        return sorted([p for p in target.iterdir() if p.suffix.lower() in supported])


def save_catalog(records: List[CardRecord], output: Path) -> None:
    output.write_text(json.dumps([asdict(rec) for rec in records], indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Scan Pokemon trading cards and fetch prices.")
    parser.add_argument("path", type=Path, help="Image file or directory of images to catalog")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("catalog.json"),
        help="Where to write catalog results (JSON)",
    )
    parser.add_argument("--api-key", help="Pokemon TCG API key (defaults to POKEMON_TCG_API_KEY env var)")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    cataloger = CardCataloger(args.api_key)
    records = cataloger.catalog_path(args.path)
    save_catalog(records, args.output)
    for rec in records:
        price_str = f"{rec.currency} {rec.price:.2f}" if rec.price is not None else "unknown"
        print(f"{rec.name} ({rec.number or 'n/a'}) - {rec.set_name or 'unknown set'} - {price_str}")
    print(f"Saved catalog to {args.output}")


if __name__ == "__main__":
    main()
