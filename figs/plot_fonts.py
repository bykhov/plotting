# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Type in a figure, shown at the size it will actually be printed at. This script is
# authored at its final width, so a point size set here is a point size on the page and
# the top row is the real thing rather than a rendering of it.
#
# The top row reads two ways at once. It is a ladder of label sizes, and it is the
# relation p_page = s * p_script drawn out: 8 pt on the page is what a 10 pt setting
# delivers once the figure has been authored at 1.25 times its final width, 7 pt at
# 1.43 times, 6 pt at 1.67 times.
#
# The three kinds of face are the companion figure, plot_faces.py.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from matplotlib.textpath import TextPath

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.sans-serif': ['Arial'],
    'font.monospace': ['Courier New'],
    'font.size': 10,
    'axes.titlesize': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'mathtext.fontset': 'cm',
})

PT_MM = 25.4 / 72.0                      # one typographic point, in millimetres
BASE_PT = 10.0                           # the point size a script would normally set
SIZES = [10.0, 8.0, 7.0, 6.0]
C_LINE = '#1E90FF'

rng = np.random.default_rng(11)
x = np.arange(0, 11)
y = 2.0 + 0.55 * x + 0.6 * rng.standard_normal(x.size)

fig = plt.figure(figsize=(6.0, 2.1))
top = fig.add_gridspec(1, 4, wspace=0.42)

# --- one panel, four label sizes, each also an authoring scale ---------------------
for j, pt in enumerate(SIZES):
    ax = fig.add_subplot(top[j])
    ax.plot(x, y, 'o-', ms=2.5, lw=1.0, color=C_LINE)
    ax.set_xlabel('index $n$', fontsize=pt)
    ax.set_ylabel('value', fontsize=pt)
    ax.tick_params(labelsize=pt)
    ax.set_xticks([0, 5, 10])
    ax.text(0.05, 0.88, '$R^2 = 0.91$', transform=ax.transAxes, fontsize=pt)
    s = pt / BASE_PT
    ax.set_title(f'({"abcd"[j]}) {pt:.0f} pt on the page\n'
                 f'$10$ pt at ${1 / s:.2f}\\times$ width')
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

basename = 'plot_fonts'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')


def glyph_box(ch, family, pt):
    """Bounding box of one glyph, in points, at the given size."""
    fp = FontProperties(family=family, size=pt)
    return TextPath((0, 0), ch, prop=fp, size=pt).get_extents()


# --- how large the label actually is on the page, and at what authoring scale ------
print('\n           cap height   vs the 2 mm scale   the same size as')
print('pt size    (mm)         of Sec. gridlines   10 pt authored at')
for pt in SIZES:
    cap = glyph_box('H', 'Times New Roman', pt).height * PT_MM
    print(f'{pt:5.0f}      {cap:5.2f}        {cap / 2.0:5.2f}x              '
          f'{BASE_PT / pt:.2f}x final width')
