# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The same six numbers, drawn with everything a plotting library will give away for
# free and then with only the marks that carry data. Nothing was removed from the
# data between the panels; what was removed is ink that encodes nothing.
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

C_BAR = '#1E90FF'
C_TEXT = '#3A3F44'
JUNK = ['#d62728', '#2ca02c', '#9467bd', '#ff7f0e', '#8c564b', '#17becf']

models = ['Ridge', 'k-NN', 'SVM', 'Random forest', 'Gradient boosting', 'MLP']
f1 = np.array([0.71, 0.74, 0.79, 0.83, 0.86, 0.80])

fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.4))

# --- (a) the default, plus every decoration the library offers ---
ax = axes[0]
ax.set_facecolor('#EDEDED')
bars = ax.bar(models, f1, color=JUNK, edgecolor='black', linewidth=1.2,
              hatch='//', width=0.75)
ax.grid(True, which='both', color='white', lw=1.2)
ax.set_axisbelow(True)
ax.set_ylim(0, 1.0)
ax.set_ylabel('F1 score')
ax.set_title('(a) 6 numbers, a lot of ink')
ax.set_xticks(np.arange(len(models)))
ax.set_xticklabels(models, rotation=45, ha='right')
# The 6 pt legend is deliberate: an unreadable legend is part of the specimen.
ax.legend(bars, models, fontsize=6, ncol=2, loc='upper left', framealpha=1.0)

# --- (b) sorted, direct-labeled, horizontal so the names read straight ---
ax = axes[1]
order = np.argsort(f1)
pos = np.arange(len(models))
ax.barh(pos, f1[order], height=0.65, color=C_BAR)
for p, v, name in zip(pos, f1[order], np.array(models)[order]):
    ax.text(v + 0.012, p, f'{v:.2f}', va='center', fontsize=9, color=C_TEXT)
ax.set_yticks(pos)
ax.set_yticklabels(np.array(models)[order])
ax.set_xlim(0, 1.0)
ax.set_xlabel('F1 score')
ax.set_title('(b) the same 6 numbers')
ax.tick_params(axis='y', length=0)
for side in ('top', 'right', 'left'):
    ax.spines[side].set_visible(False)

plt.tight_layout()

basename = 'plot_declutter'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print('models: ' + ', '.join(f'{m} {v:.2f}' for m, v in zip(models, f1)))
print('panel (a) encodes the model name three times over: x tick, bar color, legend')
