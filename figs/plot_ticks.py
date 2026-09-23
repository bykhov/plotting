# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The two habits of the ticks section, on one record: a reference temperature near
# 1234 K that drifts by a tenth of a kelvin. (a) carries the full value on every tick,
# which is what a reader asks for and what the numbers here will not support: six digits
# per label, five of them identical down the axis, and the ticks falling at 7 s. (b)
# states the level on the panel instead and ticks the deviation from it in millikelvin,
# so every label is a small round number and the mean is a value any mark converts back
# through. Matplotlib's own default is worse than either and is not drawn here: it
# factors the common part out into an offset box in the corner of the panel.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import ScalarFormatter

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
C_LINE = '#1E90FF'
C_REF = '0.55'                                   # the 45 % ink of a reference line

# panel (b) subtracts the mean of the record, so that zero on its axis is the mean
# and nothing else, and the mean is named on the panel in full

rng = np.random.default_rng(7)
t = np.linspace(0, 42, 121)                      # seconds
T = 1234.0 + 0.040 * np.sin(t / 9.0) + 0.022 * np.sin(t / 2.3) + rng.normal(0, 0.004, t.size)

fig, axes = plt.subplots(1, 2, figsize=(6.8, 2.4))
fig.subplots_adjust(left=0.10, right=0.99, top=0.86, bottom=0.19, wspace=0.34)

for ax in axes:
    ax.set_xlim(0, 42)
    ax.grid(True, alpha=0.25)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

# --- (a) the full value on every tick, which is six digits of which five repeat ----
ax = axes[0]
ax.plot(t, T, '-', lw=1.0, color=C_LINE)         # kelvin, as measured
ax.set_xticks(np.arange(0, 43, 7))               # the 7 an automatic step sometimes lands on
ax.set_xlabel('time (s)')
ax.set_ylabel('temperature (K)')
ax.set_title('(a) the full value on every tick')
g = ScalarFormatter(useOffset=False)             # the offset box, off
g.set_scientific(False)
ax.yaxis.set_major_formatter(g)
ax.yaxis.set_major_locator(plt.MultipleLocator(0.05))

# --- (b) the level stated on the panel, the deviation ticked in mK ----------------
ax = axes[1]
dev = (T - T.mean()) * 1e3                       # millikelvin about the mean
ax.plot(t, dev, '-', lw=1.0, color=C_LINE)
ax.set_xticks(np.arange(0, 43, 10))
ax.set_xlabel('time (s)')
ax.set_ylabel('temperature deviation (mK)')
ax.set_title('(b) level stated, ticked in mK')
ax.yaxis.set_major_locator(plt.MultipleLocator(25))
# zero is the mean, and the mean is named in full, so any mark on this axis converts
# back to an absolute temperature
ax.axhline(0.0, color=C_REF, lw=0.9, ls='--', zorder=1)
ax.annotate(f'mean $= {T.mean():.3f}$ K', xy=(41, 0.0),
            xytext=(0, 5), textcoords='offset points', ha='right', va='bottom',
            fontsize=PT, color='0.35')

basename = 'plot_ticks'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

fig.canvas.draw()
print('record: %.3f to %.3f K over %.0f s, a range of %.0f mK on a value of about %.0f K'
      % (T.min(), T.max(), t[-1], 1e3 * np.ptp(T), T.mean()))
print('mean %.3f K, which is the zero of the axis of (b); the record runs %+.0f to '
      '%+.0f mK about it' % (T.mean(), 1e3 * (T.min() - T.mean()), 1e3 * (T.max() - T.mean())))
for name, ax in zip(['(a)', '(b)'], axes):
    plain = lambda s: s.replace(chr(0x2212), '-')   # the console is not unicode
    print(name, 'x ticks', [f'{v:g}' for v in ax.get_xticks()],
          '| y ticks', [plain(lab.get_text()) for lab in ax.get_yticklabels()],
          '| offset box', repr(plain(ax.yaxis.get_offset_text().get_text())))
