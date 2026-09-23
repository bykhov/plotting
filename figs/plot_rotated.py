# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Rotation, isolated. The six F1 scores of plot_declutter, drawn twice in one figure of
# fixed height, with nothing changed between the panels but the direction the bars run
# and the angle of the names. (a) is what a library does when long category names do not
# fit: it tilts them, and the tilted block takes its height out of the panel. (b) turns
# the chart on its side, which pays for the same names out of the left margin and leaves
# the bars the full height, with the names upright and the values printed at the ends.
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

MM = 25.4
C_BAR = '#1E90FF'

# the record of plot_declutter, so the two figures are visibly the same six numbers
models = ['Ridge', 'k-NN', 'SVM', 'Random forest', 'Gradient boosting', 'MLP']
f1 = np.array([0.71, 0.74, 0.79, 0.83, 0.86, 0.80])

# Both panels are given the same figure box and the same top edge, and each is then
# allowed exactly the margin its own labels need: the tilted block of (a) is 18 mm of
# height, the upright names of (b) are 23 mm of width. What is left over is the bars,
# and that difference is the whole point of the figure, so the axes are placed in inches
# rather than by a shared grid that would hand both panels the same margins.
FIG_W, FIG_H = 7.0, 2.6
fig = plt.figure(figsize=(FIG_W, FIG_H))


def place(left_in, bottom_in, width_in, top_in=0.32):
    return fig.add_axes([left_in / FIG_W, bottom_in / FIG_H, width_in / FIG_W,
                         (FIG_H - bottom_in - top_in) / FIG_H])


axes = [place(0.55, 0.80, 2.55),      # (a) 0.80 in below the axes for the tilted names
        place(4.55, 0.42, 2.30)]      # (b) the names go to the left instead

# --- (a) the names tilted to fit, which spends panel height on them ---------------
ax = axes[0]
ax.bar(models, f1, width=0.65, color=C_BAR)
ax.set_xticks(np.arange(len(models)))
ax.set_xticklabels(models, rotation=45, ha='right')
ax.set_ylim(0, 1.0)
ax.set_ylabel('$F_1$ score')
ax.set_title('(a) names rotated to fit')

# --- (b) the same numbers on their side, names upright in the margin --------------
ax = axes[1]
order = np.argsort(f1)                                # sorted, Sec. sec-app-plot-dataink
ax.barh(np.arange(len(f1)), f1[order], height=0.65, color=C_BAR)
for j, v in enumerate(f1[order]):
    ax.text(v + 0.015, j, f'{v:.2f}', va='center', fontsize=9)
ax.set_yticks(np.arange(len(f1)))
ax.set_yticklabels([models[j] for j in order])
ax.set_xlim(0, 1.0)
ax.set_xlabel('$F_1$ score')
ax.set_title('(b) the chart turned on its side')

for ax in axes:
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
axes[1].tick_params(axis='y', length=0)    # the names sit against the bars themselves
axes[0].grid(True, axis='y', alpha=0.25)
axes[1].grid(True, axis='x', alpha=0.25)

basename = 'plot_rotated'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- what the rotation costs, in millimetres on the printed page ------------------
fig.canvas.draw()
r = fig.canvas.get_renderer()


def mm_w(ext):
    return ext.width / fig.dpi * MM


def mm_h(ext):
    return ext.height / fig.dpi * MM


longest = max(models, key=len)
print(f'{len(models)} names, the longest "{longest}" at {len(longest)} characters')

for name, ax, axis in [('(a)', axes[0], 'x'), ('(b)', axes[1], 'y')]:
    labels = (ax.get_xticklabels() if axis == 'x' else ax.get_yticklabels())
    exts = [t.get_window_extent(renderer=r) for t in labels]
    block_h = max(mm_h(e) for e in exts)
    block_w = max(mm_w(e) for e in exts)
    panel = ax.get_window_extent()
    print(f'  {name} panel {mm_w(panel):.1f} x {mm_h(panel):.1f} mm; '
          f'the name block is {block_w:.1f} mm wide and {block_h:.1f} mm tall')

# what each figure spends on the names, as a share of the figure it is drawn in
fig_h_mm = fig.get_figheight() * MM
fig_w_mm = fig.get_figwidth() * MM
a_block = max(mm_h(t.get_window_extent(renderer=r)) for t in axes[0].get_xticklabels())
b_block = max(mm_w(t.get_window_extent(renderer=r)) for t in axes[1].get_yticklabels())
print(f'\n(a) spends {a_block:.1f} mm of the {fig_h_mm:.1f} mm figure height on the '
      f'names, which is {a_block / fig_h_mm:.0%} of it, and it comes out of the bars')
print(f'(b) spends {b_block:.1f} mm of the {fig_w_mm / 2:.1f} mm panel width on the same '
      f'names, which is margin, and the bars keep the full height')
print(f'bar height: {mm_h(axes[0].get_window_extent()):.1f} mm in (a) against '
      f'{mm_h(axes[1].get_window_extent()):.1f} mm in (b)')
