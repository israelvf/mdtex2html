#!/usr/bin/python3
'''
This will convert Markdown with included LaTeX-equations to HTML.
The Formulas will be in MathML-Format.

- block-equations need to start with $$ or \[
- inline-equations start with \( or $
- $-signs can be escaped with \, so \$ will be returned as $

version 1.3.1 (c) 2020-2025 by Dirk Winkel

markdown lib updated by Israel Ferreira

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the Free
Software Foundation, either version 2.1 of the License, or (at your option) any
later version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
    
    
'''

import re
import random
import string

from latex2mathml.converter import convert as tex2mathml
from markdown2 import markdown as md2html
from markdown2 import Markdown

incomplete = '<font style="color:orange;" class="tooltip">&#9888;<span class="tooltiptext">formula incomplete</span></font>'  # noqa
convError = '<font style="color:red" class="tooltip">&#9888;<span class="tooltiptext">LaTeX-convert-error</span></font>'


def convert(mdtex, extras=[], splitParagraphs=True):
    ''' converts recursively the Markdown-LaTeX-mixture to HTML with MathML '''
    found = False
    # render table of contents before splitting it up:
    if 'toc' in extras and splitParagraphs and '[TOC]' in mdtex:
        md = Markdown(extras=['toc'])
        md.convert(mdtex)
        mdtex = mdtex.replace('[TOC]', md.toc)
    # entirely skip code-blocks:
    parts = re.split('```', mdtex, 2)
    if len(parts) > 1:
        found = True
        result = convert(parts[0], extras, splitParagraphs=False)+'\n'
        result += md2html('```'+parts[1]+'```', extras=extras)+'\n'
        if len(parts) == 3:
            result += convert(parts[2], extras, splitParagraphs=False)
        return result
    # handle all paragraphs separately (prevents follow-up rendering errors)
    if splitParagraphs:
        parts = re.split("\n\n", mdtex)
        result = ''
        for part in parts:
            result += convert(part, extras, splitParagraphs=False)
        return result
    # skip code-spans:
    parts = re.split('`', mdtex, 2)
    if len(parts) > 1:
        found = True
        codehtml = md2html('`'+parts[1]+'`', extras=extras)
        codehtml = re.sub('^<[a-z]+>', '', codehtml)  # remove opening tag
        codehtml = re.sub('</[a-z]+>$', '', codehtml)  # remove closing tag
        ranString = ''.join(random.choice(string.ascii_letters) for i in range(16))
        if len(parts) == 3:
            result = convert(parts[0]+'CoDeRePlAcEmEnT'+ranString+parts[2], extras, splitParagraphs=False)
        else:
            result = convert(parts[0]+'CoDeRePlAcEmEnT'+ranString, extras, splitParagraphs=False)
        result = result.replace('CoDeRePlAcEmEnT'+ranString, codehtml)
    # find first $$-formula:
    else:
        parts = re.split(r'\${2}', mdtex, 2)
    if len(parts) > 1 and not found:
        found = True
        result = convert(parts[0], extras, splitParagraphs=False)+'\n'
        try:
            result += '<div class="blockformula">'+tex2mathml(parts[1])+'</div>\n'
        except:
            result += '<div class="blockformula">'+convError+'</div>'
        if len(parts) == 3:
            result += convert(parts[2], extras, splitParagraphs=False)
        else:
            result += '<div class="blockformula">'+incomplete+'</div>'
    # else find first $-formulas, excluding \$:
    else:
        parts = re.split(r'(?<!\\)\${1}', mdtex, 2)
    if len(parts) > 1 and not found:
        found = True
        try:
            mathml = tex2mathml(parts[1])
        except:
            mathml = convError
        if parts[0].endswith('\n') or parts[0] == '':  # make sure textblock starts before formula!
            parts[0] = parts[0]+'&#x200b;'
        if len(parts) == 3:
            result = convert(parts[0]+mathml+parts[2], extras, splitParagraphs=False)
        else:
            result = convert(parts[0]+mathml+incomplete, extras, splitParagraphs=False)
    # else find first \[..\]-equation:
    else:
        mdtex = mdtex.replace(r'\$', '$')
        parts = re.split(r'\\\[', mdtex, 1)
    if len(parts) > 1 and not found:
        found = True
        result = convert(parts[0], extras, splitParagraphs=False)+'\n'
        parts = re.split(r'\\\]', parts[1], 1)
        try:
            result += '<div class="blockformula">'+tex2mathml(parts[0])+'</div>\n'
        except:
            result += '<div class="blockformula">'+convError+'</div>'
        if len(parts) == 2:
            result += convert(parts[1], extras, splitParagraphs=False)
        else:
            result += '<div class="blockformula">'+incomplete+'</div>'
    # else find first \(..\)-equation:
    else:
        parts = re.split(r'\\\(', mdtex, 1)
    if len(parts) > 1 and not found:
        found = True
        subp = re.split(r'\\\)', parts[1], 1)
        try:
            mathml = tex2mathml(subp[0])
        except:
            mathml = convError
        if parts[0].endswith('\n\n') or parts[0] == '':  # make sure textblock starts before formula!
            parts[0] = parts[0]+'&#x200b;'
        if len(subp) == 2:
            result = convert(parts[0]+mathml+subp[1], extras, splitParagraphs=False)
        else:
            result = convert(parts[0]+mathml+incomplete, extras, splitParagraphs=False)
    if not found:
        # no more formulas found
        result = md2html(mdtex, extras=extras)
    return result
