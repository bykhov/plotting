# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The accumulation itself, a_n = 1 - (1-alpha)^n, with the ink drawn as the fill of the
# markers on one curve so the curve and the page agree. Past the dashed level a further mark
# changes nothing a reader can see, which is where transparency stops reporting count.
#
# Every number the caption quotes is printed at the end.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import to_rgb

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
FULL = 0.95                                # ink past which a further mark is invisible
ALPHAS = [0.5, 0.2, 0.05, 0.01]
A_SHOW = 0.05                              # the curve whose ink is drawn as marker fill
LABEL_Y = {0.5: 0.90, 0.2: 0.70, 0.05: 0.50, 0.01: 0.28}   # one label height per curve
SHOW_N = (1, 2, 5, 10, 50, 200)


def ink(alpha, n):
    """Ink accumulated by n marks of opacity alpha stacked at one spot."""
    return 1.0 - (1.0 - alpha) ** n


def over(top, bottom, alpha):
    """The color of a mark of opacity alpha composited over a background."""
    t, b = np.array(to_rgb(top)), np.array(to_rgb(bottom))
    return alpha * t + (1.0 - alpha) * b


fig, ax = plt.subplots(figsize=(3.4, 2.3))
fig.subplots_adjust(left=0.135, right=0.985, top=0.975, bottom=0.185)

n = np.logspace(0, np.log10(400), 400)
cross = {}
for alpha in ALPHAS:
    ax.plot(n, ink(alpha, n), '-', lw=1.0, color='0.55')
    n_star = np.log(1 - FULL) / np.log(1 - alpha)
    cross[alpha] = n_star
    ax.plot(n_star, FULL, 'o', ms=3, color=C_NOTE, zorder=4)
    # name each curve where it passes its own label height, so no two labels share a row
    y_lab = LABEL_Y[alpha]
    ax.annotate(rf'$\alpha = {alpha:g}$', (np.log(1 - y_lab) / np.log(1 - alpha), y_lab),
                textcoords='offset points', xytext=(5, -2), ha='left', va='center',
                fontsize=PT, color='0.35')
ax.axhline(FULL, ls='--', lw=0.8, color=C_NOTE)
# the A_SHOW curve again, its markers filled with the color the page actually renders
for k in SHOW_N:
    y = ink(A_SHOW, k)
    ax.plot(k, y, 's', ms=6.5, markerfacecolor=over(C_MARK, 'white', y),
            markeredgecolor='0.45', markeredgewidth=0.5, zorder=5)
ax.plot(n, ink(A_SHOW, n), '-', lw=1.3, color=C_MARK, zorder=3)
ax.set_xscale('log')
ax.set_xlim(1, 400)
ax.set_ylim(0, 1.16)
ax.set_yticks([0, 0.5, 1])
ax.set_xlabel(r'marks stacked at one spot, $n$', labelpad=1)
ax.set_ylabel(r'ink, $a_n$', labelpad=2)
ax.spines['left'].set_bounds(0, 1)
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
ax.grid(True, alpha=0.25)

basename = 'plot_alpha_accum'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

for alpha in ALPHAS:
    print(f'alpha {alpha:4.2f}: reaches {FULL:.2f} of full ink at n = {cross[alpha]:6.1f}, '
          f'a lone mark carries {alpha:.2f}')
print('rendered ink at alpha = %.2f:' % A_SHOW,
      ', '.join(f'n={k}: {ink(A_SHOW, k):.3f}' for k in SHOW_N))
