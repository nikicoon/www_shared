# Copyright (C) 2019 GNUnet e.V.
#
# This code is derived from code contributed to GNUnet e.V.
# by Nikita Ronja <nikita@NetBSD.org>
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
import html.parser
from bs4 import BeautifulSoup


class extractText(html.parser.HTMLParser):
    def __init__(self):
        super(extractText, self).__init__()
        self.result = []

    def handle_data(self, data):
        self.result.append(data)

    def text_in(self):
        return ''.join(self.result)


def html2text(html):
    k = extractText()
    k.feed(html)
    return k.text_in()


def cut_text(filename, count):
    with open(filename) as html:
        soup = BeautifulSoup(html, features="lxml")
        for script in soup(["script", "style"]):
            script.extract()
        k = []
        for i in soup.findAll('p')[1]:
            k.append(i)
        b = ''.join(str(e) for e in k)
        text = html2text(b.replace("\n", ""))
        textreduced = (text[:count] + '...') if len(text) > count else (text +
                                                                        '..')
        return (textreduced)


def cut_news_text(filename, count):
    return cut_text("news/" + filename + ".j2", count)


# TODO: replace id='...' with frontier so that we can
# pass it in cut_article reusable, or merge cut_text and
# cut_by_frontier.
def cut_by_frontier(filename):
    with open(filename) as html:
        soup = BeautifulSoup(html, features="lxml")
        k = []
        for i in soup.find(id='newspost-content'):
            k.append(i)
        b = ''.join(str(e) in k)
        text = b.replace("\n", "")
        return text


def cut_article(filename, conf, lang):
    return cut_all("news/" + filename + ".j2", conf, lang)

def cut_all(filename, conf, lang):
    with open(filename) as html:
        soup = BeautifulSoup(html, features="lxml")
        i = repr(soup).replace('{% extends "common/news.j2" %}\n{% block body_content %}\n', "").replace('\n{% endblock body_content %}', "").replace('<html><body><p></p>',"").replace('</body></html>', "")
        urlstr = "https://" + conf["siteconf"][0]["baseurl"] + "/" + lang + "/"
        text = i.replace("\n", "").replace("{{ url_localized('", urlstr).replace("') }}", "")
        # .replace('<', '&lt;').replace('>', '&gt;').replace('"', '&quot;')
        return text
