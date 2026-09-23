# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Ten recordings, overlaid and then separated. The overlay answers "how large is the
# spread" and nothing else; the grid answers "what does one recording look like",
# which is the question that matters when the recordings are inputs to a classifier.
#
# Three of the ten are not like the rest, and each is a different kind of not alike:
# one runs at twice the frequency, one at half the amplitude, one is noisy. The overlay
# hides all three, for three different reasons. The fast one is one more line in a
# thicket of lines. The small one lies inside an envelope the other traces already
# fill. The noisy one is the only trace the overlay reports at all, and it reports it
# as the spread of the whole set, since the widest trace is what draws the envelope.
#
# The point of this figure is the axes. A grid of panels is a comparison only if one
# range serves all of them, and a reader can only take the comparison on trust unless
# the range is on the page. So the ten panels are linked with sharex/sharey, ticked
# and ruled at the same values as the overlay beside them, and labeled once on the
# outer edge: ten copies of one axis would be nine copies of ink.
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

MM = 25.4
LIMIT_MM = 8 / 96 * MM                 # the 8 px of the gridline section, at 96 px/in
C_LINE = '#1E90FF'
C_GRID = '0.75'

rng = np.random.default_rng(23)
M, N = 10, 200
t = np.linspace(0, 1, N)

# Ten traces from one process: shared shape, individual phase, amplitude and drift.
# The amplitude spread is deliberately narrow, so that the half-amplitude trace reads
# as wrong rather than as the low end of a wide normal range.
F0, SD0 = 3.0, 0.12
phase = rng.uniform(0, 2 * np.pi, M)
amp = rng.uniform(0.9, 1.1, M)
drift = rng.uniform(-0.4, 0.4, M)
freq = np.full(M, F0)
sd = np.full(M, SD0)

# The three that are not like the rest, one deviation each, numbered as the panels are.
FAST, SMALL, NOISY = 3, 6, 9
freq[FAST - 1] *= 2.0
amp[SMALL - 1] *= 0.5
sd[NOISY - 1] *= 4.0

series = (amp[:, None] * np.sin(2 * np.pi * freq[:, None] * t + phase[:, None])
          + drift[:, None] * t
          + rng.normal(0, sd[:, None], (M, N)))

YLIM = (-2.2, 2.2)                     # holds every trace, and no more than that
YTICKS = [-2, 0, 2]                    # one set of values for both halves of the figure
XTICKS = [0.0, 0.5, 1.0]
# Only the ends are labeled in the block: three labels per column would collide across
# the column gap, and the project's floor of 9 pt is not negotiable to make them fit.
XLABELS = ['0', '', '1']

fig = plt.figure(figsize=(7.0, 3.4))
outer = fig.add_gridspec(1, 2, width_ratios=[1.0, 1.35], wspace=0.30,
                         left=0.075, right=0.99, bottom=0.13, top=0.88)

# --- (a) all ten on one axis ---
ax = fig.add_subplot(outer[0])
for s in series:
    ax.plot(t, s, '-', lw=0.7, color=C_LINE, alpha=0.7)
ax.set_ylim(*YLIM)
ax.set_yticks(YTICKS)                  # the same values the block is ticked at, so the
ax.set_xticks(XTICKS)                  # two halves are visibly one scale
ax.set_xticklabels(['0', '0.5', '1'])
ax.set_xlabel('time [s]')
ax.set_ylabel('amplitude')
ax.set_title('(a) ten traces overlaid')
ax.grid(True, alpha=0.25)
ax.set_axisbelow(True)
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)

# --- (b) the same ten as small multiples, on one linked range ---
NROW, NCOL = 2, 5
inner = outer[1].subgridspec(NROW, NCOL, wspace=0.22, hspace=0.18)
panels = []
for i, s in enumerate(series):
    kw = {} if i == 0 else {'sharex': panels[0], 'sharey': panels[0]}
    a = fig.add_subplot(inner[i // NCOL, i % NCOL], **kw)
    a.plot(t, s, '-', lw=0.7, color=C_LINE)
    a.text(0.06, 0.94, f'{i + 1}', transform=a.transAxes, fontsize=9,
           va='top', color='0.35')
    a.grid(True, color=C_GRID, lw=0.5, alpha=0.9)
    a.set_axisbelow(True)              # the grid is under the trace, never over it
    a.tick_params(length=2, pad=1.5)
    for side in ('top', 'right'):
        a.spines[side].set_visible(False)
    panels.append(a)

panels[0].set_ylim(*YLIM)
panels[0].set_yticks(YTICKS)
panels[0].set_xticks(XTICKS)
panels[0].set_xticklabels(XLABELS)
for a in panels:
    a.label_outer()                    # values on the left column and the bottom row only

fig.canvas.draw()
inv = fig.transFigure.inverted()

# One title, one x label and one y label for the whole block, placed off the panels
# themselves rather than off a hard-coded offset, so they follow any layout change.
tight = [a.get_tightbbox() for a in panels]
x0 = min(b.x0 for b in tight)
x1 = max(b.x1 for b in tight)
y0 = min(b.y0 for b in tight)
y1 = max(b.y1 for b in tight)
(fx0, fy0), (fx1, fy1) = inv.transform([(x0, y0), (x1, y1)])
PAD = 0.02
fig.text((fx0 + fx1) / 2, fy1 + PAD, '(b) the same ten, one per panel, one shared range',
         ha='center', va='bottom', fontsize=9)
fig.text((fx0 + fx1) / 2, fy0 - PAD, 'time [s]', ha='center', va='top', fontsize=9)
fig.text(fx0 - PAD / 2, (fy0 + fy1) / 2, 'amplitude', ha='right', va='center',
         rotation=90, fontsize=9)

basename = 'plot_small_multiples'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the record, and what the axes of the block cost and buy ----------------------
print(f'\n{M} traces of {N} samples, one shared range {YLIM}')
print(f'the record runs {series.min():.2f} to {series.max():.2f}, '
      f'{"inside" if series.min() > YLIM[0] and series.max() < YLIM[1] else "CLIPPED BY"}'
      f' the range')

# --- the three deviations, measured off the traces and not read back from the recipe -
fs = 1.0 / (t[1] - t[0])
bins = np.fft.rfftfreq(N, d=1 / fs)
peak = np.array([bins[1:][np.argmax(np.abs(np.fft.rfft(x - x.mean()))[1:])]
                 for x in series])
kern = np.ones(5) / 5                  # what a 5-sample average cannot follow is noise
resid = np.array([(x - np.convolve(x, kern, mode='same'))[3:-3].std() for x in series])
rms = series.std(axis=1)
typ = [i for i in range(M) if i + 1 not in (FAST, SMALL, NOISY)]
f_t, r_t, n_t = np.median(peak[typ]), np.median(rms[typ]), np.median(resid[typ])
print(f'the {len(typ)} typical traces: {f_t:.1f} Hz, rms {r_t:.2f}, noise {n_t:.3f}')
for what, k in (('twice the frequency', FAST), ('half the amplitude', SMALL),
                ('noisy', NOISY)):
    i = k - 1
    print(f'  trace {k}, {what}: {peak[i]:.1f} Hz, rms {rms[i]:.2f}, '
          f'noise {resid[i]:.3f}, which is {peak[i] / f_t:.1f}, {rms[i] / r_t:.2f} and '
          f'{resid[i] / n_t:.1f} times the typical trace')

box = panels[0].get_window_extent()
w_mm, h_mm = box.width / fig.dpi * MM, box.height / fig.dpi * MM
dx = (XTICKS[1] - XTICKS[0]) / np.ptp(panels[0].get_xlim()) * w_mm
dy = (YTICKS[1] - YTICKS[0]) / np.ptp(YLIM) * h_mm
flag = '  <-- below the limit' if min(dx, dy) < LIMIT_MM else ''
print(f'each panel {w_mm:.1f} x {h_mm:.1f} mm, ruled {dx:.1f} mm apart in x and '
      f'{dy:.1f} mm in y, against the {LIMIT_MM:.2f} mm limit{flag}')

# How much of the axis the block actually spends: labels on the outer edge only.
labeled_x = sum(bool([lab for lab in a.get_xticklabels() if lab.get_visible()
                      and lab.get_text()]) for a in panels)
labeled_y = sum(bool([lab for lab in a.get_yticklabels() if lab.get_visible()
                      and lab.get_text()]) for a in panels)
print(f'{labeled_x} of the {M} panels carry x values and {labeled_y} carry y values, '
      f'and one label of each serves the block')

# Do the bottom-row x labels clear one another across the column gap?
r = fig.canvas.get_renderer()
gaps = []
for left, right in zip(panels[NCOL:], panels[NCOL + 1:]):
    e_l = [lab.get_window_extent(renderer=r) for lab in left.get_xticklabels()
           if lab.get_visible() and lab.get_text()]
    e_r = [lab.get_window_extent(renderer=r) for lab in right.get_xticklabels()
           if lab.get_visible() and lab.get_text()]
    gaps.append((min(e.x0 for e in e_r) - max(e.x1 for e in e_l)) / fig.dpi * MM)
print(f'the closest pair of x labels in adjacent columns clears {min(gaps):.1f} mm '
      f'({"no collision" if min(gaps) > 0 else "COLLISION"})')
