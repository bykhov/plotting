# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Similarity with an order in it. One grouped bar chart, five model versions scored on
# three classes, shaded two ways:
#
#   (a) the arbitrary palette a library or a slide deck hands out, one of the five
#       being white with an outline;
#   (b) the same five on a light-to-dark ramp, so that the shading carries the order
#       the versions already have.
#
# Proximity makes the three groups in both panels. What changes is whether a series can
# be traced across the groups: in (a) there is nothing to trace by, since the levels
# have no order, and in (b) each group is the same ladder and a series is found by its
# rank rather than by matching a swatch.
#
# The panels are gray on purpose. Lightness is the part of a color that carries an
# order (plot_colorsort.py), and the argument is meant to survive a black-and-white
# print by construction rather than by luck.
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

MM = 25.4
versions = ['v1', 'v2', 'v3', 'v4', 'v5']
groups = ['class A', 'class B', 'class C']
K, G = len(versions), len(groups)

# One record: five successive versions of a model, scored on three classes.
f1 = np.array([[0.61, 0.64, 0.66, 0.71, 0.69],
               [0.78, 0.81, 0.83, 0.86, 0.88],
               [0.72, 0.75, 0.74, 0.79, 0.82]]).T        # versions along the rows

# (a) is the deck's palette: a mid gray, a light gray, black, white, a dark gray. The
# white bar is kept because it is half the lesson: a fill equal to the page is read as
# a gap in the row, and only its outline says a value is there at all.
ARB = [0.55, 0.80, 0.00, 1.00, 0.40]
# The ramp stays well clear of black at both ends. A near-black bar swallows its own
# outline and outweighs everything beside it, and the ladder does not need the extra
# range: five equal steps inside the middle of the scale are separable, and the whole
# set then sits at a weight the page can carry. The arbitrary palette keeps its black,
# since it is the palette under criticism.
RAMP = list(np.linspace(0.90, 0.35, K))                  # light to dark, equal steps

BAR_LW = 0.8
fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.9), sharey=True)
width = 0.16
pos = np.arange(G)

bars_a = []
for ax, levels, title in ((axes[0], ARB, '(a) shaded in no particular order'),
                          (axes[1], RAMP, '(b) the same five, light to dark')):
    for k in range(K):
        b = ax.bar(pos + (k - (K - 1) / 2) * width, f1[k], width * 0.92,
                   color=str(levels[k]), edgecolor='black', linewidth=BAR_LW,
                   label=versions[k])
        if levels is ARB:
            bars_a.append(b[0])
    ax.set_ylim(0, 1.0)                                  # bars encode length, so zero
    ax.set_xticks(pos)
    ax.set_xticklabels(groups)
    ax.set_title(title, pad=20)   # the title stays above its own key
    ax.grid(True, axis='y', alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.005), ncol=K,
              frameon=False, handlelength=1.4, columnspacing=1.2, handletextpad=0.5)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
axes[0].set_ylabel('$F_1$ score')

plt.tight_layout()

basename = 'plot_gradation'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')


def inversions(levels):
    """Pairs of series whose shading contradicts their order."""
    return sum(1 for i in range(len(levels)) for j in range(i + 1, len(levels))
               if levels[i] < levels[j])                  # darker should mean later


# --- the two palettes, as the caption quotes them ---------------------------------
pairs = K * (K - 1) // 2
for name, levels in (('(a)', ARB), ('(b)', RAMP)):
    steps = np.abs(np.diff(levels))
    inv = inversions(levels)
    print(f'{name} gray levels ' + ' '.join(f'{v:.2f}' for v in levels))
    print(f'    {inv} of the {pairs} pairs are shaded against their order, '
          f'and the smallest step between neighbors is {steps.min():.2f}')

print(f'\nso the arbitrary palette is not short of contrast: its closest neighbors '
      f'differ by {np.abs(np.diff(ARB)).min():.2f} against {np.abs(np.diff(RAMP)).min():.2f} '
      f'on the ramp. What it has is no order.')

# --- what the white bar puts on the page ------------------------------------------
fig.canvas.draw()
r = fig.canvas.get_renderer()
white = bars_a[ARB.index(1.00)]
bb = white.get_window_extent(renderer=r)
w_mm, h_mm = bb.width / fig.dpi * MM, bb.height / fig.dpi * MM
edge_mm = BAR_LW / 72 * MM
ink = 2 * (w_mm + h_mm) * edge_mm
print(f'\nthe white bar is {w_mm:.1f} by {h_mm:.1f} mm and its only ink is its '
      f'{edge_mm:.2f} mm outline, {ink:.0f} of the {w_mm * h_mm:.0f} square mm a '
      f'filled bar of the same size covers, that is {100 * ink / (w_mm * h_mm):.0f}%')
