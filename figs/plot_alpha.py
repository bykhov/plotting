# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# One dense scatter, drawn three ways, to fix what alpha is for and where it stops working.
# The data has three parts a reader would want: a broad cloud, a dense core inside it and a
# small tight knot. (a) is the library default, alpha = 1, where the marks that arrive last
# cover the ones before them and the panel reports the outline of the cloud. (b) is alpha =
# 0.5, which changes almost nothing, because ink accumulates as 1 - (1-alpha)^n and is
# already full by the seventh mark. (c) is alpha matched to the typical overlap, measured
# from the data rather than guessed, where the core and the knot appear.
#
# Every number the caption quotes is printed at the end, including the measured overlap and
# the fraction of points that land on ink that is already full.
import numpy as np
import matplotlib.pyplot as plt

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

PT = 9
C_MARK = '#1E90FF'
C_NOTE = '#B03A2E'
MS = 1.6                                   # marker diameter, points
XLIM, YLIM = (-3.4, 3.4), (-3.0, 3.0)

# --- the record: a broad cloud, a dense core, a tight knot ------------------------
rng = np.random.default_rng(11)
cloud = rng.normal(0.0, 1.15, size=(12000, 2))
core = rng.normal(0.0, 1.0, size=(7000, 2)) * 0.45 + np.array([0.85, 0.35])
knot = rng.normal(0.0, 1.0, size=(1000, 2)) * 0.16 + np.array([-0.95, -0.55])
P = np.vstack([cloud, core, knot])
rng.shuffle(P)                             # draw order is an accident, which is the point
N = P.shape[0]


def ink(alpha, n):
    """Ink accumulated by n marks of opacity alpha stacked at one spot."""
    return 1.0 - (1.0 - alpha) ** n


def exhausted_at(alpha, tol=0.01):
    """The mark count past which a further mark changes the ink by less than tol."""
    if alpha >= 1.0:
        return 1
    return int(np.ceil(np.log(tol) / np.log(1.0 - alpha)))


fig = plt.figure(figsize=(5.4, 2.15))
gs = fig.add_gridspec(1, 3, wspace=0.30,
                      left=0.078, right=0.995, top=0.88, bottom=0.20)
axes = [fig.add_subplot(gs[0, k]) for k in range(3)]

for k, ax in enumerate(axes):
    ax.set_xlim(*XLIM)
    ax.set_ylim(*YLIM)
    ax.set_xticks([-2, 0, 2])
    ax.set_yticks([-2, 0, 2])
    ax.set_xlabel('$x_1$', labelpad=1)
    if k == 0:
        ax.set_ylabel('$x_2$', labelpad=1)
    else:
        ax.set_yticklabels([])
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

# --- measure the overlap the marks actually produce on the page -------------------
# A marker covers MS points across, so points closer than that share ink. Converting MS
# into data units needs the panel width in points, which is known only after a layout.
fig.canvas.draw()
bb = axes[0].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
cell = MS * (XLIM[1] - XLIM[0]) / (bb.width * 72.0)      # marker footprint, data units
gx = np.floor((P[:, 0] - XLIM[0]) / cell).astype(np.int64)
gy = np.floor((P[:, 1] - YLIM[0]) / cell).astype(np.int64)
cell_id = gx * (10 ** 6) + gy
uniq, inv, counts = np.unique(cell_id, return_inverse=True, return_counts=True)
per_point = counts[inv]                                  # marks sharing this point's spot
n_typ = int(np.median(per_point))

# rank of each point inside its own cell, in draw order: rank 0 draws on white
order = np.argsort(cell_id, kind='stable')
s_id = cell_id[order]
starts = np.flatnonzero(np.r_[True, s_id[1:] != s_id[:-1]])
run = np.diff(np.r_[starts, s_id.size])
rank = np.empty(N, dtype=np.int64)
rank[order] = np.arange(s_id.size) - np.repeat(starts, run)

alpha_matched = round(1.0 / n_typ, 3)
ALPHAS = [1.0, 0.5, alpha_matched]


def hidden_fraction(alpha):
    """Share of the points that land where the ink is already full."""
    return float(np.mean(rank >= exhausted_at(alpha)))


TITLES = [r'(a) $\alpha = 1$, as drawn',
          r'(b) $\alpha = 0.5$',
          rf'(c) $\alpha = {alpha_matched:g}$, matched']

for ax, alpha, title in zip(axes, ALPHAS, TITLES):
    ax.scatter(P[:, 0], P[:, 1], s=MS ** 2, color=C_MARK, alpha=alpha,
               linewidths=0, rasterized=True)
    ax.set_title(title)

# the knot is the structure the first two panels lose: name it once, on the panel that has it
axes[2].annotate('knot', xy=(-0.95, -0.55), xytext=(-3.1, -2.5), fontsize=PT, color=C_NOTE,
                 arrowprops=dict(arrowstyle='-', lw=0.7, color=C_NOTE,
                                 shrinkA=0, shrinkB=3))

basename = 'plot_alpha'
plt.savefig(f'{basename}.pdf', bbox_inches='tight', dpi=300)
plt.savefig(f'{basename}.svg', bbox_inches='tight', dpi=300)
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

print(f'{N} points, marker {MS} pt across, footprint {cell:.4f} data units')
print(f'typical overlap n_typ = {n_typ} marks per footprint, '
      f'so the matched alpha is 1/{n_typ} = {alpha_matched:g}')
for alpha in ALPHAS:
    n_ex = exhausted_at(alpha)
    print(f'alpha {alpha:5.3f}: ink full by n = {n_ex:3d}, '
          f'a lone mark carries {alpha:.3f} of full ink, '
          f'{100 * hidden_fraction(alpha):5.1f}% of the points land on full ink')
print(f'ink at alpha = 0.5 after 2 marks {ink(0.5, 2):.3f} and after 7 {ink(0.5, 7):.3f}')
print(f'ink at alpha = {alpha_matched:g} after {n_typ} marks '
      f'{ink(alpha_matched, n_typ):.3f}')
