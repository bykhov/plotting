# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# One series, one set of axis limits, four axes shapes. Nothing about the data changes
# between the panels; the slope the reader perceives grows by an order of magnitude.
# Panels (a) to (c) change the height of the axes; (d) and (e) repeat (c) at two thirds and
# at a third of the width, since what sets the angle is the ratio of the two page scales and
# not which side of it is moved.
# The dashed line of panels (c) to (e) is the least-squares fit of the same series, so it is
# one slope drawn three times and only its angle on the page changes. The two flattest
# panels are left as the bare series.
# The median segment angle each panel delivers is measured at the end of the script, and
# the trend angle beside it, so the caption quotes what the figure does rather than what
# it was aiming for.
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

C_LINE = '#1E90FF'
C_TREND = '0.72'          # 28% ink, the context gray of the highlight figure
TREND_DASH = (0, (4, 2))  # dashed as well as light: the fit is not a second measurement

rng = np.random.default_rng(19)
t = np.arange(0, 60)
y = 100 + 0.55 * t + 3.0 * np.sin(t / 4.5) + rng.normal(0, 1.2, t.size)

# One fit, drawn in every panel: the same slope, five angles.
K, B = np.polyfit(t, y, 1)

YLIM = (95, 140)
FIGSIZE = (4.6, 6.4)
HEIGHTS = [0.45, 1.15, 2.30, 2.30]             # relative row heights
TITLES = ['(a) wide and short: the trend flattens out',
          '(b) balanced: the rise and the wobble are both visible',
          '(c) tall and narrow: the noise reads as structure',
          '(d) panel (c) at two thirds of the width',
          '(e) panel (c) at a third of the width']

fig = plt.figure(figsize=FIGSIZE)
gs = fig.add_gridspec(4, 6, height_ratios=HEIGHTS, hspace=0.55, wspace=0.0,
                      left=0.13, right=0.98, top=0.97, bottom=0.06)
# The last row keeps the height of (c) and carries the two narrowed copies side by side,
# on a fine column grid so that their widths are set directly: (d) takes two thirds of the
# row and (e) a third of it, with one column left between them as a gap.
bottom = gs[3, :].subgridspec(1, 45, wspace=0.0)
cells = [gs[0, :], gs[1, :], gs[2, :], bottom[0, 0:30], bottom[0, 31:45]]

axes = []
for cell, title in zip(cells, TITLES):
    ax = fig.add_subplot(cell)
    ax.plot(t, y, '-', lw=1.0, color=C_LINE)
    ax.set_ylim(*YLIM)
    ax.set_xlim(t[0], t[-1])
    ax.set_title(title, loc='left')
    ax.set_yticks([100, 120, 140])
    ax.set_xticks([0, 20, 40])
    ax.grid(True, alpha=0.25)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    axes.append(ax)

axes[3].set_xlabel('sample index')      # not on (c): its label would collide with the
axes[4].set_xlabel('sample index')      # title of the row below it
# (e) sits against (d) and repeats its limits, so one set of y tick labels serves both.
axes[4].tick_params(labelleft=False)
axes[1].set_ylabel('value')
# The fit goes on the three panels that have the height to show an angle; on (a) and (b) it
# would be one more nearly horizontal line beside the series.
for ax in axes[2:]:
    ax.plot(t, K * t + B, linestyle=TREND_DASH, lw=1.0, color=C_TREND, zorder=3)

basename = 'plot_aspect'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the median segment angle each panel actually delivers ---
# Measured from the axes boxes themselves, so a change of width counts the same way a
# change of height does. Cleveland's rule asks for a median segment near 45 degrees; on a
# series this noisy the median segment is mostly noise, so the panels bracket the target
# rather than hit it, and what the reader sees is the spread between them.
# The fitted slope goes through the same normalization, which is what the dashed line of
# panels (c) to (e) is drawn at; it is printed for all five, since (a) and (b) are the
# comparison even without the line on them.
slope = np.abs(np.diff(y) / (YLIM[1] - YLIM[0])) / (np.diff(t) / np.ptp(t))
trend_slope = abs(K) * np.ptp(t) / (YLIM[1] - YLIM[0])
angles, trend_angles = [], []
for ax, title in zip(axes, TITLES):
    box = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
    angles.append(np.degrees(np.arctan(np.median(slope) * box.height / box.width)))
    trend_angles.append(np.degrees(np.arctan(trend_slope * box.height / box.width)))
    print(f'axes {box.width:4.2f} by {box.height:4.2f} in -> median segment angle '
          f'{angles[-1]:5.1f} deg, trend angle {trend_angles[-1]:5.1f} deg  {title[:24]}')
print(f'perceived slope grows by a factor of '
      f'{np.tan(np.radians(max(angles))) / np.tan(np.radians(angles[0])):.0f} '
      f'from the flattest panel to the steepest')
print(f'least-squares fit: slope {K:.3f} per sample, intercept {B:.1f}, one line drawn '
      f'at {min(trend_angles):.1f} to {max(trend_angles):.1f} deg across the five panels')
