# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# Two ways of changing one color, each shown as the reader sees it and again as the
# gray a black and white print leaves. The two are the saturation and the value axes
# of HSV: washing a color out changes the gray a little and not in a way anyone can
# rank; taking it from dark to light changes the gray over the full range, which is
# the only version of the row that survives printing.
#
# HSV's value is not HSL's lightness. Raising the value takes the color to its own
# full-strength self, while raising the lightness of HSL would take it on to white,
# so the second row here ends at a light blue rather than at white.
#
# After the RGB slides of the DLI colors lecture (Lecture 7.5, Accelerated Data
# Science Teaching Kit).
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb

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

N = 512
t = np.linspace(0, 1, N)
# hue, saturation, value of the one color used throughout: a mid sky blue
H0, S0, V0 = 0.55, 0.70, 0.95

# hsv_to_rgb is the generator of the two sweeps: the first holds hue and value and
# runs saturation from 0 to 1, the second holds hue and saturation and runs value.
# The panel titles name the axis each row moves along.
ramps = [
    ('(a) saturation: washed out to full strength',
     np.stack([np.full(N, H0), t, np.full(N, V0)], axis=-1)),
    ('(b) value (brightness): dark to light',
     np.stack([np.full(N, H0), np.full(N, S0), t], axis=-1)),
]


def gray_level(rgb):
    """Luma, from the Rec.709 coefficients applied to the sRGB numbers directly.

    This is what a black and white print keeps, and green counts about ten times
    blue in it. Relative luminance would linearize the channels first; the sRGB
    form is the approximation the printer and the photocopier actually deliver.
    """
    return 0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2]


fig = plt.figure(figsize=(6.0, 2.8))
outer = fig.add_gridspec(2, 1, hspace=0.85)

for i, (title, hsv) in enumerate(ramps):
    rgb = hsv_to_rgb(hsv)
    inner = outer[i].subgridspec(2, 1, hspace=0.12)
    ax_c = fig.add_subplot(inner[0])
    ax_l = fig.add_subplot(inner[1])

    ax_c.imshow(rgb[None, :, :], aspect='auto', origin='lower',
                extent=[0, 1, 0, 1], interpolation='bilinear')
    ax_c.set_title(title)

    ax_l.imshow(gray_level(rgb)[None, :], cmap='gray', vmin=0, vmax=1, aspect='auto',
                origin='lower', extent=[0, 1, 0, 1], interpolation='bilinear')
    ax_l.set_xlabel('the same row printed in black and white', labelpad=2)

    for ax in (ax_c, ax_l):
        ax.set_xticks([])
        ax.set_yticks([])

basename = 'plot_hsv'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')

# --- which of the two rows is a scale a reader could rank ---
print('\n' + 'row'.ljust(40) + 'gray level    spread   ordered')
for title, hsv in ramps:
    gray = gray_level(hsv_to_rgb(hsv))
    d = np.diff(gray)
    d = d[np.abs(d) > 1e-12]
    mono = bool((d > 0).all()) or bool((d < 0).all())   # either direction is ordered
    label = title.split(') ')[1]
    print(f'{label:40s} {gray.min():.2f} to {gray.max():.2f}   {np.ptp(gray):.2f}     '
          f'{mono}')

# --- one setting, very different weight on the page ---
pure = {'red': 0.0, 'yellow': 1 / 6, 'green': 1 / 3,
        'cyan': 0.5, 'blue': 2 / 3, 'magenta': 5 / 6}
grays = {k: gray_level(hsv_to_rgb(np.array([h, 1.0, 1.0]))) for k, h in pure.items()}
print('\nsaturation = 1, value = 1:')
for k, y in grays.items():
    print(f'  {k:8s} gray level = {y:.2f}')
hi, lo = max(grays, key=grays.get), min(grays, key=grays.get)
print(f'  {hi} / {lo} = {grays[hi] / grays[lo]:.1f}x at the same saturation and value')
