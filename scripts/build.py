#!/usr/bin/env python3
"""Rebuild posts/ and data/posts.json from the Jellyfish Research Substack API.

Usage: python3 scripts/build.py   (requires beautifulsoup4, markdownify)
"""
import json, os, re, sys, time, urllib.parse, urllib.request
from bs4 import BeautifulSoup
from markdownify import MarkdownConverter

BASE = "https://jellyfishresearch.substack.com"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = {"User-Agent": "Mozilla/5.0"}
TOMAS_HANDLES = {"tomaspardinas"}
TOMAS_RE = re.compile(r"Tomas Pardi[ñn]as", re.I)
TOMAS_NAME = "Tomas Pardinas"

def get(url, binary=False):
    for i in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
                b = r.read()
                return b if binary else json.loads(b)
        except Exception:
            if i == 3: raise
            time.sleep(2 * (i + 1))

def archive():
    out, off = [], 0
    while True:
        page = get(f"{BASE}/api/v1/archive?sort=new&offset={off}&limit=50")
        if not page: break
        out += page; off += len(page)
    return out

def full_res(url):
    if not url: return url
    m = re.search(r"(https?(?:%3A|:)(?:%2F|/)(?:%2F|/)substack-post-media\.s3\.amazonaws\.com.*)$", url)
    if "substackcdn.com/image/fetch" in url and m:
        return urllib.parse.unquote(m.group(1))
    return url

def body_authors(soup):
    for p in soup.find_all("p"):
        m = re.match(r"^Authors?:\s*(.+)$", p.get_text(" ", strip=True))
        if m:
            return [re.sub(r"\s+", " ", a).strip() for a in re.split(r",|\band\b", m.group(1)) if a.strip()]
    return []

def norm(name):
    return TOMAS_NAME if TOMAS_RE.fullmatch(name.strip()) else name.strip()

def mdconv(html):
    return MarkdownConverter(heading_style="ATX", bullets="-", escape_underscores=False).convert(html)

def convert(html, img_dir, rel="images"):
    soup = BeautifulSoup(html, "html.parser")
    for sel in [".subscription-widget-wrap-editor", ".subscription-widget-wrap", ".button-wrapper",
                ".image-link-expand", "button", "svg", "form", ".share-dialog", ".post-ufi"]:
        for t in soup.select(sel): t.decompose()
    for t in soup.select(".digest-post-embed, .embedded-post-wrap"):
        try: a = json.loads(t.get("data-attrs", "{}"))
        except Exception: a = {}
        title = (a.get("title") or "Linked post").strip()
        url = a.get("canonical_url") or a.get("url") or ""
        if not url:
            l = t.find("a", href=True); url = l["href"] if l else ""
        new = soup.new_tag("p"); link = soup.new_tag("a", href=url); link.string = title
        new.append(link); t.replace_with(new)
    os.makedirs(img_dir, exist_ok=True)
    images, n = [], 0
    for fig in soup.find_all(["figure", "img"]):
        if fig.name == "img" and fig.find_parent("figure"): continue
        img = fig if fig.name == "img" else fig.find("img")
        if not img: continue
        src = None
        try: src = json.loads(img.get("data-attrs", "{}")).get("src")
        except Exception: pass
        src = full_res(src or img.get("src"))
        cap = fig.find("figcaption") if fig.name == "figure" else None
        alt = cap.get_text(" ", strip=True) if cap else (img.get("alt") or "")
        n += 1
        fname = f"{n:02d}-{os.path.basename(urllib.parse.urlparse(src).path) or f'image{n}'}"
        path = os.path.join(img_dir, fname)
        if not os.path.exists(path):
            with open(path, "wb") as f: f.write(get(src, binary=True))
        images.append({"file": fname, "source": src, "alt": alt})
        wrap = soup.new_tag("p"); wrap.append(soup.new_tag("img", src=f"{rel}/{fname}", alt=alt))
        if cap:
            ce = soup.new_tag("em"); ce.string = cap.get_text(" ", strip=True)
            wrap.append(soup.new_tag("br")); wrap.append(ce)
        container = fig.find_parent(class_="captioned-image-container") if fig.name == "figure" else None
        (container or fig).replace_with(wrap)
    for a in soup.select("a.footnote-anchor"):
        a.replace_with(f"[^{a.get_text(strip=True)}]")
    notes = []
    for d in soup.select("div.footnote"):
        num = d.select_one(".footnote-number").get_text(strip=True)
        content = d.select_one(".footnote-content")
        txt = mdconv(str(content)).strip() if content else ""
        txt = re.sub(r"\n{2,}", "\n\n    ", txt).replace("\u200b", "")
        notes.append(f"[^{num}]: {txt}"); d.decompose()
    md = mdconv(str(soup)).replace("\u200b", "")
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md).strip() + "\n"
    if notes: md += "\n" + "\n\n".join(notes) + "\n"
    return md, images

def yq(s): return json.dumps(s or "", ensure_ascii=False)

def main():
    arch = archive()
    tomas, others, skipped = [], [], []
    for p in arch:
        slug = p["slug"]
        post = get(f"{BASE}/api/v1/posts/{slug}")
        html = post.get("body_html") or ""
        soup = BeautifulSoup(html, "html.parser")
        bylines = [b.get("name") for b in post.get("publishedBylines") or []]
        handles = {b.get("handle") for b in post.get("publishedBylines") or []}
        battrs = body_authors(soup)
        authors = [norm(a) for a in (bylines or battrs)]
        for a in battrs:
            if norm(a) not in authors: authors.append(norm(a))
        is_tomas = bool(handles & TOMAS_HANDLES) or any(TOMAS_RE.search(a or "") for a in bylines + battrs)
        date = post["post_date"][:10]
        rec = dict(title=post["title"].strip(), subtitle=(post.get("subtitle") or "").strip(), slug=slug, date=date,
                   authors=authors, tags=[t["name"] for t in post.get("postTags") or []],
                   canonical_url=post.get("canonical_url") or f"{BASE}/p/{slug}")
        if not is_tomas:
            others.append(rec); continue
        if post.get("audience") != "everyone" or not html or soup.select(".paywall"):
            skipped.append({**rec, "reason": f"audience={post.get('audience')} / no full body"}); continue
        d = os.path.join(ROOT, "posts", f"{date}-{slug}")
        os.makedirs(d, exist_ok=True)
        md, images = convert(html, os.path.join(d, "images"))
        if not images: os.rmdir(os.path.join(d, "images"))
        fm = ["---", f"title: {yq(rec['title'])}", f"subtitle: {yq(rec['subtitle'])}", f"date: {date}",
              "authors:"] + [f"  - {yq(a)}" for a in authors] + \
             (["tags:"] + [f"  - {yq(t)}" for t in rec["tags"]] if rec["tags"] else ["tags: []"]) + \
             [f"canonical_url: {rec['canonical_url']}", "---", ""]
        note = f"> Originally published on [Jellyfish Research]({rec['canonical_url']}) on {date}.\n\n"
        with open(os.path.join(d, "index.md"), "w") as f:
            f.write("\n".join(fm) + "\n" + f"# {rec['title']}\n\n" +
                    (f"*{rec['subtitle']}*\n\n" if rec['subtitle'] else "") + note + md)
        rec.update(image_count=len(images),
                   word_count=len(re.findall(r"\b[\w’'-]+\b", soup.get_text(" "))),
                   path=f"posts/{date}-{slug}/index.md")
        tomas.append(rec)
        print("built", date, slug, len(images), "images", file=sys.stderr)
    tomas.sort(key=lambda r: r["date"], reverse=True)
    with open(os.path.join(ROOT, "data", "posts.json"), "w") as f:
        json.dump(tomas, f, indent=2, ensure_ascii=False); f.write("\n")
    with open(os.path.join(ROOT, ".cache_others.json"), "w") as f:
        json.dump({"archive_total": len(arch), "others": others, "skipped": skipped}, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    main()
