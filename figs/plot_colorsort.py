# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The ordering test from the DLI colors lecture (Lecture 7.5, Accelerated Data
# Science Teaching Kit): "can you order these, low to high?" Eight values encoded
# dark to light, shown shuffled, in their true order, and as the gray a black and
# white print would keep. Dark to light is the only part of a color that carries an
# order, so the shuffled row can be put back by eye; sorting on the gray of the third
# row, done in the printout below, is the same operation.
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

K = 8
values = np.linspace(0.0, 1.0, K)
perm = np.random.default_rng(7).permutation(K)

seq = plt.get_cmap('Blues')(0.15 + 0.80 * values)[:, :3]  # value encoded dark to light


def gray_level(rgb):
    """What a black and white print keeps: green counts about ten times blue."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def swatches(ax, colors, title):
    for j, c in enumerate(colors):
        ax.add_patch(Rectangle((j + 0.06, 0.1), 0.88, 0.8, facecolor=c,
                               edgecolor='none'))
    ax.set_xlim(0, K)
    ax.set_ylim(0, 1)
    ax.set_aspect('equal')
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(title)


gray = gray_level(seq)
gray_rgb = np.repeat(gray[:, None], 3, axis=1)  # the same row, printed in black and white

fig, axes = plt.subplots(3, 1, figsize=(6.0, 3.4))
swatches(axes[0], seq[perm], '(a) eight values encoded dark to light, shuffled')
swatches(axes[1], seq, '(b) the same eight values, in their true order')
swatches(axes[2], gray_rgb, '(c) the same eight values, as the gray they print as')

plt.tight_layout()

basename = 'plot_colorsort'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- can the encoded order be recovered from the only ordered channel there is? ---
# A sequential scheme may run light-to-dark or dark-to-light, so recovering the
# true order in reverse counts as recovering it.
recovered = np.argsort(gray)
ok = bool((recovered == np.arange(K)).all() or
          (recovered == np.arange(K)[::-1]).all())
print(f'\ndark to light: gray level {gray.min():.2f} to {gray.max():.2f}, '
      f'sorting on it recovers the true order: {ok}')
print('  value      ' + ' '.join(f'{v:5.2f}' for v in values))
print('  gray level ' + ' '.join(f'{v:5.2f}' for v in gray))
print('  shuffled   ' + ' '.join(f'{v:5.2f}' for v in gray[perm]))
