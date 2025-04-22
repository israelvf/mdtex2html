# mdtex2html
python3-library to convert Markdown with included LaTeX-Formulas to HTML with MathML

## What is mdtex2html

`mdtex2html` is a library to convert (Github-flavored) Markdown-Code with included LaTex-formulas to HTML-Source. The formulas are converted to MathML.

An inline-formula can either start and end with `$` or it can start with `\(` and end with `\)`, according to valid LaTeX-Code. Block-formulas either start and end with `$$` or start with `\[` and end with `\]`.

An example that `mdtex2html` will convert:

```
# Example-Title

TeX-Formula: $\sqrt2=x^2 \Rightarrow x=\sqrt{\sqrt{2}}$

- This
- is
    - a List with `inline-Code`
```

## How to use mdtex2html

install it, i.e. using pip:

~~`python3 -m pip install mdtex2html`~~
(comming soon)

then in python import in your code with

~~`import mdtex2html`~~
(comming soon)

and convert your mdTeX with something like

`mdtex2html.convert('- Hello ${\sqrt{World}}^2$!')`

passing any mdTeX-Code to `mdtex2html.convert()`.

### Extra

You may want to (but don't need to) include this css-snippet on your page to hide error message texts, only showing on mouse-over:

```
.tooltip .tooltiptext {
    display: none;
}
.tooltip:hover .tooltiptext {
    display: inline;
    border-radius: 0.3em;
    background-color: #777;
    position: fixed;
}
```

### Markdown2 Extras (aka extensions)

You can use markdown2 extras for i.e. tables, definition-lists, html-attributes and much more by passing a list of the extension(s) to be used to the `markdown`-command as described in the [markdown2 documentation](https://github.com/trentm/python-markdown2/wiki/Extras).

For example `markdown2.markdown("*boo!*", extras=["footnotes"])` will make use of the extension `footnotes`.

## Dependencies

This depends on:

- [latex2html](https://github.com/roniemartinez/latex2mathml)
- [Python-Markdown2](https://github.com/trentm/python-markdown2)

The dependencies will be installed when installing using pip.

## Credits

Special thanks to [Dirk Winkel](https://github.com/polarwinkel), for creating [mdtex2html](https://github.com/polarwinkel/mdtex2html), [Ronie Martinez](https://github.com/roniemartinez), for creating [latex2html](https://github.com/roniemartinez/latex2mathml), and [Trent Mick](https://github.com/trentm), for creating [Python-Markdown2](https://github.com/trentm/python-markdown2)!

This library is just a few adjustments of [Dirk Winkel](https://github.com/polarwinkel) [code](https://github.com/polarwinkel/mdtex2html), to use [Python-Markdown2](https://github.com/trentm/python-markdown2) instead of [Python-Markdown](https://github.com/Python-Markdown/markdown).
