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

from pathlib import Path
import os
import shutil

def copy_tree(source, destination):
    destination.mkdir(parents=True, exist_ok=True)
    for _ in os.listdir(source):
        i = source / _
        o = destination / _
        if i.is_dir():
            copy_tree(i, o)
        else:
            shutil.copy2(str(i), str(o))


def copy_files(kind, conf, locale, inlist, ptarget):
    o = Path(ptarget)
    for item in conf[inlist]:
        i = Path(kind + "/" + item["file"])
        # print(i)
        for t in item["targets"]:
            d_loc = o / locale / t
            d = o / t
            # print(d)
            if i.is_file() is not False:
                d_loc.write_text(i.read_text())
                print("copied " + str(i) + " to " + str(d_loc) + "...")
                d.write_text(i.read_text())
                print("copied " + str(i) + " to " + str(d) + "...")


def rm_rf(directory):
    directory = Path(directory)
    for child in directory.glob('*'):
        if child.is_file():
            child.unlink()
        else:
            rm_rf(child)
    # directory.rmdir()


def fileop(infile, outfile, action):
    """
    infile: inputfile, Path object
    outfile: outputfile, Path object
    action: action if any, String
    """
    i = Path(infile)
    o = Path(outfile)
    outdir = Path("rendered")
    if i.is_file() is not False:
        if action == "copy":
            # Write content of i to o.
            o.write_text(i.read_text())
        if action == "link":
            o.symlink_to(i)


def write_name(filename, infile, locale, replacer):
    return "./rendered/" + locale + "/" + infile.replace(replacer,
                                                         '').rstrip(".j2")


def localized(filename, locale, *args):
    if len(args) == 0:
        return "../" + locale + "/" + filename
    ext = kwargs.get('ext', None)
    if ext is not None:
        lf = filename + "." + locale + "." + ext
        lp = Path(lf)
        if locale == "en" or not lp.is_file():
            return "../" + filename + "." + ext
        else:
            return "../" + lf
