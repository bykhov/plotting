# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The zero baseline is a property of the encoding, not a style preference. A bar
# encodes its value as a length, so cutting the axis rescales every length and the
# reader has no way to know. The same numbers drawn as points may be cut, because a point
# is at a position and is not a measurement of the distance to the baseline, and that is
# the panel to reach for when the differences are the finding. A second position encoding,
# a loss curve, is in plot_cutaxis.py.
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
    'mathtext.fontset': 'cm',
})

C_BAR = '#1E90FF'
CUT = 91.5

models = ['A', 'B', 'C', 'D']
acc = np.array([92.1, 93.4, 92.8, 94.0])       # test accuracy [%]

# the folds the four accuracies are averages of, for the interval panel (c) needs
n_fold = 5
rf = np.random.default_rng(5)
folds = rf.normal(0.0, 0.35, (len(models), n_fold))
folds += rf.normal(0.0, 0.25, (1, n_fold))     # a fold effect shared by every model
folds -= folds.mean(axis=1, keepdims=True)     # so each row averages to its stated value
folds = acc[:, None] + folds
T95_DF4 = 2.776                                # t_{0.975} on 4 degrees of freedom
ci = T95_DF4 * folds.std(axis=1, ddof=1) / np.sqrt(n_fold)

fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.3))

# --- (a) the same numbers, axis cut just below the smallest bar ---
axes[0].bar(models, acc, width=0.6, color=C_BAR)
axes[0].set_ylim(CUT, 94.5)
axes[0].set_title('(a) bars, axis cut')
axes[0].set_ylabel('accuracy [%]')

# --- (b) the same numbers as points, where the same cut is legitimate ---
axes[1].errorbar(np.arange(len(models)), acc, yerr=ci, fmt='o', ms=4.5, color=C_BAR,
                 ecolor=C_BAR, elinewidth=1.0, capsize=2.5)
axes[1].set_xticks(np.arange(len(models)))
axes[1].set_xticklabels(models)
axes[1].set_xlim(-0.5, len(models) - 0.5)
axes[1].set_ylim(CUT, 94.5)
axes[1].set_title('(b) points, axis cut, ' + r'$95\%$' + ' CI')

# --- (c) the same numbers, honest baseline ---
axes[2].bar(models, acc, width=0.6, color=C_BAR)
axes[2].set_ylim(0, 100)
axes[2].set_title('(c) bars, zero baseline')

for ax in axes:
    ax.grid(True, axis='y', alpha=0.25)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

plt.tight_layout()

basename = 'plot_baseline'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what the cut does to the ratio the eye reads off the bar lengths ---
true_ratio = acc.max() / acc.min()
cut_ratio = (acc.max() - 91.5) / (acc.min() - 91.5)
print(f'accuracies {acc}')
print(f'true length ratio D:A = {true_ratio:.2f}, '
      f'ratio seen in panel (a) = {cut_ratio:.2f}, '
      f'exaggeration factor {cut_ratio / true_ratio:.1f}')
print()
print(f'panel (b), cut at {CUT:g}, {n_fold} folds, 95 % CI:')
for m, a, c in zip(models, acc, ci):
    print(f'    {m}: {a:.2f} +/- {c:.2f} points')
lo, hi = acc - ci, acc + ci
print('    intervals that overlap A: ' +
      ', '.join(m for m, l in zip(models[1:], lo[1:]) if l <= hi[0]))
