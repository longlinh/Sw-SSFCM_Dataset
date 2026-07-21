#!/usr/bin/env bash
# Download the six openly hosted HSI benchmarks (EHU mirror) into ./HSI/.
# Houston 2013 and WHU-Hi-LongKou require registration; instructions printed below.
set -euo pipefail

ROOT="${1:-HSI}"
EHU=http://www.ehu.eus/ccwintco/uploads

declare -A FILES=(
  ["Botswana/Botswana.mat"]="$EHU/7/72/Botswana.mat"
  ["Botswana/Botswana_gt.mat"]="$EHU/5/58/Botswana_gt.mat"
  ["Salinas/Salinas_corrected.mat"]="$EHU/a/a3/Salinas_corrected.mat"
  ["Salinas/Salinas_gt.mat"]="$EHU/f/fa/Salinas_gt.mat"
  ["Kennedy_Space_Center/KSC.mat"]="$EHU/2/26/KSC.mat"
  ["Kennedy_Space_Center/KSC_gt.mat"]="$EHU/a/a6/KSC_gt.mat"
  ["Indian_Pines/Indian_pines_corrected.mat"]="$EHU/6/67/Indian_pines_corrected.mat"
  ["Indian_Pines/Indian_pines_gt.mat"]="$EHU/c/c4/Indian_pines_gt.mat"
  ["Pavia_University/PaviaU.mat"]="$EHU/e/ee/PaviaU.mat"
  ["Pavia_University/PaviaU_gt.mat"]="$EHU/5/50/PaviaU_gt.mat"
  ["Pavia_Centre/Pavia.mat"]="$EHU/e/e3/Pavia.mat"
  ["Pavia_Centre/Pavia_gt.mat"]="$EHU/5/53/Pavia_gt.mat"
)

for rel in "${!FILES[@]}"; do
  dest="$ROOT/$rel"
  mkdir -p "$(dirname "$dest")"
  if [[ -f "$dest" ]]; then
    echo "skip  $dest (exists)"
  else
    echo "fetch $dest"
    wget -q --show-progress -O "$dest" "${FILES[$rel]}"
  fi
done

cat <<'MSG'

Two datasets require manual registration (place files as shown):
  * Houston 2013  -> HSI/Houston/Houston.mat  (keys: input, TR, TE)
      https://machinelearning.ee.uh.edu/?page_id=459  (2013 IEEE GRSS DFC)
  * WHU-Hi-LongKou -> HSI/WHU-Hi-LongKou/WHU_Hi_LongKou.mat + WHU_Hi_LongKou_gt.mat
      http://rsidea.whu.edu.cn/resource_WHUHi_sharing.htm

Verify everything with:
  python hsi_loader.py --root HSI
MSG
