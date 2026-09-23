# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The gridline result, as a case to recognize rather than as the conditions it was
# measured under. One series on a 0 to 100 scale, the two values a reader is asked to
# compare marked in both panels, and one panel size throughout, so the ruling is the
# only thing that changes. (a) is what a library hands back and what the reader then
# has to interpolate against. (b) is the same panel ruled every 20 units, which at this
# size is 4.2 mm, comfortably above the 8 px the eye needs to keep two lines apart.
#
# The panels are positioned in inches and converted at 96 px per inch, so the height and
# the gridline separation printed below are the ones on the printed page.
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

PPI = 96.0                       # pixels per inch, the rendering the result assumes
MM = 25.4
LIMIT_PX = 8.0                   # the separation below which a ruling stops helping
C_LINE = '#1E90FF'
C_FRAME = '0.45'
C_GRID = '0.75'

y = np.array([30, 52, 45, 71, 58, 78, 66, 62, 84, 74], dtype=float)
x = np.arange(y.size)
MARK = (3, 6)                    # the two values a reader is asked to compare: 71 and 66

HEIGHT_PX = 80                   # one panel size for both panels
STEP = 20                        # units of the 0 to 100 scale, in (b)

FIG_W, FIG_H = 4.6, 2.0
fig = plt.figure(figsize=(FIG_W, FIG_H))


def panel(left_in, bottom_in, width_in, height_px, step=None):
    """One panel, placed and sized in inches. The frame is kept because in this figure
    it is what shows the panel size."""
    h_in = height_px / PPI
    ax = fig.add_axes([left_in / FIG_W, bottom_in / FIG_H, width_in / FIG_W, h_in / FIG_H])
    ax.plot(x, y, '-', lw=1.1, color=C_LINE)
    ax.plot(x[list(MARK)], y[list(MARK)], 'o', ms=3.4, color='black')
    ax.set_xlim(-0.4, y.size - 0.6)
    ax.set_ylim(0, 100)
    ax.set_xticks([])
    ax.set_yticks([0, 50, 100])
    ax.tick_params(axis='y', length=2, pad=1.5)
    for s in ax.spines.values():
        s.set_color(C_FRAME)
        s.set_linewidth(0.8)
    if step is not None:
        ax.set_yticks(np.arange(0, 101, step), minor=True)
        ax.grid(True, axis='y', which='minor', color=C_GRID, lw=0.5)
    return ax, h_in


L, W, GAP = 0.45, 1.75, 0.60
BOTTOM = 0.52

ax_a, h_in = panel(L, BOTTOM, W, HEIGHT_PX)
ax_b, _ = panel(L + W + GAP, BOTTOM, W, HEIGHT_PX, step=STEP)

sep_mm = STEP / 100 * h_in * MM
for cx, title, sub in [(L + W / 2, '(a) no gridlines',
                        'every value is interpolated'),
                       (L + W + GAP + W / 2, f'(b) ruled every {STEP} units',
                        f'lines {sep_mm:.1f} mm apart')]:
    fig.text(cx / FIG_W, (BOTTOM + h_in + 0.06) / FIG_H, title, ha='center', va='bottom',
             fontsize=10)
    fig.text(cx / FIG_W, (BOTTOM - 0.06) / FIG_H, sub, ha='center', va='top', fontsize=9)

basename = 'plot_gridsize'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- the numbers the caption quotes -----------------------------------------------
print(f'series of {y.size} values on a 0 to 100 scale; the marked pair is '
      f'{y[MARK[0]]:.0f} and {y[MARK[1]]:.0f}, which differ by '
      f'{y[MARK[0]] - y[MARK[1]]:.0f} units')
print(f'both panels {HEIGHT_PX} px tall at {PPI:.0f} px per inch, that is '
      f'{HEIGHT_PX / PPI * MM:.1f} mm')
print(f'(b) ruled every {STEP} units, which is {sep_mm:.2f} mm, against the '
      f'{LIMIT_PX:.0f} px limit of {LIMIT_PX / PPI * MM:.2f} mm')
print('for reference, on this panel a ruling every:')
for step in (100, 50, 20, 10, 5):
    sep = step / 100 * h_in * MM
    flag = '  <-- below the limit' if sep < LIMIT_PX / PPI * MM else ''
    print(f'    {step:3d} units is {sep:5.2f} mm{flag}')
