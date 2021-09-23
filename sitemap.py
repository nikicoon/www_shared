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
import os
from pathlib import Path, PurePosixPath


def sitemap_tree(path):
    tree = dict(name=PurePosixPath(path).name, children=[])
    try:
        mylist = os.listdir(path)
    except OSError:
        pass
    else:
        for name in mylist:
            fn = os.path.join(path, name)
            if os.path.isdir(fn):
                tree['children'].append(sitemap_tree(fn))
            else:
                np = os.path.join(name)
                if np.startswith('/'):
                    np = np[1:]
                tree['children'].append(dict(name=np))
    return tree
