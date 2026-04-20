# HSI Benchmark Datasets for Sw-SeFC

Hyperspectral image (HSI) datasets used in the paper **"Sw-SeFC: Softmax-Embedded Fuzzy Clustering with Self-Training and Spatial-Weighted Extensions"** (Nguyen Xuan Hoang, Mai Dinh Sinh, Nguyen Long Giang — ISI 2026).

This repository provides the exact datasets, semi-supervised splits, and evaluation protocol used to produce the HSI results reported in the paper (Table of HSI benchmarks and Figures of $\tau$-sweep). It is intended as a reference for reviewers and for reproducibility.

---

## 1. Datasets Overview

Six widely-used HSI benchmarks covering three sensors (Hyperion, AVIRIS, ROSIS) and four scene types (savanna, agriculture, wetland, urban).

| # | Dataset | Sensor | Scene | Size (H×W) | Bands $d$ | Classes $C$ | Labeled pixels | File size |
|---|--------------------|----------|-------------|-------------|-----------|-------------|----------------|-----------|
| 1 | Botswana           | Hyperion | Savanna     | 1476×256    | 145       | 14          | 3,248          | 76 MB     |
| 2 | Salinas            | AVIRIS   | Agriculture | 512×217     | 204       | 16          | 54,129         | 26 MB     |
| 3 | Kennedy Space Ctr. | AVIRIS   | Wetland     | 512×614     | 176       | 13          | 5,211          | 55 MB     |
| 4 | Indian Pines       | AVIRIS   | Agriculture | 145×145     | 200       | 16          | 10,249         | 6 MB      |
| 5 | Pavia University   | ROSIS    | Urban       | 610×340     | 103       | 9           | 42,776         | 34 MB     |
| 6 | Pavia Centre       | ROSIS    | Urban       | 1096×715    | 102       | 9           | 148,152        | 132 MB    |

All files are provided in MATLAB `.mat` format (original distribution from GIC / IEEE DataPort). Each dataset has a data cube and a ground-truth mask.

---

## 2. File Layout

```
HSI/
├── Botswana.mat            Botswana_gt.mat
├── Salinas_corrected.mat   Salinas_gt.mat
├── KSC.mat                 KSC_gt.mat
├── Indian_pines_corrected.mat  Indian_pines_gt.mat
├── PaviaU.mat              PaviaU_gt.mat
├── Pavia.mat               Pavia_gt.mat
└── README.md
```

Variable names inside each `.mat` follow the upstream convention (e.g. `salinas_corrected`, `salinas_gt`, `paviaU`, `paviaU_gt`, ...). Ground-truth masks use `0` as background/unlabeled and `1..C` as class indices.

---

## 3. Semi-Supervised Evaluation Protocol (paper)

All six datasets are evaluated under a unified protocol:

- **Label selection:** 60 labels per class via stratified sampling.
- **Cap for small classes:** for classes with fewer than 60 ground-truth samples (e.g. *Oats* in Indian Pines, $n=20$), the effective label count equals the class size.
- **Unlabeled set:** remaining ground-truth pixels within the region of interest.
- **Background:** pixels with ground-truth label $= 0$ are excluded from accuracy computation (but visualized in full classification maps).
- **Seed:** `42` for all stratified splits.

Effective labeled ratios (labels / labeled pixels):

| Dataset         | Labels | Labeled pixels | Ratio  |
|-----------------|-------:|---------------:|-------:|
| Botswana        |    794 |          3,248 | 24.45% |
| Salinas         |    945 |         54,129 |  1.75% |
| KSC             |    780 |          5,211 | 14.97% |
| Indian Pines    |    818 |         10,249 |  7.98% |
| Pavia Univ.     |    540 |         42,776 |  1.26% |
| Pavia Centre    |    540 |        148,152 |  0.36% |

### Fixed algorithm parameters

| Symbol   | Value    | Meaning                                                   |
|----------|----------|-----------------------------------------------------------|
| `seed`   | 42       | Reproducibility seed (splits, init)                       |
| $T_{max}$| 10,000   | Max FCM iterations                                        |
| $m$      | 2.0      | Fuzzifier                                                 |
| $\varepsilon$ | 1e-6 | Convergence threshold                                    |
| $\eta$   | 0.95     | Pseudo-label confidence threshold (St-SeFC)               |
| $\gamma$ | 0.01     | Softmax learning rate                                     |
| $\lambda$| 1e-4     | L2 regularization                                         |
| $r$      | 2        | Spatial radius (Sw-SeFC, 5×5 window)                      |
| $\tau$   | tuned    | Softmax influence ratio, grid $[0.1, 0.9]$ step $0.1$ + $\{0.95\}$ |

### Per-dataset $\tau^\ast$ (optimal) reported in the paper

| Dataset         | $\tau^\ast$ | Notes                                             |
|-----------------|:-----------:|---------------------------------------------------|
| Botswana        | 0.70        | Savanna, moderate spectral separation             |
| Salinas         | 0.70        | Agriculture, 16 crop classes                      |
| KSC             | 0.70        | Wetland, vegetation types                         |
| Indian Pines    | 0.95        | Mixed agriculture, high spectral overlap          |
| Pavia Univ.     | 0.95        | Urban, narrow streets, similar materials          |
| Pavia Centre    | 0.90        | Large urban scene, cleaner separation             |

---

## 4. Per-Dataset Details

### 4.1 Botswana (Hyperion)
- **Location:** Okavango Delta, Botswana.
- **Spatial resolution:** 30 m.
- **Spectral range:** 0.4–2.5 μm (145 bands after removing noisy/water-absorption bands).
- **Classes:** 14 land-cover types (e.g. Water, Hippo grass, Floodplain grasses, Riparian, Firescar, Island interior, ...).
- **Files:** `Botswana.mat`, `Botswana_gt.mat`.

### 4.2 Salinas (AVIRIS)
- **Location:** Salinas Valley, California, USA.
- **Spatial resolution:** 3.7 m.
- **Spectral range:** 0.4–2.5 μm (204 bands after removing water-absorption bands 108–112, 154–167, 224).
- **Data type:** int16, pixel value range $\approx[-11, 9207]$.
- **Class imbalance:** 12× (min 916 → max 11,271).
- **Files:** `Salinas_corrected.mat`, `Salinas_gt.mat`.

| # | Class | Samples | # | Class | Samples |
|---|---------------------------|--------:|----|------------------------------|--------:|
| 1 | Brocoli_green_weeds_1     |   2,009 |  9 | Soil_vinyard_develop         |   6,203 |
| 2 | Brocoli_green_weeds_2     |   3,726 | 10 | Corn_senesced_green_weeds    |   3,278 |
| 3 | Fallow                    |   1,976 | 11 | Lettuce_romaine_4wk          |   1,068 |
| 4 | Fallow_rough_plow         |   1,394 | 12 | Lettuce_romaine_5wk          |   1,927 |
| 5 | Fallow_smooth             |   2,678 | 13 | Lettuce_romaine_6wk          |     916 |
| 6 | Stubble                   |   3,959 | 14 | Lettuce_romaine_7wk          |   1,070 |
| 7 | Celery                    |   3,579 | 15 | Vinyard_untrained            |   7,268 |
| 8 | Grapes_untrained          |  11,271 | 16 | Vinyard_vertical_trellis     |   1,807 |

### 4.3 Kennedy Space Center — KSC (AVIRIS)
- **Location:** Kennedy Space Center, Florida, USA (wetland).
- **Spatial resolution:** 18 m.
- **Spectral range:** 0.4–2.5 μm (176 bands after removing water-absorption / low-SNR bands).
- **Classes:** 13 (Scrub, Willow swamp, CP hammock, Slash pine, Oak/Broadleaf, Hardwood, Swamp, Graminoid marsh, Spartina marsh, Cattail marsh, Salt marsh, Mud flats, Water).
- **Challenge:** few labeled samples (5,211 total).
- **Files:** `KSC.mat`, `KSC_gt.mat`.

### 4.4 Indian Pines (AVIRIS)
- **Location:** North-western Indiana, USA.
- **Spatial resolution:** 20 m.
- **Spectral range:** 0.4–2.5 μm (200 bands after removing water-absorption bands 104–108, 150–163, 220).
- **Classes:** 16 agricultural / forestry classes with strong spectral overlap; scene is roughly 2/3 agriculture, 1/3 forest + other perennial natural vegetation.
- **Small class:** *Oats* has only 20 labeled pixels (label count capped at class size).
- **Files:** `Indian_pines_corrected.mat`, `Indian_pines_gt.mat`.

### 4.5 Pavia University (ROSIS)
- **Location:** Pavia, northern Italy (urban — university campus).
- **Spatial resolution:** 1.3 m.
- **Spectral range:** 0.43–0.86 μm (103 bands).
- **Classes:** 9 (Asphalt, Meadows, Gravel, Trees, Painted metal sheets, Bare soil, Bitumen, Self-blocking bricks, Shadows).
- **Files:** `PaviaU.mat`, `PaviaU_gt.mat`.

### 4.6 Pavia Centre (ROSIS)
- **Location:** Pavia, northern Italy (urban — city centre).
- **Spatial resolution:** 1.3 m.
- **Spectral range:** 0.43–0.86 μm (102 bands).
- **Classes:** 9 (Water, Trees, Asphalt, Self-blocking bricks, Bitumen, Tiles, Shadows, Meadows, Bare soil).
- **Note:** original cube has 1096×1096 but a 1096×381 vertical stripe with no information is discarded; the released ground truth is 1096×715.
- **Files:** `Pavia.mat`, `Pavia_gt.mat`.

---

## 5. Download

Primary mirror (GIC, University of the Basque Country):

```bash
BASE=http://www.ehu.eus/ccwintco/uploads

# Botswana
wget $BASE/7/72/Botswana.mat          && wget $BASE/5/58/Botswana_gt.mat
# Salinas
wget $BASE/a/a3/Salinas_corrected.mat && wget $BASE/f/fa/Salinas_gt.mat
# KSC
wget $BASE/2/26/KSC.mat               && wget $BASE/a/a6/KSC_gt.mat
# Indian Pines
wget $BASE/6/67/Indian_pines_corrected.mat && wget $BASE/c/c4/Indian_pines_gt.mat
# Pavia University
wget $BASE/e/ee/PaviaU.mat            && wget $BASE/5/50/PaviaU_gt.mat
# Pavia Centre
wget $BASE/e/e3/Pavia.mat             && wget $BASE/5/53/Pavia_gt.mat
```

Alternative sources:
- GIC — *Hyperspectral Remote Sensing Scenes*: <https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes>
- IEEE DataPort — *Hyperspectral Remote Sensing Datasets (Indian Pines, Pavia, Botswana, Salinas)*: <https://ieee-dataport.org/documents/hyperspectral-remote-sensing-datasets-indian-pines-pavia-university-botswana-and-salinas>

---

## 6. Quick Load Example (Python)

```python
import scipy.io as sio
import numpy as np

cube = sio.loadmat("Salinas_corrected.mat")["salinas_corrected"]   # (H, W, d)
gt   = sio.loadmat("Salinas_gt.mat")["salinas_gt"]                  # (H, W), 0=background

H, W, d = cube.shape
X       = cube.reshape(-1, d).astype(np.float32)
y       = gt.reshape(-1)
mask    = y > 0                     # keep only labeled pixels
X_lab, y_lab = X[mask], y[mask] - 1  # 0-indexed
```

For the Sw-SeFC pipeline (spatial window $r=2$, semi-supervised split with 60 labels/class), see the experiment script `src/exp3/benchmark_top3_hsi.py` in the companion code repository.

---

## 7. License and Citation

These datasets are distributed by their original providers (GIC/UPV-EHU, Purdue MultiSpec, ROSIS/DLR). Please cite the original sources when using them. If this packaging is useful for your own work, you may additionally cite the Sw-SeFC paper:

```
@article{hoang2026swsefc,
  title   = {Sw-SeFC: Softmax-Embedded Fuzzy Clustering with Self-Training and Spatial-Weighted Extensions},
  author  = {Nguyen Xuan Hoang and Mai Dinh Sinh and Nguyen Long Giang},
  journal = {ISI},
  year    = {2026}
}
```
