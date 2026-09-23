# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Four colormaps, each shown as the reader sees it and as the gray it prints as,
# grouped by what the map claims to be. Companion to plot_schemes.py, which does the
# same for schemes; the rows are built the same way so the two figures read as a pair.
# The gray level of the same four maps is drawn against position in plot_cmap_curve.py.
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'mathtext.fontset': 'cm',
})

# Grouped by what each map claims to be, which is what decides whether a turn in the
# gray level is a design or a defect.
MAPS = [
    ('sequential', 'viridis'),
    ('sequential', 'magma'),
    ('diverging', 'coolwarm'),
    ('rainbow', 'jet'),
]
N = 512


def gray_level(rgb):
    """What a black and white print keeps: green counts about ten times blue."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def samples(name, n=N):
    return plt.get_cmap(name)(np.linspace(0, 1, n))[:, :3]


fig = plt.figure(figsize=(6.0, 3.6))
outer = fig.add_gridspec(len(MAPS), 1, hspace=0.95)

for i, (role, name) in enumerate(MAPS):
    rgb = samples(name)
    inner = outer[i].subgridspec(2, 1, hspace=0.12)
    ax_c = fig.add_subplot(inner[0])
    ax_l = fig.add_subplot(inner[1])

    ax_c.imshow(rgb[None, :, :], aspect='auto', origin='lower',
                extent=[0, 1, 0, 1], interpolation='bilinear')
    ax_c.set_title(f'({"abcd"[i]}) {role}: {name}')

    ax_l.imshow(gray_level(rgb)[None, :], cmap='gray', vmin=0, vmax=1, aspect='auto',
                origin='lower', extent=[0, 1, 0, 1], interpolation='bilinear')

    for ax in (ax_c, ax_l):
        ax.set_xticks([])
        ax.set_yticks([])

basename = 'plot_cmap_gray'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what the gray rows show, as numbers ------------------------------------------
print('\nmap        role         gray level     gets lighter throughout')
for role, name in MAPS:
    g = gray_level(samples(name, 256))
    rises = bool((np.diff(g) > 0).all())
    print(f'{name:10s} {role:12s} {g.min():.2f} to {g.max():.2f}   {rises}')
