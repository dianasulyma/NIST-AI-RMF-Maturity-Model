"""
This code extracts NIST AI RMF actions (GOVERN / MAP / MEASURE / MANAGE) from a PDF and save to CSV.

- Captures sentences like: "GOVERN 1.1: Legal and regulatory requirements ...".
- Grabs descriptions until the next action header (eg. "GOVERN 1.2 ...").
- removes whitespace for clean rows.

"""

from pathlib import Path
import re
import csv
from pypdf import PdfReader


PDF_PATH = Path("/Users/dianarogachova/Desktop/NIST.AI.100-1 copy.pdf")
CSV_PATH = Path("/Users/dianarogachova/Desktop/nist_actions.csv")


HEADER_REGEX = re.compile(
    r"""
    \b
    (?P<pillar>GOVERN|MAP|MEASURE|MANAGE)      # Pillar
    \s+
    (?P<id>\d+(?:\.\d+)*)                      # e.g., 1 or 1.1 or 2.3.4
    \s*:
    \s*
    (?P<title>.+?)                             
    (?=                                        
        \s+\b(?:GOVERN|MAP|MEASURE|MANAGE)\s+\d+(?:\.\d+)*\s*:
        | \Z
    )
    """,
    re.DOTALL | re.VERBOSE | re.IGNORECASE,
)

WS = re.compile(r"[ \t\f\v]+")


def read_pdf_text(pdf_path: Path) -> str:
    """Read a PDF into a single string with page breaks preserved."""
    reader = PdfReader(str(pdf_path))
    chunks = []
    for page in reader.pages:
        text = page.extract_text() or ""
        text = text.replace("\r", "\n")
        chunks.append(text.strip())
    return "\n\n".join(chunks)


def normalize_whitespace(s: str) -> str:
    s = WS.sub(" ", s)
    s = re.sub(r"\n\s*\n\s*\n+", "\n\n", s) 
    return s.strip()


def extract_actions(text: str):
    """Return a list of dict rows: Pillar, ID, Title."""
    rows = []
    for m in HEADER_REGEX.finditer(text):
        pillar = m.group("pillar").upper()
        action_id = m.group("id")
        title = normalize_whitespace(m.group("title"))
        rows.append(
            {
                "Pillar": pillar,
                "ID": action_id,
                "Action": title,
            }
        )
    return rows


def write_csv(rows, csv_path: Path):
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = ["Pillar", "ID", "Action"]
    with csv_path.open("w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main(pdf_path: Path = PDF_PATH, csv_path: Path = CSV_PATH):
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF not found: {pdf_path}")

    text = read_pdf_text(pdf_path)
    text = normalize_whitespace(text)

    rows = extract_actions(text)
    if not rows:
        raise RuntimeError(
            "No actions were extracted. Verify the PDF text and the header format "
        )

    write_csv(rows, csv_path)
    print(f"Wrote {len(rows)} rows → {csv_path}")


if __name__ == "__main__":
    main()
   