# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The same smooth field under three colormaps, each shown in color and as the gray a
# black and white print leaves. jet adds bands and reversals the data does not
# contain, because it goes light, dark and light again; viridis adds nothing, because
# it only gets lighter. The gray panels are what a print, a projector at the back of
# a room, and most color-vision deficiencies leave of each map.
#
# The third row is viridis_r, and it is not a hand-built map: matplotlib ships a
# reversed counterpart of every built-in colormap under the _r suffix, so the
# direction of a sequential map is selected off the shelf rather than constructed.
# Reversing keeps the map monotone, only downward, so it stays as rankable as
# viridis itself.
#
# Every panel carries its own bar, because the two panels of a row are two different
# ramps. The bar of a gray panel is the gray the map prints as rather than a plain
# gray ramp: it has to answer which value an ink means, and for jet that bar turns
# around twice along its own length, which is the failure stated as a key.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import ListedColormap, Normalize

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

# --- a field with one peak and one smooth ramp, so any band the eye sees is false ---
g = np.linspace(-3, 3, 400)
X, Y = np.meshgrid(g, g)
Z = np.exp(-(X**2 + Y**2) / 3.0) + 0.18 * X
Z = (Z - Z.min()) / (Z.max() - Z.min())


def gray_level(rgb):
    """What a black and white print keeps: green counts about ten times blue."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def gray_version(cmap, n=256):
    """The map as it prints: each of its colors replaced by the gray it leaves."""
    gray = gray_level(cmap(np.linspace(0, 1, n))[..., :3])
    return ListedColormap(np.repeat(gray[:, None], 3, axis=1))


def key(ax, cmap):
    """The bar that says which value an ink on this panel means."""
    sm = cm.ScalarMappable(norm=Normalize(0, 1), cmap=cmap)
    cb = fig.colorbar(sm, ax=ax, fraction=0.046, pad=0.04, ticks=[0, 0.5, 1])
    cb.ax.tick_params(labelsize=9)
    cb.outline.set_linewidth(0.5)
    cb.outline.set_edgecolor('0.6')


fig, axes = plt.subplots(3, 2, figsize=(6.4, 7.4))

for row, name in enumerate(['jet', 'viridis', 'viridis_r']):
    cmap = plt.get_cmap(name)
    rgb = cmap(Z)[..., :3]
    axes[row, 0].imshow(rgb, origin='lower', extent=[-3, 3, -3, 3])
    axes[row, 0].set_title(f'({"acegik"[row]}) {name}')
    key(axes[row, 0], cmap)
    axes[row, 1].imshow(gray_level(rgb), origin='lower', extent=[-3, 3, -3, 3],
                        cmap='gray', vmin=0, vmax=1)
    axes[row, 1].set_title(f'({"bdfhjl"[row]}) {name}, printed in gray')
    key(axes[row, 1], gray_version(cmap))

for ax in axes.ravel():
    ax.set_xticks([])
    ax.set_yticks([])

plt.tight_layout()

basename = 'plot_colormap'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the property that separates the maps, measured rather than asserted ---
ramp = np.linspace(0, 1, 256)
for name in ('jet', 'viridis', 'viridis_r'):
    gray = gray_level(plt.get_cmap(name)(ramp)[..., :3])
    d = np.diff(gray)
    reversals = int((np.diff(np.sign(d)) != 0).sum())
    mono = bool((d > 0).all()) or bool((d < 0).all())   # either direction is ordered
    way = 'increasing' if d.mean() > 0 else 'decreasing'
    print(f'{name:10s} gray level range {gray.min():.2f} to {gray.max():.2f}, '
          f'monotonic: {mono} ({way}), direction changes: {reversals}')
