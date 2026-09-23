# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The two ways to show a narrow feature inside a wide record. One signal carrying
# a short transient, drawn three ways on the same data:
#
#   (a) the full range alone, where the transient is present and unreadable;
#   (b) an inset drawn inside the panel, over a region carrying no data, with the
#       source window boxed on the parent and connected to the inset;
#   (c) the same window broken out as its own panel, which is the answer when the
#       parent has no free corner and when the zoom needs its own axis labels.
#
# What (b) and (c) share is the marking. An unmarked inset is a claim the reader
# cannot check, since nothing on the page says which part of the record it came
# from. Both keep their ticks for the same reason: a zoom with no scale shows a
# shape and reports no quantity.
#
# This is the companion to plot_logscale.py. A log axis buys detail across the
# whole range at once; a close-up buys it in one window and nowhere else.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, ConnectionPatch

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

rng = np.random.default_rng(3)
FS = 5000.0                       # sampling rate, Hz
T = 2.0                           # record length, s
t = np.arange(0, T, 1 / FS)

# A slow carrier the record is mostly about, plus a short high-frequency burst
# that is the thing worth seeing and that occupies a few percent of the record.
T0, WIDTH = 1.24, 0.024           # burst center and half-width, s
signal = (0.9 * np.sin(2 * np.pi * 2.0 * t)
          + 0.15 * np.sin(2 * np.pi * 5.0 * t + 0.7)
          + rng.normal(0, 0.02, t.size))
burst = 0.55 * np.exp(-((t - T0) / WIDTH) ** 2) * np.sin(2 * np.pi * 180 * t)
signal = signal + burst

X0, X1 = T0 - 3 * WIDTH, T0 + 3 * WIDTH      # the close-up window
sel = (t >= X0) & (t <= X1)
Y0, Y1 = signal[sel].min() - 0.10, signal[sel].max() + 0.10
# Headroom above the carrier, so the inset of (b) has somewhere to go that
# carries no data. An inset placed over the trace would trade the feature it
# shows for the one it hides; making room is part of choosing to use one.
YLIM = (-1.5, 3.5)

C_LINE = '#0072B2'
C_MARK = '#D55E00'                # the marking, in the one strong accent color

fig, axes = plt.subplots(1, 3, figsize=(7.0, 2.5))

# --- (a) full range only ---
ax = axes[0]
ax.plot(t, signal, lw=0.5, color=C_LINE)
ax.set_title('(a) full record: the burst is here')

# --- (b) inset inside the panel, over empty space, marked and connected ---
ax = axes[1]
ax.plot(t, signal, lw=0.5, color=C_LINE)
ax.set_title('(b) inset, source window marked')
ax.set_xlim(0, T)
ax.set_ylim(*YLIM)
axin = ax.inset_axes([0.10, 0.66, 0.52, 0.31])
axin.plot(t[sel], signal[sel], lw=0.6, color=C_LINE)
axin.set_xlim(X0, X1)
axin.set_ylim(Y0, Y1)
axin.set_xticks([1.20, 1.25, 1.30])
axin.set_yticks([-0.5, 0.0, 0.5])
axin.tick_params(labelsize=6, length=2, pad=1)
# Ticks are the minimum; the grid at those ticks is what lets a value be read off the
# magnified window instead of interpolated from its frame. The parent panels are left
# unruled on purpose: they are read for where the burst is, not for its amplitude.
axin.grid(True, color='0.75', lw=0.4, alpha=0.9)
axin.set_axisbelow(True)
for sp in axin.spines.values():
    sp.set_color(C_MARK)
    sp.set_linewidth(0.8)
ax.indicate_inset_zoom(axin, edgecolor=C_MARK, alpha=1.0, lw=0.8)

# --- (c) the same window as its own panel, marked on the parent of (b) ---
ax = axes[2]
ax.plot(t[sel], signal[sel], lw=0.7, color=C_LINE)
ax.set_xlim(X0, X1)
ax.set_ylim(Y0, Y1)
ax.set_xticks([1.20, 1.25, 1.30])
ax.set_yticks([-0.5, 0.0, 0.5])            # the same ruling as the inset of (b)
ax.grid(True, color='0.75', lw=0.5, alpha=0.9)
ax.set_axisbelow(True)
ax.set_title('(c) the same window, broken out')

for ax in (axes[0], axes[1]):
    ax.set_xlim(0, T)
    ax.set_ylim(*YLIM)
for ax in axes:
    ax.set_xlabel('time [s]')
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
axes[0].set_ylabel('amplitude')

plt.tight_layout()

# The rectangle on (b) that (c) is taken from, and two connectors to the panel
# it became, so the broken-out view is anchored to the record exactly as the
# inset is. Drawn after tight_layout, since the connectors span two axes.
axes[1].add_patch(Rectangle((X0, Y0), X1 - X0, Y1 - Y0, fill=False,
                            edgecolor=C_MARK, lw=0.8, zorder=5))
for y_src, y_dst in ((Y1, Y1), (Y0, Y0)):
    fig.add_artist(ConnectionPatch(
        xyA=(X1, y_src), coordsA=axes[1].transData,
        xyB=(X0, y_dst), coordsB=axes[2].transData,
        color=C_MARK, lw=0.6, ls=(0, (3, 2))))

basename = 'plot_closeup'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what the close-up buys, in the units the caption quotes ---
win = X1 - X0
mag = T / win
print(f'\nrecord {T:.1f} s at {FS:.0f} Hz, {t.size} samples')
print(f'close-up window {win * 1e3:.0f} ms wide, centered at {T0:.2f} s: '
      f'{100 * win / T:.1f}% of the record, a magnification of {mag:.0f} times')
print(f'the window holds {int(sel.sum())} of the {t.size} samples and gets the '
      f'full width of (b) and (c) instead of {100 * win / T:.1f}% of it')
print('burst at 180 Hz against a 2 Hz carrier, a ratio of 90, which is why the '
      'full record cannot resolve it')

# --- the ruling of the two close-ups, against the 2 mm limit of the gridline section ---
fig.canvas.draw()
MM = 25.4
LIMIT_MM = 8 / 96 * MM                       # 8 px at 96 px per inch
print(f'\ngridline separation on the close-ups, limit {LIMIT_MM:.2f} mm:')
for name, a in (('inset of (b)', axin), ('panel (c)', axes[2])):
    box = a.get_window_extent()
    w_mm, h_mm = box.width / fig.dpi * MM, box.height / fig.dpi * MM
    dx = (a.get_xticks()[1] - a.get_xticks()[0]) / np.ptp(a.get_xlim()) * w_mm
    dy = (a.get_yticks()[1] - a.get_yticks()[0]) / np.ptp(a.get_ylim()) * h_mm
    flag = '  <-- below the limit' if min(dx, dy) < LIMIT_MM else ''
    print(f'    {name}: {w_mm:.1f} x {h_mm:.1f} mm, lines {dx:.1f} mm apart in x and '
          f'{dy:.1f} mm in y{flag}')
