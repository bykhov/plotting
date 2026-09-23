# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# One set of five values put through the four charts a spreadsheet offers for it, in
# descending order of how much of the ranking survives: a flat pie, the same pie under
# a tilt, a 3D bar chart, and a sorted bar chart. The two largest values differ by one
# part in a hundred, which is the whole test - every panel holds that difference and
# only the last one shows it.
#
# The tilt of the second panel and the view of the third are the ones the source uses.
# After the chart-basics slides of the DLI Accelerated Data Science Teaching Kit
# (Lecture 7.4, slides 18-24).
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from mpl_toolkits.mplot3d import proj3d          # noqa: F401  (registers '3d')

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

labels = list('ABCDE')
values = np.array([37.0, 36.0, 24.0, 2.0, 1.0])
frac = values / values.sum()
# Okabe-Ito, the color-blind-safe qualitative scheme of Fig. plot_cvd: five unordered
# categories, so a scheme and not a colormap.
COLORS = ['#0072B2', '#E69F00', '#009E73', '#CC79A7', '#56B4E9']

START = 90.0                  # degrees; puts B at the front of the tilted pie and A at the back
TILT = 28.0                   # degrees of tilt in panel (b)
R, H = 1.0, 0.22              # pie radius and the slab thickness the tilt reveals

fig = plt.figure(figsize=(6.0, 4.4))
edges = np.deg2rad(START + 360.0 * np.concatenate([[0.0], np.cumsum(frac)]))


def label_slices(ax, squash=1.0, dy=0.0):
    """Name each slice outside the rim, with a leader for the slices too thin to
    label in place. Placing them by hand is what keeps D and E from colliding."""
    for i, lab in enumerate(labels):
        tm = 0.5 * (edges[i] + edges[i + 1])
        u = np.array([np.cos(tm), squash * np.sin(tm)])
        if frac[i] >= 0.05:
            ax.text(*(1.16 * R * u + [0.0, dy]), lab, ha='center', va='center',
                    fontsize=9)
        else:                                    # a sliver: pull the name out on a leader
            off = 1.55 + 0.30 * (i - len(values) + 1.5)
            ax.annotate(lab, xy=tuple(1.00 * R * u + [0.0, dy]),
                        xytext=tuple(off * R * u + [0.0, dy]),
                        ha='center', va='center', fontsize=9,
                        arrowprops={'arrowstyle': '-', 'linewidth': 0.6,
                                    'color': '0.4', 'shrinkA': 1, 'shrinkB': 1})


# --- (a) a flat pie: the value is an angle, which is third in the ranking ---
ax = fig.add_subplot(2, 2, 1)
ax.pie(values, colors=COLORS, startangle=START, counterclock=True,
       wedgeprops={'edgecolor': 'white', 'linewidth': 0.8})
label_slices(ax)
ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.30, 1.85)
ax.set_aspect('equal')
ax.set_title('(a) pie')

# --- (b) the same pie under a tilt: the value is now an angle plus whatever area the
#         slab wall adds, and only the front slices get a wall ---
ax = fig.add_subplot(2, 2, 2)
k = np.cos(np.deg2rad(TILT))                     # vertical foreshortening of the disc


def arc(t0, t1, n=200):
    t = np.linspace(t0, t1, n)
    return np.stack([R * np.cos(t), k * R * np.sin(t)], axis=-1)


def darker(hex_color, f=0.65):
    rgb = np.array([int(hex_color[i:i + 2], 16) / 255 for i in (1, 3, 5)])
    return tuple(f * rgb)


for i in range(len(values)):
    pts = arc(edges[i], edges[i + 1])
    ax.add_patch(Polygon(np.vstack([[0.0, 0.0], pts]), closed=True,
                         facecolor=COLORS[i], edgecolor='white', linewidth=0.8))

# the slab wall, drawn after the top faces so it sits in front of them
for i in range(len(values)):
    t = np.linspace(edges[i], edges[i + 1], 200)
    front = np.sin(t) < 0                        # only the near half of the rim is visible
    if not front.any():
        continue
    top = np.stack([R * np.cos(t[front]), k * R * np.sin(t[front])], axis=-1)
    wall = np.vstack([top, top[::-1] - [0.0, H]])
    ax.add_patch(Polygon(wall, closed=True, facecolor=darker(COLORS[i]),
                         edgecolor='none'))

label_slices(ax, squash=k, dy=-0.10)
ax.set_xlim(-1.45, 1.45)
ax.set_ylim(-1.30, 1.85)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title(f'(b) the same pie, tilted by ${TILT:.0f}^{{\\circ}}$')

# --- (c) a 3D bar chart: length from a common baseline replaced by a bar top that has
#         to be compared with a wall standing behind it ---
ax3 = fig.add_subplot(2, 2, 3, projection='3d')
xs = np.arange(len(values))
ax3.bar3d(xs - 0.35, np.zeros(len(values)), np.zeros(len(values)),
          0.7, 0.7, values, color=COLORS, shade=True, edgecolor='none')
ax3.view_init(elev=15, azim=-70)                 # the rotation the source slide uses
ax3.set_xticks(xs)
ax3.set_xticklabels(labels)
ax3.set_yticks([])
ax3.set_zlim(0, 40)
ax3.set_zticks([0, 10, 20, 30, 40])
ax3.tick_params(labelsize=8, pad=-2)
ax3.set_box_aspect((1.7, 1.0, 1.1), zoom=1.15)
ax3.set_title('(c) 3D bars')

# --- (d) length from a common baseline, sorted, with the numbers printed ---
ax = fig.add_subplot(2, 2, 4)
order = np.argsort(values)
ax.barh(np.arange(len(values)), values[order],
        color=[COLORS[j] for j in order], height=0.65)
for j, v in enumerate(values[order]):
    ax.text(v + 1.0, j, f'{v:.0f}', va='center', fontsize=9)
ax.set_yticks(np.arange(len(values)))
ax.set_yticklabels([labels[j] for j in order])
ax.set_xlim(0, 44)
ax.set_xticks([0, 10, 20, 30, 40])
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
ax.set_title('(d) sorted bars, values printed')

# tight_layout cannot place a 3D axes next to three 2D ones without complaining, so
# the grid is spaced by hand and the outer margin is trimmed at save time.
fig.subplots_adjust(left=0.02, right=0.97, top=0.93, bottom=0.06,
                    wspace=0.10, hspace=0.28)

basename = 'plot_pie'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what each panel costs, in the numbers the caption quotes -------------------
print('values ' + ', '.join(f'{l}={v:.0f}' for l, v in zip(labels, values)))

# (a) the two largest as an angle
d_ang = 360.0 * (frac[0] - frac[1])
print(f'\n(a) A and B are {values[0] - values[1]:.0f} apart in the data and '
      f'{d_ang:.1f} deg apart in arc, out of 360 deg')

# (b) apparent area of each slice: the foreshortened top face plus the slab wall,
#     which only the slices on the near side of the rim are given.
print('\n(b) apparent area under the tilt (top face + visible wall):')
areas = []
for i in range(len(values)):
    t = np.linspace(edges[i], edges[i + 1], 4000)
    top = 0.5 * R ** 2 * (t[-1] - t[0]) * k
    front = np.sin(t) < 0
    wall = H * np.abs(np.diff(R * np.cos(t[front]))).sum() if front.any() else 0.0
    areas.append(top + wall)
    print(f'    {labels[i]}: value {values[i]:4.0f}, top {top:.3f}, wall {wall:.3f}, '
          f'total {top + wall:.3f}')
areas = np.array(areas)
print(f'    B / A = {areas[1] / areas[0]:.2f} of apparent area, '
      f'though B / A = {values[1] / values[0]:.2f} in the data: '
      f'the smaller value is drawn {100 * (areas[1] / areas[0] - 1):.0f}% larger')

# (c) what a bar top reads as when it is compared with the wall behind it. The
#     projection is affine in z at fixed (x, y), so two samples fix the line.
fig.canvas.draw()
M = ax3.get_proj()
y_back = ax3.get_ylim()[1]


def disp_y(x, y, z):
    return proj3d.proj_transform(x, y, z, M)[1]


apparent = []
for x, v in zip(xs, values):
    y_top = disp_y(x, 0.0, v)                        # the bar top, at the front face
    z0, z1 = disp_y(x, y_back, 0.0), disp_y(x, y_back, 40.0)
    apparent.append(40.0 * (y_top - z0) / (z1 - z0))  # same height on the back wall
apparent = np.array(apparent)
off = apparent - values
print('\n(c) value read off the back wall against the value actually drawn:')
for lab, v, a, d in zip(labels, values, apparent, off):
    print(f'    {lab}: drawn {v:5.1f}, reads as {a:5.1f} ({d:+.1f} units)')
print(f'    every bar top reads low, by {-off.max():.0f} to {-off.min():.0f} units, '
      f'and not by the same amount: the A to B gap of '
      f'{values[0] - values[1]:.0f} reads as {apparent[0] - apparent[1]:.1f}')

# (d) nothing to report: the length is the value and the value is printed.
print('\n(d) rank low to high: ' + ' < '.join(np.array(labels)[order]))
