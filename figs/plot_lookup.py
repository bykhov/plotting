# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# One set of twenty values, drawn twice, differing only in the order of the rows.
# Alphabetical order serves table look-up: the reader knows where a named country is
# before searching. Value order serves pattern perception: the shape of the
# distribution is there without being looked for. No panel does both.
# After the example in Cleveland, The Elements of Graphing Data (1985; rev. 1994).
#
# Data: United Nations, World Population Prospects, 2024 revision, mid-2023 estimates,
# in millions. Retrieved 2026-08-10 from the UN-sourced table at
# https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'mathtext.fontset': 'cm',
})

C_MARK = '#1E90FF'
C_LEAD = '0.80'

# One vintage for all twenty, so the ranking is internally consistent.
population = {
    'Bangladesh':    171.5,
    'Brazil':        211.1,
    'China':        1422.6,
    'DR Congo':      105.8,
    'Egypt':         114.5,
    'Ethiopia':      128.7,
    'Germany':        84.5,
    'India':        1438.1,
    'Indonesia':     281.2,
    'Iran':           90.6,
    'Japan':         124.4,
    'Mexico':        129.7,
    'Nigeria':       227.9,
    'Pakistan':      247.5,
    'Philippines':   114.9,
    'Russia':        145.4,
    'Thailand':       71.7,
    'Turkey':         87.3,
    'United States': 343.5,
    'Vietnam':       100.4,
}

alpha_names = sorted(population)                       # already the dict order, made explicit
alpha_vals = np.array([population[n] for n in alpha_names])
order = np.argsort(alpha_vals)                         # ascending, so the largest ends up on top
sort_names = [alpha_names[i] for i in order]
sort_vals = alpha_vals[order]

fig, axes = plt.subplots(1, 2, figsize=(7.0, 4.0), sharex=True)

panels = [
    (axes[0], alpha_names[::-1], alpha_vals[::-1], '(a) alphabetical: made for look-up'),
    (axes[1], sort_names, sort_vals, '(b) sorted by value: made for pattern'),
]

XMAX = 1550
for ax, names, vals, title in panels:
    pos = np.arange(len(names))                        # row 0 at the bottom, so reverse above
    ax.hlines(pos, 0, vals, colors=C_LEAD, lw=0.7, linestyles=(0, (1, 2)))
    ax.plot(vals, pos, 'o', ms=4, mfc='none', mec=C_MARK, mew=1.1, linestyle='none')
    ax.set_yticks(pos)
    ax.set_yticklabels(names)
    ax.set_ylim(-0.7, len(names) - 0.3)
    ax.set_xlim(0, XMAX)
    ax.set_xlabel('Population (millions)')
    ax.set_title(title)
    ax.tick_params(axis='y', length=0)
    ax.grid(True, axis='x', alpha=0.25)
    ax.set_axisbelow(True)
    for side in ('top', 'right', 'left'):
        ax.spines[side].set_visible(False)

plt.tight_layout()

basename = 'plot_lookup'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
# The two numbers the caption quotes: the gap panel (b) shows and (a) hides.
top2, third = sort_vals[-2], sort_vals[-3]
print(f'{len(alpha_names)} countries, {sort_vals.min():.1f} to {sort_vals.max():.1f} million')
print(f'gap: 3rd = {third:.1f}, 2nd = {top2:.1f}, ratio = {top2 / third:.2f}')
print(f'rows a reader scans to find one named country: 1 in (a), up to {len(alpha_names)} in (b)')
