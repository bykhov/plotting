# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# What goes in the cell. One 4x4 matrix of transfer gaps, four marks, so the only thing
# that differs between the panels is the visual channel: square area, circle area,
# ellipse eccentricity, and length from a common baseline. This is the encoding ranking
# of the plot_encoding figure carried out inside a matrix, and it ends on the one channel
# that keeps the grid and still lets the values be ranked by eye. The shading version of
# the same matrix is panel (a) of the plot_matrix figure. Data: plot_matrix_data.py.
#
# Every panel is drawn on the same cell size and reserves the same band below the grid
# for its key, so the four channels are compared at one scale and each one has to show
# what its own scale is. No text is set below 9 pt.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Ellipse

from plot_matrix_data import GAP, CLOSE, OFF, N, CHANNELS, summary

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

C_MARK = '#1E90FF'
KEY_PT = 9                          # the floor from the font section, obeyed throughout
GMAX = GAP[OFF].max()
U = GAP / GMAX                      # the gap on [0, 1], zero on the diagonal
KEY_Y = N + 0.55                    # centre of the band below the grid, in cell units
KEY_X = 0.60                        # centre of the key mark, clear of the word 'key:'
Y_LO = N + 1.20                     # bottom of the axes, one band below the grid
SHORT = [c.replace('ch ', '') for c in CHANNELS]


def frame(ax, title):
    """One 4x4 cell grid plus the key band below it, identical in every panel."""
    for k in range(N + 1):
        ax.plot([-0.5, N - 0.5], [k - 0.5, k - 0.5], '-', color='0.85', lw=0.6, zorder=0)
        ax.plot([k - 0.5, k - 0.5], [-0.5, N - 0.5], '-', color='0.85', lw=0.6, zorder=0)
    ax.set_xlim(-0.5, N - 0.5)
    ax.set_ylim(Y_LO, -0.5)
    ax.set_xticks([])
    ax.set_yticks(range(N))
    ax.set_yticklabels(SHORT)
    for j in range(N):
        ax.text(j, N - 0.42, SHORT[j], ha='center', va='top', fontsize=KEY_PT)
    ax.tick_params(length=0, pad=2)
    ax.set_title(title, pad=4)
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(False)
    ax.set_aspect('equal')


def keytext(ax):
    ax.text(-0.45, KEY_Y, 'key:', ha='left', va='center', fontsize=KEY_PT)
    ax.text(KEY_X + 0.55, KEY_Y, f'= {GMAX:.3f}', ha='left', va='center', fontsize=KEY_PT)


fig, axes = plt.subplots(1, 4, figsize=(6.9, 2.8))
fig.subplots_adjust(left=0.045, right=0.995, top=0.865, bottom=0.03, wspace=0.16)

# --- (a) Hinton: square area, and an exact zero that draws nothing -----------------
ax = axes[0]
frame(ax, '(a) Hinton\nsquare area')
for i in range(N):
    for j in range(N):
        s = 0.85 * np.sqrt(U[i, j])                 # area proportional to the gap
        if s > 0:
            ax.add_patch(Rectangle((j - s / 2, i - s / 2), s, s,
                                   facecolor=C_MARK, edgecolor='none'))
ax.add_patch(Rectangle((KEY_X - 0.425, KEY_Y - 0.425), 0.85, 0.85,
                       facecolor=C_MARK, edgecolor='none'))
keytext(ax)

# --- (b) bubble: circle area, with the color channel left free for a second variable
ax = axes[1]
frame(ax, '(b) bubble grid\ncircle area')
jj, ii = np.meshgrid(range(N), range(N))
m = U > 0
ax.scatter(jj[m & ~CLOSE], ii[m & ~CLOSE], s=300 * U[m & ~CLOSE], color=C_MARK, zorder=2)
ax.scatter(jj[m & CLOSE], ii[m & CLOSE], s=300 * U[m & CLOSE], facecolor='white',
           edgecolor=C_MARK, linewidth=1.1, zorder=2)
ax.scatter([KEY_X], [KEY_Y], s=300, color=C_MARK)
keytext(ax)

# --- (c) ellipse: the form corrplot uses, on a quantity that has no sign to give it -
# Faithful to the convention: magnitude runs to a thin ellipse and zero is a full circle.
# Applied to a gap, that makes the diagonal, where nothing at all is lost, the largest
# mark on the panel, and the worst transfer the smallest. The tilt, which carries the
# sign of a correlation, has nothing to carry here.
ax = axes[2]
frame(ax, '(c) corrplot ellipse\neccentricity')
for i in range(N):
    for j in range(N):
        ax.add_patch(Ellipse((j, i), width=0.85, height=0.85 * (1 - 0.92 * U[i, j]),
                             angle=45, facecolor=C_MARK, edgecolor='none'))
ax.add_patch(Ellipse((KEY_X, KEY_Y), width=0.85, height=0.85 * 0.08, angle=45,
                     facecolor=C_MARK, edgecolor='none'))
keytext(ax)

# --- (d) bar in cell: length from a common baseline, the highest rank that keeps the grid
ax = axes[3]
frame(ax, '(d) bar in cell\nlength')
for j in range(N):                          # the shared baseline every bar starts from
    ax.plot([j - 0.45, j - 0.45], [-0.5, N - 0.5], '-', color='0.55', lw=0.7, zorder=1)
for i in range(N):
    for j in range(N):
        ax.add_patch(Rectangle((j - 0.45, i - 0.20), 0.9 * U[i, j], 0.40,
                               facecolor=C_MARK, edgecolor='none', zorder=2))
ax.add_patch(Rectangle((KEY_X - 0.45, KEY_Y - 0.20), 0.9, 0.40, facecolor=C_MARK,
                       edgecolor='none'))
keytext(ax)

basename = 'plot_matrix_forms'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print(summary())
ratio = GMAX / GAP[OFF].min()
print('largest gap %.4f, smallest %.4f' % (GMAX, GAP[OFF].min()))
print('between them: %.1fx of value, %.1fx of area, %.1fx of square side'
      % (ratio, ratio, np.sqrt(ratio)))
print('(a) and (b) draw nothing on the diagonal, where the gap is exactly 0')
print('(c) draws its largest mark on the diagonal, where the gap is exactly 0')
