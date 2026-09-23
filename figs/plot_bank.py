# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Why the banking target is 45 degrees and not some other angle. One three-point series
# whose two segments differ by a factor of two in slope, which is the change in trend a
# reader is asked to detect. Banking is a vertical scale on that same series, so the data
# never changes and only the angles the page delivers do. (a) shows the change vanishing at
# a shallow and at a steep banking and standing out in between; (b) is the reason, the
# angular separation the eye is given, which peaks where the two segments straddle 45.
# Notation follows the text: beta is the page scale ratio that turns a data slope into an
# angle, and panel (b) plots the separation of the two segment angles against beta's own
# angle, arctan(beta m*).
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

PT = 9
C_LINE = '#1E90FF'
C_GUIDE = '0.45'

X = np.array([0.0, 1.0, 2.0])
Y = np.array([0.0, 1.0, 3.0])        # segment slopes 1 and 2: one doubling of slope
RATIO = 2.0
TARGETS = [10.0, 45.0, 80.0]         # banking of the typical segment, in degrees
CENTERS = [0.0, 1.35, 2.70]


def beta_for(target_deg):
    """The page scale ratio beta that puts the typical segment at the target angle.

    The typical slope is the geometric mean of the two, m* = sqrt(1 * 2), and banking it
    to an angle t means beta m* = tan(t), so beta = tan(t) / sqrt(2).
    """
    return np.tan(np.radians(target_deg)) / np.sqrt(RATIO)


def angles(beta):
    """The two segment angles the page delivers at scale ratio beta, in degrees."""
    return np.degrees(np.arctan(beta)), np.degrees(np.arctan(RATIO * beta))


fig = plt.figure(figsize=(6.8, 2.5))
gs = fig.add_gridspec(1, 2, width_ratios=[1.32, 1], wspace=0.22,
                      left=0.02, right=0.97, top=0.90, bottom=0.17)

# --- (a) one slope change, banked three ways --------------------------------------
# Each copy is banked by its own scale and then scaled uniformly to a common size. A
# uniform scale changes no angle, so the comparison is untouched and the three stay
# legible at one figure size.
ax = fig.add_subplot(gs[0, 0])
for target, cx in zip(TARGETS, CENTERS):
    beta = beta_for(target)
    pts = np.column_stack([X, beta * Y])
    span = pts.max(axis=0) - pts.min(axis=0)
    pts = (pts - pts.mean(axis=0)) / np.hypot(*span)          # common bounding diagonal
    ax.plot(pts[:, 0] + cx, pts[:, 1], '-o', lw=1.4, ms=3, color=C_LINE)
    lo, hi = angles(beta)
    ax.text(cx, 0.70, rf'banked at ${target:.0f}^{{\circ}}$', ha='center', va='center',
            fontsize=PT)
    ax.text(cx, -0.70, rf'${lo:.1f}^{{\circ}}$ and ${hi:.1f}^{{\circ}}$',
            ha='center', va='center', fontsize=PT, color=C_GUIDE)
    ax.text(cx, -0.88, rf'apart by ${hi - lo:.1f}^{{\circ}}$', ha='center', va='center',
            fontsize=PT, color=C_GUIDE)
ax.set_xlim(-0.75, 3.45)
ax.set_ylim(-1.02, 0.86)
ax.set_aspect('equal')
ax.axis('off')
ax.set_title('(a) the same doubling of slope, banked three ways')

# --- (b) the separation the eye is given, against the banking ---------------------
ax = fig.add_subplot(gs[0, 1])
t = np.linspace(0.5, 89.5, 600)
lo, hi = angles(beta_for(t))
sep = hi - lo
ax.plot(t, sep, '-', lw=1.4, color=C_LINE)
ax.axvline(45, ls='--', lw=0.9, color=C_GUIDE)
for target in TARGETS:
    beta = beta_for(target)
    d = np.diff(angles(beta))[0]
    ax.plot(target, d, 'o', ms=5, color=C_LINE)
    ax.annotate(rf'${d:.1f}^{{\circ}}$', (target, d), textcoords='offset points',
                xytext=(0, 8) if target == 45 else (7, -1),
                ha='center' if target == 45 else 'left', fontsize=PT)
ax.set_xlim(0, 90)
ax.set_ylim(0, 23)
ax.set_xticks([0, 15, 30, 45, 60, 75, 90])
ax.set_xlabel(r'banking of the typical segment, $^{\circ}$')
ax.set_ylabel(r'separation of the two, $^{\circ}$')
ax.set_title('(b) how far apart the two segments read')
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)
ax.grid(True, alpha=0.25)

basename = 'plot_bank'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

for target in TARGETS:
    beta = beta_for(target)
    p, q = angles(beta)
    print(f'banked at {target:4.1f} deg: beta {beta:6.3f}, segments {p:5.1f} and '
          f'{q:5.1f} deg, apart by {q - p:5.1f} deg')
k = int(np.argmax(sep))
print(f'separation peaks at {sep[k]:.1f} deg, with the typical segment at {t[k]:.1f} deg')
print(f'the stretch in beta from {TARGETS[0]:.0f} to {TARGETS[1]:.0f} deg is '
      f'{beta_for(TARGETS[1]) / beta_for(TARGETS[0]):.1f} times')
# how forgiving the rule is: where the separation stays within a tenth of its peak
wide = t[sep >= 0.9 * sep[k]]
print(f'within a tenth of the peak for banking between {wide[0]:.0f} and '
      f'{wide[-1]:.0f} deg')
