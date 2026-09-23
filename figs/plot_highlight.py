# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The highlight budget. Twelve validation curves drawn twice, on identical axes:
# once with all twelve at full strength, and once with eleven dropped to light
# gray and one kept in a single strong color and labeled where it ends.
#
# The point is the pre-attentive pop of plot_preattentive.py. One strong mark on
# a gray page is found without a search, however many gray marks there are; a
# page on which every mark is strong has nothing to pop against, so finding the
# one under discussion becomes the serial task of plot_lookup.py.
#
# The gray of the context curves is the 20-40% ink range that plot_graycontrast.py
# panel (c) establishes for material that must be visible without competing.
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,          # the floor from the font section: a
    # 12-key legend is too big for the panel, and that is what (a) is showing
    'mathtext.fontset': 'cm',
})

rng = np.random.default_rng(11)
M, N = 12, 120
epoch = np.arange(1, N + 1)

# Twelve runs of one training setup: shared decay, individual rate and floor.
rate = rng.uniform(0.020, 0.075, M)
floor = rng.uniform(0.18, 0.52, M)
start = rng.uniform(1.35, 1.85, M)
curves = (floor[:, None]
          + (start[:, None] - floor[:, None]) * np.exp(-rate[:, None] * epoch)
          + rng.normal(0, 0.016, (M, N)))

HIGHLIGHT = 6                 # the run the surrounding text is about
CONTEXT_GRAY = '0.72'         # 28% ink: visible, does not compete
HIGHLIGHT_COLOR = '#0072B2'   # Okabe-Ito blue, the one strong color on the page
YLIM = (0.10, 1.95)

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8), sharey=True)

# --- (a) every curve at full strength: no curve is the subject ---
ax = axes[0]
cycle = plt.get_cmap('tab20')(np.linspace(0, 1, M, endpoint=False))
for i, c in enumerate(curves):
    ax.plot(epoch, c, lw=1.0, color=cycle[i], label=f'run {i + 1}')
ax.legend(ncol=2, loc='upper right', framealpha=0.9, handlelength=1.4,
          borderpad=0.3, labelspacing=0.25, columnspacing=0.9)
ax.set_title('(a) twelve runs, all at full strength')

# --- (b) eleven as context, one as the subject, labeled where it ends ---
ax = axes[1]
for i, c in enumerate(curves):
    if i == HIGHLIGHT:
        continue
    ax.plot(epoch, c, lw=0.8, color=CONTEXT_GRAY)
ax.plot(epoch, curves[HIGHLIGHT], lw=1.6, color=HIGHLIGHT_COLOR)
ax.text(epoch[-1] + 2, curves[HIGHLIGHT][-1], f'run {HIGHLIGHT + 1}',
        color=HIGHLIGHT_COLOR, va='center', ha='left', fontsize=9)
ax.set_title(f'(b) the same twelve, run {HIGHLIGHT + 1} highlighted')

for ax in axes:
    ax.set_xlim(0, N + 26)     # right margin holds the direct label of (b)
    ax.set_ylim(*YLIM)
    ax.set_xticks(np.arange(0, N + 1, 20))
    ax.set_xlabel('epoch')
    ax.grid(True, alpha=0.25)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
axes[0].set_ylabel('validation loss')

plt.tight_layout()

basename = 'plot_highlight'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')


def gray_level(rgb):
    """What a black and white print keeps: green counts about ten times blue."""
    rgb = np.asarray(rgb)
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


# --- what each panel spends its attention on ---
g_context = gray_level(mcolors.to_rgb(CONTEXT_GRAY))
g_high = gray_level(mcolors.to_rgb(HIGHLIGHT_COLOR))
g_cycle = gray_level(cycle[:, :3])

print(f'\n(b) context curves at gray {g_context:.2f}, which is '
      f'{100 * (1 - g_context):.0f}% ink, against the highlight at {g_high:.2f}, '
      f'{100 * (1 - g_high):.0f}% ink: a contrast of {g_context - g_high:.2f}')
print(f'(a) the twelve full-strength curves span gray {g_cycle.min():.2f} to '
      f'{g_cycle.max():.2f}, and {int((g_cycle < g_context).sum())} of {M} are '
      f'darker than the context gray of (b), so none of them recedes')
print(f'    legend keys needed: {M} in (a), 0 in (b)')
