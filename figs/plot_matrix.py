# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Which quantity the cells of a matrix hold. One 4x4 cross-channel transfer record drawn as
# the loss against the reference the comparison is actually made against: as a zero-anchored
# shaded grid, as the same grid with the fill replaced by a mark whose area carries the
# loss, as a test of whether the relation is symmetric at all, and as a dot plot on one
# common scale.
# The accuracies the losses are taken from are the previous figure, plot_matrix_raw.py.
# The data is in plot_matrix_data.py, which is shared with the other two matrix figures.
# The three transfers that give up the least accuracy, CLOSE in that module, are the one
# marked set of the figure: outlined in (a), open in (b), inside the shaded bands of (c),
# which show what the other panels only assert, and open again in (d).
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle

from plot_matrix_data import (ACC, GAP, CLOSE, OFF, N, CHANNELS, ROW_MEAN,
                              COL_MEAN, PAIR_ASYM, UPAIRS, PAIRS, summary)

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'mathtext.fontset': 'cm',
})

CELL_PT = 9          # never below the 9 pt floor of the font section
C_MARK = '#1E90FF'
LOST = "accuracy lost vs. the target's own model"
S_MAX = 220          # the area, in points squared, of the mark for the largest loss
C_PLAIN = '0.62'     # the nine ordinary transfers: gray, so the color budget is not spent
                     # on them (the one-strong-color rule of the color section)


def gray(rgb):
    """The gray a black-and-white print leaves, as defined in the color section."""
    r, g, b = matplotlib.colors.to_rgb(rgb)
    return 0.21 * r + 0.72 * g + 0.07 * b


def label_axes(ax):
    ax.set_xticks(range(N))
    ax.set_yticks(range(N))
    ax.set_xticklabels(CHANNELS)
    ax.set_yticklabels(CHANNELS)
    ax.set_xlabel('test (target) channel')
    ax.set_ylabel('train (source) channel')
    ax.tick_params(length=0)


fig = plt.figure(figsize=(6.9, 5.6))
gs = fig.add_gridspec(2, 2, hspace=0.38, wspace=0.45,
                      left=0.085, right=0.965, top=0.94, bottom=0.075)

# --- (a) the matrix, on the quantity the comparison is about ----------------------
# The grid is extended by one cell to the right and below, and the row and column means
# live in that band: outside the colored grid, so they cannot be mistaken for cells, and
# inside the axes, so they cannot collide with the tick labels.
ax = fig.add_subplot(gs[0, 0])
cmap = plt.get_cmap('YlOrBr')
norm = matplotlib.colors.Normalize(vmin=0.0, vmax=GAP[OFF].max())
im = ax.imshow(GAP, cmap=cmap, norm=norm)
for i in range(N):
    for j in range(N):
        txt = '0' if i == j else f'{GAP[i, j]:.3f}'
        ax.text(j, i, txt, ha='center', va='center', fontsize=CELL_PT,
                color='black' if gray(cmap(norm(GAP[i, j]))) > 0.5 else 'white')
        if CLOSE[i, j]:                              # the three closest transfers
            ax.add_patch(Rectangle((j - 0.5, i - 0.5), 1, 1, fill=False,
                                   edgecolor=C_MARK, lw=1.8, zorder=3))
for i in range(N):                                   # how good a source each row is
    ax.text(N + 0.05, i, f'{ROW_MEAN[i]:.3f}', ha='center', va='center', fontsize=CELL_PT)
for j in range(N):                                   # how easy a target each column is
    ax.text(j, N + 0.05, f'{COL_MEAN[j]:.3f}', ha='center', va='center', fontsize=CELL_PT)
ax.text(N + 0.05, N + 0.05, 'mean', ha='center', va='center', fontsize=CELL_PT, style='italic')
ax.plot([N - 0.5, N - 0.5], [-0.5, N + 0.6], '-', color='0.35', lw=0.9, zorder=4)
ax.plot([-0.5, N + 0.6], [N - 0.5, N - 0.5], '-', color='0.35', lw=0.9, zorder=4)
ax.set_xlim(-0.5, N + 0.6)
ax.set_ylim(N + 0.6, -0.5)
label_axes(ax)
ax.set_title('(a) accuracy lost, zero anchored')
# The bar hugs its own panel and takes the short label: the long phrase has room on the x
# axis of (d), and a rotated label here is what closes the gap between the two columns.
cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.05)
cb.set_label('accuracy lost', fontsize=CELL_PT)
cb.ax.tick_params(labelsize=CELL_PT)

# --- (b) the same grid, with the fill replaced by a mark ---------------------------
# The layout of (a) and the same twelve numbers, one step up the ranking: the loss is the
# area of a mark rather than the strength of a fill, so the panel needs no colorbar and no
# cell is judged against the shade of its neighbors. What area gives up is precision,
# which is why the value is printed under every mark; and an exact zero draws nothing, so
# the diagonal empties itself without being told to.
ax = fig.add_subplot(gs[0, 1])
U = GAP / GAP[OFF].max()             # the loss on [0, 1], as plot_matrix_forms.py takes it
jj, ii = np.meshgrid(range(N), range(N))
m = OFF & ~CLOSE                     # the nine, in gray: they carry the area and nothing else
ax.scatter(jj[m], ii[m], s=S_MAX * U[m], color=C_PLAIN, zorder=3)
m = OFF & CLOSE                      # the marked set, open and in the figure's one color,
                                     # as it is open in (d) and outlined in (a)
ax.scatter(jj[m], ii[m], s=S_MAX * U[m], facecolor='white', edgecolor=C_MARK,
           linewidth=1.3, zorder=4)
for i in range(N):
    for j in range(N):
        txt = '0' if i == j else f'{GAP[i, j]:.3f}'
        ax.text(j, i + 0.40, txt, ha='center', va='center', fontsize=CELL_PT, color='0.35')
ax.set_xlim(-0.6, N - 0.4)
ax.set_ylim(N - 0.30, -0.6)
ax.set_aspect('equal')               # square cells, so the grid reads as the grid of (a)
label_axes(ax)
ax.grid(True, color='0.9', lw=0.5)
ax.set_axisbelow(True)
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
ax.set_title('(b) the same losses as circle area')

# --- (c) is the relation symmetric? ------------------------------------------------
# Six points, not twelve: a point is one pair, and its two directions are its two
# coordinates. Which direction lands on which axis is the i < j convention of UPAIRS,
# so the axes have to say so or the point cannot be decoded.
# Hand-placed label offsets: three of the six pairs cluster near (0.02, 0.05), where the
# automatic corner would drop two labels on top of a third point.
# The three closest transfers are shown here rather than flagged. The band holds every
# loss below the cut between the third and the fourth smallest, so a point inside it has
# a direction among the three, and {1,2}, inside both arms, transfers well either way.
OFFSET = {(0, 1): (7, -2, 'left'), (0, 2): (7, -2, 'left'), (0, 3): (-6, -7, 'right'),
          (1, 2): (0, 9, 'center'), (1, 3): (6, 4, 'left'), (2, 3): (-6, 4, 'right')}
ax = fig.add_subplot(gs[1, 0])
hi = GAP[OFF].max() * 1.15
ax.plot([0, hi], [0, hi], '-', color='0.6', lw=0.9, zorder=1)
ax.text(hi * 0.72, hi * 0.74, 'symmetric', fontsize=CELL_PT, ha='center', va='bottom',
        color='0.45', rotation=45, rotation_mode='anchor')
CUT = 0.5 * (np.sort(GAP[OFF])[2] + np.sort(GAP[OFF])[3])
# One patch for the union of the two bands, not two overlapping ones: a darker corner
# would read as a third level of something and there are only two.
ax.add_patch(Polygon([(0, 0), (hi, 0), (hi, CUT), (CUT, CUT), (CUT, hi), (0, hi)],
                     closed=True, facecolor=C_MARK, alpha=0.10, lw=0, zorder=0))
ax.text(hi * 0.99, CUT * 0.42, 'the three closest transfers', ha='right', va='center',
        fontsize=CELL_PT, color=C_MARK)
for i, j in UPAIRS:
    dx, dy, ha = OFFSET[(i, j)]
    ax.plot(GAP[i, j], GAP[j, i], 'o', ms=5, color=C_MARK, zorder=3)
    ax.annotate(rf'$\{{{i},{j}\}}$', (GAP[i, j], GAP[j, i]), textcoords='offset points',
                xytext=(dx, dy), fontsize=CELL_PT, ha=ha)
ax.set_xlim(0, hi)
ax.set_ylim(0, hi)
ax.set_aspect('equal')
ax.set_xlabel(r'accuracy lost, $i\rightarrow j$   ($i<j$)')
ax.set_ylabel(r'accuracy lost, $j\rightarrow i$')
ax.set_title('(c) the six pairs, both directions each')
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
ax.grid(True, alpha=0.25)

# --- (d) the same twelve numbers as position on a common scale --------------------
ax = fig.add_subplot(gs[1, 1])
order = sorted(PAIRS, key=lambda p: GAP[p])
ys = np.arange(len(order))
for y, (i, j) in zip(ys, order):
    ax.plot([0, GAP[i, j]], [y, y], '-', color='0.8', lw=0.8, zorder=1)
    ax.plot(GAP[i, j], y, 'o', ms=5, zorder=2,
            markerfacecolor='white' if CLOSE[i, j] else C_MARK,
            markeredgecolor=C_MARK, markeredgewidth=1.2)
ax.set_yticks(ys)
ax.set_yticklabels([rf'${i}\rightarrow{j}$' for i, j in order])
ax.set_ylim(len(order) - 0.5, -0.5)
ax.set_xlim(0, GAP[OFF].max() * 1.12)
ax.axvline(0, color='k', lw=0.8)
ax.set_xlabel(LOST)
ax.set_title('(d) the same twelve numbers, on an axis')
ax.tick_params(axis='y', length=0)
for side in ('top', 'right', 'left'):
    ax.spines[side].set_visible(False)
ax.grid(True, axis='x', alpha=0.25)
ax.annotate('the three closest transfers', (GAP[2, 1], 1), textcoords='offset points',
            xytext=(9, 1), fontsize=CELL_PT, va='center', color=C_MARK)

basename = 'plot_matrix'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print(summary())
worst_col = int(np.argmin([ACC[OFF[:, j], j].mean() for j in range(N)]))
best_col = int(np.argmin(COL_MEAN))
print(f'the accuracies read ch {worst_col} as the hardest target; (a) makes ch {best_col} '
      f'the easiest')
print('most asymmetric pairs: ' + ', '.join(
    '{%d,%d} %.4f' % (i, j, PAIR_ASYM[i, j])
    for i, j in sorted(UPAIRS, key=lambda p: -PAIR_ASYM[p])[:2]))
ratio = GAP[OFF].max() / GAP[OFF].min()
print('(b) largest loss %.4f, smallest %.4f' % (GAP[OFF].max(), GAP[OFF].min()))
print('(b) between them: %.1fx of value, %.1fx of area, %.1fx of diameter'
      % (ratio, ratio, np.sqrt(ratio)))
print('(b) the diagonal is an exact zero, so its mark has zero area and draws nothing')
