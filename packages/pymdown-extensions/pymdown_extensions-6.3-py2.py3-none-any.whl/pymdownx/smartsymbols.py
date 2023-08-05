"""
Smart Symbols.

pymdownx.smartsymbols
Really simple plugin to add support for:
  copyright, trademark, and registered symbols
  plus/minus, not equal, arrows via:

    copyright  = `(c)`
    trademark  = `(tm)`
    registered = `(r)`
    plus/minus = `+/-`
    care/of    = `c/o`
    fractions  = `1/2` etc.
        (only certain available unicode fractions)
    arrows:
        left   = `<--`
        right  = `-->`
        both   = `<-->`
    not equal  = `=/=`
       (maybe this could be =/= in the future as this might be more
        intuitive to non-programmers)

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
from markdown import Extension
from markdown import treeprocessors
from markdown.util import Registry
from markdown.inlinepatterns import HtmlInlineProcessor

RE_TRADE = ("smart-trademark", r'\(tm\)', r'&trade;')
RE_COPY = ("smart-copyright", r'\(c\)', r'&copy;')
RE_REG = ("smart-registered", r'\(r\)', r'&reg;')
RE_PLUSMINUS = ("smart-plus-minus", r'\+/-', r'&plusmn;')
RE_NOT_EQUAL = ("smart-not-equal", r'=/=', r'&ne;')
RE_CARE_OF = ("smart-care-of", r'\bc/o\b', r'&#8453;')
RE_ORDINAL_NUMBERS = (
    "smart-ordinal-numbers",
    r'''(?x)
    \b
    (?P<leading>(?:[1-9][0-9]*)?)
    (?P<tail>(?<=1)(?:1|2|3)th|1st|2nd|3rd|[04-9]th)
    \b
    ''',
    lambda m: '%s%s<sup>%s</sup>' % (
        m.group('leading') if m.group('leading') else '',
        m.group('tail')[:-2], m.group('tail')[1:]
    )
)
RE_ARROWS = (
    "smart-arrows",
    r'(?P<arrows>\<-{2}\>|(?<!-)-{2}\>|\<-{2}(?!-))',
    lambda m: ARR[m.group('arrows')]
)
RE_FRACTIONS = (
    "smart-fractions",
    r'(?<!\d)(?P<fractions>1/4|1/2|3/4|1/3|2/3|1/5|2/5|3/5|4/5|1/6|5/6|1/8|3/8|5/8|7/8)(?!\d)',
    lambda m: FRAC[m.group('fractions')]
)

REPL = {
    'trademark': RE_TRADE,
    'copyright': RE_COPY,
    'registered': RE_REG,
    'plusminus': RE_PLUSMINUS,
    'arrows': RE_ARROWS,
    'notequal': RE_NOT_EQUAL,
    'fractions': RE_FRACTIONS,
    'ordinal_numbers': RE_ORDINAL_NUMBERS,
    'care_of': RE_CARE_OF
}

FRAC = {
    "1/4": "&frac14;",
    "1/2": "&frac12;",
    "3/4": "&frac34;",
    "1/3": "&#8531;",
    "2/3": "&#8532;",
    "1/5": "&#8533;",
    "2/5": "&#8534;",
    "3/5": "&#8535;",
    "4/5": "&#8536;",
    "1/6": "&#8537;",
    "5/6": "&#8538;",
    "1/8": "&#8539;",
    "3/8": "&#8540;",
    "5/8": "&#8541;",
    "7/8": "&#8542;"
}

ARR = {
    '-->': "&rarr;",
    '<--': "&larr;",
    '<-->': "&harr;"
}


class SmartSymbolsPattern(HtmlInlineProcessor):
    """Smart symbols patterns handler."""

    def __init__(self, pattern, replace, md):
        """Setup replace pattern."""

        super(SmartSymbolsPattern, self).__init__(pattern, md)
        self.replace = replace

    def handleMatch(self, m, data):
        """Replace symbol."""

        return self.md.htmlStash.store(
            m.expand(self.replace(m) if callable(self.replace) else self.replace),
        ), m.start(0), m.end(0)


class SmartSymbolsExtension(Extension):
    """Smart Symbols extension."""

    def __init__(self, *args, **kwargs):
        """Setup config of which symbols are enabled."""

        self.config = {
            'trademark': [True, 'Trademark'],
            'copyright': [True, 'Copyright'],
            'registered': [True, 'Registered'],
            'plusminus': [True, 'Plus/Minus'],
            'arrows': [True, 'Arrows'],
            'notequal': [True, 'Not Equal'],
            'fractions': [True, 'Fractions'],
            'ordinal_numbers': [True, 'Ordinal Numbers'],
            'care_of': [True, 'Care/of']
        }
        super(SmartSymbolsExtension, self).__init__(*args, **kwargs)

    def add_pattern(self, patterns, md):
        """Construct the inline symbol pattern."""

        self.patterns.register(SmartSymbolsPattern(patterns[1], patterns[2], md), patterns[0], 30)

    def extendMarkdown(self, md):
        """Create a dict of inline replace patterns and add to the tree processor."""

        configs = self.getConfigs()
        self.patterns = Registry()

        for k, v in REPL.items():
            if configs[k]:
                self.add_pattern(v, md)

        inline_processor = treeprocessors.InlineProcessor(md)
        inline_processor.inlinePatterns = self.patterns
        md.treeprocessors.register(inline_processor, "smart-symbols", 2.1)


def makeExtension(*args, **kwargs):
    """Return extension."""

    return SmartSymbolsExtension(*args, **kwargs)
