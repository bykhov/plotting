---
name: html-latex-fixes
description: Diagnose and fix wrong lwarp HTML output in node-*.html / index.html - misplaced or missing table rules, wrong column counts, uncentered sub-figure panels, garbled tcolorbox title bars, truncated style="..." attributes - and the toolchain traps that cause them. Use proactively before running lwarpmk html and whenever the PDF looks correct but the HTML does not.
user-invocable: true
---

# HTML / LaTeX Fixes (lwarp)

This project builds one LaTeX source into both PDF and HTML through **lwarp**. Almost
every "HTML looks wrong" report falls into one of two buckets: the toolchain mangled a
correct PDF during conversion, or lwarp genuinely emitted the wrong markup. Tell those
apart *first* — the checks below are cheap and the first one has already caused one wrong
diagnosis and a wasted patch to lwarp's internals.

## Use this skill when

- About to run `lwarpmk html` or `lwarpmk again`.
- A table, figure, or colored box renders correctly in `plotting.pdf` but wrong in
  `node-*.html` / `index.html`.
- Tags in the generated HTML look broken: attributes on the wrong element, a `style="`
  that never closes, text from one line appearing on another.
- Editing `lwarp_academic.css`, or touching tabular column types / `\newcolumntype`.

## 1. Check the toolchain first

`lwarpmk` shells out to a bare `pdftotext` off `PATH`. lwarp requires **poppler's** build.
This machine also has **Xpdf's** at `/mingw64/bin/pdftotext`, which is what a Git Bash /
MSYS2 shell resolves first.

Xpdf's `-layout` does column detection. On lwarp's HTML-as-text pages it chops long inline
`style="..."` attributes in half and moves the tail onto an earlier line, so `<td>` and
tcolorbox `<div>` tags come out with garbage attributes and truncated styles — table rules
and box title bars silently lose their colors.

```bash
pdftotext -v          # must say "The Poppler Developers", NOT "Glyph & Cog"
```

If it is the wrong one, put MiKTeX's poppler build ahead for the build:

```bash
export PATH="/c/Users/Administrator/AppData/Local/Programs/MiKTeX/miktex/bin/x64:$PATH"
```

Other poppler copies on this machine live under the anaconda `Library/bin`. Do not blame
lwarp until `pdftotext -v` is clean.

## 2. Never build with `-jobname`

`pdflatex -jobname=check plotting.tex` makes lwarp rewrite `lwarpmk.conf` from the job name,
which then points `lwarpmk` at a source that does not exist. If it happens:

```bash
cp plotting.lwarpmkconf lwarpmk.conf     # canonical copy, sourcename = plotting
```

To test-compile without touching `plotting.pdf` (e.g. when it is locked by a viewer), prefer
fixing the lock over changing the job name.

## 3. Is it lwarp, or the conversion?

`plotting_html.pdf` holds the HTML as typeset text; `pdftotext` extracts it. Compare reading
order against physical layout on the offending page:

```bash
pdftotext -enc UTF-8 -nopgbrk -raw    -f N -l N plotting_html.pdf -   # reading order
pdftotext -enc UTF-8 -nopgbrk -layout -f N -l N plotting_html.pdf -   # what lwarpmk uses
```

- Correct in `-raw`, mangled in `-layout` → the **conversion** is at fault. Go back to
  step 1.
- Wrong in `-raw` too → **lwarp** emitted it wrong. Find the emitting macro in
  `lwarp.sty` (`kpsewhich lwarp.sty`) and patch it, per step 5.

To locate the page number of a construct, scan the layout output and count page breaks.

## 4. Fixes already in place — do not re-break them

| Fix | Where | Why |
|---|---|---|
| `\HTMLnewcolumntype{L/C/R}` next to the real `\newcolumntype` | `config2.tex` | lwarp parses tabular preambles itself and does not know these take an argument, so `L{3cm}\|L{3cm}` counts as four columns (`L`, `{3cm}`, `L`, `{3cm}`) and the `\|` rules land on the wrong cells. Widths are irrelevant in HTML; only the type letter matters, as it picks the `tdl`/`tdc`/`tdr` class. |
| `tabulary` deliberately **not** loaded | `plotting.tex` | lwarp's HTML replacement `lwarp-tabulary.sty` redefines `L`/`C`/`R` as zero-argument types and silently clobbers the project's, in the HTML build only. It is unused here. |
| `align-items: center` on `figure div.minipage` | `lwarp_academic.css` | lwarp renders each `subfigure` / `\subcaptionbox` panel as an inline-flex column and drops the panel's `\centering`. The panel's width is set by its sub-caption, not its image, so with the default `stretch` the image sits flush left. Do not use `text-align: center` instead — that would also center the wrapped lines of long sub-captions. |

## 5. Where to make a change

- **`lwarp.css`** is regenerated on every build. Never edit it.
- **`lwarp_academic.css`** is hand-maintained and `@import`s `lwarp.css`. All HTML styling
  goes here. It is not regenerated, so a CSS-only fix needs **no rebuild** — just reload.
- **LaTeX-side, HTML-only** tweaks go in a `\begin{warpHTML}...\end{warpHTML}` block in
  `config2.tex` (it is `\input` after lwarp is loaded, so lwarp's macros are available).
  Patching lwarp internals there works but is fragile — exhaust steps 1-3 first.

## 6. Rebuild and verify

```bash
lwarpmk again && lwarpmk html
```

`lwarpmk html` alone is a no-op when only an `\input` file changed — it compares
timestamps against the main source only, so `lwarpmk again` is what forces the recompile.

Integrity greps on the result:

```bash
grep -c 'border-right:$\|border-left:$\|border-top:$' node-*.html   # must be 0 everywhere
grep -c 'style="[^"]*$' node-*.html                                 # only lwarp's own
                                                                    # multi-line style=" /
                                                                    # width:NNNpt; blocks
```

For a visual check, the browser extension **cannot open `file://`**. Serve the directory
first:

```bash
python -m http.server 8731 --bind 127.0.0.1
```

then browse `http://127.0.0.1:8731/node-19.html`. Measuring
`getBoundingClientRect()` on the affected elements is a fast way to prove alignment or
centering claims instead of eyeballing a screenshot. Stop the server when done.
