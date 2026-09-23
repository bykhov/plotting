# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Three grouping laws doing work inside ordinary charts: spacing makes groups,
# shared color makes series, and a connecting line makes a curve out of points that
# do not otherwise pair up. The last two panels hold identical coordinates.
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'axes.labelsize': 9,
    'mathtext.fontset': 'cm',
})

C_A = '#1E90FF'
C_B = '#E07B39'
C_NEUTRAL = '#8A94A0'

rng = np.random.default_rng(3)

fig, axes = plt.subplots(1, 4, figsize=(7.0, 1.95))

# --- proximity: one row of twelve bars, read as three groups of four ---
heights = np.array([4, 6, 5, 7, 3, 5, 4, 6, 6, 4, 7, 5], dtype=float)
gap = np.repeat(np.arange(3), 4) * 0.9
axes[0].bar(np.arange(12) + gap, heights, width=0.75, color=C_NEUTRAL)
axes[0].set_title('(a) proximity')

# --- similarity: identical positions, two colors, read as two series ---
x = np.linspace(0, 1, 24)
y = 0.5 + 0.35 * np.sin(4 * x) + rng.normal(0, 0.04, x.size)
odd = np.arange(24) % 2 == 1
axes[1].scatter(x[~odd], y[~odd], s=18, color=C_A)
axes[1].scatter(x[odd], y[odd], s=18, color=C_B)
axes[1].set_title('(b) similarity')

# --- continuity: the same dots, unpaired and then connected ---
t = np.linspace(0, 1, 18)
c1 = 0.30 + 0.55 * t
c2 = 0.85 - 0.55 * t
for ax, connect, title in ((axes[2], False, '(c) points alone'),
                           (axes[3], True, '(d) continuity')):
    style = '-o' if connect else 'o'
    ax.plot(t, c1, style, ms=3, lw=1.0, color=C_A if connect else C_NEUTRAL)
    ax.plot(t, c2, style, ms=3, lw=1.0, color=C_B if connect else C_NEUTRAL)
    ax.set_title(title)
    ax.set_ylim(0.2, 0.95)

for ax in axes:
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

plt.tight_layout()

basename = 'plot_gestalt'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print('panels (c) and (d) plot identical coordinates; only the lines differ')
