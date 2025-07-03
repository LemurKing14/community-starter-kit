import os
import sys
import argparse
import re
from typing import List, Set

try:
    from PIL import Image
    import pytesseract
except ImportError:
    Image = None
    pytesseract = None

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

try:
    import docx
except ImportError:
    docx = None


WORD_LIST_FILE = os.path.join(os.path.dirname(__file__), 'bip39_english.txt')


def load_wordlist(path: str) -> Set[str]:
    with open(path, 'r', encoding='utf-8') as f:
        return {w.strip() for w in f if w.strip()}


def tokenize(text: str) -> List[str]:
    return re.findall(r"[a-zA-Z]+", text.lower())


def find_seed_phrases(text: str, wordlist: Set[str], lengths=(12, 24)) -> List[str]:
    words = tokenize(text)
    results = []
    for length in lengths:
        for i in range(len(words) - length + 1):
            seq = words[i:i+length]
            if all(w in wordlist for w in seq):
                results.append(" ".join(seq))
    return results


def extract_text_from_file(path: str) -> str:
    ext = os.path.splitext(path)[1].lower()
    if ext in {'.txt', '.md'}:
        with open(path, 'r', errors='ignore', encoding='utf-8') as f:
            return f.read()
    if ext == '.pdf' and PyPDF2:
        text = []
        with open(path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                t = page.extract_text()
                if t:
                    text.append(t)
        return "\n".join(text)
    if ext in {'.docx', '.doc'} and docx:
        doc = docx.Document(path)
        return "\n".join(p.text for p in doc.paragraphs)
    if ext in {'.png', '.jpg', '.jpeg', '.gif', '.bmp'} and Image and pytesseract:
        try:
            img = Image.open(path)
            return pytesseract.image_to_string(img)
        except Exception:
            return ""
    return ""


def scan_paths(paths: List[str], wordlist: Set[str]):
    for root in paths:
        for dirpath, _, filenames in os.walk(root):
            for fname in filenames:
                fpath = os.path.join(dirpath, fname)
                text = extract_text_from_file(fpath)
                if not text:
                    continue
                seeds = find_seed_phrases(text, wordlist)
                if seeds:
                    print(f"Possible seeds in {fpath}:")
                    for seed in seeds:
                        print(f"  {seed}")


def main():
    parser = argparse.ArgumentParser(description="Scan directories for potential seed phrases")
    parser.add_argument('paths', nargs='+', help='Directories to scan')
    args = parser.parse_args()

    if not os.path.exists(WORD_LIST_FILE):
        sys.exit(f"Word list not found: {WORD_LIST_FILE}")

    wordlist = load_wordlist(WORD_LIST_FILE)
    scan_paths(args.paths, wordlist)


if __name__ == '__main__':
    main()
