"""Mirror niapower.org (Squarespace) pages into nia-web as static Jekyll pages.

Keeps each page's section and fluid-grid structure (the per-block grid positions for desktop
and mobile) so the layout matches; drops Squarespace scripts and platform attributes; points
images at local copies in assets/images/.

Usage: python3 -I mirror.py <live_dir> <img_map.tsv> <img_dir> <nia_web_dir>
"""
import html
import os
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser

LIVE, MAP, IMGDIR, WEB = sys.argv[1:5]

PAGES = [  # (live file, output file, permalink, title, redirect_from)
    ("home.html", "index.html", "/", "Nia", ["/home/", "/events/"]),
    ("about.html", "about.html", "/about/", "About", []),
    ("programs.html", "programs.html", "/programs/", "Programs", []),
    ("inspire.html", "inspire.html", "/inspire/", "Inspire", []),
    ("sumathi-radhakrishnan-memorial-award.html", "sumathi-radhakrishnan-memorial-award.html",
     "/sumathi-radhakrishnan-memorial-award/", "Sumathi Radhakrishnan Memorial Award", []),
    ("stories.html", "stories.html", "/stories/", "Stories", []),
    ("partners.html", "partners.html", "/partners/", "Partners", []),
    ("contact.html", "contact.html", "/contact/", "Contact", []),
    ("donate.html", "donate.html", "/donate/", "Donations", ["/cart/", "/contact-copy/"]),
    ("faqs.html", "faqs.html", "/faqs/", "FAQs", []),
    ("privacy-information.html", "privacy-information.html", "/privacy-information/", "Privacy Information", []),
    ("terms-conditions.html", "terms-conditions.html", "/terms-conditions/", "Terms & Conditions", []),
    ("cookies-statement.html", "cookies-statement.html", "/cookies-statement/", "Cookies Statement", []),
    ("post-divya.html", "stories/divya.html", "/stories/divya/", "Divya", []),
    ("post-jeyalakshmi.html", "stories/jeyalakshmi.html", "/stories/jeyalakshmi/", "Jeyalakshmi", []),
    ("post-kanmani.html", "stories/kanmani.html", "/stories/kanmani/", "Kanmani", []),
    ("post-ranjitha.html", "stories/ranjitha.html", "/stories/ranjitha/", "Ranjitha", []),
    ("post-nia-pathways.html", "stories/nia-pathways.html", "/stories/nia-pathways/", "Introducing Nia Pathways", []),
]

ICONS = {
    "linkedin": '<svg class="nia-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.02-3.04-1.85-3.04-1.85 0-2.14 1.45-2.14 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.85 3.6 0 4.27 2.37 4.27 5.46v6.28zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45z"/></svg>',
    "instagram": '<svg class="nia-icon" viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.16c3.2 0 3.58.01 4.85.07 1.17.05 1.8.25 2.23.41.56.22.96.48 1.38.9.42.42.68.82.9 1.38.16.42.36 1.06.41 2.23.06 1.27.07 1.65.07 4.85s-.01 3.58-.07 4.85c-.05 1.17-.25 1.8-.41 2.23-.22.56-.48.96-.9 1.38-.42.42-.82.68-1.38.9-.42.16-1.06.36-2.23.41-1.27.06-1.65.07-4.85.07s-3.58-.01-4.85-.07c-1.17-.05-1.8-.25-2.23-.41a3.72 3.72 0 0 1-1.38-.9 3.72 3.72 0 0 1-.9-1.38c-.16-.42-.36-1.06-.41-2.23C2.17 15.58 2.16 15.2 2.16 12s.01-3.58.07-4.85c.05-1.17.25-1.8.41-2.23.22-.56.48-.96.9-1.38.42-.42.82-.68 1.38-.9.42-.16 1.06-.36 2.23-.41C8.42 2.17 8.8 2.16 12 2.16zM12 0C8.74 0 8.33.01 7.05.07 5.78.13 4.9.33 4.14.63a5.88 5.88 0 0 0-2.13 1.38A5.88 5.88 0 0 0 .63 4.14C.33 4.9.13 5.78.07 7.05.01 8.33 0 8.74 0 12s.01 3.67.07 4.95c.06 1.27.26 2.15.56 2.91.31.79.72 1.46 1.38 2.13a5.88 5.88 0 0 0 2.13 1.38c.76.3 1.64.5 2.91.56C8.33 23.99 8.74 24 12 24s3.67-.01 4.95-.07c1.27-.06 2.15-.26 2.91-.56a5.88 5.88 0 0 0 2.13-1.38 5.88 5.88 0 0 0 1.38-2.13c.3-.76.5-1.64.56-2.91.06-1.28.07-1.69.07-4.95s-.01-3.67-.07-4.95c-.06-1.27-.26-2.15-.56-2.91a5.88 5.88 0 0 0-1.38-2.13A5.88 5.88 0 0 0 19.86.63C19.1.33 18.22.13 16.95.07 15.67.01 15.26 0 12 0zm0 5.84a6.16 6.16 0 1 0 0 12.32 6.16 6.16 0 0 0 0-12.32zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.85a1.44 1.44 0 1 0 0 2.88 1.44 1.44 0 0 0 0-2.88z"/></svg>',
}

DROP = {"script", "noscript", "link", "meta", "template", "iframe", "input", "select", "textarea", "label", "form"}
VOID = {"img", "br", "hr", "source", "col", "wbr"}
KEEP_ATTR = {"class", "style", "href", "src", "alt", "width", "height", "target", "rel", "aria-label",
             "datetime", "data-section-theme", "colspan", "rowspan",
             "viewbox", "points", "fill", "stroke", "stroke-miterlimit", "stroke-width", "d", "x", "y", "rx", "ry", "cx", "cy", "r"}

# ---------------------------------------------------------------- images
imgmap = {}
for line in open(MAP).read().strip().split("\n"):
    u, n = line.split("\t")
    imgmap[urllib.parse.urlsplit(u).path] = n.rsplit(".", 1)[0] + ".webp"
used_names = set(imgmap.values())
new_downloads = []


def local_image(url):
    url = html.unescape(url)
    if url.startswith("//"):
        url = "https:" + url
    parts = urllib.parse.urlsplit(url)
    if "squarespace" not in parts.netloc:
        return url
    path = parts.path
    if path in imgmap:
        return "assets/images/" + imgmap[path]
    base = urllib.parse.unquote(path.rsplit("/", 1)[1]).replace("+", "-").replace(" ", "-").lstrip("-").lower()
    stem = re.sub(r"[^a-z0-9.-]", "-", base.rsplit(".", 1)[0])
    stem = re.sub(r"-+", "-", stem).strip("-") or "image"
    name, i = stem + ".webp", 2
    while name in used_names:
        name, i = f"{stem}-{i}.webp", i + 1
    used_names.add(name)
    imgmap[path] = name
    dest = os.path.join(IMGDIR, name)
    if not os.path.exists(dest):
        req = urllib.request.Request(f"https://{parts.netloc}{path}?format=1500w", headers={"User-Agent": "Mozilla/5.0", "Accept": "image/webp,*/*"})
        with urllib.request.urlopen(req, timeout=60) as r, open(dest, "wb") as f:
            f.write(r.read())
        new_downloads.append(name)
    return "assets/images/" + name


def local_link(href):
    href = html.unescape(href).strip()
    for prefix in ("https://niapower.org", "http://niapower.org", "https://www.niapower.org"):
        if href.startswith(prefix):
            href = href[len(prefix):] or "/"
    if href.startswith("/") and not href.startswith("//"):
        path, _, frag = href.partition("#")
        path = path.split("?")[0]
        if path in ("/", "/home"):
            return "./" + (("#" + frag) if frag else "")
        if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
            path += "/"
        return path.lstrip("/") + (("#" + frag) if frag else "")
    return href


# ---------------------------------------------------------------- cleaner
class Cleaner(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=False)
        self.out = []
        self.drop_depth = 0
        self.stack = []

    def attrs_out(self, tag, attrs):
        a = dict(attrs)
        keep = []
        if tag == "img":
            src = a.get("data-src") or a.get("data-image") or a.get("src") or ""
            a["src"] = local_image(src.split("?")[0]) if src else ""
            fp = a.get("data-image-focal-point")
            st = a.get("style") or ""
            if fp and "object-position" not in st:
                x, y = (float(v) * 100 for v in fp.split(","))
                st += f";object-position:{x:g}% {y:g}%"
            a["style"] = st
            a.setdefault("alt", "")
        if tag == "a" and "href" in a:
            a["href"] = local_link(a["href"])
            if a.get("target") == "_blank":
                a["rel"] = "noopener"
        if "data-shape-name" in a:  # shape block: carry its corner radii into a style
            r = [a.get(f"data-border-{k}-radius", "0") for k in ("top-left", "top-right", "bottom-right", "bottom-left")]
            a["style"] = (a.get("style") or "") + ";--shape-radius:" + " ".join(f"{v}px" for v in r)
        for k, v in a.items():
            if v is None:
                continue
            if k == "id" and (v.startswith("block-") or v.startswith("item-")):
                keep.append((k, v))
            elif k in KEEP_ATTR:
                if k == "class":
                    v = " ".join(c for c in v.split() if not c.startswith("js-"))
                keep.append((k, v))
        keep = [("viewBox" if k == "viewbox" else k, v) for k, v in keep]
        return "".join(f' {k}="{html.escape(html.unescape(v), quote=True)}"' for k, v in keep)

    def handle_starttag(self, tag, attrs):
        if self.drop_depth:
            if tag not in VOID:
                self.drop_depth += 1
            return
        if tag in DROP:
            if tag not in VOID and tag not in ("link", "meta", "input"):
                self.drop_depth = 1
            return
        self.out.append(f"<{tag}{self.attrs_out(tag, attrs)}>")

    def handle_startendtag(self, tag, attrs):
        if self.drop_depth or tag in DROP:
            return
        end = "" if tag in VOID else "/"
        self.out.append(f"<{tag}{self.attrs_out(tag, attrs)}{end}>")

    def handle_endtag(self, tag):
        if self.drop_depth:
            if tag not in VOID:
                self.drop_depth -= 1
            return
        if tag in DROP or tag in VOID:
            return
        self.out.append(f"</{tag}>")

    def handle_data(self, data):
        if not self.drop_depth:
            self.out.append(data)

    def handle_entityref(self, name):
        if not self.drop_depth:
            self.out.append(f"&{name};")

    def handle_charref(self, name):
        if not self.drop_depth:
            self.out.append(f"&#{name};")

    def handle_comment(self, data):
        pass


def balanced(t, start, tag):
    """Return t[start:end] for the element starting at start (balanced on tag)."""
    depth, i = 0, start
    pat = re.compile(rf"<(/?){tag}\b[^>]*>", re.I)
    for m in pat.finditer(t, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return t[start:m.end()]
    raise ValueError("unbalanced " + tag)


def pre(t):
    # social icons: replace sprite <use> references with inline icons
    t = re.sub(r'<svg[^>]*>\s*<use[^>]*#(linkedin|instagram)-unauth-icon[^>]*>\s*</use>\s*(?:<use[^>]*>\s*</use>\s*)*</svg>',
               lambda m: ICONS[m.group(1)], t)
    # accordion buttons -> summary-like markup kept as plain elements
    return t


def clean(fragment):
    c = Cleaner()
    c.feed(pre(fragment))
    c.close()
    s = "".join(c.out)
    s = re.sub(r"[ \t]*\n\s*\n+", "\n", s)
    s = re.sub(r">\s{2,}<", "> <", s)
    return s.strip()


def front(title, permalink, redirects):
    fm = f'---\nlayout: mirror\ntitle: "{title}"\npermalink: {permalink}\n'
    if redirects:
        fm += "redirect_from:\n" + "".join(f"  - {r}\n" for r in redirects)
    return fm + "---\n"


footer_html = None
for live, out, permalink, title, redirects in PAGES:
    t = open(os.path.join(LIVE, live), encoding="utf-8").read()
    i = t.find('<main id="page"')
    body = clean(balanced(t, i, "main"))
    body = re.sub(r"^<main[^>]*>|</main>$", "", body).strip()
    body = re.sub(r'(<section\b[^>]*class=")(page-section)', r'\1nia-first \2', body, count=1)
    if footer_html is None:
        f = t.find('<footer class="sections"')
        footer_html = clean(balanced(t, f, "footer"))
    path = os.path.join(WEB, out)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(front(title, permalink, redirects) + "\n" + body + "\n")
    print(f"{out}: {len(body)//1024} KB")

os.makedirs(os.path.join(WEB, "_includes"), exist_ok=True)
with open(os.path.join(WEB, "_includes", "mirror-footer.html"), "w", encoding="utf-8") as fh:
    fh.write(footer_html + "\n")
print("footer:", len(footer_html) // 1024, "KB; new images:", new_downloads)
