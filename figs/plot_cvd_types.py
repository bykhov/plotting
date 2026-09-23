# --- Match LaTeX document: Times New Roman, 10pt, textwidth=7in ---
# The visible spectrum, once per common form of color vision deficiency. Each row
# is the same spectrum bar passed through one simulation, so the row shows which
# parts of the spectrum arrive as the same color to that reader.
#
# Reproduction of "Color blindness" by SyntaxTerror, Public domain, via Wikimedia
# Commons, https://commons.wikimedia.org/wiki/File:Color_blindness.svg, redrawn from
# the published simulation matrices rather than copied. Prevalence is kept out of
# the figure and tabulated in the text instead.
#
# Simulation: Machado, Oliveira and Fernandes, "A Physiologically-based Model for
# Simulation of Color Vision Deficiency", IEEE Trans. Visualization and Computer
# Graphics 15(6), 2009, pp. 1291-1298. Severity 1.0 for the -anopia forms and 0.6
# for the -anomaly forms, applied in linear RGB. Achromatopsia is not one of their
# matrices: it is the CIE luminance of the linear RGB, which is what a single
# channel of any kind leaves.
#
# Spectrum colors: CIE 1931 color matching functions via the multi-lobe Gaussian
# fit of Wyman, Sloan and Shirley, "Simple Analytic Approximations to the CIE XYZ
# Color Matching Functions", J. Computer Graphics Techniques 2(2), 2013, pp. 1-11,
# then XYZ to sRGB. Out-of-gamut wavelengths are desaturated toward white, so the
# bar approximates the spectrum rather than reproducing it colorimetrically. The
# bar starts at 400 nm: below that the fitted functions are within numerical noise
# of zero, and normalizing them to full brightness turns that noise into a color.
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({
    'font.family': 'serif',
    'font.serif': ['Times New Roman'],
    'font.size': 10,
    'axes.titlesize': 9,
    'axes.labelsize': 9,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'mathtext.fontset': 'cm',
})

# Machado et al. (2009), for linear RGB. The -anopia matrices are severity 1.0,
# the -anomaly matrices severity 0.6.
CVD = {
    'deuteranomaly': np.array([[0.498864, 0.674741, -0.173604],
                               [0.205199, 0.754872,  0.039929],
                               [-0.011131, 0.030969, 0.980162]]),
    'protanomaly': np.array([[0.385450, 0.769005, -0.154455],
                             [0.100526, 0.829802,  0.069673],
                             [-0.007442, -0.022190, 1.029632]]),
    'protanopia': np.array([[0.152286, 1.052583, -0.204868],
                            [0.114503, 0.786281,  0.099216],
                            [-0.003882, -0.048116, 1.051998]]),
    'deuteranopia': np.array([[0.367322, 0.860646, -0.227968],
                              [0.280085, 0.672501,  0.047413],
                              [-0.011820, 0.042940, 0.968881]]),
    'tritanopia': np.array([[1.255528, -0.076749, -0.178779],
                            [-0.078411, 0.930809,  0.147602],
                            [0.004733, 0.691367,  0.303900]]),
    'tritanomaly': np.array([[1.104996, -0.046633, -0.058363],
                             [-0.032137, 0.971635,  0.060503],
                             [0.001336, 0.317922,  0.680742]]),
}

LUMA = np.array([0.2126, 0.7152, 0.0722])          # CIE luminance, linear RGB

# Row order follows the Commons original: descending frequency.
ROWS = [('normal vision', None),
        ('deuteranomaly', 'deuteranomaly'),
        ('protanomaly', 'protanomaly'),
        ('protanopia', 'protanopia'),
        ('deuteranopia', 'deuteranopia'),
        ('tritanopia', 'tritanopia'),
        ('tritanomaly', 'tritanomaly'),
        ('achromatopsia', 'achromatopsia')]

LO, HI = 400.0, 700.0     # below 400 nm the fitted CMFs are ~0 and the hue is noise


def srgb_to_linear(c):
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(c):
    c = np.clip(c, 0.0, 1.0)
    return np.where(c <= 0.0031308, 12.92 * c, 1.055 * c ** (1 / 2.4) - 0.055)


def simulate(rgb, kind):
    """Deficient appearance of an sRGB array, computed in linear RGB."""
    lin = srgb_to_linear(np.asarray(rgb, dtype=float))
    if kind == 'achromatopsia':
        lin = np.repeat((lin @ LUMA)[..., None], 3, axis=-1)
    else:
        lin = lin @ CVD[kind].T
    return linear_to_srgb(lin)


def _lobe(x, mu, s1, s2):
    """Piecewise Gaussian: width s1 below the peak, s2 above it."""
    t = (x - mu) / np.where(x < mu, s1, s2)
    return np.exp(-0.5 * t * t)


def wavelength_to_srgb(nm):
    """Approximate sRGB of a monochromatic wavelength, at full brightness."""
    x = (1.056 * _lobe(nm, 599.8, 37.9, 31.0) + 0.362 * _lobe(nm, 442.0, 16.0, 26.7)
         - 0.065 * _lobe(nm, 501.1, 20.4, 26.2))
    y = 0.821 * _lobe(nm, 568.8, 46.9, 40.5) + 0.286 * _lobe(nm, 530.9, 16.3, 31.1)
    z = 1.217 * _lobe(nm, 437.0, 11.8, 36.0) + 0.681 * _lobe(nm, 459.0, 26.0, 13.8)
    xyz_to_rgb = np.array([[3.2406, -1.5372, -0.4986],
                           [-0.9689, 1.8758, 0.0415],
                           [0.0557, -0.2040, 1.0570]])
    lin = np.stack([x, y, z], axis=-1) @ xyz_to_rgb.T
    lin = lin - np.minimum(lin.min(axis=-1, keepdims=True), 0.0)   # into gamut
    lin = lin / np.maximum(lin.max(axis=-1, keepdims=True), 1e-12)  # full brightness
    return linear_to_srgb(lin)


nm = np.linspace(LO, HI, 640)
bar = wavelength_to_srgb(nm)[None, :, :]                       # one pixel row

fig, axes = plt.subplots(len(ROWS), 1, figsize=(6.8, 3.4))

for ax, (label, kind) in zip(axes, ROWS):
    ax.imshow(bar if kind is None else simulate(bar, kind),
              extent=[LO, HI, 0, 1], aspect='auto', interpolation='antialiased')
    ax.set_yticks([])
    ax.set_ylabel(label, rotation=0, ha='right', va='center', labelpad=6)
    ax.set_xlim(LO, HI)
    ax.set_xticks(np.arange(400, 701, 50))
    for sp in ax.spines.values():
        sp.set_visible(False)
    if ax is axes[-1]:
        ax.set_xlabel('wavelength (nm)', labelpad=2)
    else:
        ax.set_xticklabels([])
        ax.tick_params(axis='x', length=0)

plt.tight_layout(h_pad=0.4)

basename = 'plot_cvd_types'
plt.savefig(f'{basename}.pdf', bbox_inches='tight')
plt.savefig(f'{basename}.svg', bbox_inches='tight')
plt.savefig(f'{basename}.jpeg', dpi=300, bbox_inches='tight')
print(f'Saved {basename}.pdf, {basename}.svg, {basename}.jpeg')


# --- checks: the numbers behind the figure, not printed into it ---
# Two wavelengths merge when they arrive as the same color, which is a question
# about hue and not about brightness: a dichromat still tells 550 nm from 620 nm
# by lightness alone. Each color is therefore scaled to a common maximum channel
# before the two are compared, so the distance below measures color only.
def chroma(nm_value, kind=None):
    c = wavelength_to_srgb(np.array([float(nm_value)]))
    lin = srgb_to_linear(c if kind is None else simulate(c, kind))[0]
    return lin / max(lin.max(), 1e-12)


def gap(a, b, kind=None):
    """How different two wavelengths look, brightness divided out."""
    return float(np.linalg.norm(chroma(a, kind) - chroma(b, kind)))


print('\nseparation of a red-green pair and of a blue-green pair')
print(f'{"view":15s} {"550/620":>9s} {"480/520":>9s} {"450/620":>9s}')
for label, kind in ROWS:
    print(f'{label:15s} {gap(550, 620, kind):9.3f} {gap(480, 520, kind):9.3f} '
          f'{gap(450, 620, kind):9.3f}')

ref_rg, ref_by = gap(550, 620), gap(480, 520)
for partial, full in [('protanomaly', 'protanopia'),
                      ('deuteranomaly', 'deuteranopia'),
                      ('tritanomaly', 'tritanopia')]:
    pair, ref = ((480, 520), ref_by) if 'trit' in full else ((550, 620), ref_rg)
    assert gap(pair[0], pair[1], full) < gap(pair[0], pair[1], partial) < ref, \
        f'{partial} is not between normal vision and {full}'
for kind in ['protanopia', 'deuteranopia']:
    assert gap(550, 620, kind) < 0.3 * ref_rg, f'{kind} should merge red and green'
    assert gap(450, 620, kind) > ref_rg * 0.8, f'{kind} should keep blue apart'
assert gap(480, 520, 'tritanopia') < 0.3 * ref_by, 'tritanopia should merge blue-green'
assert gap(550, 620, 'tritanopia') > ref_rg, 'tritanopia should keep red-green'
gray = simulate(bar, 'achromatopsia')[0]
assert np.allclose(gray[:, 0], gray[:, 1]) and np.allclose(gray[:, 1], gray[:, 2])
assert [label for label, _ in ROWS] == [
    'normal vision', 'deuteranomaly', 'protanomaly', 'protanopia',
    'deuteranopia', 'tritanopia', 'tritanomaly', 'achromatopsia']
print('\nall checks passed')
