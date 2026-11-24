#!/usr/bin/env python3
"""One sentence for a traveler from 1800.

Writes the entry sentence to ``$MAKEFUN_OUTPUT_DIR/entry.txt`` (falling
back to ``./entry.txt`` when the variable is unset).

Standard library only. Deterministic: no clock, no randomness, no network,
no writes outside the output directory. The sentence is a fixed string, so
every run produces byte-identical output.
"""

import os
import sys

ENTRY = (
    "Picture a market square where every town on earth keeps a stall, "
    "and any question asked aloud may find its answer from a stranger "
    "across the sea before your breath is spent."
)

# Words whose modern sense was coined after 1800, which the traveler
# could not know. The entry must contain none of these (matched as whole
# words, case-insensitive). Every word in the sentence above dates to
# 1800 or earlier: picture (14th c.), market (Old English), square
# (14th c.), town (Old English), stall (Old English), question (14th c.),
# aloud (13th c.), stranger (14th c.), sea, breath, spent (Old English).
BANNED_WORDS = (
    "internet", "computer", "phone", "screen", "website", "email",
    "digital", "online", "software", "data", "network", "radio",
    "television", "video", "app", "cyber", "web",
)


def check_entry(text: str) -> list:
    """Return a list of problems with the entry text (empty = valid)."""
    problems = []
    if not 1 <= len(text) <= 200:
        problems.append(f"length {len(text)} is outside 1-200 characters")
    if not text.strip():
        problems.append("entry is blank")
    if text.count(".") != 1 or not text.endswith("."):
        problems.append("entry must be exactly one sentence")
    words = set(text.lower().replace(".", "").split())
    for banned in BANNED_WORDS:
        if banned in words:
            problems.append(f"post-1800 word present: {banned}")
    return problems


def main() -> int:
    text = ENTRY.strip()
    problems = check_entry(text)
    if problems:
        for problem in problems:
            print(f"invalid entry: {problem}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
