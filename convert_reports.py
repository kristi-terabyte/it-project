"""
Utility script to convert all lab*_report.html files into PDF using Playwright.
"""

from __future__ import annotations

from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Playwright is required. Install it via 'pip install playwright' "
        "and run 'playwright install chromium'."
    ) from exc


def convert_reports(base_dir: Path) -> None:
    html_files = sorted(base_dir.glob("lab*_report.html"))
    if not html_files:
        print("No lab*_report.html files found.")
        return

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        for html_file in html_files:
            output_pdf = html_file.with_suffix(".pdf")
            print(f"Converting {html_file.name} -> {output_pdf.name}")
            page.goto(html_file.resolve().as_uri())
            page.pdf(
                path=str(output_pdf),
                format="A4",
                print_background=True,
                margin={"top": "15mm", "bottom": "15mm", "left": "15mm", "right": "15mm"},
            )
        browser.close()


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    convert_reports(base_dir)


if __name__ == "__main__":
    main()


