# -*- coding: utf-8 -*-
"""Find near-identical verses across chants and report where they differ.

A line the book prints twice should read the same both times unless the book
itself differs. Anything close-but-not-equal is either a transcription error
here or a real variation worth recording — either way it needs the photograph.
"""
import difflib
import os
import re
import sys

sys.path.insert(0, ".")
os.environ["DATABASE_URL"] = ""
sys.stdout.reconfigure(encoding="utf-8")
import chanting  # noqa: E402

NEW = set(sys.argv[1:])


def norm(s):
    return re.sub(r"[\s.,]+", "", s or "")


rows = []
for c in chanting.CHANTS:
    pg = c.get("page_start")
    for v in c["verses"]:
        pg = v.get("page", pg)
        t = v.get("pali") or v.get("thai") or ""
        if len(norm(t)) >= 18:
            rows.append((c["id"], pg, v["number"], t, norm(t)))

mine = [r for r in rows if r[0] in NEW]
seen = set()
hits = 0
for cid, pg, n, text, key in mine:
    best, score = None, 0.0
    for ocid, opg, on, otext, okey in rows:
        if ocid == cid:
            continue
        s = difflib.SequenceMatcher(None, key, okey).ratio()
        if s > score:
            best, score = (ocid, opg, on, otext), s
    if best and 0.90 <= score < 1.0:
        pair = tuple(sorted([f"{cid}:{n}", f"{best[0]}:{best[2]}"]))
        if pair in seen:
            continue
        seen.add(pair)
        hits += 1
        print(f"\n~{score:.3f}  p{pg} {cid} v{n}")
        print(f"   mine : {text}")
        print(f"   p{best[1]} {best[0]} v{best[2]}")
        print(f"   there: {best[3]}")
print(f"\n{len(mine)} verses compared, {hits} near-matches that are not equal")
