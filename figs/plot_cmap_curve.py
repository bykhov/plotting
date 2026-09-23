# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The gray level of the four colormaps of plot_cmap_gray.py, drawn against position
# along the map. This one curve carries the whole test: a sequential map has to climb
# throughout, a diverging map has to turn once at its center, and a map that turns
# anywhere else puts an edge on the page that the data does not contain. The gray
# colormap itself is the dashed straight line the others are read against.
#
# Series are labeled at the end of each curve rather than through a legend, which is
# the recommendation of the data-ink section applied to this figure.
import numpy as np
import matplotlib.pyplot as plt

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

# name, curve color, and a vertical nudge for the end label where two curves finish
# close together
MAPS = [
    ('viridis', '#440154', 0.00),
    ('magma', '#B63679', 0.00),
    ('coolwarm', '#B40426', 0.03),
    ('jet', '#1F77B4', -0.03),
]
N = 512


def gray_level(rgb):
    """What a black and white print keeps: green counts about ten times blue."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


def samples(name, n=N):
    return plt.get_cmap(name)(np.linspace(0, 1, n))[:, :3]


t = np.linspace(0, 1, N)
fig, ax = plt.subplots(figsize=(5.8, 3.0))

ax.plot(t, t, '--', lw=0.9, color='0.55')
ax.text(0.98, 0.995, 'gray', fontsize=9, color='0.45', ha='right', va='bottom')

for name, color, dy in MAPS:
    g = gray_level(samples(name))
    ax.plot(t, g, '-', lw=1.4, color=color)
    ax.text(1.02, g[-1] + dy, name, fontsize=9, color=color, va='center')

ax.set_xlim(0, 1)
ax.set_ylim(-0.02, 1.02)
ax.set_xlabel('position along the map')
ax.set_ylabel('gray level')
ax.grid(True, alpha=0.25)
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)

basename = 'plot_cmap_curve'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the shape of each curve, as numbers -------------------------------------------
# "Turns" counts the sign changes of the slope. One of them is a design, at the center
# of a diverging map; the rest are edges the data does not have.
print('\nmap        gray level     climbs   turns   at                 step evenness')
for name, _, _ in MAPS:
    g = gray_level(samples(name, 256))
    d = np.diff(g)
    turn_at = np.nonzero(np.diff(np.sign(d)))[0] / (len(d) - 1)
    even = np.std(np.abs(d)) / np.mean(np.abs(d))
    where = ', '.join(f'{p:.2f}' for p in turn_at) if turn_at.size else '-'
    print(f'{name:10s} {g.min():.2f} to {g.max():.2f}   '
          f'{str(bool((d > 0).all())):8s} {turn_at.size:3d}   {where:18s} {even:.2f}')
print('\nstep evenness is std(|dg|)/mean(|dg|) along the map: how even the steps are '
      'in printed gray.\nIt is not a perceptual measure, but it is the one the curves '
      'above can be checked against.')
