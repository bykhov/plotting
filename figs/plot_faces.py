# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The difference between the three kinds of face, measured rather than asserted, and
# drawn at the size it is printed at so the specimens are the real thing.
#
# The usual claim - that monospace is what makes a column of numbers line up - is
# wrong, and the figure shows why: digits are drawn to one width in text faces too, so
# the number rows align in all three columns. What monospace adds is that the letters
# and the punctuation share that width as well, which is why the i and m rows end
# together in one column and nowhere else.
#
# This was panel (e) of plot_fonts.py, which is now the size ladder alone.
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import matplotlib.font_manager as fm
from matplotlib.ft2font import FT2Font

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.sans-serif': ['Arial'],
    'font.monospace': ['Courier New'],
    'font.size': 10,
    'axes.titlesize': 9,
    'mathtext.fontset': 'cm',
})

FACES = [('serif', 'Times New Roman'), ('sans-serif', 'Arial'),
         ('monospace', 'Courier New')]
NARROW, WIDE = 'iiiiiiii', 'mmmmmmmm'        # eight of the thinnest and widest letter
COLUMN = ['1.11', '88.88']                   # digits, to show they align everywhere
SPECIMEN_PT = 9

# Two guides per column: the letters are set from the left one and the numbers back
# from the right one, so both alignments are judged against a drawn line rather than
# against the reader's eye.
fig = plt.figure(figsize=(6.0, 1.75))
ax = fig.add_axes([0.0, 0.0, 1.0, 1.0])
ax.set_xlim(-0.62, 3.0)
ax.set_ylim(0.02, 1.0)
ax.axis('off')

for j, (family, name) in enumerate(FACES):
    x0, x1 = j + 0.12, j + 0.88
    ax.plot([x0, x0], [0.10, 0.74], '-', lw=0.6, color='0.75', zorder=0)
    ax.plot([x1, x1], [0.10, 0.40], '-', lw=0.6, color='0.75', zorder=0)
    ax.text(x0, 0.92, f'{family}: {name}', family=family, fontsize=9,
            ha='left', va='center', color='0.35')
    for i, s in enumerate((NARROW, WIDE)):
        ax.text(x0, 0.68 - 0.14 * i, s, family=family, fontsize=SPECIMEN_PT,
                ha='left', va='center')
    for i, num in enumerate(COLUMN):
        ax.text(x1, 0.34 - 0.14 * i, num, family=family, fontsize=SPECIMEN_PT,
                ha='right', va='center')

# The two claims, named where they are made, so the figure says what each pair of rows
# is for without a caption.
ax.text(-0.02, 0.61, 'letters,\nset from the left', fontsize=9, ha='right',
        va='center', color='0.35', linespacing=1.3)
ax.text(-0.02, 0.27, 'numbers,\nset from the right', fontsize=9, ha='right',
        va='center', color='0.35', linespacing=1.3)

basename = 'plot_faces'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')


# --- what makes a monospace face monospace, in advance widths ---------------------
# The advance width is the space a character claims, which is what decides whether two
# strings end at the same place. It is not the width of the ink.
def advance(ch, name, pt=10.0):
    font = FT2Font(fm.findfont(FontProperties(family=name)))
    font.set_size(pt, 72)
    return font.load_char(ord(ch)).linearHoriAdvance / 65536.0


print('\nadvance width at 10 pt, in points')
print('face                        i      m     i/m       1      8     1/8')
for family, name in FACES:
    wi, wm = advance('i', name), advance('m', name)
    d1, d8 = advance('1', name), advance('8', name)
    print(f'{family:10s} {name:15s} {wi:5.2f}  {wm:5.2f}   {wi / wm:.2f}    '
          f'{d1:5.2f}  {d8:5.2f}    {d1 / d8:.2f}')
print('so the digits are one width in every face, and the number rows align in all '
      'three;\nonly the monospace face gives the letters that width too, which is the '
      'i and m rows.')
