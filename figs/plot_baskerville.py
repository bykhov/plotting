# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The two faces that came first and second in the 2012 New York Times quiz, in which one
# passage was set in one of six typefaces chosen at random and about 45,000 readers were
# asked whether they agreed with it. Agreement ran about 1.5 points higher in Baskerville
# than in the rest, with Computer Modern the runner-up.
#
#   (a) the same sentence in both, at reading size, which is how the readers met it;
#   (b) a few letters of each, magnified, since at reading size the two are a pair of
#       serif book faces no ordinary reader could name apart.
#
# That is why these two are shown rather than the whole field: whatever produced the
# difference, it was not anybody noticing the typeface.
#
# Panel (b) draws glyph outlines rather than text, and an outline lives in data
# coordinates, so the panel is given a data range equal to its own size in points. One
# data unit is then one typographic point on the printed page, which is what makes the
# magnification stated in its title true rather than approximate.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch
from matplotlib.transforms import Affine2D

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'mathtext.fontset': 'cm',
})

# (name shown, family actually used)
FACES = [('Baskerville', 'Baskerville Old Face'),
         ('Computer Modern', 'cmr10')]

SENTENCE = 'the Earth is unlikely to be destroyed by an asteroid'
READ_PT = 11.0                       # the size panel (a) is set and printed at
LETTERS = 'agne'                     # a few letters, chosen for their serifs and bowls
BIG_PT = 66.0                        # the close-up, 6 times READ_PT
PT_MM = 25.4 / 72.0
GRID = 2000                          # columns of the mask the ink is measured on


def path_of(text, family, pt):
    return TextPath((0, 0), text, prop=FontProperties(family=family), size=pt)


def stem_width(family, pt=100.0):
    """The width of the left stem of an n, measured across the ink at mid height."""
    p = path_of('n', family, pt)
    bb = p.get_extents()
    y = bb.y0 + 0.5 * (bb.y1 - bb.y0)
    xs = np.linspace(bb.x0 - 2, bb.x1 + 2, GRID)
    ink = p.contains_points(np.column_stack([xs, np.full(GRID, y)]))
    first = int(np.flatnonzero(ink)[0])
    end = first
    while end + 1 < ink.size and ink[end + 1]:
        end += 1
    return (xs[end] - xs[first]) / pt        # as a fraction of the point size


def metrics(family):
    xh = path_of('x', family, 100.0).get_extents().y1
    cap = path_of('H', family, 100.0).get_extents().y1
    return xh / 100.0, cap / 100.0, xh / cap, stem_width(family)


measured = {name: metrics(fam) for name, fam in FACES}

# --- the figure, authored at final width so a point here is a point on the page ----
# Panel (b) is sized from the letters it has to hold rather than from a guess, since a
# panel that is one point too short crops a glyph instead of scaling it.
paths = [path_of(LETTERS, fam, BIG_PT) for _, fam in FACES]
boxes = [p.get_extents() for p in paths]
H = max(b.y1 for b in boxes)                 # cap height of the magnified row
DESC = -min(b.y0 for b in boxes)             # the descender of the g
GAP = 0.34 * BIG_PT                          # baseline to baseline, less the descender
BASE = 0.16 * BIG_PT + DESC                  # baseline of the lower row

FIG_W = 7.0
TITLE = 0.24                         # room above each panel for its title, inches
H_A = 0.80                           # two lines of the sentence, inches
H_B = (BASE + H + GAP + H + 0.10 * BIG_PT) / 72.0
FIG_H = H_B + TITLE + H_A + TITLE
fig = plt.figure(figsize=(FIG_W, FIG_H))

# --- (a) one sentence, the two faces, at reading size -----------------------------
ax = fig.add_axes([0.0, (H_B + TITLE) / FIG_H, 1.0, H_A / FIG_H])
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')
ax.set_title('(a) one passage, two of the six typefaces it was set in',
             loc='left', x=0.02)

X_NAME, X_TEXT = 0.04, 0.23
for i, (name, family) in enumerate(FACES):
    y = 0.56 - i * 0.40
    ax.text(X_NAME, y, name, fontsize=9, color='0.35', ha='left', va='baseline')
    ax.text(X_TEXT, y, SENTENCE, family=family, fontsize=READ_PT, ha='left',
            va='baseline')

# --- (b) a few letters of each, magnified -----------------------------------------
ax = fig.add_axes([0.0, 0.0, 1.0, H_B / FIG_H])
ax.set_xlim(0, FIG_W * 72)           # one data unit is one point on the page
ax.set_ylim(0, H_B * 72)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(rf'(b) the same letters in both, magnified ${BIG_PT / READ_PT:.0f}\times$',
             loc='left', x=0.02, pad=2)

NAMES = 132.0                                     # room for the face names
BLOCK = NAMES + max(b.x1 - b.x0 for b in boxes)
X_LET = (FIG_W * 72 - BLOCK) / 2 + NAMES          # the block sits centered

for j, ((name, family), path, bb) in enumerate(zip(FACES, paths, boxes)):
    y = BASE + (1 - j) * (H + GAP)
    ax.add_patch(PathPatch(path, facecolor='0.15', edgecolor='none',
                           transform=Affine2D().translate(X_LET - bb.x0, y)
                           + ax.transData))
    # Panel (a) already shows both faces at reading size, so a second copy at that
    # size here would be the same statement twice.
    ax.text(X_LET - 14, y + 0.30 * H, name, fontsize=9, color='0.35',
            ha='right', va='center')

basename = 'plot_baskerville'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- how alike the two are, measured off their outlines ---------------------------
print(f'\nsentence set at {READ_PT:.0f} pt, close-up at {BIG_PT:.0f} pt, a '
      f'magnification of {BIG_PT / READ_PT:.0f}; both are the sizes on the page')
print('metrics as a fraction of the point size')
print('face              x-height   cap    x/cap   stem')
for name, family in FACES:
    xh, cap, ratio, stem = measured[name]
    print(f'{name:16s} {xh:7.3f} {cap:7.3f} {ratio:7.3f} {stem:6.3f}')

a, b = FACES[0][0], FACES[1][0]
xa, _, ra, sa = measured[a]
xb, _, rb, sb_ = measured[b]
print(f'\n{a} against {b}:')
print(f'  x-height differs by {abs(xa - xb) / max(xa, xb):.1%}, '
      f'x-height over cap height by {abs(ra - rb) / max(ra, rb):.1%}, '
      f'stem width by {abs(sa - sb_) / max(sa, sb_):.1%}')
print(f'  at {READ_PT:.0f} pt that is {abs(xa - xb) * READ_PT * PT_MM:.3f} mm of '
      f'x-height and {abs(sa - sb_) * READ_PT * PT_MM:.4f} mm of stem, both far below '
      f'the 2 mm at which detail stops being resolved')
