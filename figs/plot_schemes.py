# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The three scheme families of ColorBrewer, each shown twice: as the reader sees
# it and as the gray a black and white print leaves. A scheme is a fixed short
# list, so every family is drawn as its k separated swatches and not as a ramp;
# the ramps belong to the colormap figures that follow. The gray rows are what
# separates the families mechanically rather than by taste - sequential gets
# lighter throughout, diverging is lightest at its neutral middle and darkens to
# both ends, and qualitative stays at one darkness while the colors do the work.
#
# k is odd for the diverging pair on purpose: sampling at cell centers puts the
# middle class exactly on the neutral point of the map, so the neutral color is a
# swatch of its own instead of a boundary between two.
#
# All six palettes are Brewer's, shipped with matplotlib. Source: Harrower and
# Brewer, "ColorBrewer.org", The Cartographic Journal 40(1), 2003, pp. 27-37;
# the picker is at https://colorbrewer2.org. After the scheme slides of the DLI
# colors lecture (Lecture 7.5, Accelerated Data Science Teaching Kit).
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

PALETTES = [
    ('Sequential', 'Blues', 8),
    ('Sequential', 'YlOrRd', 8),
    ('Diverging', 'RdBu', 7),
    ('Diverging', 'PuOr', 7),
    ('Qualitative', 'Set2', 8),
    ('Qualitative', 'Dark2', 8),
]
GAP = 0.12      # white gap as a fraction of one cell, so the row reads as a list


def gray_level(rgb):
    """What a black and white print keeps: green counts about ten times blue."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def positions(k):
    """Cell centers, the standard way a colormap is cut into k classes."""
    return (np.arange(k) + 0.5) / k


def samples(name, k):
    return plt.get_cmap(name)(positions(k))[:, :3]


def swatch_row(ax, rgb):
    """One scheme as k separated chips across the unit interval."""
    k = len(rgb)
    w = 1.0 / k
    for j, c in enumerate(rgb):
        ax.add_patch(Rectangle((j * w + GAP * w / 2, 0.0), w * (1 - GAP), 1.0,
                               facecolor=c, edgecolor='none'))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    for side in ax.spines.values():
        side.set_visible(False)


fig = plt.figure(figsize=(6.0, 5.4))
outer = fig.add_gridspec(len(PALETTES), 1, hspace=0.95)

for i, (family, name, k) in enumerate(PALETTES):
    rgb = samples(name, k)
    gray = gray_level(rgb)

    inner = outer[i].subgridspec(2, 1, hspace=0.12)
    ax_c = fig.add_subplot(inner[0])
    ax_l = fig.add_subplot(inner[1])
    ax_c.set_title(f'({"abcdef"[i]}) {family}: {name}, $k={k}$')

    swatch_row(ax_c, rgb)
    swatch_row(ax_l, np.repeat(gray[:, None], 3, axis=1))

    for ax in (ax_c, ax_l):
        ax.set_xticks([])
        ax.set_yticks([])

basename = 'plot_schemes'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the property that defines each family, measured on the palettes themselves ---
print('\nfamily       palette  k  gray level range  spread  ordered  lightest at')
for family, name, k in PALETTES:
    gray = gray_level(samples(name, k))
    d = np.diff(gray)
    d = d[np.abs(d) > 1e-12]
    mono = bool((d > 0).all()) or bool((d < 0).all())
    peak = np.argmax(gray) / (len(gray) - 1)
    print(f'{family:12s} {name:8s} {k}  {gray.min():.2f} to {gray.max():.2f}     '
          f'{gray.max() - gray.min():.2f}    {str(mono):9s}  {peak:.2f}')
