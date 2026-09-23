# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# One set of five values, encoded six ways, one panel per entry of the Cleveland and
# McGill ranking, in descending order of how accurately a reader can recover them.
# Rank the five categories in each panel and notice where the task stops being
# automatic and starts being a guess. The volume panel carries the same five values
# twice, as balls and as cubes, because the loss there belongs to the cube root and
# not to the solid picked to show it. The last entry of the ranking, encoding the
# value as a different color, is the subject of its own figure in the color section.
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
from matplotlib.patches import Polygon

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

C_MARK = '#1E90FF'
LIGHT = np.array([-0.40, 0.50, 0.77])
LIGHT = LIGHT / np.linalg.norm(LIGHT)          # one light for the balls and the cubes

labels = list('ABCDE')
values = np.array([3.0, 7.0, 5.0, 9.0, 4.0])
xs = np.arange(5)
unit = values / values.max()                   # normalized once, reused by every panel

Y_BALL, Y_CUBE = 0.70, 0.28                    # the two lines of marks in panel (e)
MARK_AREA = 260                                # points^2 on the page for the largest
# mark of (d) and of each line of (e), so the three sets of marks compare directly. It
# is set by the tightest pair of the ball line, C and D: at this area they clear each
# other by about 2.7 pt, and the line reads as five marks rather than one run of them.

fig, axes = plt.subplots(2, 3, figsize=(5.6, 4.2))
ax = axes.ravel()

# --- 1. position on a common scale ---
ax[0].plot(xs, values, 'o', ms=6, color=C_MARK)
ax[0].set_ylim(0, 10)
ax[0].set_title('(a) position')

# --- 2. length from a common baseline ---
ax[1].bar(xs, values, width=0.6, color=C_MARK)
ax[1].set_ylim(0, 10)
ax[1].set_title('(b) length')

# --- 3. slope ---
for i, u in enumerate(unit):
    ax[2].plot([i - 0.3, i + 0.3], [0.5 - 0.45 * u, 0.5 + 0.45 * u],
               '-', lw=1.6, color=C_MARK)
ax[2].set_ylim(0, 1)
ax[2].set_title('(c) slope')

# --- 4. area: marker size in points^2 is an area, so this is a true area encoding ---
ax[3].scatter(xs, np.full(5, 0.5), s=MARK_AREA * unit, color=C_MARK)
ax[3].set_ylim(0, 1)
ax[3].set_title('(d) area')

# --- 5. volume, twice: a ball and a cube whose volume is the value, so the radius
#        and the edge both follow the cube root and the shape the reader sees grows
#        only as the two-thirds power. Both lines are placed after the first draw,
#        once the panel geometry is known (see below) ---
ax[4].set_ylim(0, 1)
ax[4].set_title('(e) volume')

# --- 6. color strength: one color, from washed out to full ---
strength = np.stack([hsv_to_rgb([0.58, 0.15 + 0.85 * u, 0.85]) for u in unit])
ax[5].bar(xs, np.ones(5), width=0.8, color=strength)
ax[5].set_ylim(0, 1)
ax[5].set_title('(f) color strength')

for i, a in enumerate(ax):
    a.set_xticks(xs)
    a.set_xticklabels(labels)
    a.set_xlim(-0.7, 4.7)
    if i in (0, 1):                            # the two panels with one shared scale
        a.grid(True, axis='y', alpha=0.25)
        hidden = ('top', 'right')
    else:
        a.set_yticks([])
        hidden = ('top', 'right', 'left')      # no common y scale, so no y axis line
    for side in hidden:
        a.spines[side].set_visible(False)

plt.tight_layout()


def ball_image(color, n=320):
    """A lit sphere as an RGBA image: shading only, no drawn highlight mark."""
    g = np.linspace(-1, 1, n)
    X, Y = np.meshgrid(g, g)
    R = np.hypot(X, Y)
    Z = np.sqrt(np.clip(1 - R**2, 0, None))       # the front half of the ball
    lit = np.clip(X * LIGHT[0] + Y * LIGHT[1] + Z * LIGHT[2], 0, 1)
    shade = 0.30 + 0.70 * lit                     # ambient plus diffuse
    base = np.array(matplotlib.colors.to_rgb(color))
    rgb = np.clip(base[None, None, :] * shade[..., None]
                  + 0.45 * lit[..., None] ** 22, 0, 1)   # soft sheen, not a second disc
    alpha = np.clip((1.0 - R) * n / 3.0, 0, 1)    # one-pixel-ish soft edge
    return np.concatenate([rgb, alpha[..., None]], axis=-1)


# Seen along (1, 1, 1), a cube shows three faces and its outline is a regular hexagon.
E_U = np.array([1.0, -1.0, 0.0]) / np.sqrt(2)     # screen right, in cube coordinates
E_V = np.array([-1.0, -1.0, 2.0]) / np.sqrt(6)    # screen up
E_W = np.array([1.0, 1.0, 1.0]) / np.sqrt(3)      # out of the page, toward the reader
FACES = [                                         # the three faces that face the reader
    ((0, 0, 1), [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)]),   # top
    ((0, 1, 0), [(0, 1, 0), (1, 1, 0), (1, 1, 1), (0, 1, 1)]),   # left
    ((1, 0, 0), [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)]),   # right
]


def cube_faces(color, x, y, s_in, x_per_in, y_per_in):
    """The three lit faces of a cube of edge s_in inches, centered on (x, y)."""
    base = np.array(matplotlib.colors.to_rgb(color))
    out = []
    for normal, corners in FACES:
        n = np.array(normal, float)
        cam = np.array([n @ E_U, n @ E_V, n @ E_W])    # the normal as the reader sees it
        shade = 0.45 + 0.55 * max(cam @ LIGHT, 0.0)    # the ball's light, plus a fill
        p = (np.array(corners, float) - 0.5) * s_in    # centered on the body, in inches
        uv = np.stack([x + (p @ E_U) * x_per_in,
                       y + (p @ E_V) * y_per_in], axis=-1)
        out.append((uv, np.clip(base * shade, 0, 1)))
    return out


# The marks of panel (e) are sized on the page, not in data units, so their extents
# would come out distorted unless the panel's own scaling is undone. Draw once,
# measure the panel, then size every mark in inches: the largest ball projects to the
# same disc as the largest mark of panel (d), and the hexagon of the largest cube
# covers that same area too, so (d) and both lines of (e) compare.
fig.canvas.draw()
box = ax[4].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
x_per_in = np.diff(ax[4].get_xlim())[0] / box.width
y_per_in = np.diff(ax[4].get_ylim())[0] / box.height
r_in = np.sqrt(MARK_AREA / np.pi) / 72 * unit ** (1 / 3)        # points -> inches
s_in = np.sqrt(MARK_AREA / np.sqrt(3)) / 72 * unit ** (1 / 3)   # hexagon, area sqrt(3) s^2
ball = ball_image(C_MARK)
ax[4].set_autoscale_on(False)                    # the marks must not move the limits
for x, r, s in zip(xs, r_in, s_in):
    ax[4].imshow(ball, extent=[x - r * x_per_in, x + r * x_per_in,
                               Y_BALL - r * y_per_in, Y_BALL + r * y_per_in],
                 aspect='auto', interpolation='bilinear', zorder=3)
    for uv, rgb in cube_faces(C_MARK, x, Y_CUBE, s, x_per_in, y_per_in):
        ax[4].add_patch(Polygon(uv, closed=True, facecolor=rgb, edgecolor=rgb,
                                lw=0.3, zorder=3))        # the seam between faces closed

basename = 'plot_encoding'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print('values ' + ', '.join(f'{l}={v:g}' for l, v in zip(labels, values)))
print('rank low to high: ' + ' < '.join(np.array(labels)[np.argsort(values)]))
# How much of a threefold difference each size channel actually shows: D is three
# times A, and the shape drawn for it is three times the area in (d) but only
# 3^(2/3) times in (e), where the radius of the ball and the edge of the cube both
# follow the cube root of the value, so the two lines lose exactly the same amount.
big = values.max() / values.min()
shown, edge = big ** (2 / 3), big ** (1 / 3)
print(f'D / A = {big:.1f}x in the data, {big:.1f}x of disc area in (d), '
      f'{shown:.1f}x of mark area in (e)')
print(f'in (e) the ball radius and the cube edge both grow {edge:.2f}x, so both '
      f'lines show {shown:.1f}x of the {big:.1f}x in the data')
