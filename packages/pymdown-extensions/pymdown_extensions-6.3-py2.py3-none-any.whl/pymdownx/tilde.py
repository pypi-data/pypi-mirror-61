"""
Tilde.

pymdownx.tilde
Really simple plugin to add support for
`<del>test</del>` tags as `~~test~~` and
`<sub>test</sub>` tags as `~test~`

MIT license.

Copyright (c) 2014 - 2017 Isaac Muse <isaacmuse@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions
of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
from __future__ import unicode_literals
import re
from markdown import Extension
from . import util

SMART_CONTENT = r'((?:(?<=\s)~+?(?=\s)|.)+?~*?)'
SMART_MIXED_CONTENT = r'((?:~(?=[^\s])|(?<=\s)~+?(?=\s))+?~*)'
CONTENT = r'(~|[^\s]+?)'
CONTENT2 = r'((?:[^~]|(?<!~{2})~)+?)'

# `~~~del,sub~~~`
DEL_SUB = r'(~{3})(?!\s)(~{1,2}|[^~\s]+?)(?<!\s)\1'
# `~~~del,sub~del~~`
DEL_SUB2 = r'(~{3})(?![\s~])%s(?<!\s)~%s(?<!\s)~{2}' % (CONTENT, CONTENT2)
# `~~~sub,del~~sub~`
SUB_DEL = r'(~{3})(?![\s~])%s(?<!\s)~{2}%s(?<!\s)~' % (CONTENT, CONTENT)
# `~~del~sub,del~~~`
DEL_SUB3 = r'(~{2})(?![\s~])%s~(?![\s~])%s(?<!\s)~{3}' % (CONTENT2, CONTENT)
# `~~del~~`
DEL = r'(~{2})(?!\s)%s(?<!\s)\1' % CONTENT2
# `~sub~`
SUB = r'(~)(?!\s)%s(?<!\s)\1' % CONTENT

# Smart rules for when "smart tilde" is enabled
# SMART: `~~~del,sub~~~`
SMART_DEL_SUB = r'(~{3})(?![\s~])%s(?<!\s)\1' % CONTENT
# `~~~del,sub~ del~~`
SMART_DEL_SUB2 = \
    r'(~{3})(?![\s~])%s(?<!\s)~(?:(?=_)|(?![\w~]))%s(?<!\s)~{2}' % (
        CONTENT, SMART_CONTENT
    )
# `~~~sub,del~~ sub~`
SMART_SUB_DEL = \
    r'(~{3})(?![\s~])%s(?<!\s)~{2}(?:(?=_)|(?![\w~]))%s(?<!\s)~' % (
        CONTENT, CONTENT
    )
# `~~del~~`
SMART_DEL = r'(?:(?<=_)|(?<![\w~]))(~{2})(?![\s~])%s(?<!\s)\1(?:(?=_)|(?![\w~]))' % SMART_CONTENT


class TildeProcessor(util.PatternSequenceProcessor):
    """Emphasis processor for handling delete and subscript matches."""

    PATTERNS = [
        util.PatSeqItem(re.compile(DEL_SUB, re.DOTALL | re.UNICODE), 'double', 'del,sub'),
        util.PatSeqItem(re.compile(SUB_DEL, re.DOTALL | re.UNICODE), 'double', 'sub,del'),
        util.PatSeqItem(re.compile(DEL_SUB2, re.DOTALL | re.UNICODE), 'double', 'del,sub'),
        util.PatSeqItem(re.compile(DEL_SUB3, re.DOTALL | re.UNICODE), 'double2', 'del,sub'),
        util.PatSeqItem(re.compile(DEL, re.DOTALL | re.UNICODE), 'single', 'del'),
        util.PatSeqItem(re.compile(SUB, re.DOTALL | re.UNICODE), 'single', 'sub')
    ]


class TildeSmartProcessor(util.PatternSequenceProcessor):
    """Smart delete and subscript processor."""

    PATTERNS = [
        util.PatSeqItem(re.compile(SMART_DEL_SUB, re.DOTALL | re.UNICODE), 'double', 'del,sub'),
        util.PatSeqItem(re.compile(SMART_SUB_DEL, re.DOTALL | re.UNICODE), 'double', 'sub,del'),
        util.PatSeqItem(re.compile(SMART_DEL_SUB2, re.DOTALL | re.UNICODE), 'double', 'del,sub'),
        util.PatSeqItem(re.compile(SMART_DEL, re.DOTALL | re.UNICODE), 'single', 'del'),
        util.PatSeqItem(re.compile(SUB, re.DOTALL | re.UNICODE), 'single', 'sub')
    ]


class TildeSubProcessor(util.PatternSequenceProcessor):
    """Just subscript processor."""

    PATTERNS = [
        util.PatSeqItem(re.compile(SUB, re.DOTALL | re.UNICODE), 'single', 'sub')
    ]


class TildeDeleteProcessor(util.PatternSequenceProcessor):
    """Just delete processor."""

    PATTERNS = [
        util.PatSeqItem(re.compile(DEL, re.DOTALL | re.UNICODE), 'single', 'del')
    ]


class TildeSmartDeleteProcessor(util.PatternSequenceProcessor):
    """Just smart delete processor."""

    PATTERNS = [
        util.PatSeqItem(re.compile(SMART_DEL, re.DOTALL | re.UNICODE), 'single', 'del')
    ]


class DeleteSubExtension(Extension):
    """Add delete and/or subscript extension to Markdown class."""

    def __init__(self, *args, **kwargs):
        """Initialize."""

        self.config = {
            'smart_delete': [True, "Treat ~~connected~~words~~ intelligently - Default: True"],
            'delete': [True, "Enable delete - Default: True"],
            'subscript': [True, "Enable subscript - Default: True"]
        }

        super(DeleteSubExtension, self).__init__(*args, **kwargs)

    def extendMarkdown(self, md):
        """Insert `<del>test</del>` tags as `~~test~~` and `<sub>test</sub>` tags as `~test~`."""

        config = self.getConfigs()
        delete = bool(config.get('delete', True))
        subscript = bool(config.get('subscript', True))
        smart = bool(config.get('smart_delete', True))

        md.registerExtension(self)

        escape_chars = []
        if delete or subscript:
            escape_chars.append('~')
        if subscript:
            escape_chars.append(' ')
        util.escape_chars(md, escape_chars)

        tilde = None
        if delete and subscript:
            tilde = TildeSmartProcessor(r'~') if smart else TildeProcessor(r'~')
        elif delete:
            tilde = TildeSmartDeleteProcessor(r'~') if smart else TildeDeleteProcessor(r'~')
        elif subscript:
            tilde = TildeSubProcessor(r'~')

        if tilde is not None:
            md.inlinePatterns.register(tilde, "sub_del", 65)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return DeleteSubExtension(*args, **kwargs)
