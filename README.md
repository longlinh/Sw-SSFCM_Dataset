# HSI Benchmark Datasets for Sw-SSFCM

Hyperspectral image (HSI) datasets used in the paper **"Sw-SSFCM: Spatial-weighted Softmax-Embedded Semi-Supervised Fuzzy C-Means"** (Nguyen Xuan Hoang, Mai Dinh Sinh, Nguyen Long Giang — ISI 2026).

This page documents the exact datasets, semi-supervised splits, and evaluation protocol used to produce the HSI results reported in the paper (Table~IV — `tab:hsi_benchmark`, Table~III — `tab:hsi_datasets`, and the per-algorithm $\tau$-sweep figures `fig:tau_botswana` … `fig:tau_longkou`). It is intended as a single reference point for reviewers and for reproducibility.

---

## 1. Datasets Overview (8 benchmarks)

Eight widely-used HSI benchmarks covering five sensors (Hyperion, AVIRIS, ROSIS, ITRES CASI-1500, Headwall Nano-Hyperspec) and five scene types (savanna, agriculture, wetland, urban, university campus, and UAV crop).

| # | Dataset | Sensor | Scene | Size (H×W) | Bands $d$ | Classes $C$ | Labeled pixels | File size |
|---|----------------------|----------------------|---------------------|-------------|----------:|------------:|---------------:|----------:|
| 1 | Botswana             | EO-1 Hyperion        | Savanna             | 1476×256    | 145       | 14          |          3,248 | 76 MB     |
| 2 | Salinas              | AVIRIS               | Agriculture         | 512×217     | 204       | 16          |         54,129 | 26 MB     |
| 3 | Kennedy Space Center | AVIRIS               | Wetland             | 512×614     | 176       | 13          |          5,211 | 55 MB     |
| 4 | Indian Pines         | AVIRIS               | Mixed agriculture   | 145×145     | 200       | 16          |         10,249 | 6 MB      |
| 5 | Pavia University     | ROSIS-03             | Urban               | 610×340     | 103       | 9           |         42,776 | 34 MB     |
| 6 | Pavia Centre         | ROSIS-03             | Urban               | 1096×715    | 102       | 9           |        148,152 | 124 MB    |
| 7 | Houston 2013         | ITRES CASI-1500      | University campus   | 349×1905    | 144       | 15          |         15,029 | 161 MB    |
| 8 | WHU-Hi-LongKou       | Headwall Nano-Hyperspec (UAV) | Crop      | 550×400     | 270       | 9           |        204,542 | 178 MB    |

All files are provided in MATLAB `.mat` format (original distribution from GIC / IEEE DataPort / RSIDEA group at Wuhan University). Each dataset has a data cube and a ground-truth mask. Ground-truth masks use `0` as background/unlabeled and `1..C` as class indices.

---

## 2. File Layout

The `.mat` files are NOT tracked in git because of size; only this README is versioned. The expected layout (relative to repository root or to `/home/dll/nckh/dataset/HSI/`) is:

```
HSI/
├── Botswana/             Botswana.mat                 Botswana_gt.mat
├── Salinas/              Salinas_corrected.mat        Salinas_gt.mat
├── Kennedy_Space_Center/ KSC.mat                      KSC_gt.mat
├── Indian_Pines/         Indian_pines_corrected.mat   Indian_pines_gt.mat
├── Pavia_University/     PaviaU.mat                   PaviaU_gt.mat
├── Pavia_Centre/         Pavia.mat                    Pavia_gt.mat
├── Houston/              Houston.mat                  (gt embedded)
├── WHU-Hi-LongKou/       WHU_Hi_LongKou.mat           WHU_Hi_LongKou_gt.mat
└── README.md             (this file)
```

Variable names inside each `.mat` follow the upstream convention (e.g. `salinas_corrected` / `salinas_gt`, `paviaU` / `paviaU_gt`, `WHU_Hi_LongKou` / `WHU_Hi_LongKou_gt`). The Houston 2013 release packages the cube and the ground truth inside a single `.mat` file.

---

## 3. Semi-Supervised Evaluation Protocol (paper)

All eight datasets are evaluated under a unified protocol.

- **Label selection:** 60 labels per class via stratified sampling (`seed = 42`).
- **Cap for small classes:** for classes with fewer than 60 ground-truth samples (e.g. *Oats* in Indian Pines, $n=20$), the effective label count equals the class size. This is why Indian Pines has 833 effective labels instead of $16 \times 60 = 960$.
- **Unlabeled set:** remaining ground-truth pixels.
- **Background:** pixels with ground-truth label $= 0$ are excluded from accuracy computation but rendered in classification maps.

### Effective labeled ratios

| # | Dataset              | Labels | Labeled pixels | Ratio   |
|---|----------------------|-------:|---------------:|--------:|
| 1 | Botswana             |    840 |          3,248 | 25.86 % |
| 2 | Salinas              |    960 |         54,129 |  1.77 % |
| 3 | KSC                  |    780 |          5,211 | 14.97 % |
| 4 | Indian Pines         |    833 |         10,249 |  8.13 % |
| 5 | Pavia University     |    540 |         42,776 |  1.26 % |
| 6 | Pavia Centre         |    540 |        148,152 |  0.36 % |
| 7 | Houston 2013         |    900 |         15,029 |  5.99 % |
| 8 | WHU-Hi-LongKou       |    540 |        204,542 |  0.26 % |

### Fixed algorithm parameters

| Symbol         | Value     | Meaning                                                  |
|----------------|-----------|----------------------------------------------------------|
| `seed`         | 42        | Reproducibility seed (splits, init)                      |
| $T_{\max}$     | 10,000    | Max FCM iterations                                       |
| $m$            | 2.0       | Fuzzifier                                                |
| $\varepsilon$  | 1e-4      | Convergence threshold (Exp3)                             |
| $\gamma$       | 0.01      | Softmax learning rate                                    |
| $\lambda$      | 1e-4      | L2 regularization (Softmax)                              |
| $T_s$          | 1000      | Softmax max epochs                                       |
| $r$            | 1, 2      | Spatial radius for Sw-SSFCM ($3\times3$ / $5\times5$)    |
| $\tau$         | tuned     | Softmax influence ratio, grid $\{0.1, 0.2, \ldots, 0.9, 0.95\}$ |
| timeout        | 600 s     | Per-baseline wall-clock cap (`signal.alarm`, in-process) |

### Per-algorithm optimal $(\tau^\ast, \alpha^\ast)$ reported in the paper

Values reproduced from `paper_final/pictures/fig-tau-hsi.tex`. ACC reported on labeled pixels (background excluded).

| Dataset          | SeFCM $\tau^\ast$ / $\alpha^\ast$ / ACC | Sw-SSFCM $r{=}1$ $\tau^\ast$ / $\alpha^\ast$ / ACC | Sw-SSFCM $r{=}2$ $\tau^\ast$ / $\alpha^\ast$ / ACC |
|------------------|------------------------------------------|----------------------------------------------------|----------------------------------------------------|
| Botswana         | 0.80 /  219.8 / 94.67 %                 | 0.95 / 1043.9 / 96.27 %                            | 0.95 / 1043.9 / 96.40 %                            |
| Salinas          | 0.60 /  110.4 / 87.68 %                 | 0.95 / 1398.0 / 89.27 %                            | 0.95 / 1398.0 / 89.38 %                            |
| KSC              | 0.90 /  617.6 / 89.68 %                 | 0.90 /  617.6 / 91.88 %                            | 0.95 / 1303.7 / 92.55 %                            |
| Indian Pines     | 0.90 /  649.2 / 71.23 %                 | 0.95 / 1370.6 / 74.54 %                            | 0.95 / 1370.6 / 75.12 %                            |
| Pavia University | 0.95 /  890.7 / 79.15 %                 | 0.95 /  890.7 / 82.37 %                            | 0.95 /  890.7 / 82.86 %                            |
| Pavia Centre     | 0.95 /  882.0 / 97.16 %                 | 0.95 /  882.0 / 97.71 %                            | 0.95 /  882.0 / 97.78 %                            |
| Houston 2013     | 0.95 / 1010.3 / 80.77 %                 | 0.95 / 1010.3 / 81.71 %                            | 0.95 / 1010.3 / 82.31 %                            |
| WHU-Hi-LongKou   | 0.90 / 1105.9 / 93.14 %                 | 0.95 / 2334.8 / 94.40 %                            | 0.95 / 2334.8 / 94.62 %                            |

---

## 4. Per-Dataset Details

### 4.1 Botswana (EO-1 Hyperion)

- **Location:** Okavango Delta, Botswana.
- **Spatial resolution:** 30 m.
- **Spectral range:** 0.4–2.5 μm; 145 bands retained after removing noisy / water-absorption bands (10, 55–82, 97–102, 134–164, 187–220).
- **Classes (14):** Water; Hippo grass; Floodplain grasses 1; Floodplain grasses 2; Reeds; Riparian; Firescar 2; Island interior; Acacia woodlands; Acacia shrublands; Acacia grasslands; Short mopane; Mixed mopane; Exposed soils.
- **Files:** `Botswana.mat`, `Botswana_gt.mat` (variable keys: `Botswana`, `Botswana_gt`).

### 4.2 Salinas (AVIRIS)

- **Location:** Salinas Valley, California, USA.
- **Spatial resolution:** 3.7 m.
- **Spectral range:** 0.4–2.5 μm; 204 bands retained (water-absorption bands 108–112, 154–167, 224 removed).
- **Data type:** int16; pixel value range $\approx [-11, 9207]$.
- **Class imbalance:** $\approx$ 12× (min 916 → max 11,271).
- **Files:** `Salinas_corrected.mat`, `Salinas_gt.mat`.

| #  | Class                      | Samples | #   | Class                      | Samples |
|----|----------------------------|--------:|-----|----------------------------|--------:|
| 1  | Brocoli_green_weeds_1      |   2,009 |  9  | Soil_vinyard_develop       |   6,203 |
| 2  | Brocoli_green_weeds_2      |   3,726 | 10  | Corn_senesced_green_weeds  |   3,278 |
| 3  | Fallow                     |   1,976 | 11  | Lettuce_romaine_4wk        |   1,068 |
| 4  | Fallow_rough_plow          |   1,394 | 12  | Lettuce_romaine_5wk        |   1,927 |
| 5  | Fallow_smooth              |   2,678 | 13  | Lettuce_romaine_6wk        |     916 |
| 6  | Stubble                    |   3,959 | 14  | Lettuce_romaine_7wk        |   1,070 |
| 7  | Celery                     |   3,579 | 15  | Vinyard_untrained          |   7,268 |
| 8  | Grapes_untrained           |  11,271 | 16  | Vinyard_vertical_trellis   |   1,807 |

### 4.3 Kennedy Space Center — KSC (AVIRIS)

- **Location:** Kennedy Space Center, Florida, USA (wetland mosaic).
- **Spatial resolution:** 18 m.
- **Spectral range:** 0.4–2.5 μm; 176 bands retained after removing low-SNR / water-absorption bands.
- **Classes (13):** Scrub; Willow swamp; CP hammock; Slash pine; Oak/broadleaf; Hardwood; Swamp; Graminoid marsh; Spartina marsh; Cattail marsh; Salt marsh; Mud flats; Water.
- **Challenge:** few labeled samples (5,211 total).
- **Files:** `KSC.mat`, `KSC_gt.mat`.

### 4.4 Indian Pines (AVIRIS)

- **Location:** North-western Indiana, USA (Purdue test site).
- **Spatial resolution:** 20 m.
- **Spectral range:** 0.4–2.5 μm; 200 bands retained (water-absorption bands 104–108, 150–163, 220 removed).
- **Classes:** 16 agricultural / forestry classes with strong spectral overlap.
- **Small classes:** *Oats* (20 px), *Grass-pasture-mowed* (28 px) — label counts capped at class size (effective labels = 833).
- **Files:** `Indian_pines_corrected.mat`, `Indian_pines_gt.mat`.

| #  | Class                                | Samples | #  | Class                                  | Samples |
|----|--------------------------------------|--------:|----|----------------------------------------|--------:|
| 1  | Alfalfa                              |      46 |  9 | Oats                                   |      20 |
| 2  | Corn-notill                          |   1,428 | 10 | Soybean-notill                         |     972 |
| 3  | Corn-mintill                         |     830 | 11 | Soybean-mintill                        |   2,455 |
| 4  | Corn                                 |     237 | 12 | Soybean-clean                          |     593 |
| 5  | Grass-pasture                        |     483 | 13 | Wheat                                  |     205 |
| 6  | Grass-trees                          |     730 | 14 | Woods                                  |   1,265 |
| 7  | Grass-pasture-mowed                  |      28 | 15 | Buildings-Grass-Trees-Drives           |     386 |
| 8  | Hay-windrowed                        |     478 | 16 | Stone-Steel-Towers                     |      93 |

### 4.5 Pavia University (ROSIS-03)

- **Location:** Pavia, northern Italy (university campus).
- **Spatial resolution:** 1.3 m.
- **Spectral range:** 0.43–0.86 μm; 103 bands.
- **Classes (9):** Asphalt; Meadows; Gravel; Trees; Painted metal sheets; Bare soil; Bitumen; Self-blocking bricks; Shadows.
- **Files:** `PaviaU.mat`, `PaviaU_gt.mat`.

### 4.6 Pavia Centre (ROSIS-03)

- **Location:** Pavia, northern Italy (city centre).
- **Spatial resolution:** 1.3 m.
- **Spectral range:** 0.43–0.86 μm; 102 bands.
- **Classes (9):** Water; Trees; Asphalt; Self-blocking bricks; Bitumen; Tiles; Shadows; Meadows; Bare soil.
- **Note:** the original cube is 1096×1096; a 1096×381 vertical stripe with no information is discarded by the upstream provider, hence the released ground truth is 1096×715.
- **Files:** `Pavia.mat`, `Pavia_gt.mat`.

### 4.7 Houston 2013 (ITRES CASI-1500)

- **Location:** University of Houston campus and adjacent urban area, Texas, USA.
- **Provenance:** 2013 IEEE GRSS Data Fusion Contest [Debes et al., *IEEE J-STARS*, 2014].
- **Spatial resolution:** 2.5 m.
- **Spectral range:** 0.38–1.05 μm; 144 bands.
- **Classes (15):** Healthy grass; Stressed grass; Synthetic grass; Trees; Soil; Water; Residential; Commercial; Road; Highway; Railway; Parking Lot 1; Parking Lot 2; Tennis court; Running track.
- **Challenge:** heterogeneous illumination (shadow strip from a cloud), narrow man-made structures.
- **Files:** `Houston.mat` (single packaged file containing both data and ground truth).

### 4.8 WHU-Hi-LongKou (Headwall Nano-Hyperspec, UAV)

- **Location:** Longkou Town, Hubei province, China (UAV-borne acquisition by RSIDEA group, Wuhan University).
- **Provenance:** WHU-Hi benchmark suite [Zhong et al., *RSE*, 2020].
- **Flight altitude:** 500 m; **GSD ≈ 0.463 m**.
- **Spectral range:** 0.40–1.00 μm; 270 bands.
- **Classes (9):** Corn; Cotton; Sesame; Broad-leaf soybean; Narrow-leaf soybean; Rice; Water; Roads & houses; Mixed weed.
- **Strong spatial continuity** (typical of UAV crop imagery), highest spectral dimensionality of the eight datasets.
- **Files:** `WHU_Hi_LongKou.mat`, `WHU_Hi_LongKou_gt.mat` (the official release also bundles a `Training samples and test samples/` subfolder with `Train{25..300}.mat` / `Test{25..300}.mat` splits — not used by Sw-SSFCM, which uses its own stratified 60-labels-per-class split).

---

## 5. Download

### 5.1 Six classic scenes — GIC mirror (UPV/EHU)

Primary mirror page: <https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes>
Alternative mirror: <https://ieee-dataport.org/documents/hyperspectral-remote-sensing-datasets-indian-pines-pavia-university-botswana-and-salinas>

Direct download URLs (each row is one cube file and one ground-truth file):

| Dataset           | Cube                                                                                                | Ground truth                                                                              |
|-------------------|-----------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| Botswana          | <http://www.ehu.eus/ccwintco/uploads/7/72/Botswana.mat>                                             | <http://www.ehu.eus/ccwintco/uploads/5/58/Botswana_gt.mat>                                |
| Salinas           | <http://www.ehu.eus/ccwintco/uploads/a/a3/Salinas_corrected.mat>                                    | <http://www.ehu.eus/ccwintco/uploads/f/fa/Salinas_gt.mat>                                 |
| KSC               | <http://www.ehu.eus/ccwintco/uploads/2/26/KSC.mat>                                                  | <http://www.ehu.eus/ccwintco/uploads/a/a6/KSC_gt.mat>                                     |
| Indian Pines      | <http://www.ehu.eus/ccwintco/uploads/6/67/Indian_pines_corrected.mat>                               | <http://www.ehu.eus/ccwintco/uploads/c/c4/Indian_pines_gt.mat>                            |
| Pavia University  | <http://www.ehu.eus/ccwintco/uploads/e/ee/PaviaU.mat>                                               | <http://www.ehu.eus/ccwintco/uploads/5/50/PaviaU_gt.mat>                                  |
| Pavia Centre      | <http://www.ehu.eus/ccwintco/uploads/e/e3/Pavia.mat>                                                | <http://www.ehu.eus/ccwintco/uploads/5/53/Pavia_gt.mat>                                   |

These six scenes are not assigned individual DOIs by the GIC mirror. Indian Pines is additionally available on the Purdue University Research Repository with a formal DOI (see Section 6).

### 5.2 Houston 2013 (2013 IEEE GRSS Data Fusion Contest)

Distributed by the IEEE GRSS through the Machine Learning Lab at the University of Houston (free, registration required for the full bundle):

- Distribution page: <https://machinelearning.ee.uh.edu/?page_id=459>
- IEEE GRSS Data and Algorithm Standard Evaluation (DASE) entry: <https://dase.grss-ieee.org/index.php>
- Reference paper (DOI): <https://doi.org/10.1109/JSTARS.2014.2305441> (C. Debes et al., *IEEE J. Sel. Topics Appl. Earth Observ. Remote Sens.*, 7(6):2405–2418, 2014).

The dataset itself is *not* released with a stand-alone DOI — the canonical citation is the contest-outcome paper above.

### 5.3 WHU-Hi-LongKou (RSIDEA, Wuhan University)

- Project page: <http://rsidea.whu.edu.cn/resource_WHUHi_sharing.htm>
- Reference paper (DOI): <https://doi.org/10.1016/j.rse.2020.112012> (Y. Zhong et al., *Remote Sensing of Environment*, 250:112012, 2020).

---

## 6. DOI summary

Stand-alone dataset DOIs and reference-paper DOIs:

| Dataset           | Dataset DOI                                                              | Reference-paper DOI                                                         |
|-------------------|--------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| Botswana          | — (no individual DOI; GIC mirror)                                        | —                                                                           |
| Salinas           | — (no individual DOI; GIC mirror)                                        | —                                                                           |
| KSC               | — (no individual DOI; GIC mirror)                                        | —                                                                           |
| Indian Pines      | <https://doi.org/10.4231/R7RX991C> (Purdue University Research Repository) | —                                                                         |
| Pavia University  | — (no individual DOI; GIC mirror)                                        | —                                                                           |
| Pavia Centre      | — (no individual DOI; GIC mirror)                                        | —                                                                           |
| Houston 2013      | — (no stand-alone DOI; distributed by IEEE GRSS / Univ. of Houston)      | <https://doi.org/10.1109/JSTARS.2014.2305441>                               |
| WHU-Hi-LongKou    | — (no stand-alone DOI; distributed by RSIDEA, Wuhan University)          | <https://doi.org/10.1016/j.rse.2020.112012>                                 |

---

## 7. License and Citation

These datasets are distributed by their original providers (GIC/UPV-EHU; Purdue MultiSpec; ROSIS/DLR; IEEE GRSS / University of Houston; RSIDEA / Wuhan University). Please cite the original sources when using them:

- **Indian Pines:** M. F. Baumgardner, L. L. Biehl, D. A. Landgrebe, "220 Band AVIRIS Hyperspectral Image Data Set: June 12, 1992 Indian Pine Test Site 3," Purdue University Research Repository, 2015. <https://doi.org/10.4231/R7RX991C>
- **Pavia University, Pavia Centre, Salinas, KSC, Botswana:** GIC, *Hyperspectral Remote Sensing Scenes*, University of the Basque Country (UPV/EHU). <https://www.ehu.eus/ccwintco/index.php/Hyperspectral_Remote_Sensing_Scenes>
- **Houston 2013:** C. Debes et al., "Hyperspectral and LiDAR data fusion: Outcome of the 2013 GRSS Data Fusion Contest," *IEEE J. Sel. Topics Appl. Earth Observ. Remote Sens.*, 7(6):2405–2418, 2014. <https://doi.org/10.1109/JSTARS.2014.2305441>
- **WHU-Hi-LongKou:** Y. Zhong et al., "WHU-Hi: UAV-borne hyperspectral with high spatial resolution (H²) benchmark datasets and classifier for precise crop identification based on deep convolutional neural network with CRF," *Remote Sensing of Environment*, 250:112012, 2020. <https://doi.org/10.1016/j.rse.2020.112012>

If this packaging is useful for your own work, please additionally cite the Sw-SSFCM paper (Nguyen Xuan Hoang, Mai Dinh Sinh, Nguyen Long Giang, ISI 2026).
