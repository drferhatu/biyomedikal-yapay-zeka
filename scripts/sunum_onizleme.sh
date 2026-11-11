#!/bin/zsh
# Şablonu üretir, doğrular ve önizleme ızgarası çıkarır. Kullanım: scripts/sunum_onizleme.sh <pptx-skill-scripts-dizini> <çıktı-dizini>
set -e
SK="$1"; S="$2"; PY=/opt/miniconda3/envs/ferhat_ml/bin/python
NODE_PATH="$PWD/node_modules" node scripts/make_sunum_sablonu.cjs "$SK/apply_theme.js"
$PY "$SK/office/validate.py" public/proje/ara-sunum-sablonu.pptx
mkdir -p "$S"; cp public/proje/ara-sunum-sablonu.pptx "$S/"; cd "$S"
$PY "$SK/office/soffice.py" --headless --convert-to pdf ara-sunum-sablonu.pptx >/dev/null 2>&1
rm -f slide-*.jpg; pdftoppm -jpeg -r 70 ara-sunum-sablonu.pdf slide
$PY - <<'PYEOF'
from PIL import Image; import glob
fs=sorted(glob.glob('slide-*.jpg')); ims=[Image.open(f) for f in fs]; w,h=ims[0].size
for k in range(0,len(ims),4):
    g=Image.new('RGB',(2*w+6,2*h+6),'#888')
    for i,im in enumerate(ims[k:k+4]): g.paste(im,((i%2)*(w+6),(i//2)*(h+6)))
    g.save(f'grid-{k//4+1}.jpg',quality=85)
PYEOF
ls "$S"/grid-*.jpg
