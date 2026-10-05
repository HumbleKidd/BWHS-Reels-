#!/usr/bin/env python3
"""Insert the first-launch and updater script into index.html."""
import sys
path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
html = open(path, encoding="utf-8").read()
tag = '<script src="reels-boot.js"></script>'
if tag not in html:
    html = html.replace("</body>", tag + "\n</body>", 1)
    open(path, "w", encoding="utf-8").write(html)
    print("injected", path)
else:
    print("already injected", path)
