# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# What a legend key is made of. Five learning curves, drawn twice from one record,
# with a boxed legend in both panels so that the only thing changing between them is
# the channel the key maps.
#
#   (a) dash pattern and marker shape, all in black. Both are nominal channels: the
#       keys have no order among them, so the reader matches a glyph to a key, and
#       has to do it again at every crossing, which is where the curves are densest.
#   (b) line width and lightness, varied together along one ladder. Both are ordered,
#       so the five keys are a sequence rather than a set: read once, the reader can
#       predict the rest, and the vertical order of the curves is the order of the key.
#
# Panel (b) is the deliberate exception to "do not encode anything twice" of
# plot_declutter.py: the redundancy is what makes the key survive a gray print and a
# color vision deficiency simulation (plot_cvd.py), which a color-only key does not.
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
    'legend.fontsize': 9,
    'mathtext.fontset': 'cm',
})

# Five models on the learning curve of plot_legend.py: accuracy against training set
# size, which is a curve all five of them have.
names = ['ridge', 'k-NN', 'SVM', 'forest', 'MLP']
K = len(names)
n_train = np.linspace(200, 2000, 12)

rng = np.random.default_rng(11)
# The five plateaus are spread far enough that the curves are separated where the
# reader is asked to compare them, and close enough at the left that they cross while
# they are still climbing, which is where a nominal key costs the most.
ceiling = np.array([0.762, 0.826, 0.878, 0.932, 0.800])
start = np.array([0.700, 0.686, 0.672, 0.706, 0.662])
rate = np.array([2.2, 1.5, 1.8, 1.3, 1.7]) / 1000.0
curves = (ceiling[:, None] - (ceiling - start)[:, None]
          * np.exp(-rate[:, None] * (n_train - n_train[0]))
          + rng.normal(0, 0.007, (K, n_train.size)))

YLIM = (0.62, 1.02)

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)

# --- (a) nominal channels: a dash pattern and a marker shape per series -----------
patterns = [('-', 'o', 'black'), ('-', 'o', 'white'), ('-', 's', 'black'),
            ('--', None, 'black'), (':', None, 'black')]
ax = axes[0]
for c, name, (ls, mk, mfc) in zip(curves, names, patterns):
    ax.plot(n_train, c, ls=ls, marker=mk, ms=4.5, mfc=mfc, mec='black',
            lw=1.1, color='black', label=name)
ax.set_title('(a) keyed by pattern and marker')

# --- (b) ordered channels: width and lightness, moved together -------------------
order = np.argsort(-curves[:, -1])          # topmost curve first, so the key is sorted
widths = np.array([2.6, 2.0, 1.5, 1.0, 0.7])
grays = np.array([0.00, 0.22, 0.42, 0.58, 0.72])
ax = axes[1]
for rank, j in enumerate(order):
    ax.plot(n_train, curves[j], '-', lw=widths[rank], color=str(grays[rank]),
            label=names[j])
ax.set_title('(b) the same five, width and lightness together')

for ax in axes:
    ax.set_ylim(*YLIM)
    ax.set_xlim(0, 2100)
    ax.set_xticks([0, 500, 1000, 1500, 2000])
    ax.set_xlabel('training set size [samples]')
    ax.grid(True, alpha=0.25)
    ax.set_axisbelow(True)
    # The key goes where there is no data, which for a rising curve is the top left.
    ax.legend(loc='upper left', framealpha=1.0, handlelength=2.2, borderpad=0.4,
              labelspacing=0.25)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
axes[0].set_ylabel('validation accuracy')

plt.tight_layout()

basename = 'plot_patterned'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what each key costs, in the units the caption quotes -------------------------
crossings = 0
for i in range(K):
    for j in range(i + 1, K):
        d = curves[i] - curves[j]
        crossings += int((np.sign(d[:-1]) != np.sign(d[1:])).sum())
marks = sum(1 for _, mk, _ in patterns if mk) * n_train.size
print(f'\n{K} series of {n_train.size} points, crossing one another {crossings} times')
print(f'(a) {K} keys with no order among them, and {marks} markers on the page; at '
      f'each of the {crossings} crossings both curves are identified again by glyph')
print('    ' + ', '.join(f'{n}: {ls!r}{"" if mk is None else " " + mk}'
                         for n, (ls, mk, _) in zip(names, patterns)))
print(f'(b) one ladder, width {widths[0]:.1f} to {widths[-1]:.1f} pt against gray '
      f'{grays[0]:.2f} to {grays[-1]:.2f}, both moving with the rank')
print('    widths ' + ' '.join(f'{w:.1f}' for w in widths) +
      ' pt, grays ' + ' '.join(f'{g:.2f}' for g in grays))
print(f'    the smallest step between neighbors is '
      f'{np.abs(np.diff(widths)).min():.1f} pt of width and '
      f'{np.abs(np.diff(grays)).min():.2f} of gray, and the two always move together')
edge = list(np.argsort(-curves[:, -1]))
print(f'    order of the key   {[names[j] for j in order]}')
print(f'    order at the edge  {[names[j] for j in edge]}')
print(f'    the two agree: {edge == list(order)}, so the key is read once rather than '
      f'per curve')
