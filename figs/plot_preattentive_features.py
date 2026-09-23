# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The pre-attentive attribute gallery from the DLI human-perception slides
# (after Few, "Show Me the Numbers", 2012). Each mini-panel is a small grid in
# which exactly one element differs; that element is found without a search.
# Attributes are grouped as Form / Color / Spatial position / Motion. Flicker
# and motion cannot be shown on a static page, so Direction only hints a heading.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'axes.labelsize': 10,
    'mathtext.fontset': 'cm',
})

NEUTRAL = '#333333'       # the distractors, drawn dark like the source chart
C_TARGET = '#D62728'      # the color target, the one place a color is used


def cell_grid(nx=4, ny=3, margin=0.16):
    xs = np.linspace(margin, 1 - margin, nx)
    ys = np.linspace(1 - margin, margin, ny)      # top-to-bottom
    X, Y = np.meshgrid(xs, ys)
    return np.column_stack([X.ravel(), Y.ravel()])


def center_index(P):
    return int(np.argmin(((P - [0.5, 0.5]) ** 2).sum(axis=1)))


def bar(ax, x, y, length=0.16, angle=90, lw=1.5):
    a = np.radians(angle)
    dx, dy = 0.5 * length * np.cos(a), 0.5 * length * np.sin(a)
    ax.plot([x - dx, x + dx], [y - dy, y + dy], color=NEUTRAL, lw=lw,
            solid_capstyle='round')


# --- one draw function per attribute -------------------------------------
def draw_length(ax):
    xs = np.linspace(0.22, 0.78, 4)
    for i, x in enumerate(xs):
        h = 0.30 if i == 2 else 0.58            # one is short
        ax.plot([x, x], [0.5 - h / 2, 0.5 + h / 2], color=NEUTRAL, lw=1.6,
                solid_capstyle='butt')


def draw_width(ax):
    xs = np.linspace(0.22, 0.78, 4)
    for i, x in enumerate(xs):
        lw = 5.0 if i == 2 else 1.6             # one is thick
        ax.plot([x, x], [0.22, 0.78], color=NEUTRAL, lw=lw, solid_capstyle='butt')


def draw_orientation(ax):
    P = cell_grid(4, 3)
    ti = center_index(P)
    for i, (x, y) in enumerate(P):
        bar(ax, x, y, 0.17, angle=45 if i == ti else 90)


def draw_size(ax):
    P = cell_grid(4, 3)
    ti = center_index(P)
    s = [90 if i == ti else 26 for i in range(len(P))]
    ax.scatter(P[:, 0], P[:, 1], s=s, c=NEUTRAL, edgecolors='none')


def draw_shape(ax):
    P = cell_grid(4, 3)
    ti = center_index(P)
    for i, (x, y) in enumerate(P):
        if i == ti:
            ax.scatter(x, y, s=42, c=NEUTRAL, marker='s', edgecolors='none')
        else:
            bar(ax, x, y, 0.17, 90)


def draw_curvature(ax):
    P = cell_grid(4, 3)
    ti = center_index(P)
    for i, (x, y) in enumerate(P):
        if i == ti:
            ax.plot([x, x], [y - 0.09, y + 0.09], color=NEUTRAL, lw=1.5)
        else:
            ax.add_patch(Arc((x - 0.03, y), 0.15, 0.20, theta1=-70, theta2=70,
                             color=NEUTRAL, lw=1.5))


def draw_enclosure(ax):
    P = cell_grid(4, 3)
    ti = center_index(P)
    ax.scatter(P[:, 0], P[:, 1], s=44, c=NEUTRAL, marker='s', edgecolors='none')
    x, y = P[ti]
    ax.add_patch(Rectangle((x - 0.095, y - 0.11), 0.19, 0.22, fill=False,
                           edgecolor=NEUTRAL, lw=1.1))


def draw_blur(ax):
    P = cell_grid(4, 3)
    ti = center_index(P)
    for i, (x, y) in enumerate(P):
        if i == ti:
            ax.scatter(x, y, s=110, c=NEUTRAL, alpha=0.22, edgecolors='none')
        else:
            ax.scatter(x, y, s=28, c=NEUTRAL, edgecolors='none')


def draw_color(ax):
    P = cell_grid(4, 3)
    ti = center_index(P)
    c = [C_TARGET if i == ti else NEUTRAL for i in range(len(P))]
    ax.scatter(P[:, 0], P[:, 1], s=34, c=c, edgecolors='none')


def draw_intensity(ax):
    P = cell_grid(4, 3)
    ti = center_index(P)
    c = ['#BEBEBE' if i == ti else NEUTRAL for i in range(len(P))]
    ax.scatter(P[:, 0], P[:, 1], s=34, c=c, edgecolors='none')


def draw_position(ax):
    pts = np.array([[0.22, 0.62], [0.42, 0.62], [0.62, 0.62], [0.66, 0.26]])
    ax.scatter(pts[:, 0], pts[:, 1], s=34, c=NEUTRAL, edgecolors='none')


def draw_grouping(ax):
    r = np.random.default_rng(3)
    c1 = r.normal([0.5, 0.62], 0.07, (9, 2))
    c2 = r.normal([0.28, 0.28], 0.035, (3, 2))
    c3 = r.normal([0.72, 0.28], 0.035, (3, 2))
    for c in (c1, c2, c3):
        ax.scatter(c[:, 0], c[:, 1], s=24, c=NEUTRAL, edgecolors='none')


def draw_direction(ax):
    th = np.linspace(0, 2 * np.pi, 9, endpoint=False)
    xs, ys = 0.5 + 0.28 * np.cos(th), 0.5 + 0.28 * np.sin(th)
    ti = 3
    for i in range(len(th)):
        d = -1 if i == ti else 1                 # one heads the other way
        ax.annotate('', xy=(xs[i] + d * 0.06, ys[i] + d * 0.05),
                    xytext=(xs[i], ys[i]),
                    arrowprops=dict(arrowstyle='-|>', color=NEUTRAL, lw=1.0))
        ax.scatter(xs[i], ys[i], s=16, c=NEUTRAL, edgecolors='none')


# --- layout: rows are groups, as on the slide ----------------------------
panels = {
    (0, 0): ('Length', draw_length),
    (0, 1): ('Width', draw_width),
    (0, 2): ('Orientation', draw_orientation),
    (1, 0): ('Size', draw_size),
    (1, 1): ('Shape', draw_shape),
    (1, 2): ('Curvature', draw_curvature),
    (2, 0): ('Enclosure', draw_enclosure),
    (2, 1): ('Blur', draw_blur),
    (3, 0): ('Color', draw_color),
    (3, 1): ('Light or dark', draw_intensity),
    (4, 0): ('2-D position', draw_position),
    (4, 1): ('Spatial grouping', draw_grouping),
    (5, 0): ('Direction', draw_direction),
}
group_labels = {0: 'Form', 3: 'Color', 4: 'Spatial\nposition', 5: 'Motion'}

fig, axes = plt.subplots(6, 3, figsize=(7.0, 7.0))
fig.subplots_adjust(left=0.15, wspace=0.15, hspace=0.45)

for r in range(6):
    for c in range(3):
        ax = axes[r, c]
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_visible(False)
        if (r, c) in panels:
            title, fn = panels[(r, c)]
            fn(ax)
            ax.set_title(title, fontsize=9)
        else:
            ax.set_visible(False)
    if r in group_labels:
        axes[r, 0].text(-0.30, 0.5, group_labels[r], transform=axes[r, 0].transAxes,
                        ha='right', va='center', fontsize=10, fontstyle='italic')

basename = 'plot_preattentive_features'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print(f'{len(panels)} attribute panels across Form/Color/Spatial/Motion groups')
