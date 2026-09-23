# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# One record of three variables, forty training runs, put on a flat page four ways. The
# question the panels are drawn to answer is the one the record is built around: model
# size stops paying past about ten million parameters, and training set size does not
# stop paying, so which of the two is worth the next budget.
#
# (a) is the answer the question usually gets, a 3D scatter, and it is the one form here
# that puts the third variable into no channel at all. The projection is orthographic, so
# it is affine in the data and the direction it collapses can be solved for: the script
# takes that direction, walks it across the record, and reports the whole line of runs
# that lands on one place on the page.
# (b) puts the third variable in area, fourth in the ranking, and pays for it twice: the
# range has to be squeezed into marks that stay visible at the bottom and stay apart at
# the top, and area is compressed by the eye on top of that.
# (c) puts it in a sequential colormap, sixth in the ranking. It supports more and less
# and not how much: neighboring deciles differ by a gray step the eye cannot name.
# (d) is the recommendation. The variable the question is about takes the horizontal
# axis, position on a common scale, first in the ranking, and model size becomes three
# named bins carried by color and marker shape at once so the panel survives a gray
# print. Nothing is spent on a key for the third variable, because it has an axis.
# Each bin also carries a trendline fitted within the bin and drawn only over the runs
# that support it. All three are a straight line in the logarithm of the training set,
# which rises and flattens for any positive slope and so cannot bend back the way a
# polynomial does, and all three are drawn alike, dashed and faded, so that a fitted
# curve is never mistaken for a measured one and the runs keep the ink; the bin's
# color is what tells them apart.
# The print block reports the residual and checks each curve for rise and concavity.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import Normalize
from mpl_toolkits.mplot3d import proj3d          # noqa: F401  (registers '3d')

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

# Okabe-Ito, the palette of Fig. plot_okabeito, and one marker per bin as well as one
# color, so the bins survive a gray print and a deficiency simulation.
C_BIN = ['#0072B2', '#E69F00', '#009E73']
M_BIN = ['o', 's', '^']
FIT_LS = (0, (5, 2))            # every trendline dashed and faded, so a fitted curve
FIT_LW = 1.1                    # never reads as a measured one and the runs stay the
FIT_ALPHA = 0.75                # ink the eye lands on first
C_MARK = '#1B7F5A'
AREA_PER_K = 0.8            # points^2 of marker area per thousand training samples
TARGET = 0.88               # the accuracy the reader is asked to reach

# --- forty runs: model size, training set size, and what they scored ----------------
rng = np.random.default_rng(11)
n = 40
size = rng.uniform(2, 40, n)                     # millions of parameters
train = rng.uniform(5, 200, n)                   # thousands of samples
acc = (0.63 + 0.12 * (1 - np.exp(-size / 6.0))   # saturates by about 10 M
       + 0.20 * (train / (train + 40))           # still climbing at 200 k
       + rng.normal(0, 0.006, n))


def gray_level(rgb):
    """What a black and white print keeps: green counts about ten times blue."""
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


fig = plt.figure(figsize=(6.4, 5.2))
gs = fig.add_gridspec(2, 2, hspace=0.42, wspace=0.30,
                      left=0.09, right=0.97, top=0.90, bottom=0.09)

# --- (a) the third variable as depth ------------------------------------------------
ax_a = fig.add_subplot(gs[0, 0], projection='3d')
ax_a.scatter(size, train, acc, s=12, color=C_MARK, depthshade=False)
ax_a.view_init(elev=18, azim=-62)
ax_a.set_proj_type('ortho')          # affine in the data, so the line the projection
                                     # cannot separate is exact and can be measured
ax_a.set_box_aspect(None, zoom=1.10)
ax_a.set_xlabel('size (M)', labelpad=-4)
ax_a.set_ylabel('train (k)', labelpad=-4)
ax_a.set_zlabel('accuracy', labelpad=-6)
ax_a.locator_params(nbins=4)
ax_a.tick_params(labelsize=9, pad=-1)
ax_a.set_title('(a) all three as a 3D scatter', pad=26)   # level with the title of (b),
                                                          # which carries a key beneath it

# --- (b) the third variable as area -------------------------------------------------
ax_b = fig.add_subplot(gs[0, 1])
ax_b.scatter(size, acc, s=AREA_PER_K * train, facecolor=C_MARK, alpha=0.55,
             edgecolor=C_MARK, lw=0.5)
for key in (50, 125, 200):
    ax_b.scatter([], [], s=AREA_PER_K * key, facecolor=C_MARK, alpha=0.55,
                 edgecolor=C_MARK, lw=0.5, label=f'{key} k')
# The key goes above the panel: every corner inside it holds marks, and a key that covers
# data would be one more cost of this encoding rather than a fair drawing of it.
key_b = ax_b.legend(loc='lower left', bbox_to_anchor=(0.0, 1.01, 1.0, 0.12),
                    mode='expand', ncol=3, frameon=False, handletextpad=0.7,
                    columnspacing=1.0, borderpad=0.2)
ax_b.margins(x=0.09, y=0.09)         # the largest marks need room off the frame
ax_b.set_title('(b) the third variable as area', pad=26)

# --- (c) the third variable as color ------------------------------------------------
ax_c = fig.add_subplot(gs[1, 0])
ax_c.scatter(size, acc, c=train, cmap='viridis', s=20, vmin=train.min(),
             vmax=train.max())
sm = cm.ScalarMappable(norm=Normalize(train.min(), train.max()), cmap='viridis')
cb = fig.colorbar(sm, ax=ax_c, fraction=0.046, pad=0.04, ticks=[50, 100, 150, 200])
cb.ax.tick_params(labelsize=9)
cb.outline.set_linewidth(0.5)
cb.outline.set_edgecolor('0.6')
cb.ax.set_title('train (k)', fontsize=9, pad=4)   # above the bar: beside it would land
                                                  # on the y label of the panel to its right
ax_c.set_title('(c) the third variable as color')

for ax in (ax_b, ax_c):
    ax.set_xlabel('model size (M parameters)')
    ax.set_ylabel('accuracy')

# --- (d) the third variable on the axis ---------------------------------------------
ax_d = fig.add_subplot(gs[1, 1])
edges = np.quantile(size, [0, 1 / 3, 2 / 3, 1.0])
edges[-1] += 1e-9
names = [f'{edges[i]:.0f} to {edges[i + 1]:.0f}' for i in range(3)]
fits = []
for i in range(3):
    m = (size >= edges[i]) & (size < edges[i + 1])
    ax_d.scatter(train[m], acc[m], s=20, marker=M_BIN[i], color=C_BIN[i],
                 label=names[i], zorder=3)
    # Two parameters on thirteen or so runs; Polynomial.fit maps the window onto
    # [-1, 1] itself, and the curve is never extended past the bin's own runs.
    p = np.polynomial.Polynomial.fit(np.log(train[m]), acc[m], 1)
    fit = lambda v, p=p: p(np.log(v))                       # noqa: E731
    xs = np.linspace(train[m].min(), train[m].max(), 200)
    ax_d.plot(xs, fit(xs), ls=FIT_LS, lw=FIT_LW, color=C_BIN[i], alpha=FIT_ALPHA,
              zorder=2)
    fits.append((m, fit, xs))
ax_d.axhline(TARGET, color='0.55', lw=0.8, ls=(0, (4, 2)), zorder=1)
ax_d.text(8, TARGET + 0.004, f'{TARGET:.2f}', fontsize=9, color='0.35', va='bottom')
ax_d.legend(loc='lower right', frameon=False, title='size (M)', borderpad=0.1)
ax_d.set_xlabel('training set (k samples)')
ax_d.set_ylabel('accuracy')
ax_d.set_title('(d) the third variable on the axis')

# One accuracy scale in all four panels, ticked through 0.95, so that a height in one
# panel is the same accuracy in the next and the eye can carry a reading across the
# figure instead of re-reading the axis at every panel.
ACC_TICKS = np.arange(0.75, 0.96, 0.05)
ACC_LIM = (0.735, 0.955)
for ax in (ax_b, ax_c, ax_d):
    ax.set_yticks(ACC_TICKS)
    ax.set_ylim(*ACC_LIM)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.grid(True, alpha=0.22)
ax_a.set_zticks(ACC_TICKS)
ax_a.set_zlim(*ACC_LIM)

basename = 'plot_thirdvar'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what each channel delivers, measured rather than asserted -----------------------
fig.canvas.draw()
MM = 25.4 / fig.dpi                              # display pixels to millimetres
print(f'{n} runs: model size {size.min():.1f} to {size.max():.1f} M, training set '
      f'{train.min():.0f} to {train.max():.0f} k, accuracy {acc.min():.3f} to '
      f'{acc.max():.3f}')

# (a) depth is not recoverable: one place on the page is a whole line in the data
def page(xyz):
    """Where a run lands on the printed page, in millimetres."""
    px, py, _ = proj3d.proj_transform(xyz[:, 0], xyz[:, 1], xyz[:, 2], ax_a.get_proj())
    return ax_a.transData.transform(np.column_stack([px, py])) * MM


runs = np.column_stack([size, train, acc])
base = runs[np.argmin(np.hypot(*(page(runs) - page(runs).mean(0)).T))]   # a central run
step = np.array([np.ptp(size), np.ptp(train), np.ptp(acc)]) * 1e-3
A = np.column_stack([(page((base + np.eye(3)[i] * step[i])[None]) - page(base[None]))[0]
                     / step[i] for i in range(3)])
d = np.linalg.svd(A)[2][-1]                      # the direction the projection kills
lim = np.array([[size.min(), size.max()],        # the box the record itself occupies,
                [train.min(), train.max()],      # so every point of the line is a run
                [acc.min(), acc.max()]])         # that could have been observed
t = np.concatenate([(lim[:, 0] - base) / d, (lim[:, 1] - base) / d])
seg = base + np.outer([t[t < 0].max(), t[t > 0].min()], d)
print(f'  (a) every run on one line of the record lands on one place on the page, within '
      f'{np.hypot(*np.diff(page(seg), axis=0)[0]):.2f} mm:\n      along it the training '
      f'set runs {seg[:, 1].min():.0f} to {seg[:, 1].max():.0f} k and the accuracy '
      f'{seg[:, 2].min():.3f} to {seg[:, 2].max():.3f}, and the panel reports neither')

# (b) area: what the range costs at both ends, and what the eye keeps of it
d_mm = 2 * np.sqrt(AREA_PER_K * train / np.pi) * 25.4 / 72
ratio = train.max() / train.min()
xy = ax_b.transData.transform(np.column_stack([size, acc]))
r_px = np.sqrt(AREA_PER_K * train / np.pi) * fig.dpi / 72
sep = np.hypot(xy[:, 0:1] - xy[None, :, 0], xy[:, 1:2] - xy[None, :, 1])
covered = ((sep < (r_px[:, None] + r_px[None, :])) & ~np.eye(n, dtype=bool)
           & (train[None, :] > train[:, None])).any(axis=1)
key_box = key_b.get_window_extent()
key_frac = (key_box.width * key_box.height
            / (ax_b.get_window_extent().width * ax_b.get_window_extent().height))
print(f'  (b) marks run {d_mm.min():.1f} to {d_mm.max():.1f} mm across; the range is a '
      f'factor of {ratio:.0f} in area,\n      which the eye reads as about '
      f'{ratio ** 0.7:.0f} at an area exponent of 0.7, and {covered.sum()} of the {n} '
      f'marks are overlapped by a larger one;\n      the size key claims '
      f'{key_frac:.0%} of the panel and still names only {len(key_b.get_texts())} '
      f'reference values')

# (c) color: the gray step between neighboring deciles, against what a reader can name
deciles = np.quantile(train, np.linspace(0, 1, 11))
g = gray_level(plt.get_cmap('viridis')(
    (deciles - train.min()) / np.ptp(train))[..., :3])
print(f'  (c) one decile of training set, {np.diff(deciles).mean():.0f} k on average, is '
      f'{np.abs(np.diff(g)).mean():.3f} of gray,\n      against the five or so levels a '
      f'reader can name on a sequential ramp')

# (d) the reading the panel is for, and the comparison it settles
reached = train[acc >= TARGET]
qt, qs = np.quantile(train, [0.25, 0.75]), np.quantile(size, [0.25, 0.75])
gain_train = acc[train >= qt[1]].mean() - acc[train <= qt[0]].mean()
gain_size = acc[size >= qs[1]].mean() - acc[size <= qs[0]].mean()
print(f'  (d) the smallest training set reaching {TARGET:.2f} is {reached.min():.0f} k, '
      f'read off the horizontal axis;\n      the top quarter of training sets scores '
      f'{gain_train:.3f} above the bottom quarter, and the top quarter of model sizes '
      f'{gain_size:.3f} above its own')
for i, (m, fit, xs) in enumerate(fits):
    res, ys = acc[m] - fit(train[m]), fit(xs)
    d1, d2 = np.diff(ys), np.diff(ys, 2)
    bend = ('straight' if np.allclose(d2, 0, atol=1e-12)
            else 'concave' if (d2 < 0).all() else 'NOT concave')
    print(f'      {names[i]:>8s} M: a + b log(train) over {m.sum()} runs, '
          f'{train[m].min():.0f} to {train[m].max():.0f} k, rms residual '
          f'{np.sqrt((res ** 2).mean()):.4f}, accuracy {ys.min():.3f} to '
          f'{ys.max():.3f},\n                    '
          f'{"rising" if (d1 > 0).all() else "NOT rising"} and '
          f'{bend} throughout, '
          f'drawn dashed at {FIT_LW:.1f} pt and alpha {FIT_ALPHA:g}')
