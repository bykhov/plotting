# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The 4x4 cross-channel record as it was measured, with nothing subtracted. Panel (a) is the
# grid the research script produced, faults included; (b) and (c) keep the same accuracies
# and put them on an axis, each transfer beside the target channel's own model.
# The loss against that model is the next figure, plot_matrix.py, which folds each target's
# own model into the number and takes the level away with the reference: on the loss, ch 3
# is the easiest target of the four, and on the accuracies a model transferred into ch 3 is
# the least accurate of the four. Both are true, and only a figure that keeps the measured
# numbers can say the second.
# Data: plot_matrix_data.py, shared with the other matrix figures. GAP is deliberately not
# imported. The one difference taken here is the sort key of panel (c), which sets the row
# order and is never drawn or printed.
import numpy as np
import matplotlib.pyplot as plt

from plot_matrix_data import ACC, NATIVE, CLOSE, OFF, N, CHANNELS, PAIRS, summary

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

PT = 9                       # the floor from the font section, obeyed throughout
C_MARK = '#1E90FF'           # the transfer, and the open marker of the closest three
C_REF = '#333333'            # the target's own model, neutral so it is not a fourth transfer
XLO, XHI = 0.870, 0.932      # one accuracy axis for both dot panels
TICKS = [0.87, 0.89, 0.91, 0.93]


def transfer(ax, x, y, i, j):
    """One measured transfer accuracy. Open where plot_matrix.py draws it open."""
    ax.plot(x, y, 'o', ms=5, zorder=3,
            markerfacecolor='white' if CLOSE[i, j] else C_MARK,
            markeredgecolor=C_MARK, markeredgewidth=1.2)


def frame(ax, title):
    ax.set_xlim(XLO, XHI)
    ax.set_xticks(TICKS)
    ax.set_xlabel('accuracy')
    ax.set_title(title)
    ax.tick_params(axis='y', length=0)
    for side in ('top', 'right', 'left'):
        ax.spines[side].set_visible(False)
    ax.grid(True, axis='x', alpha=0.25)


fig = plt.figure(figsize=(6.9, 4.6))
gs = fig.add_gridspec(2, 2, width_ratios=[1.02, 1.0], height_ratios=[1.0, 1.0],
                      hspace=0.55, wspace=0.28,
                      left=0.075, right=0.985, top=0.93, bottom=0.09)

# --- (a) as the research script drew it -------------------------------------------
# imshow(M, cmap='viridis', vmin=M.min(), vmax=M.max()) with no colorbar: viridis is
# stretched across the observed range, so the page carries no scale at all.
# The asterisk marks the three closest transfers, the same cells plot_matrix.py outlines.
# The panel never says so, which is one more fault on display: a glyph with no key.
ax = fig.add_subplot(gs[0, 0])
ax.imshow(ACC, cmap='viridis', vmin=ACC.min(), vmax=ACC.max())
for i in range(N):
    for j in range(N):
        star = '*' if CLOSE[i, j] else ''
        ax.text(j, i, f'{ACC[i, j]:.3f}{star}', ha='center', va='center',
                fontsize=PT,
                color='white' if ACC[i, j] < ACC.mean() else 'black',
                fontweight='bold' if i == j else 'normal')
ax.set_xticks(range(N))
ax.set_yticks(range(N))
ax.set_xticklabels(CHANNELS)
ax.set_yticklabels(CHANNELS)
ax.set_xlabel('test (target) channel')
ax.set_ylabel('train (source) channel')
ax.tick_params(length=0)
ax.set_title('(a) accuracy, as produced')

# --- (b) the record as measured, one row per target -------------------------------
# The rule is that channel's own model, and each of the three transfers into that channel
# gets its own sub-row, so all three distances to the rule are drawn rather than implied.
# The distance is the loss of plot_matrix.py, on the page without being computed.
# Row ch 3 carries the caveat: the whole row, rule included, sits left.
ax = fig.add_subplot(gs[1, 0])
for j in range(N):
    ax.plot([NATIVE[j], NATIVE[j]], [j - 0.36, j + 0.36], '-', color=C_REF, lw=1.6, zorder=4)
    for k, i in enumerate([s for s in range(N) if s != j]):
        y = j + (k - 1) * 0.24
        ax.plot([ACC[i, j], NATIVE[j]], [y, y], '-', color='0.75', lw=1.1, zorder=1)
        transfer(ax, ACC[i, j], y, i, j)
ax.set_yticks(range(N))
ax.set_yticklabels(CHANNELS)
ax.set_ylim(N - 0.38, -0.72)
ax.set_ylabel('test (target) channel')
# both keys on one line above the first block, each over the mark it names
ax.text(NATIVE[0], -0.55, 'own model', ha='center', va='center', fontsize=PT, color=C_REF)
ax.text(0.8790, -0.55, 'transferred in', ha='center', va='center', fontsize=PT,
        color=C_MARK)
frame(ax, '(b) accuracy as measured, per target')

# --- (c) each transfer against its own reference ----------------------------------
# The unsubtracted twin of plot_matrix.py(b): same twelve rows, same order, but the row is
# the pair of measured numbers and the loss is the segment between them.
ax = fig.add_subplot(gs[:, 1])
order = sorted(PAIRS, key=lambda p: NATIVE[p[1]] - ACC[p])
for y, (i, j) in enumerate(order):
    ax.plot([ACC[i, j], NATIVE[j]], [y, y], '-', color='0.75', lw=1.1, zorder=1)
    ax.plot(NATIVE[j], y, '|', ms=7, color=C_REF, markeredgewidth=1.6, zorder=4)
    transfer(ax, ACC[i, j], y, i, j)
ax.set_yticks(range(len(order)))
ax.set_yticklabels([rf'${i}\rightarrow{j}$' for i, j in order])
ax.set_ylim(len(order) - 0.5, -0.5)
frame(ax, '(c) each transfer against its own model')

basename = 'plot_matrix_raw'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print(summary())
col_acc = np.array([ACC[OFF[:, j], j].mean() for j in range(N)])
print('mean accuracy into each target: '
      + ', '.join('%s %.4f' % (c, v) for c, v in zip(CHANNELS, col_acc)))
print('lowest destination %s %.4f, highest %s %.4f'
      % (CHANNELS[col_acc.argmin()], col_acc.min(),
         CHANNELS[col_acc.argmax()], col_acc.max()))
print('(a) reads ch %d as the hardest target, on the accuracies alone'
      % int(np.argmin(col_acc)))
print('the closest three, as accuracies: '
      + ', '.join('%d -> %d %.4f against %.4f' % (i, j, ACC[i, j], NATIVE[j])
                  for i in range(N) for j in range(N) if CLOSE[i, j]))
