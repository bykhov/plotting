# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The two ways transparency is misused, each with the fix beside it. (a) is what happens
# when two categorical colors are given alpha and allowed to overlap: the intersection is a
# third color that appears in neither key, and which of the two mixtures it is depends on the
# draw order. (b) is the same two regions with no alpha anywhere: both classes filled solid,
# and the area they share carrying one fill under the other class color as a hatch, so every
# color on the page is a color in the key, the shared area is still visible, and the draw
# order cannot change anything.
# (c) and (d) are the same twenty context series behind one highlighted one,
# once at low alpha, where every crossing darkens and reads as structure, and once in a solid
# light gray, where the context is uniform and the crossings say nothing.
#
# Every number the caption quotes is printed at the end.
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Rectangle
from matplotlib.colors import to_rgb, to_hex

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 10,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'mathtext.fontset': 'cm',
    'hatch.linewidth': 0.6,                # fine enough to stay a texture at 10 pt text size
})

PT = 9
C_NOTE = '#B03A2E'
C_A = '#1F77B4'
C_B = '#D95F02'
A_REGION = 0.5                             # the opacity the two regions in (a) are given
# Panels (c) and (d) are matched on purpose: black at A_CONTEXT, which is the idiom the
# libraries invite, composites over white to exactly C_GRAY, the solid gray of (d). One
# context line is therefore identical in the two panels and every difference is a crossing.
# C_GRAY lands at 30% ink, inside the 20 to 40% band the one-strong-color section asks for.
#
# (b) uses no alpha at all: the fill is the solid color that (a) only reaches by compositing,
# so the two panels put the same blue on the page and only (b) can name it in a key. The
# shared area is B hatched and clipped to A, which is a third key entry rather than a third
# color, and unlike a mixture it does not depend on which region was drawn first.
HATCH = '///'
A_CONTEXT = 0.30
C_CTX = 'black'


def ink(alpha, n):
    """Ink accumulated by n marks of opacity alpha stacked at one spot."""
    return 1.0 - (1.0 - alpha) ** n


def over(top, bottom, alpha):
    """The color of a mark of opacity alpha composited over a background."""
    t, b = np.array(to_rgb(top)), np.array(to_rgb(bottom))
    return alpha * t + (1.0 - alpha) * b


C_GRAY = to_hex(over(C_CTX, 'white', A_CONTEXT))
# the tints (a) reaches by compositing, used as plain solid colors in (b)
C_A_SOLID = to_hex(over(C_A, 'white', A_REGION))
C_B_SOLID = to_hex(over(C_B, 'white', A_REGION))


fig = plt.figure(figsize=(6.8, 2.25))
gs = fig.add_gridspec(1, 4, width_ratios=[1.0, 1.0, 0.92, 0.92], wspace=0.34,
                      left=0.015, right=0.995, top=0.87, bottom=0.19)


def regions(ax, title):
    """The two class regions and the key above them, shared by (a) and (b)."""
    ax.text(-0.72, 0.0, 'A', ha='center', va='center', fontsize=PT)
    ax.text(0.72, 0.0, 'B', ha='center', va='center', fontsize=PT)
    ax.text(-1.06, 0.96, 'the key:', fontsize=PT, color='0.35')
    ax.set_xlim(-1.15, 1.15)
    ax.set_ylim(-1.05, 1.15)
    ax.set_aspect('equal')
    ax.set_anchor('N')        # an equal-aspect box shrinks: pin it so the titles line up
    ax.axis('off')
    ax.set_title(title)


def key_box(ax, k, name, step=0.44, **kw):
    """One legend swatch and its label, drawn the way a legend draws them: over nothing."""
    ax.add_patch(Rectangle((-1.06 + step * k, 0.74), 0.20, 0.15, **kw))
    ax.text(-0.82 + step * k, 0.815, name, ha='left', va='center', fontsize=PT)


# --- (a) two keys, three colors ---------------------------------------------------
ax = fig.add_subplot(gs[0, 0])
ax.add_patch(Ellipse((-0.32, 0.0), 1.35, 1.05, facecolor=C_A, alpha=A_REGION,
                     edgecolor='none'))
ax.add_patch(Ellipse((0.32, 0.0), 1.35, 1.05, facecolor=C_B, alpha=A_REGION,
                     edgecolor='none'))
for k, (c, name) in enumerate(((C_A, 'A'), (C_B, 'B'))):
    key_box(ax, k, name, facecolor=c, alpha=A_REGION, edgecolor='none')
ax.annotate('in neither key', xy=(0.0, -0.20), xytext=(0.0, -0.86), ha='center',
            fontsize=PT, color=C_NOTE,
            arrowprops=dict(arrowstyle='-', lw=0.7, color=C_NOTE, shrinkA=2, shrinkB=2))
regions(ax, rf'(a) both at $\alpha = {A_REGION:g}$')

# --- (b) the same two regions, no alpha anywhere ----------------------------------
# Both classes filled solid at full opacity, and the area they share is B hatched and clipped
# to A. Nothing is composited, so every color on the page is a color in the key, the shared
# area is still visible, and it is a key entry rather than a mixture the draw order decides.
ax = fig.add_subplot(gs[0, 1])
ax.add_patch(Ellipse((0.32, 0.0), 1.35, 1.05, facecolor=C_B_SOLID, edgecolor='none'))
a_ell = Ellipse((-0.32, 0.0), 1.35, 1.05, facecolor=C_A_SOLID, edgecolor='none')
ax.add_patch(a_ell)
shared = Ellipse((0.32, 0.0), 1.35, 1.05, facecolor='none', edgecolor=C_B, hatch=HATCH, lw=0)
ax.add_patch(shared)
shared.set_clip_path(a_ell)          # the hatch stops exactly at A's boundary
# Each region outlined in its own key color at full strength. The two arcs that bound the
# shared area belong one to each region, so this is also what gives the overlap an edge.
for xc, edge in ((-0.32, C_A), (0.32, C_B)):
    ax.add_patch(Ellipse((xc, 0.0), 1.35, 1.05, facecolor='none', edgecolor=edge, lw=1.0))
key_box(ax, 0, 'A', step=0.42, facecolor=C_A_SOLID, edgecolor=C_A, lw=1.0)
key_box(ax, 1, 'B', step=0.42, facecolor=C_B_SOLID, edgecolor=C_B, lw=1.0)
key_box(ax, 2, 'both', step=0.42, facecolor=C_A_SOLID, edgecolor=C_B, hatch=HATCH, lw=1.0)
ax.annotate('in the key', xy=(0.0, -0.20), xytext=(0.0, -0.86), ha='center',
            fontsize=PT, color='0.35',
            arrowprops=dict(arrowstyle='-', lw=0.7, color='0.35', shrinkA=2, shrinkB=2))
regions(ax, '(b) solid fills, hatched overlap')

# --- (c) and (d) the same context, de-emphasized two ways -------------------------
# Twenty runs of one training job, converging as runs do, with one of them the subject.
# The convergence is where the lines bunch, and it is the region alpha turns into a bar.
rng = np.random.default_rng(5)
YLIM_C = (0.12, 1.05)
ep = np.linspace(0, 40, 400)
N_CTX = 20
CTX = np.array([p + a * np.exp(-ep / tau)
                for p, a, tau in zip(rng.uniform(0.20, 0.34, N_CTX),
                                     rng.uniform(0.55, 0.70, N_CTX),
                                     rng.uniform(4.0, 11.0, N_CTX))])
HL = 0.165 + 0.66 * np.exp(-ep / 7.5)

for k, (col, alpha, title) in enumerate(
        ((C_CTX, A_CONTEXT, rf'(c) black at $\alpha = {A_CONTEXT:g}$'),
         (C_GRAY, 1.0, r'(d) solid gray, $30\%$ ink'))):
    ax = fig.add_subplot(gs[0, 2 + k])
    for row in CTX:
        ax.plot(ep, row, '-', lw=0.9, color=col, alpha=alpha)
    ax.plot(ep, HL, '-', lw=1.3, color=C_NOTE)
    ax.set_xlim(0, 40)
    ax.set_ylim(*YLIM_C)
    ax.set_yticks([0.2, 0.6, 1.0])
    ax.set_xticks([0, 20, 40])
    if k == 1:
        ax.set_yticklabels([])
    else:
        ax.set_ylabel('validation loss', labelpad=2)
    ax.set_xlabel('epoch', labelpad=1)
    ax.set_title(title)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)

# how many context lines meet at the worst crossing, at the width they are drawn
fig.canvas.draw()
bb = fig.axes[-1].get_window_extent().transformed(fig.dpi_scale_trans.inverted())
band = 0.9 * (YLIM_C[1] - YLIM_C[0]) / (bb.height * 72.0)   # one line width, in data units
k_max = int(max(np.max(np.histogram(col_y, bins=np.arange(*YLIM_C, band))[0])
                for col_y in CTX.T))

basename = 'plot_alpha_misuse'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

mix_ab = over(C_B, over(C_A, 'white', A_REGION), A_REGION)   # B drawn over A
mix_ba = over(C_A, over(C_B, 'white', A_REGION), A_REGION)   # A drawn over B
print(f'(a) key colors {C_A} and {C_B}; over white at alpha {A_REGION:g} they render as '
      f'{to_hex(over(C_A, "white", A_REGION))} and {to_hex(over(C_B, "white", A_REGION))}')
print(f'(a) the intersection is {to_hex(mix_ab)} with B on top and {to_hex(mix_ba)} '
      f'with A on top, neither of them in the key')
print(f'(b) the same regions with no alpha: A solid {C_A_SOLID} outlined {C_A}, B solid '
      f'{C_B_SOLID} outlined {C_B}, the shared area {C_A_SOLID} under a {C_B} "{HATCH}" hatch '
      f'clipped to A and bounded by one arc of each outline, so the key names all three')
print(f'(c) context {C_CTX} at alpha {A_CONTEXT:g} renders as {C_GRAY}, which is the '
      f'solid gray of (d), so one line is identical in the two panels')
print(f'(c) at most {k_max} context lines meet within one line width, so the worst '
      f'crossing carries {ink(A_CONTEXT, k_max):.2f} of full ink against '
      f'{A_CONTEXT:.2f} for a lone line, a factor of '
      f'{ink(A_CONTEXT, k_max) / A_CONTEXT:.1f}')
for j in (2, 3):
    print(f'(c) {j} lines crossing render as '
          f'{to_hex(1 - ink(A_CONTEXT, j) * (1 - np.array(to_rgb(C_CTX))))} '
          f'against {C_GRAY} for one')
