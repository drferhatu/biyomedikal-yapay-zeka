#!/usr/bin/env python
"""Haftalık uygulama defterlerini üretir ve sitede gömülmek üzere HTML'e çevirir.

- notebooks/hafta-XX.ipynb dosyalarını (yoksa) bu dosyadaki tanımlardan oluşturur.
- notebooks/ altındaki TÜM defterleri isteğe bağlı çalıştırır (--execute) ve HTML'e çevirir.
- nbconvert ile public/notebooks/<ad>.html üretir (site içinde iframe olarak gömülür).
  Çalıştırılan defter diske yazılmaz (--save verilmedikçe); kaynak defter Colab'dan gelen hâliyle kalır.

Kullanım:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/build_notebooks.py [--execute] [--save] [--force]
GitHub Actions bu scripti her push'ta --execute ile çalıştırır (bkz. .github/workflows/deploy.yml).
"""
import sys
from pathlib import Path

import nbformat
from nbformat.v4 import new_code_cell, new_markdown_cell, new_notebook

ROOT = Path(__file__).resolve().parent.parent
NB_DIR = ROOT / "notebooks"
OUT_DIR = ROOT / "public" / "notebooks"
REPO = "drferhatu/biyomedikal-yapay-zeka"

md, code = new_markdown_cell, new_code_cell

# --------------------------------------------------------------------------
# HAFTA 1 — Biyomedikal veri türleri ve uçtan uca iş akışı: ilk tur
# --------------------------------------------------------------------------
WEEK01 = [
md("""# Hafta 1 · Biyomedikal Veri Bilimine Giriş: Uçtan Uca İlk Tur

**SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka** · Fırat Üniversitesi Yazılım ve Bilişim Araştırma Enstitüsü

Bu defter, dersin tamamında izleyeceğimiz iş akışını **tek oturumda, küçük ölçekte** gösterir:

> veri → ön işleme → model → klinik metrik → açıklama → güven

Amaç bugün yöntemleri öğrenmek değil; her adımın *neden* var olduğunu ve önümüzdeki 13 haftada hangisinin derinleşeceğini görmek.
Colab'de sağ üstteki **Bağlan**'a basın, hücreleri sırayla `Shift+Enter` ile çalıştırın.
"""),
md("""## 1 · Veri türü 1: Klinik tablo verisi

scikit-learn ile gelen **Breast Cancer Wisconsin (Diagnostic)** veri seti: 569 hasta, ince iğne aspirasyonundan çıkarılmış 30 morfolojik öznitelik, ikili etiket (malign/benign). Gerçek bir klinik veri setinin en "temiz" hâli; ilerleyen haftalarda çok daha dağınık verilerle çalışacağız."""),
code('''import numpy as np, pandas as pd
from sklearn.datasets import load_breast_cancer

ds = load_breast_cancer(as_frame=True)
df = ds.frame
df["tani"] = df["target"].map({0: "malign", 1: "benign"})
print(df.shape)
print(df["tani"].value_counts(), "\\n")
df.iloc[:, :6].describe().round(2)'''),
md("""**Okuyun:** kaç hasta, kaç öznitelik, sınıflar dengeli mi? Sınıf oranı, 4. haftada hangi metriğin (ROC-AUC mı PR-AUC mı) bilgilendirici olacağını belirler."""),
md("""## 2 · Ön işleme ve hasta-bazlı bölme

Her hasta tek satır olduğu için burada `train_test_split` yeterli. Ama 2. haftada göreceğiz: aynı hastanın birden fazla kaydı varsa (EEG segmentleri, çok sayıda görüntü) **grup-bazlı** bölme zorunludur; aksi hâlde başarım yapay olarak şişer.

Ölçekleyici **yalnızca eğitim kümesine** uydurulur. Bunu `Pipeline` içine koymak, sızıntıyı yapısal olarak engeller."""),
code('''from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression

X = df[ds.feature_names]
y = df["target"]           # 1 = benign, 0 = malign
X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.25, stratify=y, random_state=42)

model = Pipeline([("olcek", StandardScaler()),
                  ("lr", LogisticRegression(max_iter=2000))])
model.fit(X_tr, y_tr)
print("Eğitim:", X_tr.shape, " Test:", X_te.shape)'''),
md("""## 3 · Klinik metrikler: doğruluk yetmez

Doğruluk (%) tek başına yanıltıcıdır. Klinik okuma için **karışıklık matrisi**, **duyarlılık / özgüllük**, **ROC-AUC** ve **kalibrasyon** gerekir. Burada yalnızca gösteriyoruz; 4. hafta bunların tamamını türetecek."""),
code('''from sklearn.metrics import (confusion_matrix, roc_auc_score, roc_curve,
                             classification_report, brier_score_loss)
import matplotlib.pyplot as plt

p = model.predict_proba(X_te)[:, 1]          # benign olasılığı
p_malign = 1 - p
yhat = (p_malign >= 0.5).astype(int)          # 1 = malign tahmini
y_malign = (y_te == 0).astype(int)

tn, fp, fn, tp = confusion_matrix(y_malign, yhat).ravel()
duy = tp / (tp + fn); ozg = tn / (tn + fp)
print(f"Duyarlılık {duy:.3f} · Özgüllük {ozg:.3f} · ROC-AUC {roc_auc_score(y_malign, p_malign):.3f} · Brier {brier_score_loss(y_malign, p_malign):.3f}")

fpr, tpr, thr = roc_curve(y_malign, p_malign)
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(fpr, tpr, lw=2); ax[0].plot([0, 1], [0, 1], "--", c="gray")
ax[0].set(xlabel="1 − özgüllük", ylabel="duyarlılık", title="ROC eğrisi")
from sklearn.calibration import calibration_curve
fr, mp = calibration_curve(y_malign, p_malign, n_bins=8)
ax[1].plot(mp, fr, "o-"); ax[1].plot([0, 1], [0, 1], "--", c="gray")
ax[1].set(xlabel="tahmin edilen olasılık", ylabel="gözlenen oran", title="Kalibrasyon")
plt.tight_layout()'''),
md("""> **Tartışma:** Eşiği 0.5'ten 0.2'ye çekseniz duyarlılık ve özgüllük nasıl değişir? Tarama amaçlı bir modelde hangisini feda edersiniz?"""),
md("""## 4 · Açıklama: model *neden* böyle karar veriyor?

Lojistik regresyon **içsel yorumlanabilir** bir model: katsayılar doğrudan okunur. Kara kutu modellerde (XGBoost, sinir ağı) bu lüks yok; 12–13. haftalarda SHAP, LIME ve Grad-CAM ile aynı soruyu onlara soracağız. Burada en sade araç olan **permütasyon önemi** ile başlıyoruz."""),
code('''from sklearn.inspection import permutation_importance

pi = permutation_importance(model, X_te, y_te, n_repeats=20, random_state=0, scoring="roc_auc")
onem = pd.Series(pi.importances_mean, index=ds.feature_names).sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(7, 4))
onem[::-1].plot.barh(ax=ax, color="#2f3fa3")
ax.set(title="Permütasyon önemi (ROC-AUC düşüşü)", xlabel="öznitelik karıştırılınca AUC kaybı")
plt.tight_layout()'''),
md("""**Okuyun:** En önemli öznitelikler patolojik olarak anlamlı mı (ör. `worst concave points`, `worst radius`)? Bir öznitelik "önemli" çıktı diye nedensel midir? Bu soru 12. haftanın merkezinde."""),
md("""## 5 · Veri türü 2: Biyomedikal sinyal (sentetik EKG)

Tablo verisinden farklı olarak sinyal **zaman** taşır. Aşağıda sentetik bir EKG benzeri sinyal üretip 7. haftada yapacağımız işlemlerin (filtreleme, spektrum) tadına bakıyoruz. Gerçek kayıtlar için PhysioNet'i kullanacağız."""),
code('''from scipy import signal

fs = 250                                  # Hz
t = np.arange(0, 8, 1 / fs)
kalp_hizi = 72 / 60                       # atım/s
ekg = np.zeros_like(t)
for r in np.arange(0.3, t[-1], 1 / kalp_hizi):        # her atım için basit QRS + T
    ekg += 1.0 * np.exp(-((t - r) / 0.012) ** 2) - 0.15 * np.exp(-((t - r - 0.04) / 0.02) ** 2) \\
         + 0.25 * np.exp(-((t - r - 0.30) / 0.06) ** 2)
gurultu = 0.08 * np.random.default_rng(0).standard_normal(t.size) + 0.3 * np.sin(2 * np.pi * 50 * t)   # beyaz + şebeke
ham = ekg + gurultu

b, a = signal.butter(4, [0.5, 40], btype="band", fs=fs)
temiz = signal.filtfilt(b, a, ham)

fig, ax = plt.subplots(2, 1, figsize=(10, 5), sharex=True)
ax[0].plot(t, ham, lw=.8, c="#6b7a92"); ax[0].set_title("Ham sinyal (50 Hz şebeke + gürültü)")
ax[1].plot(t, temiz, lw=1, c="#0f9b8e"); ax[1].set_title("0.5–40 Hz bant geçiren filtre sonrası"); ax[1].set_xlabel("saniye")
plt.tight_layout()'''),
code('''f, P = signal.welch(ham, fs=fs, nperseg=1024)
f2, P2 = signal.welch(temiz, fs=fs, nperseg=1024)
plt.figure(figsize=(8, 3.5))
plt.semilogy(f, P, label="ham", c="#6b7a92"); plt.semilogy(f2, P2, label="filtreli", c="#0f9b8e")
plt.axvline(50, ls="--", c="#be3a5a", lw=1, label="50 Hz şebeke")
plt.xlim(0, 80); plt.xlabel("Hz"); plt.ylabel("güç"); plt.legend(); plt.title("Güç spektral yoğunluğu (Welch)")
plt.tight_layout()'''),
md("""## 6 · Veri türü 3: Görüntü (küçük bir örnek)

Tıbbi görüntü için 10. haftada MedMNIST kullanacağız. Bugün yalnızca "görüntü = sayı matrisi" fikrini görelim: scikit-learn'ün 8×8 rakam görüntüleri üzerinde bir piksel matrisine bakıyoruz."""),
code('''from sklearn.datasets import load_digits
dg = load_digits()
fig, ax = plt.subplots(1, 6, figsize=(9, 2))
for i, a in enumerate(ax):
    a.imshow(dg.images[i], cmap="gray"); a.set_title(dg.target[i]); a.axis("off")
plt.suptitle("Bir görüntü, sayısal bir matristir: 8×8 piksel", y=1.05)
print(dg.images[0].astype(int))'''),
md("""## 7 · Bugün ne gördük, nerede derinleşecek?

| Adım | Bugün | Hangi haftada derinleşecek |
|---|---|---|
| Klinik tablo verisi yükleme ve tanıma | Breast Cancer | Hafta 2–3 |
| Sızıntısız ön işleme (`Pipeline`, hasta-bazlı bölme) | StandardScaler | Hafta 2 |
| Denetimli model | Lojistik regresyon | Hafta 4–5 |
| Klinik metrikler: ROC, kalibrasyon | ROC-AUC, Brier | Hafta 4 |
| Açıklama | Permütasyon önemi | Hafta 12–13 |
| Sinyal: filtreleme ve spektrum | Sentetik EKG, Welch | Hafta 7 |
| Görüntü = matris | 8×8 rakam | Hafta 10 |

**Ders sonrası (isteğe bağlı, 20 dk):** Bu defteri Drive'ınıza kopyalayın (Dosya → Drive'a kopya kaydet). Bölüm 3'te eşiği değiştirip duyarlılık/özgüllük değişimini not edin; bölüm 4'te `n_repeats` değerini 5'e düşürüp sıralamanın kararlılığını gözlemleyin.
"""),
]

NOTEBOOKS = {"hafta-01": ("Hafta 1 · Uçtan Uca İlk Tur", WEEK01)}


def build(name, title, cells, force=False):
    path = NB_DIR / f"{name}.ipynb"
    if path.exists() and not force:
        print(f"· {path.name} mevcut, korunuyor")
    else:
        nb = new_notebook(cells=cells, metadata={
            "kernelspec": {"name": "python3", "display_name": "Python 3", "language": "python"},
            "language_info": {"name": "python"},
            "colab": {"name": f"{name}.ipynb", "toc_visible": True},
        })
        nbformat.write(nb, path)
        print(f"✓ {path.name} yazıldı")
    return path


def execute(path, save=False):
    from nbclient import NotebookClient
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=600, kernel_name="python3", allow_errors=True,
                            resources={"metadata": {"path": str(path.parent)}})
    client.execute()
    if save:
        nbformat.write(nb, path)
    errs = [o for c in nb.cells if c.cell_type == "code" for o in c.get("outputs", []) if o.get("output_type") == "error"]
    print(f"✓ {path.name} çalıştırıldı ({len(errs)} hata hücresi)")
    return nb


def to_html(path, nb=None):
    from nbconvert import HTMLExporter
    exp = HTMLExporter(template_name="lab")
    exp.exclude_input_prompt = True
    exp.exclude_output_prompt = True
    body, _ = exp.from_notebook_node(nb) if nb is not None else exp.from_filename(str(path))
    body = body.replace("</head>", """<style>
      body{background:#fff !important;margin:0}
      .jp-Notebook{padding:16px 20px !important;max-width:100% !important}
      .jp-Cell{padding:0 !important}
      .jp-InputArea-editor{border-radius:10px;border:1px solid #d9dfeb}
      .jp-RenderedHTMLCommon{font-family:"IBM Plex Sans",system-ui,sans-serif;color:#0b1526}
      .jp-RenderedHTMLCommon table{font-size:13px}
    </style></head>""")
    out = OUT_DIR / f"{path.stem}.html"
    out.write_text(body, encoding="utf-8")
    print(f"✓ {out.relative_to(ROOT)} ({len(body)//1024} KB)")


def main():
    force = "--force" in sys.argv
    run = "--execute" in sys.argv
    save = "--save" in sys.argv
    NB_DIR.mkdir(exist_ok=True)
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, (title, cells) in NOTEBOOKS.items():
        build(name, title, cells, force)
    for p in sorted(NB_DIR.glob("*.ipynb")):
        nb = execute(p, save=save) if run else None
        to_html(p, nb)
    print(f"\nColab bağlantı biçimi: https://colab.research.google.com/github/{REPO}/blob/main/notebooks/<ad>.ipynb")


if __name__ == "__main__":
    main()
