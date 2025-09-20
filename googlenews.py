#!/usr/bin/env python3
import sys
import json
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs, urljoin
from datetime import datetime

OX_USER = "USERNAME"
OX_PASS = "APİ_KEY"
BASE_URL = "https://www.google.com"

def clean_google_link(link: str) -> str:
    if not link:
        return ""
    if link.startswith("/url?") or "/url?q=" in link:
        parsed = urlparse(link)
        qs = parse_qs(parsed.query)
        if "q" in qs and qs["q"]:
            return qs["q"][0]
        if "q=" in link:
            try:
                return link.split("q=", 1)[1].split("&", 1)[0]
            except Exception:
                pass
    return urljoin(BASE_URL, link)

def make_job(query: str, geo: str = "Turkey", limit: int = 50, pages: int = 1):
    payload = {
        "source": "google_search",
        "domain": "com",
        "query": query,
        "geo_location": geo,
        "locale": "tr-TR",
        "context": [{"key": "tbm", "value": "nws"}],
        "limit": limit,
        "pages": pages,
    }
    r = requests.post("https://realtime.oxylabs.io/v1/queries",
                      auth=(OX_USER, OX_PASS), json=payload, timeout=60)
    r.raise_for_status()
    return r.json()

def fetch_raw_html(job_id: str):
    url = f"https://data.oxylabs.io/v1/queries/{job_id}/results/1/content?type=raw"
    r = requests.get(url, auth=(OX_USER, OX_PASS), timeout=60)
    r.raise_for_status()
    return r.text

def parse_html_for_articles(html: str):
    soup = BeautifulSoup(html, "html.parser")
    found = []
    selectors = [
        "a h3",
        "h3",
        "a[class*='DY5T1d']",
        "a[class*='gPFEn']",
        "div[role='article'] h3",
        "article h3",
        ".ipQwMb",
        ".xrnccd h3",
        ".dbsr a",
        ".DY5T1d",
        ".WlydOe",
    ]
    for sel in selectors:
        for tag in soup.select(sel):
            a = tag if tag.name == "a" else tag.find_parent("a")
            if not a:
                possible = tag.find_next("a")
                if possible:
                    a = possible
            title = tag.get_text(strip=True)
            href = a.get("href") if a else None
            if href and title:
                href_clean = clean_google_link(href)
                found.append({"title": title, "link": href_clean})
    seen = set()
    deduped = []
    for it in found:
        key = (it["title"].strip(), it["link"].strip())
        if key in seen:
            continue
        seen.add(key)
        deduped.append({"title": it["title"].strip(), "link": it["link"].strip()})
    return deduped

def build_html(articles, filename, query=""):
    head = f"""<!doctype html>
<html lang="tr">
<head>
<meta charset="utf-8">
<title>Haber Sonuçları - {query}</title>
<style>
  body{{font-family:Arial,Helvetica,sans-serif;background:#f6f7fb;padding:20px}}
  .wrap{{max-width:1100px;margin:0 auto;background:#fff;padding:18px;border-radius:8px;box-shadow:0 6px 18px rgba(0,0,0,0.06)}}
  table{{width:100%;border-collapse:collapse;table-layout:fixed}}
  th,td{{padding:10px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}}
  th{{background:#0d6efd;color:#fff;position:sticky;top:0}}
  tr:nth-child(even){{background:#fafafa}}
  td.link-col{{max-width:500px;word-wrap:break-word;white-space:normal}}
  a{{color:#0d6efd;text-decoration:none}}
  a:hover{{text-decoration:underline}}
  .title{{font-weight:700}}
</style>
</head>
<body>
<div class="wrap">
<h2>Haber Sonuçları {(" - " + query) if query else ""}</h2>
<table>
<thead><tr><th style="width:40px">#</th><th>Başlık</th><th>Link</th></tr></thead>
<tbody>
"""
    rows = ""
    for i, art in enumerate(articles, start=1):
        title = art["title"].replace("<", "&lt;").replace(">", "&gt;")
        link = art["link"].replace("'", "&#x27;")
        rows += (
            f"<tr>"
            f"<td>{i}</td>"
            f"<td class='title'>{title}</td>"
            f"<td class='link-col'><a href='{link}' target='_blank' title='{link}'>{link}</a></td>"
            f"</tr>\n"
        )
    foot = """
</tbody></table>
</div>
</body>
</html>"""
    html = head + rows + foot
    with open(filename, "w", encoding="utf-8") as f:
        f.write(html)

def main(query: str, geo: str = "Turkey", limit: int = 50, pages: int = 1):
    job_json = make_job(query, geo, limit, pages)
    job_id = job_json["results"][0]["job_id"]
    html = fetch_raw_html(job_id)
    articles = parse_html_for_articles(html)
    if not articles:
        print("⚠️ Haber bulunamadı.")
        return
    today = datetime.now().strftime("%Y_%m_%d")
    base_name = f"{query.lower()}_{today}"
    json_file = f"{base_name}.json"
    html_file = f"{base_name}.html"
    with open(json_file, "w", encoding="utf-8") as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    build_html(articles, html_file, query=query)
    print(f"✅ {len(articles)} haber kaydedildi → {json_file}, {html_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Kullanım: python googlenews.py "aranacak kelime" [Ülke] [Limit] [Pages]')
        sys.exit(1)
    q = sys.argv[1]
    geo = sys.argv[2] if len(sys.argv) > 2 else "Turkey"
    limit = int(sys.argv[3]) if len(sys.argv) > 3 else 50
    pages = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    main(q, geo, limit, pages)
