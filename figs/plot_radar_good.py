# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The record of plot_radar.py drawn the two ways the text argues for, against the
# four fills on a cut axis it draws there. (a) is the radar chart under the rules
# of the box: one zero-anchored scale on every spoke and named, two profiles, one
# fill, and a stated spoke order. (b) is the fix that is not a radar chart at all:
# the same 24 numbers as a dot plot, one row per attribute on a shared 0-9 scale,
# where every comparison the record supports is a length.
#
# The spoke order of (a) is the order the panel questionnaire asks the attributes
# in, which is the only order not chosen for how the polygon comes out; the printout
# below still measures what the remaining freedom is worth, because zero-anchoring
# removes neither the quadratic area nor its dependence on that order.
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

# --- the record, the same one plot_radar.py draws --------------------------------
attributes = ['appearance', 'color', 'odor', 'taste', 'texture', 'overall']
samples = ['control', 'A', 'B', 'C']
S = np.array([
    [8.2, 8.4, 7.9, 8.3, 8.1, 8.3],      # control
    [8.0, 8.1, 7.8, 8.0, 7.7, 8.0],      # sample A
    [7.6, 7.5, 7.6, 7.2, 6.9, 7.3],      # sample B
    [7.1, 6.8, 7.3, 6.1, 5.8, 6.4],      # sample C
])
k = S.shape[1]
SCALE_MAX = 9.0

# Okabe-Ito, the color-blind-safe qualitative scheme of Fig. plot_okabeito, with a
# marker shape per sample so the panel survives the deficiency check without color.
COLORS = ['#0072B2', '#E69F00', '#009E73', '#CC79A7']
MARKERS = ['o', 's', '^', 'D']

ang = np.linspace(0, 2 * np.pi, k, endpoint=False)


def closed(v):
    """A polygon has to return to its first vertex."""
    return np.concatenate([v, v[:1]])


def poly_area(r):
    """Area of the closed polygon on k equally spaced spokes, Eq. eq-plot-radar-area."""
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


fig = plt.figure(figsize=(7.0, 3.3))
gs = fig.add_gridspec(1, 2, wspace=0.38, left=0.05, right=0.97, top=0.88, bottom=0.16)

# --- (a) the same chart under the rules: zero, named, two profiles, one fill ------
ax = fig.add_subplot(gs[0], projection='polar')
polar_axes(ax, 0.0, SCALE_MAX, [3, 6, 9])
ax.plot(closed(ang), closed(S[0]), '-', lw=1.2, color=COLORS[0], label=samples[0])
ax.plot(closed(ang), closed(S[3]), '-', lw=1.2, color=COLORS[3], label=samples[3])
ax.fill(closed(ang), closed(S[3]), color=COLORS[3], alpha=0.30)
# the radial axis carries a quantity, so it is named where its ticks are
ax.text(np.deg2rad(22.5), SCALE_MAX * 1.16, 'score', fontsize=9, ha='center',
        color='0.35')
ax.legend(loc='upper left', bbox_to_anchor=(-0.13, 1.10), fontsize=9,
          handlelength=1.2, borderpad=0.4, labelspacing=0.25)
ax.set_title('(a) two profiles, every spoke from $0$ on the $9$-point scale', pad=14)

# --- (b) the same 24 numbers as a dot plot, sorted by the gap they are read for ---
ax = fig.add_subplot(gs[1])
gap = S[0] - S[3]
order = np.argsort(gap)                          # largest gap at the top of the panel
y = np.arange(k)
for row, i in enumerate(order):
    ax.plot([S[:, i].min(), S[:, i].max()], [row, row], '-', lw=0.8, color='0.85',
            zorder=0)
for j, name in enumerate(samples):
    ax.plot(S[j][order], y, MARKERS[j], ms=4.5, color=COLORS[j], linestyle='none',
            label=name, zorder=3)
top = k - 1
ax.annotate('', xy=(S[3][order[top]], top + 0.42), xytext=(S[0][order[top]], top + 0.42),
            arrowprops=dict(arrowstyle='<->', lw=0.7, color='0.45',
                            shrinkA=0, shrinkB=0))
ax.text(0.5 * (S[0][order[top]] + S[3][order[top]]), top + 0.52,
        f'${gap[order[top]]:.1f}$', fontsize=9, ha='center', va='bottom', color='0.35')
ax.set_yticks(y, [attributes[i] for i in order])
ax.set_ylim(-0.6, k - 0.15)
ax.set_xlim(0, SCALE_MAX)
ax.set_xticks([0, 3, 6, 9])
ax.set_xlabel('score, $9$-point scale')
ax.grid(True, axis='x', alpha=0.25)
for side in ('top', 'right', 'left'):
    ax.spines[side].set_visible(False)
ax.tick_params(axis='y', length=0)
ax.legend(loc='lower left', bbox_to_anchor=(0.0, 1.0), ncol=4, fontsize=9,
          frameon=False, handlelength=1.0, columnspacing=1.2, handletextpad=0.4)
ax.set_title('(b) the same $24$ numbers on one shared scale', pad=22)

basename = 'plot_radar_good'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what each panel lets the reader take off the page ---------------------------
i_top = int(order[-1])
print(f'\nlargest gap in the record: {attributes[i_top]}, control {S[0][i_top]:.1f} '
      f'against sample C {S[3][i_top]:.1f}, a gap of {gap[i_top]:.1f} points')
print('    panel (b) draws it as a length on a scale that starts at zero')
print(f'    panel (a) draws it as {gap[i_top] / SCALE_MAX:.0%} of a radius, and the '
      f'reader still has to compare two directions to find it')

print('\ngap against the control, by attribute, largest first:')
for i in order[::-1]:
    print(f'    {attributes[i]:12s} control {S[0][i]:.1f}   C {S[3][i]:.1f}   '
          f'gap {gap[i]:.1f}')

# zero-anchoring fixes the baseline; it does not make the area linear or the spoke
# order irrelevant, which is why (b) and not (a) is the form the text recommends.
a0, a3 = poly_area(S[0]), poly_area(S[3])
r_score = S[3].mean() / S[0].mean()
print(f'\npanel (a), still: sample C scores {r_score:.3f} of the control level and its '
      f'polygon covers {a3 / a0:.3f} of the area,')
print(f'    overstating the drop by a factor of '
      f'{(1 - a3 / a0) / (1 - r_score):.2f} even with the axis anchored at zero')
orders = [p for p in itertools.permutations(range(k)) if p[0] == 0 and p[1] < p[-1]]
areas = np.array([poly_area(S[3][list(p)]) for p in orders])
print(f'    over the {len(orders)} distinct spoke orderings the area still spans '
      f'{areas.min():.2f} to {areas.max():.2f}, a factor of {areas.max() / areas.min():.2f}')
