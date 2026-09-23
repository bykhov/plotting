# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# One record, two plots, opposite readings. A running total cannot fall, whatever the
# process underneath it does, so it always draws a rising curve; the quantity that
# answers "is it still working" is the rate, and here the rate is collapsing while the
# total climbs. Both panels are exact - the cumulative one is not a distortion of the
# numbers, it is an answer to a different question than the one being asked.
#
# After the chart-basics slides of the DLI Accelerated Data Science Teaching Kit
# (Lecture 7.4, slide 14), where a cumulative recovery total is presented as evidence
# of an effort that is ramping up.
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
C_MARK = '#CC3311'

# A labeling campaign: a few days to get going, then a steady loss of throughput.
day = np.arange(1, 61)
rate = 210.0 * (1.0 - np.exp(-day / 2.5)) * np.exp(-day / 26.0)
rate *= 1.0 + 0.06 * np.random.default_rng(3).standard_normal(day.size)
rate = np.round(rate)
total = np.cumsum(rate)

peak = int(np.argmax(rate))
last7 = slice(-7, None)

fig, (ax_c, ax_r) = plt.subplots(2, 1, figsize=(5.2, 3.6), sharex=True)

# --- (a) the running total: monotone by construction ---
ax_c.plot(day, total, '-', lw=1.6, color=C_LINE)
ax_c.set_ylabel('samples labeled,\ntotal to date')
ax_c.set_title('(a) cumulative total')
ax_c.set_ylim(0, 1.08 * total[-1])

# --- (b) the quantity the total is built from ---
ax_r.plot(day, rate, '-', lw=1.6, color=C_LINE)
ax_r.plot(day[peak], rate[peak], 'o', ms=5, color=C_MARK)
ax_r.annotate(f'peak {rate[peak]:.0f}/day, day {day[peak]}',
              xy=(day[peak], rate[peak]), xytext=(day[peak] + 6, rate[peak] * 0.98),
              fontsize=9, va='center', color=C_MARK)
ax_r.plot(day[-1], rate[-1], 'o', ms=5, color=C_MARK)
ax_r.annotate(f'{rate[-1]:.0f}/day', xy=(day[-1], rate[-1]),
              xytext=(day[-1] - 1, rate[-1] + 14), fontsize=9, ha='right',
              color=C_MARK)
ax_r.set_ylabel('samples labeled\nper day')
ax_r.set_xlabel('day of the campaign')
ax_r.set_title('(b) the daily rate behind it')
ax_r.set_ylim(0, 1.25 * rate.max())

for ax in (ax_c, ax_r):
    ax.set_xlim(0, day[-1] + 1)
    ax.grid(True, axis='y', alpha=0.25)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

plt.tight_layout()

basename = 'plot_cumulative'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the two readings, in the numbers the caption quotes ------------------------
print(f'\npeak rate      {rate[peak]:.0f} per day, on day {day[peak]}')
print(f'final rate     {rate[-1]:.0f} per day, on day {day[-1]}, '
      f'{100 * rate[-1] / rate[peak]:.0f}% of the peak')
print(f'total          {total[-1]:.0f} samples')
print(f'last 7 days    {rate[last7].sum():.0f} samples, '
      f'{100 * rate[last7].sum() / total[-1]:.0f}% of the total')
print(f'first 7 days   {rate[:7].sum():.0f} samples, '
      f'{100 * rate[:7].sum() / total[-1]:.0f}% of the total')
print(f'the total rises on {int((np.diff(total) > 0).sum())} of its '
      f'{len(total) - 1} steps, and cannot fall on any of them')
