# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# One synthetic sensory-panel record - four samples scored on six attributes, every
# attribute on the same 9-point scale. (a) is the form the record usually appears in:
# all four filled at alpha on a radial axis cut at 4, which is the encoding failing in
# three ways at once. (b) measures what that costs: per sample, the true level beside
# the level the polygon area of (a) makes the reader perceive, both relative to the
# control and both on a zero baseline.
import itertools
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'mathtext.fontset': 'cm',
})

# --- the record ------------------------------------------------------------------
# Synthetic, in the shape a sensory panel reports: one 9-point hedonic scale used for
# every attribute, so the radial axis means the same thing on every spoke. That is the
# condition under which a radar chart is defensible at all.
attributes = ['appearance', 'color', 'odor', 'taste', 'texture', 'overall']
# The samples carry no numeric label: a percentage on the page promises a meaning
# this synthetic record does not supply. They are ordered, control first, and the
# argument only needs each to sit further from the control than the one before it.
samples = ['control', 'A', 'B', 'C']
S = np.array([
    [8.2, 8.4, 7.9, 8.3, 8.1, 8.3],      # control
    [8.0, 8.1, 7.8, 8.0, 7.7, 8.0],      # sample A
    [7.6, 7.5, 7.6, 7.2, 6.9, 7.3],      # sample B
    [7.1, 6.8, 7.3, 6.1, 5.8, 6.4],      # sample C
])
k = S.shape[1]
SCALE_MAX = 9.0
CUT = 4.0                                 # where panel (a) starts its radial axis

# Okabe-Ito, the color-blind-safe qualitative scheme of Fig. plot_cvd
COLORS = ['#0072B2', '#E69F00', '#009E73', '#CC79A7']
C_GRAY = '0.55'
C_HIGH = '#0072B2'

# spokes: first attribute at the top, running clockwise, as radar charts are drawn
ang = np.linspace(0, 2 * np.pi, k, endpoint=False)


def closed(v):
    """A polygon has to return to its first vertex."""
    return np.concatenate([v, v[:1]])


def poly_area(r):
    """Area of the closed polygon on k equally spaced spokes, Eq. eq-plot-radar-area.
    Quadratic in the radii, and it pairs adjacent spokes only, which is why the axis
    order changes it."""
    r = np.asarray(r, dtype=float)
    return 0.5 * np.sin(2 * np.pi / len(r)) * float(np.sum(r * np.roll(r, -1)))


def polar_axes(ax, rmin, rmax, rticks):
    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_thetagrids(np.degrees(ang), attributes, fontsize=9)
    ax.set_rlim(rmin, rmax)
    ax.set_rgrids(rticks, labels=[f'{t:g}' for t in rticks], angle=22.5, fontsize=9)
    ax.tick_params(axis='y', pad=0)
    ax.grid(color='0.8', lw=0.6)
    ax.spines['polar'].set_color('0.8')


# what the record is, and what the polygon of panel (a) turns it into
a_true = np.array([poly_area(S[j]) for j in range(len(samples))])
a_cut = np.array([poly_area(S[j] - CUT) for j in range(len(samples))])
r_true = np.array([S[j].mean() / S[0].mean() for j in range(len(samples))])
r_perc = a_cut / a_cut[0]

fig = plt.figure(figsize=(7.0, 3.3))
gs = fig.add_gridspec(1, 2, wspace=0.32, left=0.05, right=0.97, top=0.90, bottom=0.14)

# --- (a) the record as it usually appears: four fills on a cut radial axis ---------
ax = fig.add_subplot(gs[0], projection='polar')
polar_axes(ax, CUT, SCALE_MAX, [5, 6, 7, 8, 9])
for j in range(len(samples)):
    ax.plot(closed(ang), closed(S[j]), '-', lw=1.0, color=COLORS[j])
    ax.fill(closed(ang), closed(S[j]), color=COLORS[j], alpha=0.35, label=samples[j])
# the key sits in the corner of the panel it belongs to, which is space the circular
# plot leaves free and is where a library would put it
ax.legend(loc='upper left', bbox_to_anchor=(-0.13, 1.10), fontsize=9,
          handlelength=1.2, borderpad=0.4, labelspacing=0.25)
ax.set_title(f'(a) four fills, radial axis cut at ${CUT:g}$', pad=14)

# --- (b) what that encoding does to the levels, as length from zero ---------------
ax = fig.add_subplot(gs[1])
x = np.arange(len(samples))
w = 0.36
ax.bar(x - w / 2, r_true, w, color=C_GRAY, label='true (mean score)')
ax.bar(x + w / 2, r_perc, w, color=C_HIGH,
       label=f'perceived (polygon area, axis cut at ${CUT:g}$)')
ax.axhline(1.0, lw=0.6, color='0.7', zorder=0)
# the pair the text quotes, named on the bars themselves
for dx, v in [(-w / 2, r_true[3]), (w / 2, r_perc[3])]:
    ax.text(x[3] + dx, v + 0.02, f'{v:.2f}', fontsize=9, ha='center', va='bottom')
ax.set_xticks(x, samples)
ax.set_ylim(0, 1.35)
ax.set_ylabel('relative to control')
ax.grid(True, axis='y', alpha=0.25)
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
ax.legend(loc='upper right', fontsize=9, handlelength=1.2, borderpad=0.4,
          labelspacing=0.25, framealpha=1.0)
ax.set_title('(b) true against perceived level', pad=14)

basename = 'plot_radar'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what the polygon does to the numbers ------------------------------------------
print('\nmean score and polygon area, by sample:')
for j, name in enumerate(samples):
    print(f'    {name:8s} mean {S[j].mean():.3f}   area {a_true[j]:6.2f}   '
          f'area on the cut axis {a_cut[j]:6.2f}')

r_score = r_true[3]
print(f'\nsample C against control: scores {r_score:.3f} of the control level, '
      f'area {a_true[3] / a_true[0]:.3f} of it, and {r_perc[3]:.3f} once the '
      f'axis is cut at {CUT:g}')
print(f'    the area is quadratic, so {r_score:.3f} of the level is '
      f'{r_score ** 2:.3f} of the area: the polygon overstates the drop by a factor of '
      f'{(1 - a_true[3] / a_true[0]) / (1 - r_score):.2f}, and by '
      f'{(1 - r_perc[3]) / (1 - r_score):.2f} on the cut axis')
print(f'    the cut removes the inner {CUT / SCALE_MAX:.0%} of every radius')
print('\npanel (b), true against perceived, relative to the control:')
for j, name in enumerate(samples):
    print(f'    {name:8s} true {r_true[j]:.3f}   perceived {r_perc[j]:.3f}   '
          f'gap {r_true[j] - r_perc[j]:.3f}')

# the same numbers under every distinct spoke ordering: rotations and reflections of
# an ordering draw the same polygon, so 6! / (6 * 2) = 60 of them are distinct.
orders = [p for p in itertools.permutations(range(k)) if p[0] == 0 and p[1] < p[-1]]
areas = np.array([poly_area(S[3][list(p)]) for p in orders])
print(f'\nover the {len(orders)} distinct orderings of the {k} spokes, sample C '
      f'has area {areas.min():.2f} to {areas.max():.2f}, a factor of '
      f'{areas.max() / areas.min():.2f}, without one number changing')
best, worst = orders[int(np.argmax(areas))], orders[int(np.argmin(areas))]
print('    largest: ' + ', '.join(attributes[i] for i in best))
print('    smallest: ' + ', '.join(attributes[i] for i in worst))
areas_cut = np.array([poly_area(S[3][list(p)] - CUT) for p in orders])
print(f'    on the cut axis of panel (a) the same 60 orderings span '
      f'{areas_cut.min():.2f} to {areas_cut.max():.2f}, a factor of '
      f'{areas_cut.max() / areas_cut.min():.2f}')

# how far the effect can go: the ordering matters in proportion to how uneven the
# profile is, so a flat record is nearly immune and a spiky one is not. Six scores at
# the two ends of the same scale are the bound.
spiky = np.array([9.0, 1.0, 9.0, 1.0, 9.0, 1.0])
a_spiky = np.array([poly_area(spiky[list(p)]) for p in orders])
print(f'    for a spiky profile on the same scale, {spiky.tolist()}, the bound is '
      f'{a_spiky.min():.2f} to {a_spiky.max():.2f}, a factor of '
      f'{a_spiky.max() / a_spiky.min():.2f}')
