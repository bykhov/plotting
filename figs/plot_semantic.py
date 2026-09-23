# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Color carries meaning the data may not intend. One quarterly profit and loss
# record drawn twice: once with red for profit and green for loss, so that every
# bar's color contradicts its own sign, and once with the convention and the sign
# in agreement. The data, the axes, the baseline and the printed values are
# identical between the panels, so the only difference is which sign gets which
# color.
#
# The second panel does not use green either: red against green is the pair that
# roughly 8% of men cannot separate (plot_cvd.py, plot_cvd_types.py), so the
# positive side is the Okabe-Ito blue and only the negative side keeps the
# conventional red.
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

# Twelve quarters of operating result, in millions. Mixed sign, and the sign is
# the thing the reader is meant to take away.
values = np.array([1.8, 2.4, -0.9, 1.1, 2.9, -1.7, 0.6, 3.2, -2.3, 1.4, 2.1, -0.5])
quarter = np.arange(1, len(values) + 1)

RED = '#D55E00'    # Okabe-Ito vermillion
GREEN = '#009E73'  # Okabe-Ito bluish green
BLUE = '#0072B2'   # Okabe-Ito blue

# (a) profit red, loss green: the color of every bar contradicts its sign.
# (b) profit blue, loss red: the color of every bar agrees with its sign.
schemes = [
    (RED, GREEN, '(a) profit red, loss green: every bar fights its own sign'),
    (BLUE, RED, '(b) profit blue, loss red: color and sign agree'),
]

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.7), sharey=True)

for ax, (pos_color, neg_color, title) in zip(axes, schemes):
    colors = [pos_color if v > 0 else neg_color for v in values]
    ax.bar(quarter, values, color=colors, width=0.72)
    ax.axhline(0, color='black', linewidth=0.8)  # bars need their zero baseline
    # No '+' on the gains: the bar direction and the baseline already carry the
    # sign, and four characters per bar do not fit at this width.
    for q, v in zip(quarter, values):
        ax.text(q, v + (0.18 if v > 0 else -0.18), f'{v:.1f}',
                ha='center', va='bottom' if v > 0 else 'top', fontsize=9)
    ax.set_xticks(quarter)
    ax.set_xlabel('quarter')
    ax.set_xlim(0.4, len(values) + 0.6)
    ax.set_ylim(-3.4, 4.2)
    ax.set_title(title)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

axes[0].set_ylabel(r'operating result [M\$]')

plt.tight_layout()

basename = 'plot_semantic'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- how much of the panel is at war with itself? ---
# Under the convention red = loss, green = gain, a bar is contradicted when a
# positive value is drawn red or a negative value green.
n_pos = int((values > 0).sum())
n_neg = int((values < 0).sum())
print(f'\n(a) {n_pos + n_neg} of {len(values)} bars carry a color that contradicts '
      f'their sign: {n_pos} profits in red, {n_neg} losses in green')
print(f'(b) 0 of {len(values)} bars contradict their sign')
print(f'    profits {n_pos}, losses {n_neg}, '
      f'total {values.sum():+.1f} M$ over {len(values)} quarters')
