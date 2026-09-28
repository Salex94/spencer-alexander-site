#!/usr/bin/env python3
# Copied on 24 Sep 2026 from the spencer-alexander-voice skill, scripts/check_style.py, so that
# routines can run it on every email before it is sent even where the skill is not installed.
# Changed here the same day, and the skill's copy should be brought into line with it: the specialist
# rule never matched the word specialist itself, so it now also fails specialist, speciality and
# expert or expertise when the sentence is about Spencer or the firm and does not negate the claim;
# the bracket exemption now spares only single letter, roman numeral and number labels, so "(same)"
# fails; and in markdown, inline code spans and horizontal rule lines are data and structure, not
# prose. When the skill's checker next changes, merge the two rather than copying over this one.
"""Check a draft against Spencer Alexander's writing rules.

Usage: python check_style.py FILE [FILE ...]

Reads .md, .txt or .docx files. Exits with status 1 if any file breaks a hard rule.

Hard rules, which fail the draft:
  1. a dash used as punctuation: an em dash, an en dash, a spaced hyphen or a double hyphen
  2. a bracket or parenthesis in prose, other than clause labels such as (a) at the start of
     a paragraph, cross references such as 17.1(a), and brackets inside a statute's title
  3. describing Spencer or the firm as a specialist, as specialising in anything, as having a
     speciality, or as an expert or having expertise

Notes, which are reported but do not fail the draft:
  stock words and structures of machine written prose, including a quote or fee given a human verb and staged
  openings that build up to the point, paragraphs of uniform length, American spellings, sentences over
  sixty words, runs of clipped sentences, prose broken into bullet points, and exclamation marks.
"""
import re
import sys
import zipfile
from xml.etree import ElementTree as ET

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"

STOCK_PHRASES = [
    "delve", "delves", "delving", "tapestry", "testament to", "navigate the complexities",
    "navigating the complexities", "in today's fast paced", "in today's fast-paced", "in today's world",
    "it is important to note", "it's important to note", "it is worth noting", "it's worth noting",
    "rest assured", "hope this email finds you well", "hope this finds you well", "wanted to reach out",
    "reaching out", "feel free to", "do not hesitate to", "don't hesitate to", "seamless", "seamlessly",
    "robust", "leverage", "leveraging", "elevate", "unlock", "unlocking", "empower", "empowering",
    "embark", "journey", "landscape", "realm", "holistic", "synergy", "cutting edge", "cutting-edge",
    "game changer", "game-changer", "meticulous", "meticulously", "underscore", "underscores",
    "showcase", "showcases", "vibrant", "bustling", "nestled", "in conclusion", "in summary",
    "a myriad of", "plethora", "at the end of the day", "moving forward", "going forward",
    "comprehensive update", "valuable insights", "key takeaways",
    "earns its keep", "earn its keep", "heavy lifting", "the short answer", "the short version",
    "here's the thing", "here is the thing", "the real question", "the upshot", "the bottom line",
    "put simply", "simply put", "boils down to", "at its core", "in essence",
]
STRUCTURES = [
    (re.compile(r"\bnot only\b[^.]*\bbut also\b", re.I), "not only ... but also construction"),
    (re.compile(r"\b(is not|isn't|it's not|it is not) (just|merely|simply)\b", re.I), "it is not just ... construction"),
    (re.compile(r"(^|[.!?]\s+)(Furthermore|Moreover|Additionally|In addition|Ultimately|Overall),", re.M), "stock transition opening a sentence"),
    (re.compile(r"\b(quote|price|fee|figure|estimate|offer|advice|position)s?\s+(still\s+)?(stands|holds|lands|sits)\b", re.I),
     "a quote, fee or price given a human verb; say it as a person would, such as I can confirm the fee is still"),
    (re.compile(r"(^|[.!?]\s+)(The one thing|The only thing|What matters (here|now|most) is|The (short|simple|real) answer is|The point is|Here is why|Here's why)\b", re.M),
     "staged opening that builds up to the point; state the point directly"),
]
AMERICAN = {
    "center": "centre", "centers": "centres", "color": "colour", "colors": "colours", "favor": "favour",
    "favors": "favours", "favorable": "favourable", "favorite": "favourite", "honor": "honour",
    "honors": "honours", "behavior": "behaviour", "behaviors": "behaviours", "defense": "defence",
    "offense": "offence", "catalog": "catalogue", "fulfill": "fulfil", "fulfillment": "fulfilment",
    "enroll": "enrol", "enrollment": "enrolment", "skillful": "skilful", "traveled": "travelled",
    "traveling": "travelling", "modeled": "modelled", "canceled": "cancelled", "canceling": "cancelling",
    "labeled": "labelled", "counselor": "counsellor", "jewelry": "jewellery", "aluminum": "aluminium",
    "gray": "grey", "percent": "per cent",
}
IZE_WHITELIST = {"size", "sizes", "sized", "sizing", "prize", "prizes", "prized", "seize", "seizes",
                 "seized", "seizing", "capsize", "capsized", "maize", "baize", "downsize", "downsized",
                 "oversize", "oversized", "resize", "resized"}
SPECIALIST = re.compile(r"\b(speciali[sz](e|es|ed|ing|ation|ations)|specialists?|speciali?t(y|ies)|experts?|expertise)\b", re.I)
# A sentence that negates the claim before making it, such as "never describe Spencer as an expert",
# states the rule rather than breaking it.
NEGATED_CLAIM = re.compile(r"\b(never|not|no|nor|without|avoid|avoids|bars?|barred|prohibits?|don't|do not|must not)\b[^.;:]*"
                           r"\b(speciali[sz]\w*|speciali?t(y|ies)|experts?|expertise)\b", re.I)
# "I" is matched in capitals only; every other word about Spencer or the firm in any case, since a
# sentence often opens with "We" or "The firm".
ABOUT_FIRM = re.compile(r"\b(Spencer|Spencer Alexander Lawyers|I|(?i:the firm|our firm|our practice|we|our|my))\b")


def read_paragraphs(path):
    if path.lower().endswith(".docx"):
        with zipfile.ZipFile(path) as z:
            root = ET.fromstring(z.read("word/document.xml"))
        paras = []
        for p in root.iter(W + "p"):
            parts = []
            for el in p.iter():
                if el.tag == W + "t":
                    parts.append(el.text or "")
                elif el.tag in (W + "tab", W + "br"):
                    parts.append("\t")
            t = "".join(parts).strip()
            if t:
                paras.append(t)
        return paras, 0
    text = open(path, encoding="utf-8").read()
    is_md = path.lower().endswith(".md")
    out, bullets, in_code = [], 0, False
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or not line.strip():
            out.append("")
            continue
        s = line.strip()
        if s.startswith("<<<") and s.endswith(">>>"):
            out.append("")
            continue
        if re.match(r"^([-*\u2022])\s+", s):
            bullets += 1
            s = re.sub(r"^([-*\u2022])\s+", "", s)
        s = re.sub(r"^#{1,6}\s+", "", s)
        s = re.sub(r"^\[[^\]]{1,20}\]\s+", "", s)
        s = re.sub(r"^:: (.+?) :: ", r"\1 ", s)
        s = re.sub(r"^\+{0,2}(\((?:[a-z]|[ivxlc]{1,6}|[A-Z]|\d{1,3})\))\s+", "", s)
        s = s.replace("**", "").replace("~~", "")
        if is_md:
            # A horizontal rule is structure, and an inline code span is data, such as a file name, a
            # calendar tag or a tracker value like `Replied - interested`, never prose.
            if re.fullmatch(r"(-\s*){3,}|(\*\s*){3,}|(_\s*){3,}", s):
                out.append("")
                continue
            s = re.sub(r"`[^`]*`", "", s)
        if s.startswith("|"):
            s = " ".join(c.strip() for c in s.strip("|").split("|") if not re.fullmatch(r":?-+:?", c.strip()))
            out.append(s)
            out.append("")
            continue
        out.append(s)
    paras, cur = [], []
    for line in out:
        if line:
            cur.append(line)
        elif cur:
            paras.append(" ".join(cur)); cur = []
    if cur:
        paras.append(" ".join(cur))
    return paras, bullets


def prose_brackets(p):
    """Brackets that hold only a label, such as (a), (iv), (B) or (2), are numbering or cross
    references like clause 17.1(a) and paragraph (b), and brackets inside a statute's official
    title are part of its name. Any other bracket is a bracket in prose."""
    t = re.sub(r"\((?:[a-z]|[ivxlc]{1,6}|[A-Z]|\d{1,3})\)", "", p)
    t = re.sub(r"\([A-Z][^()]{0,60}\)(?=\s+Act\b)", "", t)
    t = t.replace("Uniform Law (Victoria)", "Uniform Law Victoria")
    t = re.sub(r"(\d{4})\s*\((?:Vic|Cth|NSW|Qld|SA|WA|Tas|NT|ACT)\)", r"\1", t)
    return re.findall(r"[()\[\]]", t)


def sentences(p):
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9])", p) if s.strip()]


def check(path):
    paras, bullets = read_paragraphs(path)
    fails, notes, long_sentences = [], [], []
    for p in paras:
        snippet = p[:90]
        if re.search(r"[\u2013\u2014]", p) or re.search(r"\S\s-\s\S", p) or "--" in p:
            fails.append(f"dash used as punctuation: {snippet!r}")
        if prose_brackets(p):
            fails.append(f"bracket in prose: {snippet!r}")
        for s in sentences(p):
            if SPECIALIST.search(s):
                if ABOUT_FIRM.search(s) and not NEGATED_CLAIM.search(s):
                    fails.append(f"describes Spencer or the firm as a specialist: {s[:90]!r}")
                else:
                    notes.append(f"the word specialist or specialise appears, check it does not describe the firm: {s[:80]!r}")
        low = p.lower()
        for phrase in STOCK_PHRASES:
            if re.search(r"\b" + re.escape(phrase) + r"\b", low):
                notes.append(f"stock phrase {phrase!r}: {snippet!r}")
        for rx, label in STRUCTURES:
            if rx.search(p):
                notes.append(f"{label}: {snippet!r}")
        for word in re.findall(r"[A-Za-z]+", p):
            w = word.lower()
            if w in AMERICAN and not (w == "labor" and word == "Labor"):
                notes.append(f"American spelling {word!r}, Australian English is {AMERICAN[w]!r}")
            elif re.fullmatch(r"\w+(iz|yz)(e|es|ed|ing|ation|ations|er|ers)", w) and w not in IZE_WHITELIST:
                notes.append(f"American spelling {word!r}, Australian English uses s rather than z")
        run = 0
        for s in sentences(p):
            words = len(s.split())
            if words > 60:
                long_sentences.append(f"sentence of {words} words, check it can be understood first time: {s[:80]!r}")
            run = run + 1 if words < 6 else 0
            if run == 3:
                notes.append(f"three clipped sentences in a row, which reads as staccato: {snippet!r}")
        if p.count("!") > 0:
            notes.append(f"exclamation mark: {snippet!r}")
    # paragraphs that are all much the same length read as machine made
    prose = [p for p in paras if len(p.split()) >= 12 and not re.match(r"^\s*(\d+(\.\d+)*|\(\w{1,4}\))[\s\t]", p)]
    if len(prose) >= 5:
        lengths = [len(p.split()) for p in prose]
        mean = sum(lengths) / len(lengths)
        spread = (sum((x - mean) ** 2 for x in lengths) / len(lengths)) ** 0.5 / mean
        counts = [len(sentences(p)) for p in prose]
        same_run, best = 1, 1
        for a, b in zip(counts, counts[1:]):
            same_run = same_run + 1 if a == b else 1
            best = max(best, same_run)
        if spread < 0.25:
            notes.append(f"paragraph lengths are very even, around {round(mean)} words each, which reads as machine made; "
                         "let them vary with the thought")
        if best >= 5:
            notes.append(f"{best} paragraphs in a row have the same number of sentences; vary their shape")
    notes.extend(long_sentences[:5])
    if len(long_sentences) > 5:
        notes.append(f"and {len(long_sentences) - 5} more sentences over sixty words")
    if bullets > 6:
        notes.append(f"{bullets} bullet points, check the document genuinely calls for them rather than prose")
    seen, uniq = set(), []
    for n in notes:
        if n not in seen:
            seen.add(n); uniq.append(n)
    return fails, uniq


def main():
    import signal
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    failed = False
    for path in sys.argv[1:]:
        fails, notes = check(path)
        status = "FAIL" if fails else "PASS"
        failed = failed or bool(fails)
        print(f"{status} {path}")
        for f in fails:
            print("  fail: " + f)
        for n in notes:
            print("  note: " + n)
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
