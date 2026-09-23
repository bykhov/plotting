# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Table or figure, in both directions.
# (a) Four hyperparameters drawn as bars on one axis: they share no unit and span five
#     orders of magnitude, so two bars vanish and the other two cannot be read exactly.
#     They belong in a four-row table.
# (b) Training and validation loss over 30 epochs: the question is where validation
#     stops improving, which is a shape, so it belongs in a figure. The same numbers as
#     a table hide the minimum among fifteen similar rows.
# The script prints the LaTeX rows of that table, so the table and the curve cannot drift.
import numpy as np
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 10,
    'axes.labelsize': 10,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'mathtext.fontset': 'cm',
})

C_TRAIN = '#999999'
C_VAL = '#1E90FF'
C_TEXT = '#3A3F44'

# --- data ---
names = ['Learning rate', 'Batch size', 'Epochs', 'Dropout']
values = np.array([3e-4, 64, 30, 0.1])

rng = np.random.default_rng(7)
epoch = np.arange(1, 31)
train = 0.22 + 1.10 * np.exp(-epoch / 6.0) + rng.normal(0, 0.004, epoch.size)
val = 0.33 + 1.00 * np.exp(-epoch / 5.0) + 0.00045 * epoch**2 \
    + rng.normal(0, 0.006, epoch.size)
best = int(np.argmin(val))

fig, axes = plt.subplots(1, 2, figsize=(7.0, 2.8),
                         gridspec_kw={'width_ratios': [1, 1.4]})

# --- (a) counterexample: four unrelated settings as bars ---
ax = axes[0]
pos = np.arange(len(names))
ax.bar(pos, values, width=0.6, color=C_VAL)
ax.set_xticks(pos)
ax.set_xticklabels(names, rotation=30, ha='right')
ax.set_ylabel('Value')
ax.set_title('(a) Four settings on one axis')
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)

# --- (b) example: the loss curves, minimum marked ---
ax = axes[1]
ax.plot(epoch, train, color=C_TRAIN, lw=1.5)
ax.plot(epoch, val, color=C_VAL, lw=1.8)
ax.plot(epoch[best], val[best], 'o', color=C_VAL, ms=5)
ax.annotate(f'minimum, epoch {epoch[best]}', (epoch[best], val[best]),
            xytext=(epoch[best] + 4, 0.85), ha='center', fontsize=10, color=C_TEXT,
            arrowprops=dict(arrowstyle='-', color=C_TEXT, lw=0.6, shrinkB=4))
ax.text(epoch[-1] + 0.5, train[-1], 'training', va='center', color=C_TRAIN)
ax.text(epoch[-1] + 0.5, val[-1], 'validation', va='center', color=C_VAL)
ax.set_xlim(0, 36)
ax.set_xticks([0, 10, 20, 30])
ax.set_xlabel('Epoch')
ax.set_ylabel('Loss')
ax.set_title('(b) Loss per epoch')
for side in ('top', 'right'):
    ax.spines[side].set_visible(False)

plt.tight_layout()

basename = 'plot_table_or_figure'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')
print(f'validation minimum: epoch {epoch[best]}, loss {val[best]:.3f}')
print('LaTeX rows for the loss table (every second epoch):')
for e, t, v in zip(epoch[1::2], train[1::2], val[1::2]):
    print(f'\t\t{e} & {t:.3f} & {v:.3f} \\\\')
