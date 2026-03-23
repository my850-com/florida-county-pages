# Florida County Lis Pendens Pages

67 SEO-optimized HTML landing pages for Florida counties.

## Auto-Generated

- Source: Google Sheet "FLP SEO List" (Sherlock Data)
- Script: `generate_pages.py`
- Last updated: 2026-03-22

## Structure

- `{county-slug}.html` — One file per county
- `index.html` — Redirects to main site
- `generate_pages.py` — Rebuild script

## URLs

Each county page is at:
```
https://my850-com.github.io/florida-county-pages/{slug}.html
```

Examples:
- `/broward.html` — Broward County
- `/miami-dade.html` — Miami-Dade County
- `/palm-beach.html` — Palm Beach County

## Deployment

1. Push to GitHub
2. Enable GitHub Pages in repo settings (Source: main branch, / root)
3. Pages deploy automatically on push

## Data Sources

- Weekly filings: Google Sheet calculations
- Cities/FAQs: AI-generated + human reviewed
- Nearby counties: Geographic adjacency
