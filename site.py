# Copyright (C) 2019 GNUnet e.V.
#
# This code is derived from code contributed to GNUnet e.V.
# by Nikita Ronja <nikita@NetBSD.org> and based on code by Florian Dold.
#
# Permission to use, copy, modify, and/or distribute this software for
# any purpose with or without fee is hereby granted.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL
# WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE
# AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL
# DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA
# OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER
# TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.
#
# SPDX-License-Identifier: 0BSD
import os
import os.path
import sys
import re
import gettext
import glob
import codecs
import jinja2
from pathlib import Path, PurePosixPath, PurePath
from ruamel.yaml import YAML

# Make sure the current directory is in the search path when trying
# to import i18nfix.
sys.path.insert(0, ".")

import inc.i18nfix as i18nfix
from inc.textproc import cut_news_text, cut_article
from inc.fileproc import copy_files, copy_tree
from inc.make_rss import *

class gen_site:
    def __init__(self, debug):
        self.debug = debug

    def load_config(self, name="www.yml"):
        yaml = YAML(typ='safe')
        site_configfile = Path(name)
        return yaml.load(site_configfile)

    def copy_trees(self, directory):
        """ Take a directory name (string) and pass it to copy_tree() as Path object. """
        i = Path(directory)
        o = Path("rendered/" + directory)
        copy_tree(i, o)

    def gen_abstract(self, conf, name, member, pages, length):
        if self.debug:
            print("generating abstracts...")
        for item in conf[name]:
            item[member] = cut_news_text(item[pages], length)
        if self.debug:
            print("cwd: " + str(Path.cwd()))
        if self.debug > 1:
            print(conf["newsposts"])
        if self.debug:
            print("[done] generating abstracts")

    def gen_newspost_content(self, conf, name, member, pages, lang):
        if self.debug:
            print("generating newspost content...")
        for item in conf[name]:
            item[member] = cut_article(item[pages], conf, lang)
        if self.debug:
            print("cwd: " + str(Path.cwd()))
        if self.debug > 1:
            print(conf["newsposts"])
        if self.debug:
            print("[done] generating newspost content")

    def gen_rss(self, directory, conf, env):
        make_rss(directory, conf, env)

    def run(self, root, conf, env):
        # root = "../" + root
        if self.debug > 1:
            _ = Path(".")
            q = list(_.glob("**/*.j2"))
            print(q)
        # for in_file in glob.glob(root + "/*.j2"):
        for in_file in Path(".").glob(root + "/*.j2"):
            in_file = str(in_file)
            if self.debug > 1:
                print(in_file)
            name, ext = re.match(r"(.*)\.([^.]+)$",
                                 in_file.rstrip(".j2")).groups()
            tmpl = env.get_template(in_file)

            def self_localized(other_locale):
                """
                Return URL for the current page in another locale.
                """
                if root == "news":
                    return "../../" + other_locale + "/news/" + in_file.replace(
                       root + '/', '').rstrip(".j2")
                else:
                    return "../" + other_locale + "/" + in_file.replace(
                       root + '/', '').rstrip(".j2")

            def url_localized(filename):
                if root == "news":
                    return "../../" + locale + "/" + filename
                else:
                    return "../" + locale + "/" + filename

            def url_static(filename):
                if root == "news":
                    return "../../static/" + filename
                else:
                    return "../static/" + filename

            def url_dist(filename):
                if root == "news":
                    return "../../dist/" + filename
                else:
                    return "../dist/" + filename

            def svg_localized(filename):
                lf = filename + "." + locale + ".svg"
                if locale == "en" or not Path(lf).is_file():
                    return "../" + filename + ".svg"
                else:
                    return "../" + lf

            def url(x):
                # TODO: look at the app root environment variable
                # TODO: check if file exists
                #if root == "news":
                #    return "../" + "../" + x
                #else:
                #    return "../" + x
                return "../" + x

            # for l in glob.glob("locale/*/"):
            # https://bugs.python.org/issue22276
            for l in list(x for x in Path(".").glob("locale/*/") if x.is_dir()):
                l = str(PurePath(l).name)
                if self.debug > 1:
                    print(l)
                # locale = os.path.basename(l[:-1])
                locale = l

                tr = gettext.translation("messages",
                                         localedir="locale",
                                         languages=[locale])

                tr.gettext = i18nfix.wrap_gettext(tr.gettext)

                env.install_gettext_translations(tr, newstyle=True)

                content = tmpl.render(lang=locale,
                                      lang_full=conf["langs_full"][locale],
                                      url=url,
                                      conf=conf,
                                      siteconf=conf["siteconf"],
                                      meetingnotesdata=conf["meetingnotes"],
                                      newsdata=conf["newsposts"],
                                      videosdata=conf["videoslist"],
                                      self_localized=self_localized,
                                      url_localized=url_localized,
                                      url_static=url_static,
                                      url_dist=url_dist,
                                      svg_localized=svg_localized,
                                      filename=name + "." + ext)

                if root == "news":
                    out_name = "./rendered/" + locale + "/" + root + "/" + in_file.replace(
                        root + '/', '').rstrip(".j2")
                else:
                    out_name = "./rendered/" + locale + "/" + in_file.replace(
                        root + '/', '').rstrip(".j2")

                outdir = Path("rendered")

                if root == "news":
                    langdir = outdir / locale / root
                else:
                    langdir = outdir / locale

                try:
                    langdir.mkdir(parents=True, exist_ok=True)
                except e as FileNotFoundError:
                    print(e)

                with codecs.open(out_name, "w", encoding='utf-8') as f:
                    try:
                        if self.debug > 1:
                            print(Path.cwd())
                        f.write(content)
                    except e as Error:
                        print(e)
