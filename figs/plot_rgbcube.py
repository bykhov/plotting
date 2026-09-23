# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# A color is three numbers. The unit RGB cube holds all of them: the eight corners
# are black, white and the six pure colors, the black to white diagonal carries the
# grays, and every color a figure can use is a point inside. The corner labels give
# the same three numbers as hex codes, which is the form a plotting library takes.
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D            # noqa: F401  (registers '3d')

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

CORNERS = {
    'black': (0, 0, 0), 'white': (1, 1, 1),
    'red': (1, 0, 0), 'yellow': (1, 1, 0), 'green': (0, 1, 0),
    'cyan': (0, 1, 1), 'blue': (0, 0, 1), 'magenta': (1, 0, 1),
}
# The two ends of the diagonal are the corners worth naming on the page; the rest
# of the hex codes are in the printout and in the text.
LABELLED = [('black', '#000000'), ('white', '#FFFFFF')]

fig = plt.figure(figsize=(3.6, 3.4))
ax = fig.add_subplot(1, 1, 1, projection='3d')

n = 24
g = np.linspace(0, 1, n)
A, B = np.meshgrid(g, g)
O, I = np.zeros_like(A), np.ones_like(A)

# six faces, each a fine mesh colored by its own RGB coordinates
faces = [
    (O, A, B, np.stack([O, A, B], -1)), (I, A, B, np.stack([I, A, B], -1)),
    (A, O, B, np.stack([A, O, B], -1)), (A, I, B, np.stack([A, I, B], -1)),
    (A, B, O, np.stack([A, B, O], -1)), (A, B, I, np.stack([A, B, I], -1)),
]
for X, Y, Z, C in faces:
    ax.plot_surface(X, Y, Z, facecolors=C, shade=False, rstride=1, cstride=1,
                    linewidth=0, antialiased=False)

ax.plot([0, 1], [0, 1], [0, 1], '--', color='0.3', lw=1.1, zorder=10)
ax.text(0.52, 0.52, 0.60, 'the grays:\nblack to white', fontsize=9,
        ha='center', color='0.15', zorder=11,
        bbox=dict(fc='white', ec='none', alpha=0.9, pad=1.5))

# Corner labels are pushed a little away from the cube so they sit on the page
# background rather than on the colored faces.
OFFSET = {'black': (-0.10, -0.06, -0.10), 'white': (0.06, 0.06, 0.12)}
for name, hexcode in LABELLED:
    x, y, z = np.array(CORNERS[name], float) + np.array(OFFSET[name])
    ax.text(x, y, z, f'{name}\n{hexcode}', fontsize=9, ha='center', va='center',
            color='0.15', zorder=12,
            bbox=dict(fc='white', ec='none', alpha=0.75, pad=1.5))

ax.set_xlabel('$R$', labelpad=-12)
ax.set_ylabel('$G$', labelpad=-12)
ax.set_zlabel('$B$', labelpad=-12)
ax.set_xticks([])
ax.set_yticks([])
ax.set_zticks([])
ax.grid(False)
for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
    pane.pane.set_visible(False)
    pane.line.set_color('0.4')
ax.set_box_aspect([1, 1, 1])
ax.view_init(elev=20, azim=-58)

plt.tight_layout()

basename = 'plot_rgbcube'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the eight corners, as the three numbers and as the hex code they are written in ---
print('\ncorner    R  G  B   hex')
for name, rgb in CORNERS.items():
    hexcode = '#{:02X}{:02X}{:02X}'.format(*(int(round(255 * c)) for c in rgb))
    print(f'{name:9s} {rgb[0]:.0f}  {rgb[1]:.0f}  {rgb[2]:.0f}   {hexcode}')
mid = '#{0:02X}{0:02X}{0:02X}'.format(128)
print(f'mid gray on the diagonal, R = G = B = 0.5: {mid}')
