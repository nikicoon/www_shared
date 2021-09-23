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
# process a number of .xml.j2 files with jinja2 and output
# a .xml file which according to the template results in a
# spec conform rss file. There could be more than one file,
# so we do it this way.
#
# this generator in the current form is rather simplistic and assumes
# too much structure in the yaml file, which should be improved
# eventually.

from pathlib import Path, PurePath
import re
import codecs
from inc.time import time_rfc822, time_now, conv_date_rfc822

debug=0

def make_rss(directory, conf, env):
    if debug > 1:
        _ = Path(".")
        q = list(_.glob("**/*.j2"))
        print(q)
    for infile in Path(directory).glob("*.xml.j2"):
        infile = str(infile)
        if debug > 1:
            print(infile)
        name, ext = re.match(r"(.*)\.([^.]+)$", infile.rstrip(".j2")).groups()
        tmpl = env.get_template(infile)

        def self_localized(other_locale):
            """
            Return absolute URL for the current page in another locale.
            """
            return "https://" + conf["siteconf"]["baseurl"] + "/" + other_locale + "/" + infile.replace(directory + '/', '').rstrip(".j2")

        def url_localized(filename):
            return "https://" + conf["siteconf"]["baseurl"] + "/" + locale + "/" + filename

        def url_static(filename):
            return "https://" + conf["siteconf"]["baseurl"] + "/static/" + filename

        def url_dist(filename):
            return "https://" + conf["siteconf"]["baseurl"] + "/dist/" + filename

        def url(x):
            return "https://" + conf["siteconf"]["baseurl"] + "/" + x
        
        for l in list(x for x in Path(".").glob("locale/*/") if x.is_dir()):
            locale = str(PurePath(l).name)
            if debug > 1:
                print(locale)
            content = tmpl.render(lang=locale,
                                  url=url,
                                  now=time_rfc822(time_now()),
                                  conv_date_rfc822=conv_date_rfc822,
                                  siteconf=conf["siteconf"],
                                  newsposts=conf["newsposts"],
                                  self_localized=self_localized,
                                  url_localized=url_localized,
                                  url_static=url_static,
                                  url_dist=url_dist,
                                  filename=name + "." + ext)
            outname = "./rendered/" + locale + "/" + infile.replace(directory + "/", '').rstrip(".j2")
            outdir = Path("rendered")
            langdir = outdir / locale
            try:
                langdir.mkdir(parents=True, exist_ok=True)
            except e as FileNotFoundError:
                print(e)

            with codecs.open(outname, "w", encoding='utf-8') as f:
                try:
                    if debug > 1:
                        print(Path.cwd())
                    f.write(content)
                except e as Error:
                    print(e)
