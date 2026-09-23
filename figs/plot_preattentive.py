# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The three pre-attentive search demonstrations, posed the way the DLI human-
# perception slides pose them: each row is a left/right pair, and the reader is
# asked which side holds the odd mark. A single-feature target (color, shape) is
# found before the eye moves, however many marks are present; the conjunction
# target (red AND round) has to be searched item by item.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 10,
    'axes.labelsize': 10,
    'mathtext.fontset': 'cm',
})

C_TARGET = '#D62728'      # red target, as on the slides
C_BLUE = '#2E4C99'        # distractor blue
FIELD_BG = '#C8CCD0'      # gray field background, as on the slides

N = 20                    # marks per field
rng = np.random.default_rng(7)


NX, NY = 5, 4                                 # field is a 5x4 grid, N = 20

# Interior slots only, so the target never lands on an edge (where it would be
# easy to find by position, or get clipped by the field border).
INTERIOR = [row * NX + col for row in range(1, NY - 1) for col in range(1, NX - 1)]


def field_positions(seed):
    """A jittered 5x4 grid, so density is even and the target is not found by a
    gap in the layout rather than by its feature."""
    r = np.random.default_rng(seed)
    gx, gy = np.meshgrid(np.arange(NX), np.arange(NY))
    pos = np.column_stack([gx.ravel(), gy.ravel()]).astype(float)
    pos += r.uniform(-0.24, 0.24, pos.shape)
    return pos


# Which side (0 = left, 1 = right) carries the target in each row.
target_side = [0, 1, 1]                       # matches image6/7/8 of the deck

R_DOT = 0.26              # mark radii in DATA units, so they never overflow the
H_SQ = 0.24               # field edge regardless of how the axes are scaled


def add_dot(ax, x, y, color):
    ax.add_patch(Circle((x, y), R_DOT, facecolor=color, edgecolor='none'))


def add_square(ax, x, y, color):
    ax.add_patch(Rectangle((x - H_SQ, y - H_SQ), 2 * H_SQ, 2 * H_SQ,
                           facecolor=color, edgecolor='none'))


# Each row is one axes holding two gray fields with a white gap between them,
# drawn as rectangles in data coordinates. Keeping both fields in a single axes
# means no mark ever sits on an axes boundary, so nothing is clipped to a sliver.
DX = 6.0                                      # x-offset of the right field
FW, FH = 5.4, 4.4                             # gray field width and height
FX0, FY0 = -0.7, -0.7                         # gray field lower-left (local)

fig, axes = plt.subplots(3, 1, figsize=(7.0, 6.6))
fig.subplots_adjust(hspace=0.30)

row_titles = [
    '(a) color: a red dot among blue',
    '(b) shape: a red circle among red squares',
    '(c) conjunction: the only red, round mark',
]


def draw_marks(ax, pos, tgt, row, off):
    if row == 0:
        # color: all blue dots; target dot is red.
        for i, (x, y) in enumerate(pos):
            add_dot(ax, x + off, y, C_TARGET if i == tgt else C_BLUE)
    elif row == 1:
        # shape: all red squares; target is a red circle.
        for i, (x, y) in enumerate(pos):
            if i == tgt:
                add_dot(ax, x + off, y, C_TARGET)
            else:
                add_square(ax, x + off, y, C_TARGET)
    else:
        # conjunction: blue circles + red squares; target is a red circle.
        is_square = rng.permutation(N) < N // 2       # ~half squares
        if tgt >= 0:
            is_square[tgt] = False                    # target is a circle
        for i, (x, y) in enumerate(pos):
            if i == tgt:
                add_dot(ax, x + off, y, C_TARGET)     # the only red, round mark
            elif is_square[i]:
                add_square(ax, x + off, y, C_TARGET)
            else:
                add_dot(ax, x + off, y, C_BLUE)


for row in range(3):
    ax = axes[row]
    for off in (0.0, DX):
        ax.add_patch(Rectangle((FX0 + off, FY0), FW, FH, facecolor=FIELD_BG,
                               edgecolor='none', zorder=0))
    for side in range(2):
        pos = field_positions(seed=100 * row + side)
        has_target = (side == target_side[row])
        tgt = int(rng.choice(INTERIOR)) if has_target else -1
        draw_marks(ax, pos, tgt, row, 0.0 if side == 0 else DX)

    ax.set_xlim(FX0 - 0.2, DX + FX0 + FW + 0.2)
    ax.set_ylim(FY0 - 0.2, FY0 + FH + 0.2)
    ax.set_aspect('equal')
    ax.axis('off')
    ax.text(-0.015, 0.5, row_titles[row], transform=ax.transAxes,
            ha='right', va='center')

basename = 'plot_preattentive'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print(f'{N} marks per field; target side per row (0=left,1=right): {target_side}')
