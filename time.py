# Copyright (C) 2019 GNUnet e.V.
#
# This code is derived from code contributed to GNUnet e.V.
# by Nikita Ronja <nikita@NetBSD.org>.
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
import time
import datetime
import email.utils

def time_now():
    return datetime.datetime.now()

def conv_date(t):
    # naively assumes its input is always a Y-m-d.
    if type(t) == str:
        i = datetime.datetime.strptime(t, "%Y-%m-%d").timetuple()
        return time.mktime(i)
    elif type(t) == datetime.date:
        i = t.timetuple()
        return time.mktime(i)
    else:
        return sys.exit(1)

def conv_date_rfc822(t):
    return time_rfc822(conv_date(t))

def time_rfc822(t):
    if type(t) == float:
        return email.utils.formatdate(t)
    elif type(t) == datetime.datetime:
        return email.utils.format_datetime(t)
    else:
        return sys.exit(1)
