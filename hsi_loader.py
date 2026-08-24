"""Self-contained loader for the six HSI benchmarks used in the Sw-SSFCM paper.

Reproduces the exact experimental protocol:
  * z-score normalization (per-band StandardScaler on float64),
  * label encoding: -1 = unlabeled, 0..C-1 = class index,
  * stratified n-labels-per-class split, capped at class size.

The paper evaluates a label budget of n_l in {5, 10, 20, 40, 60} labels per
class with ten draws (seeds 42-51). All 300 resulting splits (6 scenes x 5
budgets x 10 seeds) are shipped as CSV files in ``splits/`` (one row per
labeled pixel: pixel_index, row, col, class).
``load_dataset(..., use_shipped_split=True)`` (default) reads those files, so
results are reproducible regardless of NumPy version. Set it to False to
regenerate the split with ``numpy.random.default_rng(seed)``.

Requires: numpy, scipy, scikit-learn.
"""

from pathlib import Path

import numpy as np
import scipy.io as sio
from sklearn.preprocessing import StandardScaler

SEED = 42                     # first of the ten draws (42-51)
LABELS_PER_CLASS = 60         # largest of the five budgets (5, 10, 20, 40, 60)
SEEDS = tuple(range(42, 52))
BUDGETS = (5, 10, 20, 40, 60)

# dataset key -> (cube file, cube mat-key, gt file, gt mat-key, expected C)
DATASETS = {
    "botswana": ("Botswana/Botswana.mat", "Botswana",
                 "Botswana/Botswana_gt.mat", "Botswana_gt", 14),
    "ksc": ("Kennedy_Space_Center/KSC.mat", "KSC",
            "Kennedy_Space_Center/KSC_gt.mat", "KSC_gt", 13),
    "indian_pines": ("Indian_Pines/Indian_pines_corrected.mat", "indian_pines_corrected",
                     "Indian_Pines/Indian_pines_gt.mat", "indian_pines_gt", 16),
    "pavia_university": ("Pavia_University/PaviaU.mat", "paviaU",
                         "Pavia_University/PaviaU_gt.mat", "paviaU_gt", 9),
    # Houston 2013 ships cube + TR/TE ground-truth masks in one file.
    "houston2013": ("Houston/Houston.mat", "input", None, None, 15),
    "whuhi_longkou": ("WHU-Hi-LongKou/WHU_Hi_LongKou.mat", "WHU_Hi_LongKou",
                      "WHU-Hi-LongKou/WHU_Hi_LongKou_gt.mat", "WHU_Hi_LongKou_gt", 9),
}


def _mat_key(mat, wanted):
    """Return ``wanted`` if present, otherwise the single non-meta key."""
    if wanted in mat:
        return wanted
    keys = [k for k in mat if not k.startswith("__")]
    if len(keys) == 1:
        return keys[0]
    for k in keys:  # case-insensitive fallback
        if k.lower() == wanted.lower():
            return k
    raise KeyError(f"cannot find key '{wanted}' among {keys}")


def build_split(y_true, mask, labels_per_class=LABELS_PER_CLASS, seed=SEED):
    """Stratified N labels/class, capped at class size (paper protocol)."""
    rng = np.random.default_rng(seed)
    y_lab = np.full_like(y_true, -1)
    for c in np.unique(y_true[mask]):
        idx = np.where(y_true == c)[0]
        pick = rng.choice(idx, size=min(labels_per_class, len(idx)), replace=False)
        y_lab[pick] = c
    return y_lab


def load_shipped_split(ds_key, n_pixels, labels_per_class=LABELS_PER_CLASS,
                       seed=SEED, splits_dir=None):
    """Read one canonical split CSV shipped with this repository."""
    splits_dir = Path(splits_dir or Path(__file__).parent / "splits")
    path = splits_dir / f"{ds_key}_labels{labels_per_class}_seed{seed}.csv"
    rows = np.loadtxt(path, delimiter=",", skiprows=1, dtype=np.int64)
    y_lab = np.full(n_pixels, -1, dtype=np.int32)
    y_lab[rows[:, 0]] = rows[:, 3]
    return y_lab


def load_dataset(ds_key, root, labels_per_class=LABELS_PER_CLASS, seed=SEED,
                 use_shipped_split=True):
    """Load one benchmark.

    Returns ``X, y_true, y_lab, mask, H, W`` where X is the z-scored (N, d)
    matrix, y_true/y_lab use -1 for unlabeled, and mask marks ground-truth
    pixels.
    """
    root = Path(root)
    cube_file, cube_key, gt_file, gt_key, C = DATASETS[ds_key]

    if ds_key == "houston2013":
        m = sio.loadmat(str(root / cube_file))
        data = m[_mat_key(m, cube_key)]
        tr = m["TR"].reshape(-1).astype(np.int32)
        te = m["TE"].reshape(-1).astype(np.int32)
        gt = np.where(tr > 0, tr, te)
    else:
        data = sio.loadmat(str(root / cube_file))
        data = data[_mat_key(data, cube_key)]
        g = sio.loadmat(str(root / gt_file))
        gt = g[_mat_key(g, gt_key)].reshape(-1).astype(np.int32)

    H, W, B = data.shape
    X = StandardScaler().fit_transform(data.reshape(-1, B).astype(np.float64))
    mask = gt > 0
    y_true = np.full(H * W, -1, dtype=np.int32)
    y_true[mask] = gt[mask] - 1

    if use_shipped_split:
        y_lab = load_shipped_split(ds_key, H * W, labels_per_class, seed)
    else:
        y_lab = build_split(y_true, mask, labels_per_class, seed)
    return X, y_true, y_lab, mask, H, W


if __name__ == "__main__":
    import argparse

    ap = argparse.ArgumentParser(description="Sanity-check one or all datasets.")
    ap.add_argument("--root", required=True, help="folder holding the .mat files")
    ap.add_argument("--dataset", default=None, choices=list(DATASETS))
    ap.add_argument("--labels", type=int, default=LABELS_PER_CLASS,
                    choices=list(BUDGETS), help="labels per class")
    ap.add_argument("--seed", type=int, default=SEED, choices=list(SEEDS))
    args = ap.parse_args()
    for key in ([args.dataset] if args.dataset else DATASETS):
        X, y_true, y_lab, mask, H, W = load_dataset(
            key, args.root, args.labels, args.seed)
        n_lab = int((y_lab >= 0).sum())
        n_cls = len(np.unique(y_true[mask]))
        print(f"{key:18s} H={H:5d} W={W:5d} d={X.shape[1]:3d} "
              f"C={n_cls:2d} gt_pixels={int(mask.sum()):7d} labeled={n_lab}")
