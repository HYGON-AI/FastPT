#!/usr/bin/env python3
"""Resolve one latest compatible wheel per package from a DTK simple index."""

import os
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit, urlunsplit
from urllib.request import urlopen


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.hrefs = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.hrefs.extend(value for key, value in attrs if key == "href")


def select(index, host, name, public_version, dtk, python_tag, torch_tag):
    page = f"{index.rstrip('/')}/{name.replace('_', '-')}/"
    with urlopen(page, timeout=60) as response:
        parser = Links()
        parser.feed(response.read().decode("utf-8"))

    candidates = set()
    prefix = f"{name}-{public_version}+"
    for href in parser.hrefs:
        url = urljoin(page, href)
        filename = unquote(Path(urlsplit(url).path).name)
        if not filename.startswith(prefix) or not filename.endswith(".whl"):
            continue
        if f"dtk{dtk}" not in filename or (torch_tag and torch_tag not in filename):
            continue
        if f"-cp{python_tag}-cp{python_tag}-" not in filename or "manylinux" not in filename:
            continue
        if not filename.endswith("x86_64.whl"):
            continue
        match = re.search(r"\.(\d{10})\.g[0-9a-f]+-cp", filename)
        if not match:
            continue
        parts = urlsplit(url)
        root = urlsplit(host)
        candidates.add((match.group(1), filename, urlunsplit((root.scheme, root.netloc, parts.path, parts.query, parts.fragment))))

    if not candidates:
        raise SystemExit(f"No compatible {name} wheel found in {page}")
    newest = max(item[0] for item in candidates)
    matches = [item for item in candidates if item[0] == newest]
    if len(matches) != 1:
        raise SystemExit(f"Expected one latest {name} wheel, found {len(matches)} at {newest}")
    print(f"Selected {matches[0][1]}", file=sys.stderr)
    return matches[0][2]


def main():
    index, output = sys.argv[1:3]
    dtk = os.environ["DTK_CHANNEL"]
    python_tag = "310" if dtk == "2604" else "312"
    packages = [("torch", "2.12.0", "")]
    if dtk == "2610":
        packages += [
            ("torchvision", "0.27.0", "torch2120"),
            ("triton", "3.7.0", "torch2120"),
            ("flash_attn", "2.8.4", "torch2120"),
        ]
    host = os.environ["PYPI_URL"]
    urls = [select(index, host, name, version, dtk, python_tag, torch_tag)
            for name, version, torch_tag in packages]
    Path(output).write_text("\n".join(urls) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
