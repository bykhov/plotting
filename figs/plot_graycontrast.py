# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Simultaneous contrast: five squares of one identical gray, placed along a ramp
# that runs from black to white. They read as light on the left and dark on the
# right, and the square sitting where the ramp equals their own value disappears
# entirely. Nothing about the squares changes across the panel, so the apparent
# ordering belongs to the surround, not to the marks.
#
# After the "grayscale can be risky" demonstration in the DLI colors slides
# (Lecture 7.5, Accelerated Data Science Teaching Kit).
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'mathtext.fontset': 'cm',
})

PATCH = 0.5        # the one value every square is painted with
FIELD = 0.85       # the uniform field of the control panel
CENTERS = np.array([1.0, 3.0, 5.0, 7.0, 9.0])
SIDE = 1.2
W, H = 10.0, 2.0


def gray_level(rgb):
    """What a black and white print keeps: green counts about ten times blue."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def squares(ax):
    for cx in CENTERS:
        ax.add_patch(Rectangle((cx - SIDE / 2, (H - SIDE) / 2), SIDE, SIDE,
                               facecolor=(PATCH, PATCH, PATCH), edgecolor='none'))


fig = plt.figure(figsize=(6.0, 3.0))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.0], hspace=0.55)
axes = [fig.add_subplot(gs[i]) for i in range(2)]

# --- (a) the ramp: same square, five different surrounds ---
ramp = np.linspace(0, 1, 1024)[None, :]
axes[0].imshow(ramp, cmap='gray', vmin=0, vmax=1, origin='lower',
               extent=[0, W, 0, H], aspect='equal', interpolation='bilinear')
squares(axes[0])
axes[0].set_title('(a) five identical squares on a ramp from black to white')

# --- (b) the control: same squares, one surround ---
axes[1].imshow(np.full((1, 2), FIELD), cmap='gray', vmin=0, vmax=1, origin='lower',
               extent=[0, W, 0, H], aspect='equal', interpolation='bilinear')
squares(axes[1])
axes[1].set_title('(b) the same five squares on a uniform field')

for ax in axes:
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)

basename = 'plot_graycontrast'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the squares are one value; only what is behind them changes ---
rgb = np.tile(PATCH, (len(CENTERS), 3))
print('\nsquare   RGB              gray level   surround')
for i, cx in enumerate(CENTERS):
    behind = cx / W
    print(f'{i + 1:^6d}  ({rgb[i, 0]:.3f}, {rgb[i, 1]:.3f}, {rgb[i, 2]:.3f})'
          f'  {gray_level(rgb[i]):10.4f}   {behind:8.2f}')
print(f'distinct square values: {len(np.unique(rgb.round(6), axis=0))}, '
      f'surround range {CENTERS.min() / W:.2f} to {CENTERS.max() / W:.2f}')
