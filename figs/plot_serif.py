# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# What a serif is, at a magnification where it can be seen. One letter drawn in the two
# text faces at the same size, with the foot of its left stem measured against the stem
# itself: in a serif face the foot is several times the stem, and in a sans-serif face
# the foot is the stem. That difference is the whole of the distinction, and it is also
# why the serif is the first thing a small size or a poor projector takes away.
#
# Nothing here is placed by hand. The glyph is a TextPath, the ink is measured off that
# path on a grid, and the marks are put at the runs of ink the measurement finds, so
# the figure cannot drift out of agreement with the numbers printed below it.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath
from matplotlib.patches import PathPatch, Circle

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.sans-serif': ['Arial'],
    'font.size': 10,
    'axes.titlesize': 9,
    'mathtext.fontset': 'cm',
})

LETTER = 'n'
BIG_PT = 200.0                       # the size the close-up is drawn at
READ_PT = 9.0                        # the size a tick label is read at
FACES = [('serif', 'Times New Roman'), ('sans-serif', 'Arial')]
C_MARK = '#D55E00'
GRID = 1200                          # columns of the mask the ink is measured on


def glyph(name, pt):
    return TextPath((0, 0), LETTER, prop=FontProperties(family=name), size=pt)


def runs(path, y, x0, x1):
    """The horizontal runs of ink the glyph has at height y, in path coordinates."""
    xs = np.linspace(x0, x1, GRID)
    inside = path.contains_points(np.column_stack([xs, np.full(GRID, y)]))
    out, start = [], None
    for i, v in enumerate(inside):
        if v and start is None:
            start = xs[i]
        elif not v and start is not None:
            out.append((start, xs[i - 1]))
            start = None
    if start is not None:
        out.append((start, xs[-1]))
    return out


paths = [glyph(name, BIG_PT) for _, name in FACES]
boxes = [p.get_extents() for p in paths]
H = max(b.y1 for b in boxes)                     # one scale for both panels
W = max(b.x1 for b in boxes)

# --- measure first, so the panels can be titled with what they show ---------------
measured = []
for (family, name), path, bb in zip(FACES, paths, boxes):
    y_foot = bb.y0 + 0.03 * (bb.y1 - bb.y0)      # just above the baseline
    y_mid = bb.y0 + 0.55 * (bb.y1 - bb.y0)       # clear of both foot and shoulder
    y_head = bb.y0 + 0.92 * (bb.y1 - bb.y0)      # the head of the same stem
    feet = runs(path, y_foot, bb.x0 - 5, bb.x1 + 5)
    stems = runs(path, y_mid, bb.x0 - 5, bb.x1 + 5)
    head = runs(path, y_head, bb.x0 - 5, bb.x1 + 5)[0]
    measured.append((family, name, feet, stems, y_foot, y_mid,
                     feet[0][1] - feet[0][0], stems[0][1] - stems[0][0],
                     head, y_head))

smalls = [glyph(name, READ_PT) for _, name in FACES]
X_SMALL = 1.32 * W                               # where the reading-size letter goes
# One pair of limits for both panels, so the two faces are drawn at one scale and the
# comparison is not a matter of trust.
XLIM = (min(b.x0 for b in boxes) - 0.10 * W,
        X_SMALL + max(s.get_extents().width for s in smalls) + 0.06 * W)
YLIM = (-0.22 * H, 1.12 * H)

fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.6))

for j, (ax, path, m, small) in enumerate(zip(axes, paths, measured, smalls)):
    family, name, feet, stems, y_foot, y_mid, w_foot, w_stem, head, y_head = m
    ax.add_patch(PathPatch(path, facecolor='0.15', edgecolor='none'))

    # The two widths the distinction lives in, drawn where they were measured.
    for (a, b), y in ((feet[0], y_foot), (stems[0], y_mid)):
        ax.plot([a, b], [y, y], '-', lw=2.0, color=C_MARK, solid_capstyle='butt',
                zorder=3)
    # Every foot the measurement finds, ringed, so the serifs are pointed at rather
    # than described. In the sans-serif panel the same rings enclose bare stem ends.
    for a, b in feet:
        ax.add_patch(Circle(((a + b) / 2, boxes[j].y0 + 0.06 * H), 0.11 * H,
                            fill=False, edgecolor=C_MARK, lw=0.9, zorder=2))
    # The head of the left stem, which in a serif face carries a flag and in a
    # sans-serif face is a cut end.
    ax.add_patch(Circle(((head[0] + head[1]) / 2, y_head), 0.11 * H, fill=False,
                        edgecolor=C_MARK, lw=0.9, zorder=2))

    # The same letter at the size it is actually read at, so the magnification is on
    # the page instead of in the caption.
    sb = small.get_extents()
    ax.add_patch(PathPatch(small, facecolor='0.15', edgecolor='none',
                           transform=(plt.matplotlib.transforms.Affine2D()
                                      .translate(X_SMALL - sb.x0, 0.06 * H)
                                      + ax.transData)))
    ax.text(X_SMALL + sb.width / 2, -0.02 * H, f'{READ_PT:.0f} pt', fontsize=9,
            ha='center', va='top', color='0.35')

    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_aspect('equal')
    ax.axis('off')
    # The ratio itself stays in the caption; the panel says which face it is.
    ax.set_title(f'({"ab"[j]}) {family}: {name}')

plt.tight_layout()

basename = 'plot_serif'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the distinction, in the units the caption quotes -----------------------------
print(f'\nletter "{LETTER}" at {BIG_PT:.0f} pt, a magnification of '
      f'{BIG_PT / READ_PT:.0f} over the {READ_PT:.0f} pt of a tick label')
print('face                       foot    stem   foot/stem')
for family, name, _, _, _, _, w_foot, w_stem, head, _ in measured:
    print(f'{family:10s} {name:15s} {w_foot:6.1f}  {w_stem:6.1f}     '
          f'{w_foot / w_stem:.2f}   head {head[1] - head[0]:5.1f}, that is '
          f'{(head[1] - head[0]) / w_stem:.2f} of the stem')
serif_ratio, sans_ratio = (m[6] / m[7] for m in measured)
print(f'so the serif face carries a foot {serif_ratio:.1f} times its own stem, and the '
      f'sans-serif face {sans_ratio:.2f} times')
print(f'at {READ_PT:.0f} pt that extra width is '
      f'{(measured[0][6] - measured[0][7]) * READ_PT / BIG_PT:.2f} pt, or '
      f'{(measured[0][6] - measured[0][7]) * READ_PT / BIG_PT * 25.4 / 72:.3f} mm, '
      f'which is what a small size or a projector loses first')
