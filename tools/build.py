#!/usr/bin/env python3
"""Builds the static Leucy website from the fragments in src/.

Each fragment starts with a front-matter comment (title, description, nav) and holds only the page body.
This script wraps it in the shared head, header and footer and writes the finished page:
  src/index.html   -> index.html
  src/privacy.html -> privacy/index.html   (clean URL: /privacy/)
  src/404.html     -> 404.html
The generated HTML is committed, so any static host can serve the repo as is. Re-run after editing src/:

    python3 tools/build.py
"""
from __future__ import annotations

import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "src"

# ---- Site settings. Change these in one place. ----
SITE_NAME = "Leucy"
SITE_URL = "https://leucyapp.com"       # Used for canonical links, the sitemap and social cards.
SUPPORT_EMAIL = "support@dosely.app"     # Same address the app uses in lib/config.ts.
PRIVACY_EMAIL = "support@dosely.app"     # Requests about personal data. Can be a separate inbox later.
APP_STORE_URL = ""                       # Paste the App Store link once the app is live; buttons switch automatically.
EFFECTIVE_DATE = "November 9, 2026"
# ----------------------------------------------------

NAV = [
    ("screens", "Screens", "#screens"),
    ("features", "Features", "#features"),
    ("pricing", "Pricing", "#pricing"),
    ("privacy-home", "Privacy", "#privacy"),
    ("support", "Support", "support/"),
]

ICON_MENU = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg>'
ICON_APPLE = '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.37 12.6c-.02-2.2 1.8-3.26 1.88-3.31-1.03-1.5-2.62-1.7-3.18-1.73-1.35-.14-2.64.8-3.33.8-.69 0-1.74-.78-2.87-.76-1.47.02-2.83.86-3.59 2.17-1.54 2.66-.39 6.6 1.1 8.76.73 1.06 1.6 2.24 2.73 2.2 1.1-.04 1.51-.71 2.84-.71 1.32 0 1.7.71 2.86.69 1.18-.02 1.93-1.07 2.65-2.13.84-1.22 1.18-2.41 1.2-2.47-.03-.01-2.27-.87-2.29-3.51ZM14.2 6.13c.6-.74 1.01-1.75.9-2.77-.87.04-1.93.58-2.55 1.31-.56.65-1.05 1.69-.92 2.68.97.08 1.96-.49 2.57-1.22Z"/></svg>'


def app_button(prefix: str, small: bool = False) -> str:
    cls = "btn small" if small else "btn"
    if APP_STORE_URL:
        return f'<a class="{cls}" href="{APP_STORE_URL}">{ICON_APPLE}Download on the App Store</a>'
    return f'<a class="{cls}" href="{prefix}support/#launch">{ICON_APPLE}Coming soon to iPhone</a>'


def header(prefix: str, nav: str, home: bool) -> str:
    links = []
    for key, label, href in NAV:
        url = href if (home and href.startswith("#")) else (f"{prefix}{href}" if not href.startswith("#") else f"{prefix}{href}")
        cur = ' aria-current="page"' if key == nav else ""
        links.append(f'<a href="{url}"{cur}>{label}</a>')
    links.append(app_button(prefix, small=True))
    return f"""<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap nav">
    <a class="brand" href="{prefix or './'}"><img src="{prefix}assets/img/icon-192.png" alt="" width="34" height="34">{SITE_NAME}</a>
    <button class="nav-toggle" aria-expanded="false" aria-controls="nav-links" aria-label="Open menu">{ICON_MENU}</button>
    <nav class="nav-links" id="nav-links" aria-label="Main">
      {''.join(links)}
    </nav>
  </div>
</header>"""


def footer(prefix: str) -> str:
    year = date.today().year
    return f"""<footer class="site-footer">
  <div class="wrap">
    <div class="foot-grid">
      <div>
        <a class="brand" href="{prefix or './'}"><img src="{prefix}assets/img/icon-192.png" alt="" width="34" height="34">{SITE_NAME}</a>
        <p class="about">The GLP-1 tracker that scans your food, so you lose fat and keep your muscle.</p>
      </div>
      <div>
        <h4>Product</h4>
        <ul>
          <li><a href="{prefix}#features">Features</a></li>
          <li><a href="{prefix}#pricing">Pricing</a></li>
          <li><a href="{prefix}#privacy">Privacy by design</a></li>
          <li><a href="{prefix}support/">Support and FAQ</a></li>
        </ul>
      </div>
      <div>
        <h4>Legal</h4>
        <ul>
          <li><a href="{prefix}privacy/">Privacy Policy</a></li>
          <li><a href="{prefix}terms/">Terms of Use</a></li>
          <li><a href="{prefix}health-data/">Consumer Health Data Notice</a></li>
          <li><a href="{prefix}medical-disclaimer/">Medical Disclaimer</a></li>
        </ul>
      </div>
      <div>
        <h4>Your account</h4>
        <ul>
          <li><a href="{prefix}subscriptions/">Subscriptions and refunds</a></li>
          <li><a href="{prefix}delete-data/">Delete your data</a></li>
          <li><a href="{prefix}legal/">All policies</a></li>
          <li><a href="mailto:{SUPPORT_EMAIL}">{SUPPORT_EMAIL}</a></li>
        </ul>
      </div>
    </div>
    <div class="disclaimer">
      <p>Leucy is for tracking and education only. It is not a medical device and does not give medical advice, diagnose, treat or recommend doses. Always follow your healthcare provider. If you think you have a medical emergency, call your local emergency number.</p>
      <p>Ozempic®, Wegovy®, Rybelsus® and Saxenda® are registered trademarks of Novo Nordisk A/S. Zepbound®, Mounjaro® and Trulicity® are registered trademarks, and Foundayo™ is a trademark, of Eli Lilly and Company. They are used only to identify the medications the app can track. Leucy is not affiliated with, sponsored by or endorsed by Novo Nordisk or Eli Lilly. Apple, the Apple logo, iPhone and Apple Health are trademarks of Apple Inc.</p>
      <p>© {year} {SITE_NAME}. All rights reserved.</p>
    </div>
  </div>
</footer>"""


def page(meta: dict, body: str, prefix: str, path: str) -> str:
    home = path == ""
    title = meta["title"] if home else f'{meta["title"]} | {SITE_NAME}'
    canonical = f"{SITE_URL}/{path}"
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{meta['description']}">
<link rel="canonical" href="{canonical}">
<meta name="theme-color" content="#FBF6EC" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#111413" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{SITE_NAME}">
<meta property="og:title" content="{meta['title']}">
<meta property="og:description" content="{meta['description']}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{SITE_URL}/assets/img/og.jpg">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{prefix}favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="{prefix}assets/img/favicon-32.png">
<link rel="apple-touch-icon" href="{prefix}assets/img/apple-touch-icon.png">
<link rel="manifest" href="{prefix}site.webmanifest">
<link rel="preload" href="{prefix}assets/fonts/fraunces-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="{prefix}assets/fonts/inter-latin-wght-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{prefix}assets/css/site.css">
<script defer src="{prefix}assets/js/site.js"></script>
</head>
<body>
{header(prefix, meta.get('nav', ''), home)}
<main id="main">
{body}
</main>
{footer(prefix)}
</body>
</html>
"""


FRONT = re.compile(r"^\s*<!--(.*?)-->", re.S)


def parse(text: str) -> tuple[dict, str]:
    m = FRONT.match(text)
    meta: dict = {}
    if m:
        for line in m.group(1).strip().splitlines():
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip()
        text = text[m.end():]
    return meta, text.strip()


def fill(body: str, prefix: str) -> str:
    return (body.replace("{{root}}", prefix)
                .replace("{{email}}", SUPPORT_EMAIL)
                .replace("{{privacy_email}}", PRIVACY_EMAIL)
                .replace("{{effective}}", EFFECTIVE_DATE)
                .replace("{{app_button}}", app_button(prefix)))


def main() -> None:
    urls = []
    for src in sorted(SRC.glob("*.html")):
        meta, body = parse(src.read_text(encoding="utf-8"))
        name = src.stem
        if name == "index":
            out, prefix, path = ROOT / "index.html", "", ""
        elif name == "404":
            out, prefix, path = ROOT / "404.html", "/", "404.html"
        else:
            out, prefix, path = ROOT / name / "index.html", "../", f"{name}/"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(page(meta, fill(body, prefix), prefix, path), encoding="utf-8")
        if name != "404":
            urls.append(path)
        print(f"built {out.relative_to(ROOT)}")
    sitemap = "\n".join(f"  <url><loc>{SITE_URL}/{u}</loc></url>" for u in urls)
    (ROOT / "sitemap.xml").write_text(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{sitemap}\n</urlset>\n',
        encoding="utf-8")
    (ROOT / "robots.txt").write_text(f"User-agent: *\nAllow: /\n\nSitemap: {SITE_URL}/sitemap.xml\n", encoding="utf-8")
    print("built sitemap.xml, robots.txt")


if __name__ == "__main__":
    main()
