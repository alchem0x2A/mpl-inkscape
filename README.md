# mpl-inkscape
Matplotlib backend for exporting Inkscape svg + TeX math

## Purpose of backend

The vector graphic designer `Inkscape` is a powerful tool combining
`svg` with `TeX` by using its `pdf+LaTeX` exporting engine. One can
easily edit the math equations / symbols / formulae in a way close to
WYSIWYG and render using `TeX` engines without the steep learning
curve of other TeX tools like `pgf` or `Tikz`.

The original svg backend of `matplotlib` works nicely to generate a
svg file, however the math notations in text and axis labels are
exported as collections of glyphs with pre-computed
coordinates. Directly using svg files exported by original svg backend
will cause the math equations to break after TeX rendering.
