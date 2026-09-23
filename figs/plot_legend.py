# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The two ways to name a series. Four curves drawn twice on identical axes: once
# with a boxed legend at the matplotlib default position, and once with the names
# set at the ends of the lines they belong to.
#
# Three costs of the box are measured below rather than asserted: the fraction of
# the panel it covers, whether it overlaps data, and how far its entry order is
# from the order the curves arrive in at the right edge, which is the order the
# reader sees. Each mismatch is one more re-sort the reader performs per lookup.
#
# The look-up itself is the serial operation of plot_lookup.py: a boxed legend
# turns naming a curve into a search, while a label at the line end is read in
# place. The end label also survives gray conversion and color vision deficiency
# (plot_cvd.py), because there the name identifies the curve and the color only
# decorates it.
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,          # the floor from the font section
    'mathtext.fontset': 'cm',
})

rng = np.random.default_rng(5)
N = 90
step = np.arange(1, N + 1)
# Learning curves against training set size, which is a curve all four of these
# models have. None of them is trained by epoch.
n_train = np.linspace(100, 2000, N)

# Four models, plotted in the order they were trained, which is not the order
# they finish in. The legend inherits the plotting order; the reader sees the
# finishing order.
names = ['ridge', 'k-NN', 'linear SVM', 'random forest']
start = np.array([1.62, 1.48, 1.71, 1.55])
# The four floors are spread far enough that the end labels of panel (b) clear
# one another. Where curves do converge at the right edge, an end label stops
# working and a box or a leader line is the honest answer; that is the one case
# the subsection reserves for the box.
floor = np.array([0.70, 0.34, 0.52, 0.16])
rate = np.array([0.055, 0.040, 0.065, 0.030])
curves = (floor[:, None] + (start[:, None] - floor[:, None])
          * np.exp(-rate[:, None] * step)
          + rng.normal(0, 0.014, (len(names), N)))

# Okabe-Ito, the palette of plot_cvd.py panel (c).
colors = ['#0072B2', '#D55E00', '#009E73', '#CC79A7']
YLIM = (0.10, 1.95)

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), sharey=True)

# --- (a) boxed legend, default placement, plotting order ---
ax = axes[0]
for c, name, col in zip(curves, names, colors):
    ax.plot(n_train, c, lw=1.2, color=col, label=name)
leg = ax.legend(loc='best', framealpha=1.0, handlelength=1.8, borderpad=0.4)
ax.set_xlim(0, 2050)
ax.set_title('(a) boxed legend, where the library put it')

# --- (b) the same four, named where they end ---
ax = axes[1]
for c, name, col in zip(curves, names, colors):
    ax.plot(n_train, c, lw=1.2, color=col)
    ax.text(2080, c[-1], name, color=col, va='center', ha='left', fontsize=9)
ax.set_xlim(0, 3050)            # right margin sized for the longest name at 9 pt
ax.set_title('(b) the same four, labeled at the line ends')

for ax in axes:
    ax.set_ylim(*YLIM)
    ax.set_xticks([0, 500, 1000, 1500, 2000])
    ax.set_xlabel('training set size [samples]')
    ax.grid(True, alpha=0.25)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
axes[0].set_ylabel('validation loss')

plt.tight_layout()

basename = 'plot_legend'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what the box costs, in the units the caption quotes ---
fig.canvas.draw()
ax = axes[0]
box = leg.get_window_extent().transformed(ax.transData.inverted())
panel_w = ax.get_xlim()[1] - ax.get_xlim()[0]
panel_h = YLIM[1] - YLIM[0]
area = 100 * (box.width * box.height) / (panel_w * panel_h)

# Does the box sit on top of any curve?
inside = ((n_train >= box.x0) & (n_train <= box.x1))
covered = sum(bool(((c[inside] >= box.y0) & (c[inside] <= box.y1)).any())
              for c in curves)

# Legend order against the order the curves arrive in at the right edge.
legend_order = list(range(len(names)))
edge_order = list(np.argsort(-curves[:, -1]))       # topmost curve first
swaps = sum(1 for i, j in zip(legend_order, edge_order) if i != j)

print(f'\n(a) the legend box covers {area:.0f}% of the panel and lies over '
      f'{covered} of the {len(names)} curves')
print(f'    legend order      {[names[i] for i in legend_order]}')
print(f'    order at the edge {[names[i] for i in edge_order]}')
print(f'    {swaps} of {len(names)} entries are out of place, so the reader '
      f're-sorts on every lookup')
print(f'(b) 0% of the panel spent on a key, {len(names)} names read in place')
