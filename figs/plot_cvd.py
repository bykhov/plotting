# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The same four-series chart drawn twice, once in a red-green palette and once in
# the Okabe-Ito palette, and each of the two run through simulated dichromatic
# vision. Only the palette differs between the rows; the data, the layout and the
# legend are identical, so whatever separates the rows is the palette alone.
#
# The chart is rendered offscreen and the simulation applied to its pixels, so
# the legend keys degrade exactly as the lines do - which is the failure being
# shown, since a legend keyed by color is unusable once the colors merge.
#
# Only deuteranopia is shown, the most frequent form; the full list of forms and
# what each does to the spectrum is plot_cvd_types.py.
#
# Simulation: Machado, Oliveira and Fernandes, "A Physiologically-based Model for
# Simulation of Color Vision Deficiency", IEEE Trans. Visualization and Computer
# Graphics 15(6), 2009, pp. 1291-1298, severity 1.0 matrices, applied in linear
# RGB. Palette: Okabe and Ito, "Color Universal Design" (2008). After the
# colorblindness slides of the DLI colors lecture (Lecture 7.5, Accelerated Data
# Science Teaching Kit).
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
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

RISKY = ['#D62728', '#2CA02C', '#BCBD22', '#8C564B']       # red, green, olive, brown
SAFE = ['#0072B2', '#E69F00', '#009E73', '#CC79A7']        # Okabe-Ito
LABELS = ['A', 'B', 'C', 'D']


def srgb_to_linear(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)


def simulate(rgb, kind):
    """Dichromatic appearance of an sRGB array, via linear RGB."""
    lin = srgb_to_linear(np.asarray(rgb, dtype=float))
    return linear_to_srgb(lin @ CVD[kind].T)


def render(colors):
    """Draw the chart offscreen and return it as an sRGB array in [0, 1]."""
    f = plt.figure(figsize=(2.9, 2.1), dpi=200)
    ax = f.add_axes([0.17, 0.19, 0.80, 0.68])
    x = np.linspace(0, 6, 200)
    for k, (c, lab) in enumerate(zip(colors, LABELS)):
        ax.plot(x, np.exp(-0.25 * x) * np.cos(x - 0.6 * k) + 0.22 * k,
                color=c, lw=1.4, label=lab)
    ax.set_xlabel('time (s)', labelpad=1)
    ax.set_ylabel('response', labelpad=1)
    ax.set_xlim(0, 6)
    ax.set_ylim(-0.75, 1.75)
    ax.legend(loc='upper right', ncol=4, frameon=False, handlelength=1.2,
              columnspacing=0.8, borderpad=0.1, handletextpad=0.4)
    f.canvas.draw()
    img = np.asarray(f.canvas.buffer_rgba())[..., :3] / 255.0
    plt.close(f)
    return img


views = [('normal vision', None), ('deuteranopia', 'deuteranopia')]
rows = [('red-green palette', RISKY), ('Okabe-Ito palette', SAFE)]

fig, axes = plt.subplots(2, 2, figsize=(6.8, 4.6))

for r, (row_label, colors) in enumerate(rows):
    base = render(colors)
    for c, (view_label, kind) in enumerate(views):
        ax = axes[r, c]
        ax.imshow(base if kind is None else simulate(base, kind),
                  interpolation='antialiased')
        ax.set_title(f'({"abcd"[2 * r + c]}) {view_label}')
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
    axes[r, 0].text(-0.06, 0.5, row_label, transform=axes[r, 0].transAxes,
                    ha='right', va='center', fontsize=9, fontstyle='italic',
                    rotation=90)

plt.tight_layout()

basename = 'plot_cvd'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')


def closest_pair(colors, kind=None):
    """Smallest sRGB distance between any two series colors, the pair that merges."""
    rgb = np.array([matplotlib.colors.to_rgb(c) for c in colors])
    if kind is not None:
        rgb = simulate(rgb, kind)
    d = np.linalg.norm(rgb[:, None, :] - rgb[None, :, :], axis=-1)
    iu = np.triu_indices(len(colors), 1)
    k = np.argmin(d[iu])
    return d[iu][k], LABELS[iu[0][k]] + LABELS[iu[1][k]]


# --- how far apart the four series stay, which is what the palette buys ---
print('\npalette            view           closest pair  distance  retained')
for row_label, colors in rows:
    ref, _ = closest_pair(colors)
    for view_label, kind in views:
        dist, pair = closest_pair(colors, kind)
        print(f'{row_label:18s} {view_label:14s} {pair:^12s}  {dist:8.3f}  '
              f'{dist / ref:7.0%}')
