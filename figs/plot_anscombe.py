# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Anscombe's quartet: four datasets that agree on mean, variance, correlation and
# least-squares line, and agree on nothing a reader would care about. The summary
# statistics are computed here rather than quoted, so the caption's numbers and the
# panels come from the same array.
#
# Data: F. J. Anscombe, "Graphs in Statistical Analysis", The American
# Statistician 27(1), 1973, pp. 17-21, Table 1.
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'mathtext.fontset': 'cm',
})

C_POINT = '#1E90FF'
C_FIT = '#D62728'

x123 = np.array([10, 8, 13, 9, 11, 14, 6, 4, 12, 7, 5], dtype=float)
x4 = np.array([8, 8, 8, 8, 8, 8, 8, 19, 8, 8, 8], dtype=float)

sets = [
    ('I', x123, np.array([8.04, 6.95, 7.58, 8.81, 8.33, 9.96, 7.24, 4.26, 10.84, 4.82, 5.68])),
    ('II', x123, np.array([9.14, 8.14, 8.74, 8.77, 9.26, 8.10, 6.13, 3.10, 9.13, 7.26, 4.74])),
    ('III', x123, np.array([7.46, 6.77, 12.74, 7.11, 7.81, 8.84, 6.08, 5.39, 8.15, 6.42, 5.73])),
    ('IV', x4, np.array([6.58, 5.76, 7.71, 8.84, 8.47, 7.04, 5.25, 12.50, 5.56, 7.91, 6.89])),
]

# What each panel actually contains, which is the part no statistic reports.
verdict = {
    'I': 'a linear relation with scatter',
    'II': 'an exact curve, not a line',
    'III': 'a tight line and one outlier',
    'IV': 'one point decides the slope',
}

# Equal axis scaling: x and y are the same kind of quantity here, so one unit must
# be the same length on both axes. The figure height follows from the 18:12 span
# ratio of the shared limits, otherwise the equal-aspect boxes leave a white band.
fig, axes = plt.subplots(2, 2, figsize=(7.0, 5.4), sharex=True, sharey=True)
grid = np.linspace(2, 20, 100)

for ax, (name, x, y) in zip(axes.ravel(), sets):
    slope, intercept = np.polyfit(x, y, 1)
    ax.plot(grid, intercept + slope * grid, '-', lw=1.0, color=C_FIT, zorder=2)
    ax.plot(x, y, 'o', ms=5, color=C_POINT, mec='white', mew=0.6, zorder=3)
    ax.set_title(f'{name}: {verdict[name]}')
    ax.set_xlim(2, 20)
    ax.set_ylim(2, 14)
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True, alpha=0.25)

for ax in axes[1, :]:
    ax.set_xlabel('$x$')
for ax in axes[:, 0]:
    ax.set_ylabel('$y$')

plt.tight_layout()

basename = 'plot_anscombe'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- variances use the biased (1/n) normalization used throughout the book ---
print('\nset  mean x  var x  mean y  var y   corr   intercept  slope')
for name, x, y in sets:
    slope, intercept = np.polyfit(x, y, 1)
    print(f'{name:>3s} {x.mean():7.2f} {np.var(x):6.2f} {y.mean():7.2f} '
          f'{np.var(y):6.2f} {np.corrcoef(x, y)[0, 1]:6.3f} '
          f'{intercept:10.2f} {slope:6.2f}')
