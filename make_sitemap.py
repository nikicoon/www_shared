# Copyright (C) 2019 GNUnet e.V.
#
# This code is derived from code contributed to GNUnet e.V.
# by Nikita Ronja <nikita@NetBSD.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE
# LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES
# OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
# WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION,
# ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE OF
# THIS SOFTWARE.
#
# SPDX-License-Identifier: 0BSD
#
# A sitemap generator.

import sys
from pathlib import Path
from datetime import datetime

def main():
    if len(sys.argv) >= 2 and sys.argv[1] == "-i":
        i = sys.argv[2]
    else:
        i = "rendered"

    p = Path(i)
    links = sorted(p.rglob("*.html"))
    t0 = datetime.now()
    timestamp = t0.strftime("%Y-%m-%d")

    o = Path("sitemap.xml")
    with o.open("w") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        f.write('<urlset\n')
        f.write('xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n')
        f.write('xsi:schemaLocation="http://www.sitemaps.org/schemas/sitemap/0.9 ')
        f.write('http://www.sitemaps.org/schemas/sitemap/0.9/sitemap.xsd"\n')
        f.write('xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
        for link in links:
            f.write('<url><loc>' + str(link).lstrip("rendered") + '</loc><lastmod>' + timestamp + '</lastmod><priority>1.0</priority></url>\n')
        f.write('</urlset>\n')


if __name__ == "__main__":
    main()
