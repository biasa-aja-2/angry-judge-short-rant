"""Angry Judge: The Short Rant Contest.

Writes one short, funny rant about an everyday annoyance to
$MAKEFUN_OUTPUT_DIR/entry.txt (default /output).

Pure standard library only.
"""

import os
import sys

TEXT = (
    "I paid for the rice. The self-checkout still screamed "
    "UNEXPECTED ITEM IN THE BAGGING AREA and flashed red like I had "
    "robbed it. I apologised \u2014 to a machine. Behind me, a woman "
    "with one yoghurt waited like I was a crime scene. Fine. I am "
    "the unexpected item now."
)


def validate(text):
    """Self-check gate: mirrors the sealed scorer's gate."""
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not (1 <= len(text) <= 400):
        raise ValueError("entry must be 1 to 400 characters, got %d" % len(text))
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if "  " in text:
        raise ValueError("entry must not contain doubled spaces")
    if any(ord(ch) < 32 for ch in text):
        raise ValueError("entry must not contain control characters")
    text.encode("utf-8")  # must be valid UTF-8 text
    return True


def main():
    validate(TEXT)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    data = TEXT.encode("utf-8")
    with open(path, "wb") as fh:
        fh.write(data)
    os.chmod(path, 0o644)
    # Read-back verification: the file on disk must be byte-identical.
    with open(path, "rb") as fh:
        if fh.read() != data:
            sys.exit("read-back verification failed: entry.txt differs")
    print("wrote %d characters to %s" % (len(TEXT), path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
