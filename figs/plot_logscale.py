# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# An eigenvalue spectrum spanning five decades, drawn on a linear and a logarithmic
# axis. The linear panel is not wrong, it is simply blind below the first decade:
# every eigenvalue after the fourth is pinned to the axis and the exponential decay
# that the log panel shows as a straight line is invisible.
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

C_MARK = '#1E90FF'
C_KNEE = '#D62728'

rng = np.random.default_rng(5)
k = np.arange(1, 25)
lam = 400.0 * np.exp(-0.55 * (k - 1)) * np.exp(rng.normal(0, 0.12, k.size))

KNEE = 6                                       # where the spectrum stops falling fast

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.6))

for ax, logy, title in ((axes[0], False, '(a) linear axis'),
                        (axes[1], True, '(b) logarithmic axis')):
    ax.plot(k, lam, 'o-', ms=4, lw=1.0, color=C_MARK)
    ax.axvline(KNEE, color=C_KNEE, lw=1.0, ls='--')
    if logy:
        ax.set_yscale('log')
        ax.set_ylim(1e-4, 1e3)
    else:
        ax.set_ylim(0, 450)
    ax.set_xlabel('component index $k$')
    ax.set_ylabel(r'eigenvalue $\lambda_k$')
    ax.set_title(title)
    ax.grid(True, alpha=0.25, which='major')   # minor decade lines are pure ink
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

# the cut is named by its own index rather than described
axes[1].text(KNEE + 0.4, 3e-4, f'$k = {KNEE}$', fontsize=9, color=C_KNEE,
             ha='left', va='bottom')

plt.tight_layout()

basename = 'plot_logscale'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

span = np.log10(lam.max() / lam.min())
below = (lam < 0.01 * lam.max()).sum()
print(f'spectrum spans {span:.1f} decades, from {lam.max():.3g} to {lam.min():.3g}')
print(f'{below} of {k.size} eigenvalues are below 1% of the largest, so on the '
      f'linear axis they sit within one marker of zero')
