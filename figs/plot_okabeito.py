# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The Okabe-Ito qualitative palette, named and with the code to copy, shown as the
# reader sees it and as a deuteranope receives it. The point of the second row is
# that the eight stay separable: the palette was constructed so that no two of its
# colors merge under any of the common forms of deficiency, which is what makes it
# the default answer to "which colors, then?" of the section around it.
#
# Four of these eight are the palette of plot_cvd.py panel (c), where they are used
# in a chart rather than listed.
#
# Palette: Okabe and Ito, "Color Universal Design" (2008), tabulated in Wong,
# "Points of View: Color Blindness", Nature Methods 8(6), 2011, p. 441.
# Simulation: Machado, Oliveira and Fernandes, "A Physiologically-based Model for
# Simulation of Color Vision Deficiency", IEEE Trans. Visualization and Computer
# Graphics 15(6), 2009, pp. 1291-1298, severity 1.0 matrices, applied in linear RGB.
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'mathtext.fontset': 'cm',
})

# Machado et al. (2009), severity 1.0, for linear RGB.
CVD = {
    'deuteranopia': np.array([[0.367322, 0.860646, -0.227968],
                              [0.280085, 0.672501,  0.047413],
                              [-0.011820, 0.042940, 0.968881]]),
    'protanopia': np.array([[0.152286, 1.052583, -0.204868],
                            [0.114503, 0.786281,  0.099216],
                            [-0.003882, -0.048116, 1.051998]]),
}

# The palette in its published order.
PALETTE = [
    ('black', '#000000'),
    ('orange', '#E69F00'),
    ('sky blue', '#56B4E9'),
    ('bluish green', '#009E73'),
    ('yellow', '#F0E442'),
    ('blue', '#0072B2'),
    ('vermillion', '#D55E00'),
    ('reddish purple', '#CC79A7'),
]
K = len(PALETTE)
GAP = 0.12      # white gap as a fraction of one cell, so the row reads as a list


def srgb_to_linear(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)


def simulate(rgb, kind):
    """Dichromatic appearance of an sRGB array, via linear RGB."""
    lin = srgb_to_linear(np.asarray(rgb, dtype=float))
    return linear_to_srgb(lin @ CVD[kind].T)


def swatch_row(ax, rgb, title):
    """The palette as k separated chips, one cell each."""
    for j, c in enumerate(rgb):
        ax.add_patch(Rectangle((j + GAP / 2, 0.0), 1 - GAP, 1.0,
                               facecolor=c, edgecolor='0.6', lw=0.5))
    ax.set_xlim(0, K)
    ax.set_xticks([])
    ax.set_yticks([])
    for side in ax.spines.values():
        side.set_visible(False)
    ax.set_title(title)


names = [n for n, _ in PALETTE]
hexes = [h for _, h in PALETTE]
rgb = np.array([matplotlib.colors.to_rgb(h) for h in hexes])

fig = plt.figure(figsize=(6.8, 2.5))
gs = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.75], hspace=0.45,
                      left=0.01, right=0.99, top=0.90, bottom=0.04)
ax_a = fig.add_subplot(gs[0])
ax_b = fig.add_subplot(gs[1])

swatch_row(ax_a, rgb, '(a) the eight colors as seen')
ax_a.set_ylim(0, 1)

swatch_row(ax_b, simulate(rgb, 'deuteranopia'),
           '(b) the same eight under simulated deuteranopia')
ax_b.set_ylim(-1.05, 1.0)

# The name and the code go under the lower row, where they label the column and so
# both rows at once. Two lines for the name always, so the codes stay on one line.
for j, (name, hexcode) in enumerate(PALETTE):
    label = name.replace(' ', '\n')
    if '\n' not in label:
        label += '\n'
    ax_b.text(j + 0.5, -0.10, label, ha='center', va='top', fontsize=9)
    ax_b.text(j + 0.5, -0.72, hexcode, ha='center', va='top', fontsize=9,
              color='0.35')

basename = 'plot_okabeito'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')


def closest_pair(colors):
    """Smallest sRGB distance between any two of the colors, the pair that merges."""
    d = np.linalg.norm(colors[:, None, :] - colors[None, :, :], axis=-1)
    iu = np.triu_indices(len(colors), 1)
    k = int(np.argmin(d[iu]))
    return d[iu][k], f'{names[iu[0][k]]} and {names[iu[1][k]]}'


# --- how far apart the eight stay, which is what the palette is for ---
print('\nview             closest pair                     distance  retained')
ref, pair = closest_pair(rgb)
print(f'{"normal vision":16s} {pair:32s} {ref:8.3f}  {1.0:7.0%}')
for kind in ('deuteranopia', 'protanopia'):
    dist, pair = closest_pair(simulate(rgb, kind))
    print(f'{kind:16s} {pair:32s} {dist:8.3f}  {dist / ref:7.0%}')

print('\nname             code      as seen                under deuteranopia')
sim = simulate(rgb, 'deuteranopia')
for j, (name, hexcode) in enumerate(PALETTE):
    seen = '({:.2f}, {:.2f}, {:.2f})'.format(*rgb[j])
    deut = '({:.2f}, {:.2f}, {:.2f})'.format(*sim[j])
    print(f'{name:16s} {hexcode}   {seen}     {deut}')
