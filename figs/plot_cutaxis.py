# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The other half of the baseline argument: when a cut axis is the right call, and what
# forcing zero costs when it is not. (a) is the loss curve of the old plot_baseline
# panel (c), unchanged, on the range its own values occupy. (b) is the identical curve
# forced onto 0 to 1, where the plateau the reader is asked to judge gets less page than
# a reader can resolve.
#
# The limits of (a) are not merely legal, they are chosen: 0.40 to 0.75 leaves the curve
# filling three quarters of the panel, the top of the two thirds to three quarters band
# the section recommends, with the extremes off the frame rather than on it. The marked
# span in the panel is that fill, and the print block measures every panel against the
# band rather than asserting it.
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

C_LINE = '#1B7F5A'

# --- the loss record, exactly as plot_baseline drew it --------------------------
epoch = np.arange(1, 41)
rng = np.random.default_rng(7)
val = 0.42 + 0.30 * np.exp(-epoch / 9) + rng.normal(0, 0.004, epoch.size)
CUT_LO, CUT_HI = 0.40, 0.75
BAND = (2 / 3, 3 / 4)                        # the share of the panel the data should fill
TAIL = 20                                    # the plateau the reader is asked to judge

fig, axes = plt.subplots(1, 2, figsize=(4.9, 2.3))
fig.subplots_adjust(left=0.07, right=0.99, top=0.87, bottom=0.21, wspace=0.34)

# --- (a) a line encodes position, so the axis may be cut -------------------------
ax = axes[0]
ax.plot(epoch, val, '-', lw=1.2, color=C_LINE)
ax.set_ylim(CUT_LO, CUT_HI)
ax.set_xlabel('epoch')
ax.set_ylabel('validation loss')
ax.set_title('(a) a line, axis cut')

# --- and the fill those limits were chosen for --------------------------------------
lo, hi = val.min(), val.max()
for level in (lo, hi):
    ax.axhline(level, color='0.55', lw=0.6, ls=(0, (1, 2)), zorder=1)
ax.annotate('', xy=(36.5, lo), xytext=(36.5, hi),
            arrowprops=dict(arrowstyle='<->', lw=0.8, color='0.45'))
ax.text(34.0, (lo + hi) / 2, 'about three quarters\nof the panel', fontsize=9,
        color='0.35', ha='right', va='center')

# --- (b) the same curve forced onto a zero baseline ------------------------------
ax = axes[1]
ax.plot(epoch, val, '-', lw=1.2, color=C_LINE)
ax.set_ylim(0, 1)
ax.set_xlabel('epoch')
ax.set_ylabel('validation loss')
ax.set_title('(b) the same curve, forced to $0$')

for ax in axes:
    ax.grid(True, axis='y', alpha=0.25)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

basename = 'plot_cutaxis'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what forcing zero costs, in millimetres on the printed page -----------------
fig.canvas.draw()
print(f'loss runs {val.min():.3f} to {val.max():.3f} over {epoch.size} epochs')
tail = val[-TAIL:]
span_tail = np.ptp(tail)
print(f'the last {TAIL} epochs move by {span_tail:.3f}, from {tail.max():.3f} to '
      f'{tail.min():.3f}')
for name, ax, lo, hi in [('(a)', axes[0], CUT_LO, CUT_HI), ('(b)', axes[1], 0.0, 1.0)]:
    h_mm = ax.get_window_extent().height / fig.dpi * 25.4
    frac = np.ptp(val) / (hi - lo)
    below, above = (val.min() - lo) / (hi - lo), (hi - val.max()) / (hi - lo)
    print(f'  {name} axis {lo:g} to {hi:g}: panel {h_mm:.1f} mm tall, the whole curve '
          f'occupies {frac:.0%} of it against the recommended {BAND[0]:.0%} to '
          f'{BAND[1]:.0%},\n      {below:.0%} of the panel is left below the curve and '
          f'{above:.0%} above it, and the last {TAIL} epochs get '
          f'{span_tail / (hi - lo) * h_mm:.2f} mm')

