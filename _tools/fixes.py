"""Content changes agreed with Arun (2026-11-26), applied on top of the mirrored pages.

Usage: python3 -I fixes.py <nia-web dir>
"""
import os
import re
import sys

W = sys.argv[1]


def rd(p):
    return open(os.path.join(W, p), encoding="utf-8").read()


def wr(p, s):
    open(os.path.join(W, p), "w", encoding="utf-8").write(s)


def balanced_div(s, start):
    depth = 0
    for m in re.compile(r"<(/?)div\b[^>]*>").finditer(s, start):
        depth += -1 if m.group(1) else 1
        if depth == 0:
            return start, m.end()
    raise ValueError


def remove_block(s, block_id):
    i = s.index(f'<div class="fe-block {block_id}"')
    a, b = balanced_div(s, i)
    return s[:a] + s[b:]


def areas(s, block_id):
    return re.findall(rf"\.{block_id} \{{\s*grid-area: ([\d/ -]+);", s)


def set_areas(s, block_id, new):
    it = iter(new)
    return re.sub(rf"(\.{block_id} \{{\s*grid-area: )([\d/ -]+)(;)", lambda m: m.group(1) + next(it) + m.group(3), s)


def must(s, old, new, count=1):
    assert s.count(old) == count, (old[:60], s.count(old))
    return s.replace(old, new)


# 1. Every page: Arun's LinkedIn link, the old contact address
AUTHWALL = re.compile(r"https://www\.linkedin\.com/authwall\?[^\"]*thearunmani[^\"]*")
for root, _, files in os.walk(W):
    if "/." in root or "_archive" in root:
        continue
    for f in files:
        if f.endswith(".html"):
            p = os.path.relpath(os.path.join(root, f), W)
            s = rd(p)
            o = s
            s = AUTHWALL.sub("https://www.linkedin.com/in/thearunmani/", s)
            s = s.replace("contact@nia-thepowerofchoice.org", "hello@niapower.org")
            if s != o:
                wr(p, s)

# 2. About: 2001 start, 2004 incorporation
s = rd("about.html")
s = re.sub(r"Thus, Nia was born, energi[sz]ed by the early success",
           "Thus Nia was born, and in 2004 it was formally incorporated, energized by the early success", s)
assert "formally incorporated" in s
wr("about.html", s)

# 3. FAQ: specific girl -> Nia Inspire
s = rd("faqs.html")
s, n = re.subn(r"At present, we do not match specific donors to specific students[^<]*",
               'Yes, through <a href="inspire/">Nia Inspire</a>. Sponsors who institute a scholarship through Nia Inspire '
               "support girls hand-picked by Nia and receive regular updates on their progress. General donations are "
               "pooled to support all the girls in our programmes, so they are not matched to individual students.", s)
assert n == 1
wr("faqs.html", s)

# 4. Partners: Pardada Pardadi slot -> AID INDIA (no logo); drop Shishu Shakthi; IBIC moves up into its slot
s = rd("partners.html")
PP_IMG, PP_TXT = "fe-block-yui_3_17_2_1_1659440862485_2674847", "fe-block-yui_3_17_2_1_1659440862485_2706323"
SS_IMG, SS_TXT = "fe-block-yui_3_17_2_1_1659440862485_2727362", "fe-block-yui_3_17_2_1_1659440862485_2844329"
IB_IMG, IB_TXT = "fe-block-d1c3f022be26a2162ef9", "fe-block-01b775c876ff1e3d8bb7"
ss_img_areas, ss_txt_areas = areas(s, SS_IMG), areas(s, SS_TXT)
pp_img_areas = areas(s, PP_IMG)
s = remove_block(s, PP_IMG)
s = remove_block(s, SS_IMG)
s = remove_block(s, SS_TXT)
s = set_areas(s, IB_IMG, ss_img_areas)
s = set_areas(s, IB_TXT, ss_txt_areas)
aid = ('<p class="sqsrte-large" style="white-space:pre-wrap;"><a href="https://aidindia.org/" target="_blank" rel="noopener">'
       "<strong>AID INDIA</strong></a></p>"
       '<p class="" style="white-space:pre-wrap;">AID (Association for India’s Development) and its sister organisation '
       "AID INDIA in Chennai work with grassroots communities across India on education, livelihoods, health, women’s "
       "empowerment and social justice. In Tamil Nadu, their Eureka programme runs schools, free evening tutoring and "
       "village libraries, and their You GO Girl! initiative gives girls bicycles so that distance doesn’t end their "
       "schooling. As one of Nia’s partners, AID INDIA helps us find girls who need support to continue their education.</p>")
s, n = re.subn(r'<p class="sqsrte-large"[^>]*><strong>Pardada Pardadi</strong></p>\s*<p[^>]*>Founded in the year 2000, Pardada[^<]*</p>', aid, s)
assert n == 1, "PP text"
s = s.replace("SEA wsa founded", "SEA was founded").replace("Shortly know as SEA", "shortly known as SEA")
wr("partners.html", s)
print("partners: PP image areas were", pp_img_areas, "| IBIC now at", ss_img_areas, ss_txt_areas)

# 5. Alt text (screen readers); decorative images keep alt=""
ALT = {
    "hero": "Smiling young woman in a red dupatta, arms folded",
    "img-2": "Smiling teenage girl with a long braid",
    "nia-students": "Six Nia students standing together in a garden",
    "nia-students-2": "Smiling students in an audience at a Nia event",
    "nia-1": "Nia student standing in a garden", "nia-2": "Six Nia students giving a thumbs-up",
    "nia-3": "Smiling Nia student in a yellow dupatta",
    "uni": "Shobana Radhakrishnan with her parents outside the University of Illinois Digital Computer Laboratory",
    "tamil-nadu": "Misty sunrise over fields and hills in Tamil Nadu",
    "shobana": "Shobana Radhakrishnan", "shobana-radhakrishnan": "Shobana Radhakrishnan",
    "shobana-sumathi-1": "Shobana Radhakrishnan with her mother, Sumathi Radhakrishnan",
    "shobana-sumathi-2": "Shobana Radhakrishnan with her mother, Sumathi Radhakrishnan",
    "kanmani-1": "Kanmani, a Nia student", "kanmani-2": "Kanmani, a Nia student",
    "empowering-females-1": "Empowering females", "funds-logo": "100% pass-through of funds", "501c": "501(c)(3) approved",
    "paypal-logo-01": "Donate with PayPal", "turning-point": "Turning Point Educational Trust logo",
    "sea": "Society for Education and Action logo", "ibic-logo": "I Believe I Can (IBIC) logo",
    "thomas-edison": "Thomas Edison", "pathways-1": "Nia Pathways", "nia-pathways-social": "Nia Pathways virtual event",
    "thumbnail-80": "Nia Pathways",
    "divya-blog-1": "Divya", "divya-blog-2": "Divya", "jeyalakshmi-blog-1": "Jeyalakshmi", "jeyalakshmi-blog-2": "Jeyalakshmi",
    "kanmani-blog-1": "Kanmani", "kanmani-blog-2": "Kanmani", "ranjitha-blog-1": "Ranjitha", "ranjitha-blog-2": "Ranjitha",
    "arun": "Arun Mani", "bala-balasubramanian-scaled": "Bala Balasubramanian", "rajamani": "Rajamani Thangapandiyan",
    "neetha": "Neetha Edwin", "swati": "Swati Sharma", "myriam-bahi": "Myriam Bahi", "gareth-nia": "Gareth Strange",
    "sarah": "Sarah Burley", "namrata-sandhu": "Namrata Sandhu", "shikha-goyal": "Shikha Goyal", "priya": "Priya Selvaraj",
    "logo-150x300": "Nia",
}
for root, _, files in os.walk(W):
    if "/." in root or "_archive" in root:
        continue
    for f in files:
        if not f.endswith(".html"):
            continue
        p = os.path.relpath(os.path.join(root, f), W)
        s = rd(p)

        def fix(m):
            tag = m.group(0)
            src = re.search(r'src="assets/images/([^"]+)\.webp"', tag)
            if not src or src.group(1) not in ALT:
                return tag
            return re.sub(r'alt="[^"]*"', f'alt="{ALT[src.group(1)]}"', tag, count=1)

        o = s
        s = re.sub(r"<img\b[^>]*>", fix, s)
        if s != o:
            wr(p, s)
print("fixes applied")

# 6. FAQ accordion: native <details> so it opens without Squarespace's script
s = rd("faqs.html")
if "<details" not in s:
    s, n1 = re.subn(r'<p class="accordion-item__title-wrapper">\s*<button class="accordion-item__click-target">',
                    '<details><summary class="accordion-item__click-target">', s)
    s, n2 = re.subn(r"</button>\s*</p>\s*(<div class=\"accordion-item__dropdown\">)", r"</summary> \1", s)
    s, n3 = re.subn(r'(</div>\s*</div>)\s*(<div class="accordion-divider"></div>\s*</li>)', r"\1</details> \2", s)
    assert n1 == n2 == n3 == 17, (n1, n2, n3)
    wr("faqs.html", s)
print("faq accordion converted")
