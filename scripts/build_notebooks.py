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

# --------------------------------------------------------------------------
# HAFTA 2 — Biyomedikal verinin doğası ve ön işleme
# --------------------------------------------------------------------------
WEEK02 = [
md("""# Hafta 2 · Biyomedikal Verinin Doğası ve Ön İşleme

**SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka** · Fırat Üniversitesi Yazılım ve Bilişim Araştırma Enstitüsü

Bu defterde model kurmaktan çok, modelden önce yapılması gerekenlerle uğraşıyoruz. Beş bölüm var: eksik verinin
gerçek yüzü, imputasyon seçeneklerinin dürüst karşılaştırması, veri sızıntısının ne kadar kolay olduğu, aynı hastanın
iki kümeye düşmesinin başarımı nasıl şişirdiği ve dengesiz sınıflarda doğruluğun neden anlamsızlaştığı.

Her bölümün sonunda küçük bir "deneyin" notu var; derste birlikte ilerleyeceğiz."""),
md("""## 1 · Veri: Pima diyabet seti ve gizli eksikler

768 kadın hasta, 8 klinik ölçüm, ikili sonuç (5 yıl içinde diyabet). Veri setinin ünlü bir tuzağı var:
ölçülmemiş değerler **0** olarak kaydedilmiş. Glukozu 0 olan hasta olmaz; o hücre aslında boş."""),
code('''import numpy as np, pandas as pd
import matplotlib.pyplot as plt

URL = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
COLS = ["gebelik", "glukoz", "tansiyon", "deri_kalinligi", "insulin", "vki", "soyagaci", "yas", "diyabet"]
try:
    df = pd.read_csv(URL, header=None, names=COLS)
    print("Veri indirildi:", df.shape)
except Exception as e:
    print("İndirme başarısız, sentetik veri üretiliyor:", e)
    rng = np.random.default_rng(0); n = 768
    df = pd.DataFrame({"gebelik": rng.integers(0, 15, n), "glukoz": rng.normal(120, 30, n).clip(0),
                       "tansiyon": rng.normal(70, 12, n).clip(0), "deri_kalinligi": rng.normal(20, 10, n).clip(0),
                       "insulin": rng.normal(80, 100, n).clip(0), "vki": rng.normal(32, 7, n).clip(0),
                       "soyagaci": rng.random(n), "yas": rng.integers(21, 70, n)})
    df["diyabet"] = (rng.random(n) < 1 / (1 + np.exp(-(df.glukoz - 125) / 25))).astype(int)
    oranlar = {"glukoz": 0.01, "tansiyon": 0.05, "deri_kalinligi": 0.3, "insulin": 0.49, "vki": 0.015}
    for c, o in oranlar.items():
        df.loc[rng.random(n) < o, c] = 0

sifir_olamaz = ["glukoz", "tansiyon", "deri_kalinligi", "insulin", "vki"]
print("\\nSıfır olarak kodlanmış hücre sayısı:")
print((df[sifir_olamaz] == 0).sum())'''),
md("""`describe()` bu tuzağı size söylemez; minimum 0 görünür ve geçer gidersiniz. Önce sıfırları gerçek boşluğa (`NaN`) çevirelim,
sonra eksikliğin **rastgele olup olmadığına** bakalım. Sorumuz şu: insülin ölçülmeyen hastalar, ölçülenlerle aynı hastalar mı?"""),
code('''X = df.drop(columns="diyabet").copy()
y = df["diyabet"]
X[sifir_olamaz] = X[sifir_olamaz].replace(0, np.nan)

eksik = X.isna().mean().sort_values(ascending=False)
print("Eksik oranı:\\n", eksik.round(3), "\\n")

# Eksiklik sonuçla ilişkili mi?  (MAR/MNAR ipucu)
tablo = pd.DataFrame({
    "insulin_eksik_orani": [X.loc[y == 0, "insulin"].isna().mean(), X.loc[y == 1, "insulin"].isna().mean()],
    "deri_eksik_orani":    [X.loc[y == 0, "deri_kalinligi"].isna().mean(), X.loc[y == 1, "deri_kalinligi"].isna().mean()],
}, index=["diyabet yok", "diyabet var"]).round(3)
tablo'''),
md("""> **Deneyin:** İnsülin eksikliği iki grupta aynı oranda mı? Değilse eksikliğin kendisi bilgi taşıyor demektir. Bu durumda
> "eksik mi?" sorusunu ayrı bir sütun olarak modele vermek (eksiklik göstergesi) çoğu zaman başarımı artırır."""),
md("""## 2 · İmputasyon: beş yöntem, tek dürüst karşılaştırma

Karşılaştırmayı dürüst yapmanın tek yolu, imputasyonu **çapraz doğrulama döngüsünün içine** koymak. Yani `Pipeline`.
Aksi hâlde test katlamasındaki bilgi, medyanı hesaplarken eğitime karışır. Etkisi küçük olabilir ama alışkanlık büyük."""),
code('''from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.experimental import enable_iterative_imputer  # noqa
from sklearn.impute import IterativeImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
def boru(imputer):
    return Pipeline([("impute", imputer), ("olcek", StandardScaler()),
                     ("lr", LogisticRegression(max_iter=2000))])

adaylar = {
    "medyan":                 SimpleImputer(strategy="median"),
    "medyan + gösterge":      SimpleImputer(strategy="median", add_indicator=True),
    "KNN (k=5)":              KNNImputer(n_neighbors=5),
    "MICE (iteratif)":        IterativeImputer(random_state=0, max_iter=10),
    "MICE + gösterge":        IterativeImputer(random_state=0, max_iter=10, add_indicator=True),
}
for ad, imp in adaylar.items():
    s = cross_val_score(boru(imp), X, y, cv=cv, scoring="roc_auc")
    print(f"{ad:22s} ROC-AUC = {s.mean():.3f} ± {s.std():.3f}")'''),
md("""Farklar küçük; bu normal. Ders kitapları imputasyonu büyük bir mesele gibi anlatır ama pratikte **hangi yöntemi seçtiğinizden çok,
eksikliğin neden olduğunu anlamanız** sonucu değiştirir. Göstergeli sürümlerin öne çıkıp çıkmadığına bakın."""),
md("""## 3 · Sızıntı ne kadar kolay? Tamamen rastgele veriyle AUC 0.80

Şimdi kasıtlı bir hata yapacağız. 200 hastalık bir veri seti, **tamamen rastgele** 2000 öznitelik, rastgele etiket.
Hiçbir şey öğrenilemez; doğru AUC 0.50 olmalı. Ama özellik seçimini çapraz doğrulamanın *dışında* yaparsak..."""),
code('''from sklearn.feature_selection import SelectKBest, f_classif

rng = np.random.default_rng(1)
Xr = rng.standard_normal((200, 2000)); yr = rng.integers(0, 2, 200)

# YANLIŞ: en iyi 20 özniteliği tüm veriye bakarak seç, sonra çapraz doğrula
Xsec = SelectKBest(f_classif, k=20).fit_transform(Xr, yr)
yanlis = cross_val_score(LogisticRegression(max_iter=2000), Xsec, yr, cv=cv, scoring="roc_auc").mean()

# DOĞRU: seçim de Pipeline'ın içinde, her katlamada yeniden
dogru_boru = Pipeline([("sec", SelectKBest(f_classif, k=20)), ("lr", LogisticRegression(max_iter=2000))])
dogru = cross_val_score(dogru_boru, Xr, yr, cv=cv, scoring="roc_auc").mean()

print(f"Rastgele veri, seçim dışarıda : ROC-AUC = {yanlis:.3f}   <- sızıntı")
print(f"Rastgele veri, seçim Pipeline  : ROC-AUC = {dogru:.3f}   <- gerçek")'''),
md("""Bu, omik verideki (p ≫ n) en yaygın hatadır ve yayımlanmış makalelerde defalarca görülmüştür. Kural basit:
**test katlamasının etiketine dokunan her adım Pipeline'ın içinde olmalı.** Ölçekleme, imputasyon, özellik seçimi, hepsi."""),
md("""## 4 · Aynı hasta iki kümede: hasta-bazlı bölme

Pima'da her hasta bir satır. Ama EEG segmentleri, çok sayıda görüntü ya da tekrarlayan yatışlarla çalışırken aynı hastadan
onlarca satır olur. Bunu simüle edelim: her hastadan 5 "kayıt" üretelim (küçük gürültüyle), sonra rastgele bölme ile hasta-bazlı
bölmeyi karşılaştıralım. Model olarak bilerek ezberlemeye yatkın bir şey seçiyoruz: k-NN (k=1)."""),
code('''from sklearn.model_selection import KFold, GroupKFold
from sklearn.neighbors import KNeighborsClassifier

Xi = SimpleImputer(strategy="median").fit_transform(X)
rng = np.random.default_rng(2)
tekrar = 5
Xg = np.vstack([Xi + rng.normal(0, 0.02 * Xi.std(axis=0), Xi.shape) for _ in range(tekrar)])
yg = np.tile(y.values, tekrar)
hasta_id = np.tile(np.arange(len(y)), tekrar)

ezber = Pipeline([("olcek", StandardScaler()), ("knn", KNeighborsClassifier(n_neighbors=1))])
rastgele = cross_val_score(ezber, Xg, yg, cv=KFold(5, shuffle=True, random_state=0), scoring="roc_auc").mean()
gruplu   = cross_val_score(ezber, Xg, yg, cv=GroupKFold(5), groups=hasta_id, scoring="roc_auc").mean()

print(f"Rastgele KFold   (aynı hasta iki kümede olabilir): ROC-AUC = {rastgele:.3f}")
print(f"GroupKFold       (hasta tek kümede):               ROC-AUC = {gruplu:.3f}")'''),
md("""> **Deneyin:** Gürültüyü 0.02 yerine 0.3 yapın; rastgele bölmedeki AUC ne kadar düşüyor? Fark sürdükçe model hastalığı değil
> hastayı tanıyor. 7. haftada EEG'de aynı deneyi gerçek kayıtlarla yapacağız."""),
md("""## 5 · Dengesiz sınıf: doğruluk %90 ama model işe yaramıyor

Pozitif oranını yapay olarak %8'e düşürelim (nadir hastalık senaryosu). "Herkes sağlıklı" diyen bir model %92 doğru olur.
Klinik olarak sıfır değeri vardır. Doğruluk yerine PR-AUC ve duyarlılığa bakalım; sınıf ağırlığı ve SMOTE'un ne yaptığını görelim."""),
code('''from sklearn.metrics import average_precision_score, recall_score, accuracy_score, roc_auc_score
from sklearn.model_selection import cross_val_predict

pos = np.where(y == 1)[0]; neg = np.where(y == 0)[0]
rng = np.random.default_rng(3)
sec_pos = rng.choice(pos, size=int(len(neg) * 0.08), replace=False)
idx = np.concatenate([neg, sec_pos]); rng.shuffle(idx)
Xd, yd = X.iloc[idx], y.iloc[idx]
print(f"Örneklem: {len(yd)} hasta, pozitif oranı %{100*yd.mean():.1f}\\n")

def degerlendir(ad, model):
    p = cross_val_predict(model, Xd, yd, cv=cv, method="predict_proba")[:, 1]
    yhat = (p >= 0.5).astype(int)
    print(f"{ad:24s} doğruluk {accuracy_score(yd, yhat):.3f} | duyarlılık {recall_score(yd, yhat):.3f} | "
          f"ROC-AUC {roc_auc_score(yd, p):.3f} | PR-AUC {average_precision_score(yd, p):.3f}")

taban = [("impute", SimpleImputer(strategy="median")), ("olcek", StandardScaler())]
degerlendir("düz lojistik", Pipeline(taban + [("lr", LogisticRegression(max_iter=2000))]))
degerlendir("class_weight='balanced'", Pipeline(taban + [("lr", LogisticRegression(max_iter=2000, class_weight="balanced"))]))
try:
    from imblearn.pipeline import Pipeline as ImbPipeline
    from imblearn.over_sampling import SMOTE
    degerlendir("SMOTE (Pipeline içinde)", ImbPipeline(taban + [("smote", SMOTE(random_state=0)), ("lr", LogisticRegression(max_iter=2000))]))
except ImportError:
    print("imbalanced-learn kurulu değil; SMOTE satırı atlandı (pip install imbalanced-learn)")'''),
md("""Üç şeye dikkat edin. Birincisi, ROC-AUC üç modelde de neredeyse aynı; sıralama gücü değişmedi. İkincisi, duyarlılık düz modelde
çok düşük, ağırlıklı modelde yükseldi; değişen şey aslında **eşik**. Üçüncüsü, SMOTE'un `Pipeline` içinde olması şart: sentetik
örnekler test katlamasına sızarsa PR-AUC yalan söyler.

Klinik sonuç: dengesiz sınıfta yeniden örnekleme çoğu zaman şık bir eşik ayarından fazlasını vermez. Önce eşiği klinik maliyete göre
seçin (4. hafta), sonra hâlâ gerekiyorsa örneklemeye bakın."""),
md("""## 6 · Bugün ne gördük?

| Konu | Bugünkü kanıt | Alışkanlık |
|---|---|---|
| Sıfır = eksik | Pima'da insülinin yarısı | `describe()` yetmez; alan bilgisiyle bak |
| Eksiklik bilgi taşır | Eksiklik oranı sınıfa göre farklı | `add_indicator=True` dene |
| İmputasyon yöntemi | Farklar küçük | Mekanizmayı anla, yöntemi abartma |
| Sızıntı | Rastgele veriyle AUC 0.80 | Etikete dokunan her adım Pipeline'da |
| Hasta-bazlı bölme | KFold vs GroupKFold farkı | Grup kimliğini ilk günden taşı |
| Dengesiz sınıf | Doğruluk yüksek, duyarlılık düşük | PR-AUC + eşik; SMOTE'u Pipeline'da |

**Ders sonrası (isteğe bağlı):** Bölüm 4'te `tekrar=20` ile deneyi yineleyin; Bölüm 5'te eşiği 0.5 yerine 0.2 yapıp
duyarlılık–özgüllük değişimini not edin. Kendi tez verinizde "grup" hangi sütun olurdu, bir cümleyle yazın.
"""),
]

NOTEBOOKS = {"hafta-01": ("Hafta 1 · Uçtan Uca İlk Tur", WEEK01),
             "hafta-02": ("Hafta 2 · Eksik Veri, Sızıntı ve Hasta-Bazlı Bölme", WEEK02)}


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
