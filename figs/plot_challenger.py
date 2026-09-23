# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The O-ring damage record of the 23 shuttle flights that preceded Challenger,
# drawn twice: once from the damage flights alone, which is roughly the selection
# discussed the night before the launch, and once from every flight. The second
# panel is the plot that was never made.
#
# Data: DAAG::orings (R package DAAG, "Challenger O-rings Data"), 23 rows, taken
# from https://vincentarelbundock.github.io/Rdatasets/csv/DAAG/orings.csv
# Original source: Report of the Presidential Commission on the Space Shuttle
# Challenger Accident, Vol. 1, 1986, pp. 129-131.
#
# On the plotted quantity. DAAG's Total column is Erosion + Blowby, which counts a
# ring twice when it suffered both. Tufte's figure plots the number of *distinct*
# damaged rings, which for every row of this dataset is max(Erosion, Blowby): the
# 53F flight had 3 eroded rings, 2 of them also blown by, so 3 rings damaged and
# not the 5 that Total reports. That is the column reproduced here.
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

C_FLIGHT = '#1E90FF'
C_ALERT = '#D62728'
C_RANGE = '#9AA5B1'

# --- DAAG::orings, in file order: Temperature, Erosion, Blowby, Total ---
orings = np.array([
    [53, 3, 2, 5], [57, 1, 0, 1], [58, 1, 0, 1], [63, 1, 0, 1],
    [66, 0, 0, 0], [67, 0, 0, 0], [67, 0, 0, 0], [67, 0, 0, 0],
    [68, 0, 0, 0], [69, 0, 0, 0], [70, 1, 0, 1], [70, 0, 0, 0],
    [70, 1, 0, 1], [70, 0, 0, 0], [72, 0, 0, 0], [73, 0, 0, 0],
    [75, 0, 0, 0], [75, 0, 2, 1], [76, 0, 0, 0], [76, 0, 0, 0],
    [78, 0, 0, 0], [79, 0, 0, 0], [81, 0, 0, 0],
])
temp, erosion, blowby, total = orings.T
damaged = np.maximum(erosion, blowby)

# The subset the DAAG help page names as the pre-launch chart selection,
# orings[c(1,2,4,11,13,18),] in R's 1-based indexing. Note that it leaves out the
# 58F flight of row 3, which also showed damage.
PRELAUNCH = np.array([1, 2, 4, 11, 13, 18]) - 1

FORECAST = 31.0                     # forecast O-ring temperature, 28 January 1986


def spread(x, width=0.7):
    """Deterministic symmetric offsets so tied points stay countable.

    Overplotting would hide that three flights sit at 67F and four at 70F, and a
    reader cannot count marks that are drawn on top of one another.
    """
    out = np.zeros_like(x, dtype=float)
    for value in np.unique(x):
        idx = np.flatnonzero(x == value)
        if idx.size > 1:
            out[idx] = np.linspace(-width / 2, width / 2, idx.size)
    return x + out


fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), sharex=True, sharey=True)

panels = [
    (axes[0], PRELAUNCH, '(a) pre-launch selection, 6 flights'),
    (axes[1], np.arange(len(temp)), '(b) the full record, 23 flights'),
]

for ax, idx, title in panels:
    ax.plot(spread(temp[idx]), damaged[idx], 'o', ms=5, color=C_FLIGHT,
            mfc=C_FLIGHT, mec='white', mew=0.6, zorder=3)
    ax.set_title(title)
    ax.set_xlabel('O-ring temperature [°F]')
    ax.set_xlim(28, 85)
    ax.set_ylim(-0.35, 3.6)
    ax.set_xticks([30, 40, 50, 60, 70, 80])
    ax.set_yticks([0, 1, 2, 3])
    ax.grid(True, alpha=0.25)

axes[0].set_ylabel('damaged O-rings per launch')

# --- the launch morning, and how far outside the record it sat ---
ax = axes[1]
ax.axvspan(temp.min(), temp.max(), color=C_RANGE, alpha=0.18, lw=0, zorder=0)
ax.axvline(FORECAST, color=C_ALERT, lw=1.2, zorder=2)
ax.annotate(f'{FORECAST:.0f}°F\nforecast', xy=(FORECAST, 2.6),
            xytext=(FORECAST + 3, 3.1), fontsize=9, color=C_ALERT, va='top',
            arrowprops=dict(arrowstyle='-', color=C_ALERT, lw=0.8))
ax.text((temp.min() + temp.max()) / 2, 3.25, 'observed range', fontsize=9,
        color='0.35', ha='center', va='center')

plt.tight_layout()

basename = 'plot_challenger'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

print('\n temp  erosion  blowby  total  damaged  prelaunch')
for i in range(len(temp)):
    mark = 'x' if i in PRELAUNCH else ''
    print(f'{temp[i]:5d} {erosion[i]:8d} {blowby[i]:7d} {total[i]:6d} '
          f'{damaged[i]:8d}  {mark:>5s}')

cold = temp <= 63
print(f'\nflights at or below 63F: {cold.sum()}, all damaged: {bool((damaged[cold] > 0).all())}')
print(f'flights above 63F: {(~cold).sum()}, of which damaged: {(damaged[~cold] > 0).sum()}')
print(f'coldest prior launch {temp.min()}F, forecast {FORECAST:.0f}F, '
      f'extrapolation {temp.min() - FORECAST:.0f}F below the record')
print(f'damage flights in the pre-launch subset: {len(PRELAUNCH)} of '
      f'{(damaged > 0).sum()} in the full record')
