# Figure text size

How to set font size in the three figure generators so that labels are readable both
in `plotting.pdf` and in the HTML build, and why the same number means something different
in each tool.

Baseline for every rule below: the book is `\documentclass[a4paper,12pt,...]` with
`textwidth=7in` (504 pt), and the HTML body text renders at 16 px.

## Target

Aim for **10 pt in the figure's own PDF**, and never go below **9 pt**.

Against the 12 pt body that is the usual 0.83 ratio in print, and with the HTML scale
factor described below it lands at 16 to 18 px against 16 px body text.

| tool | set this | in the PDF | on screen |
|---|---|---|---|
| matplotlib | `font.size: 10` | 10.0 pt | 17.3 px |
| MATLAB | `'FontSize', 10` | 10.0 pt | 17.3 px |
| draw.io | font size **14** | 10.1 pt | 18.2 px |
| floor | 9 / 9 / **13** | 9.0 / 9.0 / 9.4 pt | 15.6 / 15.6 / 16.9 px |

## Why the numbers differ: units

Only matplotlib is 1:1 in both directions. The other two are not.

| tool | unit you type | factor to PDF pt | factor to CSS px |
|---|---|---|---|
| matplotlib | pt | 1.000 | 1.333 |
| MATLAB | pt | 1.000 | 1.333, or 1.778 (see caveat) |
| draw.io | **px** | 0.720 | 1.000 |

The 1.333 comes from the SVG carrying its size in `pt` while the browser renders
1 pt as 4/3 px. draw.io writes its SVG in `px`, so it renders 1:1 on screen but
shrinks by 0.72 on the way into the PDF.

## matplotlib

```python
plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,        # legend, annotations, anything unspecified
    'axes.titlesize': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,   # ticks one step down, at the floor
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'mathtext.fontset': 'cm',
})
```

Points in, points out: whatever you set here is exactly what appears in the PDF and
in the SVG. Keep `figsize` at 7.0 in or less so LaTeX never has to shrink the figure.

Note that many existing `figs/*.py` scripts set `font.size: 10` but then
override titles, labels and ticks to 9. That is what pulls the matplotlib corpus
median down to 9.0 pt.

## MATLAB

```matlab
set(findall(gcf, '-property', 'FontName'), 'FontName', 'Times New Roman')
set(findall(gcf, '-property', 'FontSize'), 'FontSize', 10)
exportgraphics(gcf, 'name.pdf')
exportgraphics(gcf, 'name.svg')
exportgraphics(gcf, 'name.jpeg', 'Resolution', 300)
```

**Caveat: check the SVG after exporting.** Most MATLAB exports outline the glyphs, so
the SVG matches the PDF. Some instead write live `<text>` elements with the size in px
while the viewBox unit is a pt, and those render 4/3 larger in HTML than in print
(10 pt becomes 23 px instead of 17 px). The same MATLAB build produces both kinds, so
what triggers it is unknown; treat it as a post-export check:

```bash
grep -c '<text' name.svg     # 0 = outlined, matches the PDF; >0 = 4/3 larger in HTML
```

Seven figures currently do this and are pinned to `--figscale: 1` in
`lwarp_academic.css`:

```
matlab/general_aspects/anomaly_example.svg
matlab/general_aspects/classification_example.svg
matlab/general_aspects/clustering_example.svg
matlab/general_aspects/regression_example.svg
matlab/general_aspects/semisupervised_example.svg
matlab/signals_inference/granger_example.svg
dl_arch/figs/window_segmentation.svg
```

If a re-export adds or removes a file from that set, update the rule.

## draw.io

Set the font size in the Format panel to **14**, not the default 12. The default is
why the draw.io corpus median sits at 8.6 pt, just under the 9 pt floor.

Because Chrome does not render `foreignObject` inside `<img>`, the HTML build falls
back to draw.io's PNG copy of each label. Those are rendered at 4x the display box, so
they stay sharp under the HTML scale factor (about 3x effective), but they are bitmaps
rather than selectable text. Raising the font size is still the right lever; resolution
is not the problem.

## Do not resize figures in LaTeX

`\includegraphics[width=...]` rescales the text along with the image and overrides
whatever the generator was told. Set the size in the generator instead (`figsize`, the
MATLAB figure `Position`, the draw.io page), keep the export at 7 in or less, and
include it with no `width` option, as 303 of the 338 `\includegraphics` calls in the
book already do.

Of the 16 width-scaled figures whose text could be measured, four print below the 9 pt
floor purely from this:

| figure | natural width | included at | resize | printed text |
|---|---|---|---|---|
| `pca/local_global` | 892 pt (12.4 in) | `width=\linewidth` | 0.57x | 5.7 pt |
| `dl_repr/mae` | 549 pt | `width=\textwidth` | 0.92x | 6.6 pt |
| `vnn/fig2/activation_functions_derivatives` | 575 pt | `width=\linewidth` | 0.88x | 6.9 pt |
| `vnn/fig2/activation_functions` | 593 pt | `width=0.9\linewidth` | 0.76x | 7.7 pt |

## The HTML scale factor

Figures reach the browser at their print size while the text column does not, so a
10 pt label would render at 13.3 px against 16 px body text. `lwarp_academic.css`
compensates with

```css
:root { --figscale: 1.3; }
img.inlineimage[src$=".svg"] { zoom: var(--figscale); max-width: 100%; height: auto; }
```

`zoom` is the only CSS property that multiplies an image's intrinsic size and still
reflows the layout. `max-width: 100%` needs no correction for the factor: percentages
inside a zoomed element resolve in that element's own coordinate space.

That file is hand-maintained and is not regenerated by `lwarpmk`, so changing the
factor takes effect on reload with no rebuild.

## Checking a figure

Print the PDF's width and the set of text sizes actually used in it:

```bash
python -c "import fitz,sys; d=fitz.open(sys.argv[1]); p=d[0]; \
s=[(sp['size'],len(sp['text'].strip())) for b in p.get_text('dict')['blocks'] \
for l in b.get('lines',[]) for sp in l['spans']]; \
print(f'{p.rect.width:.0f}pt wide; text pt:', sorted({round(x,1) for x,n in s if n}))" figure.pdf
```

## Measured baseline

Character-weighted median text size across the 222 figures referenced by the HTML
build, measured 2026-08-24, before any of the recommendations above were applied:

| generator | figures | text in its PDF (median, range) | on screen at zoom 1 | at `--figscale: 1.3` |
|---|---|---|---|---|
| matplotlib | 116 | 9.0 pt (7 to 12) | 12.0 px | 15.6 px |
| MATLAB | 71 | 9.8 pt (7.5 to 12) | 13.1 px | 17.0 px |
| draw.io | 35 | 8.6 pt (7.2 to 10.8) | 11.9 px | 15.5 px |

Measure from the PDFs, not the SVGs: most MATLAB SVGs carry `font-size` attributes on
empty `<g>` wrappers whose glyphs are outlines, and 31 of the 35 draw.io SVGs carry
only the `font-size="10px"` of draw.io's "Text is not SVG" placeholder. Both are
decoys.
