# One 4x4 cross-channel transfer record, shared by the three matrix figures so that they
# cannot drift apart. Every number below is transcribed from the research output
#   D:\Google Drive\Research\22 NDT2\code\python40\channel_transfer\
#     alignment_recovery_matrices.csv   (the method=paired block -> ACC)
#     alignment_recovery_offdiag.csv    (the 12 paired rows -> NATIVE)
# and nothing here reads that tree, so the book is self-contained.
#
# ACC[i, j] is the accuracy of a classifier trained on channel i and tested on channel j
# after a linear alignment learnt on the training fold only. NATIVE[j] is the
# within-channel cross-validated accuracy of channel j's own model, which is the reference
# every off-diagonal cell is compared against.
import numpy as np

CHANNELS = ['ch 0', 'ch 1', 'ch 2', 'ch 3']
N = 4

ACC = np.array([
    [0.921250, 0.883333, 0.885417, 0.877083],
    [0.884583, 0.926250, 0.916250, 0.875000],
    [0.897500, 0.910417, 0.922917, 0.879583],
    [0.879167, 0.875833, 0.876667, 0.900000],
])

NATIVE = np.array([0.921667, 0.926250, 0.922917, 0.900000])

# The quantity the figure is actually about: how much accuracy a transfer gives up against
# the target channel's own model. Zero on the diagonal by construction, which is what lets
# it be drawn with an area, a width, or a map anchored at zero.
GAP = NATIVE[None, :] - ACC
np.fill_diagonal(GAP, 0.0)

OFF = ~np.eye(N, dtype=bool)

# Collapsing direction: the pair's mean gap, and how much the two directions differ.
PAIR_MEAN = (GAP + GAP.T) / 2.0
PAIR_ASYM = np.abs(GAP - GAP.T)

# Row i: how well channel i serves as a source. Column j: how easy channel j is as a
# target. The column reading is the one the raw-accuracy matrix gets backwards.
ROW_MEAN = GAP.sum(axis=1) / (N - 1)
COL_MEAN = GAP.sum(axis=0) / (N - 1)

PAIRS = [(i, j) for i in range(N) for j in range(N) if i != j]
UPAIRS = [(i, j) for i in range(N) for j in range(i + 1, N)]

# The three transfers that give up the least accuracy. Named here so that the panels mark
# the same three cells; it is a reading of GAP itself and not an external criterion.
CLOSEST = sorted(PAIRS, key=lambda p: GAP[p])[:3]
CLOSE = np.zeros((N, N), dtype=bool)
for _i, _j in CLOSEST:
    CLOSE[_i, _j] = True


def summary():
    """Every number a caption is allowed to quote, printed by the script that draws it."""
    col_acc = np.array([ACC[OFF[:, j], j].mean() for j in range(N)])
    named = lambda v: ', '.join('%s %.4f' % (c, x) for c, x in zip(CHANNELS, v))
    paired = lambda M: ', '.join('{%d,%d} %.4f' % (i, j, M[i, j]) for i, j in UPAIRS)
    out = [
        'accuracy range   %.3f to %.3f (span %.3f)'
        % (ACC.min(), ACC.max(), ACC.max() - ACC.min()),
        'gap range        %.4f to %.4f (ratio %.1fx, side ratio %.1fx)'
        % (GAP[OFF].min(), GAP[OFF].max(), GAP[OFF].max() / GAP[OFF].min(),
           np.sqrt(GAP[OFF].max() / GAP[OFF].min())),
        'acc side ratio   %.2fx (what a Hinton of the raw accuracies would show)'
        % np.sqrt(ACC.min() / ACC.max()),
        'closest three    ' + ', '.join('%d -> %d, gap %.4f' % (i, j, GAP[i, j])
                                        for i, j in CLOSEST),
        'native           ' + named(NATIVE),
        'row mean gap     ' + named(ROW_MEAN),
        'col mean gap     ' + named(COL_MEAN),
        'col mean acc     ' + named(col_acc),
        'pair mean gap    ' + paired(PAIR_MEAN),
        'pair asymmetry   ' + paired(PAIR_ASYM),
    ]
    return chr(10).join(out)


if __name__ == '__main__':
    print(summary())
