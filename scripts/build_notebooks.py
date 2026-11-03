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

# --------------------------------------------------------------------------
# HAFTA 3 — Keşifçi veri analizi, öznitelik mühendisliği ve boyut indirgeme
# --------------------------------------------------------------------------
WEEK03 = [
md("""# Hafta 3 · Veriyi Tanımak: Keşif, Yeni Öznitelikler ve Boyut İndirgeme

**SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka** · Fırat Üniversitesi Yazılım ve Bilişim Araştırma Enstitüsü

Bu hafta model kurmuyoruz. Veriye bakıyoruz, ona sorular soruyoruz, ondan yeni sütunlar türetiyoruz ve çok sütunlu
veriyi iki boyuta indirip resmini çiziyoruz. Dört bölüm var: keşif, yeni öznitelik türetme, özellik seçimi (ve geçen
haftadan tanıdık bir tuzak), PCA ve UMAP.

Veri seti: UCI Heart Disease (Cleveland). 303 hasta, 13 klinik ölçüm, hedef: koroner arter hastalığı var mı?"""),
md("""## 1 · Veriyi yükle ve ilk bakış

Veri setini doğrudan UCI'dan çekiyoruz. İnternet yoksa benzer yapıda sentetik bir veri üretiliyor; kod aynı şekilde çalışır."""),
code('''import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_theme(style="whitegrid", font_scale=0.9)

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
COLS = ["yas", "cinsiyet", "gogus_agrisi", "tansiyon", "kolesterol", "aclik_sekeri", "ekg", "max_nabiz",
        "efor_anjina", "st_depresyon", "st_egim", "damar_sayisi", "talasemi", "hedef"]
try:
    df = pd.read_csv(URL, header=None, names=COLS, na_values="?")
    print("Veri indirildi:", df.shape)
except Exception as e:
    print("İndirme başarısız, sentetik veri üretiliyor:", e)
    rng = np.random.default_rng(0); n = 303
    df = pd.DataFrame({"yas": rng.integers(29, 78, n), "cinsiyet": rng.integers(0, 2, n), "gogus_agrisi": rng.integers(1, 5, n),
        "tansiyon": rng.normal(131, 17, n), "kolesterol": rng.normal(246, 50, n), "aclik_sekeri": rng.integers(0, 2, n),
        "ekg": rng.integers(0, 3, n), "max_nabiz": rng.normal(150, 23, n), "efor_anjina": rng.integers(0, 2, n),
        "st_depresyon": rng.exponential(1, n), "st_egim": rng.integers(1, 4, n), "damar_sayisi": rng.integers(0, 4, n),
        "talasemi": rng.choice([3, 6, 7], n)})
    df["hedef"] = (rng.random(n) < 1 / (1 + np.exp(-(0.05 * (df.yas - 55) + 0.8 * (df.gogus_agrisi == 4) + 0.6 * df.damar_sayisi - 0.02 * (df.max_nabiz - 150) - 1)))).astype(int)

# UCI'da hedef 0–4 arası; 0 = hastalık yok, 1–4 = var. İkili yapıyoruz.
df["hedef"] = (df["hedef"] > 0).astype(int)
print(df["hedef"].value_counts().rename({0: "hastalık yok", 1: "hastalık var"}))
df.head()'''),
md("""İlk bakışta üç soru soruyoruz: kaç satır, kaç sütun, kaç sınıf? Sonra her sütunun ne olduğunu anlamaya çalışıyoruz.
Burada sütunların bir kısmı **sayı** (yaş, kolesterol), bir kısmı aslında **kategori** ama sayıyla kodlanmış (göğüs ağrısı tipi 1–4,
talasemi 3/6/7). Bu ayrımı yapmazsanız model "göğüs ağrısı tipi 4, tip 2'nin iki katı" diye düşünür. Öyle bir şey yok."""),
code('''sayisal = ["yas", "tansiyon", "kolesterol", "max_nabiz", "st_depresyon"]
kategorik = ["cinsiyet", "gogus_agrisi", "aclik_sekeri", "ekg", "efor_anjina", "st_egim", "damar_sayisi", "talasemi"]

print("Eksik değer sayısı:\\n", df.isna().sum()[df.isna().sum() > 0], "\\n")
df[sayisal].describe().round(1)'''),
md("""## 2 · Keşif: dağılımlar ve gruplar arası farklar

Keşifçi analizin amacı basit: veriyi görmek. Hangi değişken iki grupta farklı dağılıyor? Nerede garip bir değer var?
Aşağıdaki grafikte her sayısal değişkeni hastalığı olan ve olmayan gruplar için yan yana çiziyoruz."""),
code('''fig, axes = plt.subplots(1, 5, figsize=(15, 3.4))
for ax, c in zip(axes, sayisal):
    sns.boxplot(data=df, x="hedef", y=c, ax=ax, palette=["#0f9b8e", "#be3a5a"], hue="hedef", legend=False)
    ax.set_xlabel(""); ax.set_xticks([0, 1]); ax.set_xticklabels(["yok", "var"]); ax.set_title(c)
plt.suptitle("Sayısal değişkenler: hastalık yok / var", y=1.03); plt.tight_layout()'''),
md("""**Okuyun:** Hangi kutular belirgin biçimde kayıyor? Maksimum nabız ve ST depresyonu iki grupta ayrışıyor; kolesterol pek ayrışmıyor.
Bu, modeli kurmadan önce hangi değişkenlerin işe yarayacağına dair ilk sezgidir.

Kategorik değişkenler için oran tablosu daha anlamlı: her kategoride hastalık oranı kaç?"""),
code('''fig, axes = plt.subplots(2, 4, figsize=(14, 6))
for ax, c in zip(axes.ravel(), kategorik):
    oran = df.groupby(c)["hedef"].mean()
    oran.plot.bar(ax=ax, color="#2f3fa3"); ax.set_ylim(0, 1); ax.set_ylabel("hastalık oranı"); ax.set_title(c)
    ax.tick_params(axis="x", rotation=0)
plt.suptitle("Kategorik değişkenler: her kategoride hastalık oranı", y=1.02); plt.tight_layout()'''),
md("""Göğüs ağrısı tipi 4 (asemptomatik) ve tıkalı damar sayısı arttıkça hastalık oranı belirgin artıyor. Bir kardiyolog için bu şaşırtıcı değil;
bizim için de iyi haber: veri klinik bilgiyle uyumlu, yani etiket makul görünüyor.

Son olarak sayısal değişkenlerin birbiriyle ilişkisine bakalım. Birbirine çok benzeyen iki sütun varsa bunu bilmek isteriz."""),
code('''plt.figure(figsize=(5.5, 4.5))
sns.heatmap(df[sayisal + ["hedef"]].corr(), annot=True, fmt=".2f", cmap="RdBu_r", vmin=-1, vmax=1, square=True)
plt.title("Korelasyon matrisi"); plt.tight_layout()'''),
md("""## 3 · Yeni öznitelik türetmek

Modelin elindeki sütunlar, hastaneden geldiği hâliyle her zaman en kullanışlı biçimde değildir. Bazen iki sütunu birleştirince
daha anlamlı bir şey çıkar. Buna öznitelik mühendisliği diyoruz; aslında yaptığımız şey klinik bilgiyi sütuna çevirmek.

Üç örnek:
- **Yaşa göre beklenen maksimum nabız:** 220 − yaş. Hastanın ulaştığı nabzın bu beklentiye oranı, "efor kapasitesi" gibi bir şey söyler.
- **Yaş grubu:** 40 altı, 40–55, 55–65, 65 üstü. Bazen yaşın etkisi düz bir çizgi değildir.
- **Risk sayacı:** Yüksek tansiyon, yüksek kolesterol, açlık şekeri yüksek, erkek... kaç risk faktörü bir arada?"""),
code('''df2 = df.copy()
df2["nabiz_orani"] = df2["max_nabiz"] / (220 - df2["yas"])
df2["yas_grubu"] = pd.cut(df2["yas"], bins=[0, 40, 55, 65, 120], labels=[0, 1, 2, 3]).astype(int)
df2["risk_sayaci"] = ((df2["tansiyon"] > 140).astype(int) + (df2["kolesterol"] > 240).astype(int)
                      + df2["aclik_sekeri"] + df2["cinsiyet"])

fig, axes = plt.subplots(1, 3, figsize=(12, 3.4))
sns.boxplot(data=df2, x="hedef", y="nabiz_orani", ax=axes[0], hue="hedef", legend=False, palette=["#0f9b8e", "#be3a5a"]); axes[0].set_title("nabız / (220 − yaş)")
df2.groupby("yas_grubu")["hedef"].mean().plot.bar(ax=axes[1], color="#2f3fa3"); axes[1].set_title("yaş grubuna göre hastalık oranı"); axes[1].tick_params(axis="x", rotation=0)
df2.groupby("risk_sayaci")["hedef"].mean().plot.bar(ax=axes[2], color="#2f3fa3"); axes[2].set_title("risk sayacına göre hastalık oranı"); axes[2].tick_params(axis="x", rotation=0)
plt.tight_layout()'''),
md("""> **Deneyin:** Kendi klinik bilginizle bir öznitelik daha türetin. Örneğin ST depresyonu ile ST eğimini birleştirmek anlamlı mı?
> Türettiğiniz sütunun iki grupta farklı dağılıp dağılmadığına bakın."""),
md("""## 4 · Özellik seçimi: hangi sütunlar kalsın?

Elimizde artık 16 sütun var. Hepsine ihtiyaç var mı? Özellik seçimi bu soruya cevap arar. İki basit yol gösteriyoruz:
istatistiksel bir skorla en iyi k sütunu seçmek (`SelectKBest`) ve bir modelin en az önem verdiği sütunları teker teker atmak (`RFE`).

Geçen haftadan hatırlayın: seçimi çapraz doğrulamanın **dışında** yaparsanız sonucu şişirirsiniz. O yüzden ikisi de `Pipeline` içinde."""),
code('''from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.feature_selection import SelectKBest, f_classif, RFE
from sklearn.model_selection import StratifiedKFold, cross_val_score

X = df2.drop(columns="hedef"); y = df2["hedef"]
cv = StratifiedKFold(5, shuffle=True, random_state=42)
taban = [("impute", SimpleImputer(strategy="median")), ("olcek", StandardScaler())]

def dene(ad, adimlar):
    s = cross_val_score(Pipeline(taban + adimlar), X, y, cv=cv, scoring="roc_auc")
    print(f"{ad:28s} ROC-AUC = {s.mean():.3f} ± {s.std():.3f}")

dene("tüm sütunlar (16)", [("lr", LogisticRegression(max_iter=2000))])
for k in [4, 8, 12]:
    dene(f"SelectKBest k={k}", [("sec", SelectKBest(f_classif, k=k)), ("lr", LogisticRegression(max_iter=2000))])
dene("RFE 8 sütun", [("sec", RFE(LogisticRegression(max_iter=2000), n_features_to_select=8)), ("lr", LogisticRegression(max_iter=2000))])'''),
md("""Hangi sütunların seçildiğine de bakalım. Tüm veriye uydurup (yalnızca görmek için, başarım ölçmüyoruz) seçilenleri yazdırıyoruz."""),
code('''sec = Pipeline(taban + [("sec", SelectKBest(f_classif, k=8))]).fit(X, y)
secilen = X.columns[sec.named_steps["sec"].get_support()]
print("SelectKBest'in seçtiği 8 sütun:", list(secilen))
rfe = Pipeline(taban + [("sec", RFE(LogisticRegression(max_iter=2000), n_features_to_select=8))]).fit(X, y)
print("RFE'nin seçtiği 8 sütun:      ", list(X.columns[rfe.named_steps["sec"].get_support()]))'''),
md("""İki yöntem tamamen aynı listeyi vermez; bu normal. Türettiğimiz özniteliklerden hangileri seçildi? Seçildiyse klinik bilgiyi
sütuna çevirmek işe yaramış demektir."""),
md("""## 5 · Boyut indirgeme: 16 sütunu 2 boyutta görmek

16 sütunlu bir veriyi gözle göremeyiz. Boyut indirgeme, veriyi mümkün olduğunca az bilgi kaybıyla 2 boyuta sıkıştırır ki çizebilelim.

**PCA** bunu düz çizgilerle yapar: verinin en çok yayıldığı yönü bulur, ona "1. bileşen" der; ona dik en çok yayılan yönü bulur, "2. bileşen" der.
Her bileşenin verideki toplam değişimin yüzde kaçını taşıdığını söyleyebilir. Bu dürüst bir yöntemdir; neyi attığını bilirsiniz."""),
code('''from sklearn.decomposition import PCA

Xs = Pipeline(taban).fit_transform(X)
pca = PCA().fit(Xs)
kum = np.cumsum(pca.explained_variance_ratio_)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
axes[0].bar(range(1, len(kum) + 1), pca.explained_variance_ratio_, color="#bcc6d9", label="bileşen başına")
axes[0].plot(range(1, len(kum) + 1), kum, "o-", color="#2f3fa3", label="birikimli")
axes[0].axhline(0.8, ls="--", c="gray", lw=1); axes[0].set_xlabel("bileşen"); axes[0].set_ylabel("açıklanan varyans oranı"); axes[0].legend(); axes[0].set_title("Kaç bileşen yeter?")
Z = pca.transform(Xs)[:, :2]
axes[1].scatter(Z[y == 0, 0], Z[y == 0, 1], s=18, c="#0f9b8e", label="hastalık yok", alpha=.7)
axes[1].scatter(Z[y == 1, 0], Z[y == 1, 1], s=18, c="#be3a5a", label="hastalık var", alpha=.7)
axes[1].set_xlabel(f"PC1 (%{100*pca.explained_variance_ratio_[0]:.0f})"); axes[1].set_ylabel(f"PC2 (%{100*pca.explained_variance_ratio_[1]:.0f})")
axes[1].legend(); axes[1].set_title("İlk iki bileşen")
plt.tight_layout()
print(f"Varyansın %80'i için gereken bileşen sayısı: {int(np.argmax(kum >= 0.8)) + 1}")'''),
md("""Sol grafik "kaç bileşen yeter?" sorusuna cevap verir. Sağ grafikte iki grup kısmen ayrılıyor ama iç içe; bu veri setinde hastalık
tek bir yöne sığmıyor. Hangi ölçümlerin PC1'i oluşturduğuna bakmak da öğreticidir: buna **yükleme** deniyor. Aşağıda göreceğiniz gibi
bir uçta maksimum nabız, diğer uçta ST depresyonu, efor anjinası, yaş ve damar sayısı var: PCA kendi başına bir "hastalık yükü" ekseni bulmuş."""),
code('''yukleme = pd.Series(pca.components_[0], index=X.columns).sort_values()
plt.figure(figsize=(6, 4.5)); yukleme.plot.barh(color=np.where(yukleme > 0, "#be3a5a", "#0f9b8e"))
plt.title("PC1'i oluşturan sütunlar (yüklemeler)"); plt.xlabel("ağırlık"); plt.tight_layout()'''),
md("""**UMAP** ise eğri yolları da kullanır. Amacı birbirine yakın hastaları yakın, uzak olanları uzak tutmaktır; ama "uzaklık" kavramı
burada esnektir. Çok güzel resimler çıkarır ve o yüzden tehlikelidir: iki kümenin arasındaki boşluğun genişliği, kümelerin şekli,
hiçbiri sayısal olarak yorumlanamaz. UMAP keşif içindir, kanıt için değil."""),
code('''try:
    import umap
    emb = umap.UMAP(n_neighbors=15, min_dist=0.1, random_state=0).fit_transform(Xs)
    baslik = "UMAP"
except ImportError:
    from sklearn.manifold import TSNE
    emb = TSNE(perplexity=30, random_state=0).fit_transform(Xs)
    baslik = "t-SNE (umap-learn kurulu değil)"

fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
axes[0].scatter(emb[y == 0, 0], emb[y == 0, 1], s=18, c="#0f9b8e", alpha=.7, label="hastalık yok")
axes[0].scatter(emb[y == 1, 0], emb[y == 1, 1], s=18, c="#be3a5a", alpha=.7, label="hastalık var")
axes[0].set_title(f"{baslik} · hedefe göre renk"); axes[0].legend(); axes[0].set_xticks([]); axes[0].set_yticks([])
sc = axes[1].scatter(emb[:, 0], emb[:, 1], s=18, c=X["gogus_agrisi"], cmap="viridis", alpha=.8)
axes[1].set_title(f"{baslik} · göğüs ağrısı tipine göre renk"); axes[1].set_xticks([]); axes[1].set_yticks([])
plt.colorbar(sc, ax=axes[1], label="göğüs ağrısı tipi"); plt.tight_layout()'''),
md("""> **Deneyin:** `n_neighbors` değerini 5 ve 50 yapın. Resim ne kadar değişiyor? Değişiyorsa gördüğünüz kümeler verinin mi,
> parametrenin mi eseri? Bu soruyu her UMAP grafiğinde sormalısınız."""),
md("""## 6 · Bugün ne gördük?

| Adım | Ne yaptık | Alışkanlık |
|---|---|---|
| İlk bakış | Satır, sütun, sınıf; sayısal mı kategorik mi | Sayıyla kodlanmış kategorilere dikkat |
| Keşif | Kutu grafikleri, oran tabloları, korelasyon | Modelden önce veriye bak; etiket klinikle uyumlu mu? |
| Yeni öznitelik | nabız oranı, yaş grubu, risk sayacı | Klinik bilgiyi sütuna çevir |
| Özellik seçimi | SelectKBest, RFE, hepsi Pipeline içinde | Seçim de çapraz doğrulamanın içinde |
| PCA | Açıklanan varyans, yüklemeler | Kaç bileşen yettiğini söyle, neyi attığını bil |
| UMAP | 2 boyutlu harita | Keşif için kullan, kanıt sayma |

**Ders sonrası (isteğe bağlı):** Bölüm 3'te kendi özniteliğinizi ekleyip Bölüm 4'te seçilip seçilmediğine bakın.
Bölüm 5'te UMAP'i üç farklı `random_state` ile çalıştırın; kümeler yerinde duruyor mu?
"""),
]

# --------------------------------------------------------------------------
# HAFTA 4 — Denetimli öğrenme ve klinik metrikler
# --------------------------------------------------------------------------
WEEK04 = [
md("""# Hafta 4 · İlk Model ve "İyi mi?" Sorusu: Klinik Metrikler

**SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka** · Fırat Üniversitesi Yazılım ve Bilişim Araştırma Enstitüsü

Bugün ilk gerçek modelimizi kuruyoruz ve asıl soruyu soruyoruz: bu model iyi mi? "Yüzde 85 doğru" cevabı yetmez.
Beş bölüm: model, karışıklık matrisi ve eşik, ROC ile PR eğrileri, kalibrasyon, karar eğrisi.

Veri: geçen haftaki Heart Disease (Cleveland). 303 hasta, hedef: koroner arter hastalığı."""),
code('''import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

URL = "https://archive.ics.uci.edu/ml/machine-learning-databases/heart-disease/processed.cleveland.data"
COLS = ["yas", "cinsiyet", "gogus_agrisi", "tansiyon", "kolesterol", "aclik_sekeri", "ekg", "max_nabiz",
        "efor_anjina", "st_depresyon", "st_egim", "damar_sayisi", "talasemi", "hedef"]
try:
    df = pd.read_csv(URL, header=None, names=COLS, na_values="?"); print("Veri indirildi:", df.shape)
except Exception as e:
    print("İndirme başarısız, sentetik veri üretiliyor:", e)
    rng = np.random.default_rng(0); n = 303
    df = pd.DataFrame({"yas": rng.integers(29, 78, n), "cinsiyet": rng.integers(0, 2, n), "gogus_agrisi": rng.integers(1, 5, n),
        "tansiyon": rng.normal(131, 17, n), "kolesterol": rng.normal(246, 50, n), "aclik_sekeri": rng.integers(0, 2, n),
        "ekg": rng.integers(0, 3, n), "max_nabiz": rng.normal(150, 23, n), "efor_anjina": rng.integers(0, 2, n),
        "st_depresyon": rng.exponential(1, n), "st_egim": rng.integers(1, 4, n), "damar_sayisi": rng.integers(0, 4, n),
        "talasemi": rng.choice([3, 6, 7], n)})
    df["hedef"] = (rng.random(n) < 1 / (1 + np.exp(-(0.05 * (df.yas - 55) + 0.8 * (df.gogus_agrisi == 4) + 0.6 * df.damar_sayisi - 0.02 * (df.max_nabiz - 150) - 1)))).astype(int)
df["hedef"] = (df["hedef"] > 0).astype(int)
X = df.drop(columns="hedef"); y = df["hedef"]
print(f"Hastalık oranı: %{100*y.mean():.0f}")'''),
md("""## 1 · İlk model: lojistik regresyon

Lojistik regresyon, her hasta için 0 ile 1 arasında bir **olasılık** üretir: "bu hastada hastalık olma olasılığı 0.72".
Bu olasılığı bir eşikle (çoğu zaman 0.5) evet/hayır'a çeviririz. Bugün göreceğiz ki asıl iş o eşikte.

Çapraz doğrulamayla her hastanın olasılığını, o hasta modelin **görmediği** katlamadayken alıyoruz (`cross_val_predict`)."""),
code('''from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict

cv = StratifiedKFold(5, shuffle=True, random_state=42)
model = Pipeline([("impute", SimpleImputer(strategy="median")), ("olcek", StandardScaler()),
                  ("lr", LogisticRegression(max_iter=2000))])
p = cross_val_predict(model, X, y, cv=cv, method="predict_proba")[:, 1]
print("İlk 8 hastanın olasılığı:", np.round(p[:8], 2))
print("Gerçek etiketleri:       ", y.values[:8])'''),
md("""## 2 · Karışıklık matrisi ve eşik

Eşik 0.5 deyince dört grup oluşur: doğru pozitif, yanlış pozitif, doğru negatif, yanlış negatif. Buradan dört sayı türer:

- **Duyarlılık** — hastaların kaçını yakaladık?
- **Özgüllük** — sağlıklıların kaçını doğru bıraktık?
- **PPV** — "hasta" dediklerimizin kaçı gerçekten hasta?
- **NPV** — "sağlıklı" dediklerimizin kaçı gerçekten sağlıklı?

Eşiği değiştirince bu dört sayı birlikte değişir. Aşağıda üç farklı eşikte görüyoruz."""),
code('''from sklearn.metrics import confusion_matrix

def dort_sayi(y, p, esik):
    yhat = (p >= esik).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, yhat).ravel()
    return dict(esik=esik, duyarlilik=tp/(tp+fn), ozgulluk=tn/(tn+fp), PPV=tp/(tp+fp), NPV=tn/(tn+fn),
                dogruluk=(tp+tn)/len(y), yanlis_pozitif=fp, yanlis_negatif=fn)

pd.DataFrame([dort_sayi(y, p, e) for e in [0.2, 0.5, 0.8]]).round(3).set_index("esik")'''),
md("""**Okuyun:** Eşik 0.2'de neredeyse hiç hasta kaçmıyor ama çok sağlıklıya "hasta" diyoruz. Eşik 0.8'de tam tersi.
Hangisi doğru? Sorunun cevabı matematikte değil, klinikte: bir hastayı kaçırmanın bedeli mi büyük, gereksiz anjiyografinin mi?

> **Deneyin:** Eşik listesine 0.35 ve 0.65 ekleyin. Doğruluk hangi eşikte en yüksek? O eşik klinik olarak da en iyi mi?"""),
md("""## 3 · Tüm eşikleri aynı anda görmek: ROC ve PR eğrileri

Her eşik için bir duyarlılık–özgüllük çifti var. Hepsini çizince **ROC eğrisi** çıkar; altındaki alan (AUC) eşikten bağımsız
tek bir özet verir: "rastgele bir hasta ile rastgele bir sağlıklıyı alsam, model hastayı daha yüksek sıralar mı?"

**PR eğrisi** ise duyarlılık ile PPV'yi çizer. Pozitif sınıf nadirse (geçen haftaki %7'lik örnek gibi) ROC iyimser görünür,
PR gerçeği söyler. Burada sınıflar dengeli; ikisi de benzer hikâye anlatır."""),
code('''from sklearn.metrics import roc_curve, roc_auc_score, precision_recall_curve, average_precision_score

fpr, tpr, _ = roc_curve(y, p)
prec, rec, _ = precision_recall_curve(y, p)
fig, ax = plt.subplots(1, 2, figsize=(10, 4))
ax[0].plot(fpr, tpr, lw=2, c="#2f3fa3", label=f"AUC = {roc_auc_score(y, p):.3f}")
ax[0].plot([0, 1], [0, 1], "--", c="gray", lw=1, label="rastgele")
ax[0].set(xlabel="1 − özgüllük (yanlış pozitif oranı)", ylabel="duyarlılık", title="ROC eğrisi"); ax[0].legend()
ax[1].plot(rec, prec, lw=2, c="#0f9b8e", label=f"PR-AUC = {average_precision_score(y, p):.3f}")
ax[1].axhline(y.mean(), ls="--", c="gray", lw=1, label=f"rastgele = prevalans {y.mean():.2f}")
ax[1].set(xlabel="duyarlılık", ylabel="PPV (kesinlik)", title="PR eğrisi"); ax[1].legend()
plt.tight_layout()'''),
md("""## 4 · Kalibrasyon: model "0.70" diyorsa gerçekten %70 mi?

AUC modelin **sıralama** gücünü ölçer. Ama klinikte olasılığın kendisi de kullanılır: "riskiniz %70" denir.
Bu sayı doğru mu? Kalibrasyon eğrisi bunu sınar: 0.6–0.7 arası olasılık verilen hastaların gerçekten %60–70'i hasta mı?

**Brier skoru** bunun tek sayılık özeti: olasılık ile gerçek (0/1) arasındaki kare farkın ortalaması. Küçük iyi."""),
code('''from sklearn.calibration import calibration_curve, CalibratedClassifierCV
from sklearn.metrics import brier_score_loss

gozlenen, tahmin = calibration_curve(y, p, n_bins=8, strategy="quantile")
fig, ax = plt.subplots(figsize=(5, 4.5))
ax.plot(tahmin, gozlenen, "o-", c="#2f3fa3", label=f"lojistik (Brier = {brier_score_loss(y, p):.3f})")
ax.plot([0, 1], [0, 1], "--", c="gray", lw=1, label="mükemmel kalibrasyon")
ax.set(xlabel="modelin verdiği olasılık", ylabel="gözlenen hastalık oranı", title="Kalibrasyon eğrisi"); ax.legend()
plt.tight_layout()'''),
md("""Lojistik regresyon genellikle doğuştan iyi kalibredir. Ağaç toplulukları ve sinir ağları öyle değildir; onlar için sonradan
kalibrasyon (Platt ya da izotonik) gerekir. Aşağıda bilerek kötü kalibre bir model (Random Forest) alıp düzeltiyoruz."""),
code('''from sklearn.ensemble import RandomForestClassifier

rf = Pipeline([("impute", SimpleImputer(strategy="median")), ("rf", RandomForestClassifier(300, random_state=0))])
p_rf = cross_val_predict(rf, X, y, cv=cv, method="predict_proba")[:, 1]
rf_kal = Pipeline([("impute", SimpleImputer(strategy="median")),
                   ("rf", CalibratedClassifierCV(RandomForestClassifier(300, random_state=0), method="isotonic", cv=5))])
p_rfk = cross_val_predict(rf_kal, X, y, cv=cv, method="predict_proba")[:, 1]

fig, ax = plt.subplots(figsize=(5, 4.5))
for q, ad, c in [(p, "lojistik", "#2f3fa3"), (p_rf, "Random Forest", "#be3a5a"), (p_rfk, "RF + izotonik", "#0f9b8e")]:
    g, t = calibration_curve(y, q, n_bins=8, strategy="quantile")
    ax.plot(t, g, "o-", c=c, label=f"{ad} (AUC {roc_auc_score(y, q):.2f}, Brier {brier_score_loss(y, q):.3f})")
ax.plot([0, 1], [0, 1], "--", c="gray", lw=1); ax.set(xlabel="modelin verdiği olasılık", ylabel="gözlenen oran", title="Kalibrasyon karşılaştırması")
ax.legend(fontsize=8); plt.tight_layout()'''),
md("""**Okuyun:** AUC'ler birbirine yakın ama eğriler farklı. Aynı sıralama gücüne sahip iki modelden biri "%70" derken
yanılıyor olabilir. Klinik karar destekte bu, AUC kadar önemlidir."""),
md("""## 5 · Karar eğrisi: model kullanmaya değer mi?

Son soru en pratik olanı. Diyelim bir hekim "riski %20'nin üstünde olanı anjiyografiye gönderirim" diyor. Modeli kullanmak,
"herkesi gönder" ya da "kimseyi gönderme" stratejilerinden daha fazla **net fayda** sağlıyor mu?
Karar eğrisi analizi bunu her eşik için çizer. Model eğrisi iki düz stratejinin üstündeyse, o eşik aralığında model işe yarar."""),
code('''def net_fayda(y, p, esikler):
    n = len(y); out = []
    for t in esikler:
        yhat = p >= t
        tp = np.sum(yhat & (y == 1)); fp = np.sum(yhat & (y == 0))
        out.append(tp / n - fp / n * t / (1 - t))
    return np.array(out)

esikler = np.linspace(0.05, 0.8, 40)
prev = y.mean()
herkes = prev - (1 - prev) * esikler / (1 - esikler)
fig, ax = plt.subplots(figsize=(6, 4.2))
ax.plot(esikler, net_fayda(y.values, p, esikler), lw=2, c="#2f3fa3", label="model (lojistik)")
ax.plot(esikler, herkes, c="#be3a5a", lw=1.5, label="herkesi tedavi et")
ax.axhline(0, c="gray", lw=1.5, label="kimseyi tedavi etme")
ax.set(xlabel="eşik olasılığı", ylabel="net fayda", title="Karar eğrisi analizi", ylim=(-0.05, prev + 0.05)); ax.legend()
plt.tight_layout()'''),
md("""## 6 · Bugün ne gördük?

| Soru | Araç | Ne söyler |
|---|---|---|
| Hastaları yakalıyor mu? | Duyarlılık, özgüllük, PPV, NPV | Seçilen eşikte dört sayı |
| Sıralama gücü ne? | ROC-AUC, PR-AUC | Eşikten bağımsız özet; nadir sınıfta PR |
| Olasılık doğru mu? | Kalibrasyon eğrisi, Brier | "%70" gerçekten %70 mi |
| Kullanmaya değer mi? | Karar eğrisi | Hangi eşik aralığında net fayda var |

**Ders sonrası (isteğe bağlı):** Bölüm 2'de kendi klinik senaryonuz için bir eşik seçin ve gerekçesini iki cümleyle yazın.
Bölüm 4'te `method="sigmoid"` (Platt) ile izotonik kalibrasyonu karşılaştırın. Proje veri setinizde aynı dört grafiği çizin; bu, raporunuzun Sonuçlar bölümünün iskeleti.
"""),
]

# --------------------------------------------------------------------------
# HAFTA 5 — Topluluk yöntemleri, SVM ve öznitelik önemi
# --------------------------------------------------------------------------
WEEK05 = [
md("""# Hafta 5 · Daha Güçlü Modeller: Ağaç Toplulukları, SVM ve "Model Neye Bakıyor?"

**SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka** · Fırat Üniversitesi Yazılım ve Bilişim Araştırma Enstitüsü

Geçen hafta tek bir basit model kurduk ve onu dört soruyla sınadık. Bugün daha güçlü modeller geliyor: Random Forest, XGBoost ve SVM.
Hepsini aynı dört soruyla sınayacağız; sonra da "model neye bakıyor?" sorusuna üç farklı cevap alıp birbirine benzeyip benzemediğine bakacağız.

Veri: **Heart Failure Clinical Records** (UCI). 299 kalp yetmezliği hastası, 12 klinik ölçüm, hedef: takip süresinde ölüm.
Defterin sonunda bir de bonus var: tamamen uydurma bir Fenerbahçe veri seti. 🙂"""),
code('''import warnings; warnings.filterwarnings("ignore")
import io, zipfile, urllib.request
import numpy as np, pandas as pd
import matplotlib.pyplot as plt

URL = "https://archive.ics.uci.edu/static/public/519/heart+failure+clinical+records.zip"
try:
    z = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(URL, timeout=30).read()))
    df = pd.read_csv(z.open([n for n in z.namelist() if n.endswith(".csv")][0]))
    print("Veri indirildi:", df.shape)
except Exception as e:
    print("İndirme başarısız, sentetik veri üretiliyor:", e)
    rng = np.random.default_rng(0); n = 299
    df = pd.DataFrame({"age": rng.normal(61, 12, n).clip(40, 95), "anaemia": rng.integers(0, 2, n), "creatinine_phosphokinase": rng.lognormal(5.5, 1, n),
        "diabetes": rng.integers(0, 2, n), "ejection_fraction": rng.normal(38, 12, n).clip(14, 80), "high_blood_pressure": rng.integers(0, 2, n),
        "platelets": rng.normal(263000, 97000, n), "serum_creatinine": rng.lognormal(0.2, 0.5, n), "serum_sodium": rng.normal(137, 4, n),
        "sex": rng.integers(0, 2, n), "smoking": rng.integers(0, 2, n), "time": rng.integers(4, 285, n)})
    df["DEATH_EVENT"] = (rng.random(n) < 1 / (1 + np.exp(-(0.04 * (df.age - 60) - 0.06 * (df.ejection_fraction - 38) + 0.8 * (df.serum_creatinine - 1.4) - 0.012 * (df.time - 130))))).astype(int)

TR = {"age": "yas", "anaemia": "anemi", "creatinine_phosphokinase": "cpk", "diabetes": "diyabet", "ejection_fraction": "ejeksiyon_fraksiyonu",
      "high_blood_pressure": "hipertansiyon", "platelets": "trombosit", "serum_creatinine": "serum_kreatinin", "serum_sodium": "serum_sodyum",
      "sex": "cinsiyet", "smoking": "sigara", "time": "takip_gun", "DEATH_EVENT": "olum"}
df = df.rename(columns=TR)
print(df["olum"].value_counts().rename({0: "sağ", 1: "öldü"}))
df.head()'''),
md("""## 1 · Bir tuzak: `takip_gun` sütunu

Her hastanın "takip süresi" var: kaç gün izlendiği. Ölen hastalar genellikle erken ölür, yani takip süresi kısadır. Bu sütunu modele
verirseniz model çok başarılı görünür. Ama bir hasta ilk geldiğinde takip süresini bilmiyorsunuz; o bilgi **gelecekten** geliyor.
Bu, 2. haftada konuştuğumuz zamansal sızıntının ders kitabı örneği. Aşağıda etkisini gösterip sonra sütunu çıkarıyoruz."""),
code('''from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

cv = StratifiedKFold(5, shuffle=True, random_state=42)
y = df["olum"]
lr = lambda: Pipeline([("olcek", StandardScaler()), ("lr", LogisticRegression(max_iter=2000))])
ile  = cross_val_score(lr(), df.drop(columns="olum"), y, cv=cv, scoring="roc_auc").mean()
siz  = cross_val_score(lr(), df.drop(columns=["olum", "takip_gun"]), y, cv=cv, scoring="roc_auc").mean()
print(f"takip_gun İLE  : ROC-AUC = {ile:.3f}   <- gelecekten gelen bilgi")
print(f"takip_gun OLMADAN: ROC-AUC = {siz:.3f}   <- gerçekçi")
X = df.drop(columns=["olum", "takip_gun"])'''),
md("""## 2 · Dört model, aynı dört soru

Lojistik regresyon (geçen haftanın temel modeli), Random Forest, XGBoost ve RBF çekirdekli SVM. Hepsi aynı çapraz doğrulamada,
hepsi geçen haftanın ölçütleriyle: ROC-AUC, PR-AUC, Brier. Ağaç modelleri ölçekleme istemez; SVM ve lojistik ister. Hepsini
`Pipeline` içine koyuyoruz, böylece karşılaştırma adil."""),
code('''from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.model_selection import cross_validate

modeller = {
    "Lojistik regresyon": Pipeline([("olcek", StandardScaler()), ("m", LogisticRegression(max_iter=2000))]),
    "Random Forest":      RandomForestClassifier(n_estimators=500, min_samples_leaf=3, random_state=0),
    "XGBoost":            XGBClassifier(n_estimators=300, learning_rate=0.05, max_depth=3, subsample=0.8, colsample_bytree=0.8,
                                        random_state=0, eval_metric="logloss"),
    "SVM (RBF)":          Pipeline([("olcek", StandardScaler()), ("m", SVC(C=1.0, gamma="scale", probability=True, random_state=0))]),
}
skor = {"roc_auc": "roc_auc", "pr_auc": "average_precision", "brier": "neg_brier_score"}
satirlar = []
for ad, m in modeller.items():
    r = cross_validate(m, X, y, cv=cv, scoring=skor)
    satirlar.append({"model": ad, "ROC-AUC": r["test_roc_auc"].mean(), "±": r["test_roc_auc"].std(),
                     "PR-AUC": r["test_pr_auc"].mean(), "Brier": -r["test_brier"].mean()})
pd.DataFrame(satirlar).set_index("model").round(3)'''),
md("""**Okuyun:** Dört model birbirine yakın mı? 299 hastalık küçük veride genellikle öyledir; karmaşık modelin avantajı veri büyüdükçe ortaya çıkar.
Standart sapmalara bakın: fark, katlamalar arası dalgalanmadan büyük mü? Değilse "X modeli daha iyi" demek için kanıt yok.

> **Deneyin:** Random Forest'ta `min_samples_leaf=1` yapın (ağaçlar her hastayı ezberleyebilsin). ROC-AUC değişti mi, Brier ne oldu?"""),
md("""## 3 · Ayar düğmeleri: hiperparametre arama

XGBoost'un düğmeleri var: ağaç sayısı, derinlik, öğrenme oranı. Bunları **test verisine bakarak** ayarlamak sızıntıdır. Doğru yol:
arama da çapraz doğrulamanın içinde. Aşağıda rastgele arama yapıyoruz; iç içe (nested) sürümü derste tartışacağız."""),
code('''from sklearn.model_selection import RandomizedSearchCV
from scipy.stats import randint, uniform

arama = RandomizedSearchCV(
    XGBClassifier(random_state=0, eval_metric="logloss"),
    {"n_estimators": randint(100, 600), "max_depth": randint(2, 6), "learning_rate": uniform(0.01, 0.2),
     "subsample": uniform(0.6, 0.4), "colsample_bytree": uniform(0.5, 0.5), "min_child_weight": randint(1, 8)},
    n_iter=25, cv=cv, scoring="roc_auc", random_state=0, n_jobs=-1).fit(X, y)
print("En iyi ayar:", {k: round(v, 3) if isinstance(v, float) else v for k, v in arama.best_params_.items()})
print(f"En iyi ROC-AUC (iç CV): {arama.best_score_:.3f}  — bu sayı iyimserdir; dış CV ile doğrulanmalı")'''),
md("""## 4 · Model neye bakıyor? Üç öznitelik önemi, üç liste

Aynı Random Forest'a üç farklı soru soruyoruz:
1. **Safsızlık temelli** (ağacın kendi hesabı): hangi sütun dallanmalarda en çok işe yaradı? Hızlı ama sürekli ve çok değerli sütunlara yanlı.
2. **Permütasyon** (geçen haftalardan tanıdık): bir sütunu karıştırınca AUC ne kadar düşüyor?
3. **Lojistik regresyonun katsayıları** (standartlaştırılmış): basit modelin gözünden aynı soru.

Üç liste aynı çıkmaz. Hangisi doğru? Hepsi, farklı sorulara cevap veriyorlar."""),
code('''from sklearn.inspection import permutation_importance

rf = RandomForestClassifier(n_estimators=500, min_samples_leaf=3, random_state=0).fit(X, y)
safsizlik = pd.Series(rf.feature_importances_, index=X.columns)
perm = permutation_importance(rf, X, y, n_repeats=30, random_state=0, scoring="roc_auc")
permutasyon = pd.Series(perm.importances_mean, index=X.columns)
lrm = Pipeline([("olcek", StandardScaler()), ("lr", LogisticRegression(max_iter=2000))]).fit(X, y)
katsayi = pd.Series(np.abs(lrm.named_steps["lr"].coef_[0]), index=X.columns)

fig, ax = plt.subplots(1, 3, figsize=(14, 4.2))
for a, (s, baslik, c) in zip(ax, [(safsizlik, "RF safsızlık önemi", "#bcc6d9"), (permutasyon, "RF permütasyon önemi (AUC kaybı)", "#2f3fa3"), (katsayi, "Lojistik |katsayı|", "#0f9b8e")]):
    s.sort_values().plot.barh(ax=a, color=c); a.set_title(baslik)
plt.tight_layout()'''),
md("""**Okuyun:** Serum kreatinin ve ejeksiyon fraksiyonu üç listede de üstte mi? Trombosit ve CPK safsızlık listesinde yukarıda ama
permütasyonda aşağıdaysa, bu safsızlık yönteminin "çok farklı değer alan sütunları sever" yanlılığıdır.

## 5 · Tuzak: birbirine benzeyen iki sütun önemi paylaşır

Şimdi küçük bir deney. Serum kreatininin neredeyse kopyası olan yeni bir sütun ekleyelim: `kreatinin_kopya` (küçük gürültüyle).
Klinikte bu çok olur: kreatinin ve eGFR, kilo ve VKİ, hemoglobin ve hematokrit. Ne olacak?"""),
code('''rng = np.random.default_rng(1)
X2 = X.copy(); X2["kreatinin_kopya"] = X2["serum_kreatinin"] * (1 + rng.normal(0, 0.05, len(X2)))
rf2 = RandomForestClassifier(n_estimators=500, min_samples_leaf=3, random_state=0).fit(X2, y)
p2 = permutation_importance(rf2, X2, y, n_repeats=30, random_state=0, scoring="roc_auc")
karsilastir = pd.DataFrame({"tek başına (önce)": permutasyon, "kopya eklenince": pd.Series(p2.importances_mean, index=X2.columns)}).round(4)
karsilastir.loc[["serum_kreatinin", "kreatinin_kopya", "ejeksiyon_fraksiyonu", "yas"]]'''),
md("""Serum kreatininin önemi "aniden" düştü; kaybolmadı, kopyasıyla paylaşıldı. Bir modelin "X sütunu önemsiz" demesi, X'in bilgisinin başka
bir sütunda da bulunmadığı anlamına gelmez. Bu, 12. haftada SHAP ile geri döneceğimiz bir konu.

> **Deneyin:** `kreatinin_kopya`yı çıkarıp `ejeksiyon_fraksiyonu`nun kopyasını ekleyin. Aynı paylaşım orada da oluyor mu?"""),
md("""## 6 · Bonus: Fenerbahçe ve taraftar morali (tamamen uydurma veri) 🟡🔵

Bugün moraller biraz düşük olabilir; o yüzden konuyu bir de uydurma bir veri setinde görelim. Aşağıdaki 400 maç **tamamen sentetik**:
hiçbir gerçek maç, hakem ya da futbolcuyla ilgisi yoktur. Gerçek olaylarla benzerlik tamamen tesadüftür (ya da değildir 🙂).

Sütunlar: rakip gücü, deplasman mı, maç saati, son 5 maç formu, sakat sayısı, hakemin "ilginç" karar sayısı, maç öncesi taraftar umudu
ve son olarak **ertesi gün taraftar moral skoru** (0–100). Hedefimiz ikili: moral 50'nin altına düştü mü?

Dikkat ederseniz "taraftar umudu" ile "son 5 maç formu" birbirine çok benziyor. Bölüm 5'teki tuzağı burada yeniden göreceğiz."""),
code('''rng = np.random.default_rng(1907)
n = 400
fb = pd.DataFrame({
    "rakip_gucu":        rng.uniform(1, 10, n).round(1),           # 10 = en güçlü
    "deplasman":         rng.integers(0, 2, n),
    "mac_saati":         rng.choice([19, 20, 21, 22], n),
    "son5_form":         rng.integers(0, 16, n),                    # son 5 maçtan alınan puan
    "sakat_sayisi":      rng.poisson(2, n),
    "ilginc_hakem_karar": rng.poisson(1.2, n),
    "sampiyonlar_ligi":  rng.integers(0, 2, n),
})
fb["taraftar_umudu"] = (fb["son5_form"] * 5 + rng.normal(0, 6, n) + 20).clip(0, 100).round()   # forma çok benzer
# Gizli "gerçek": moral neye bağlı? (modelin bunu bulup bulamayacağını göreceğiz)
gol_farki = (-0.45 * (fb["rakip_gucu"] - 5.5) - 0.6 * fb["deplasman"] + 0.08 * (fb["son5_form"] - 7.5) - 0.25 * (fb["sakat_sayisi"] - 2)
             - 0.4 * (fb["ilginc_hakem_karar"] - 1.2) - 0.8 * fb["sampiyonlar_ligi"] + rng.normal(0, 1.2, n))   # mac_saati kasıtlı olarak yok
fb["moral_ertesi_gun"] = (50 + 12 * gol_farki + 0.15 * fb["taraftar_umudu"] + rng.normal(0, 8, n)).clip(0, 100).round()
fb["moral_dustu"] = (fb["moral_ertesi_gun"] < 50).astype(int)
print(f"{n} uydurma maç · moral düşüşü oranı: %{100*fb.moral_dustu.mean():.0f}")
fb.head()'''),
code('''fig, ax = plt.subplots(1, 3, figsize=(14, 3.8))
fb.groupby("sampiyonlar_ligi")["moral_dustu"].mean().rename({0: "Lig", 1: "Şampiyonlar Ligi"}).plot.bar(ax=ax[0], color=["#0f9b8e", "#2f3fa3"]); ax[0].set_title("Moral düşüşü oranı"); ax[0].tick_params(axis="x", rotation=0)
ax[1].scatter(fb["rakip_gucu"], fb["moral_ertesi_gun"], s=12, c=np.where(fb.deplasman == 1, "#be3a5a", "#0f9b8e"), alpha=.6); ax[1].set(xlabel="rakip gücü", ylabel="ertesi gün moral", title="Rakip gücü vs moral (kırmızı: deplasman)")
ax[2].scatter(fb["son5_form"], fb["taraftar_umudu"], s=12, c="#b7791f", alpha=.6); ax[2].set(xlabel="son 5 maç formu", ylabel="taraftar umudu", title="Birbirine çok benzeyen iki sütun")
plt.tight_layout()'''),
md("""Şimdi bugünün üç modelini bu veride çalıştıralım ve "model neye bakıyor?" sorusunu soralım. Doğru cevabı biliyoruz, çünkü veriyi biz ürettik:
moral en çok rakip gücüne, Şampiyonlar Ligi'ne, deplasmana ve hakem kararlarına bağlı. Taraftar umudu ise formun kopyası."""),
code('''Xf = fb.drop(columns=["moral_ertesi_gun", "moral_dustu"]); yf = fb["moral_dustu"]
for ad, m in modeller.items():
    s = cross_val_score(m, Xf, yf, cv=cv, scoring="roc_auc")
    print(f"{ad:20s} ROC-AUC = {s.mean():.3f} ± {s.std():.3f}")

rff = RandomForestClassifier(n_estimators=500, min_samples_leaf=3, random_state=0).fit(Xf, yf)
pf = permutation_importance(rff, Xf, yf, n_repeats=30, random_state=0, scoring="roc_auc")
onem = pd.Series(pf.importances_mean, index=Xf.columns).sort_values()
plt.figure(figsize=(6.5, 4)); onem.plot.barh(color=np.where(onem.index.isin(["son5_form", "taraftar_umudu"]), "#b7791f", "#2f3fa3"))
plt.title("Taraftar morali: Random Forest permütasyon önemi"); plt.xlabel("AUC kaybı"); plt.tight_layout()'''),
md("""**Okuyun:** Model gizli gerçeği buldu mu? Rakip gücü ve Şampiyonlar Ligi üstte mi? Sarı çubuklara bakın: `son5_form` ile
`taraftar_umudu` önemi paylaşıyor; ikisi de "orta" görünüyor ama birini çıkarsanız öbürü yükselir. Bölüm 5'teki tuzak, bir başka kostümle.

Son söz: `mac_saati`nin önemi sıfıra yakın olmalı, çünkü veriyi üretirken moralle hiç ilişkilendirmedik. Model buna rağmen ona küçük bir
önem verdiyse, bu gürültüdür; gerçek veride de öyle küçük "önemler" çoğu zaman gürültüdür. Moral bozukluğuna gelince: veri diyor ki
rakip güçlüyse ve deplasmandaysanız düşüş normaldir; form gelince geçer. 🙂

## 7 · Bugün ne gördük?

| Konu | Kanıt | Alışkanlık |
|---|---|---|
| Zamansal sızıntı | `takip_gun` ile AUC şişti | "Bu bilgi tahmin anında var mıydı?" diye sor |
| Dört model | Küçük veride farklar küçük | Standart sapmaya bak; temel modeli geçemeyeni savunma |
| Hiperparametre | Rastgele arama CV içinde | Test verisine bakarak ayar yapma |
| Üç öznitelik önemi | Üç farklı liste | Hangi soruya cevap verdiğini bil; safsızlık yanlıdır |
| Benzeyen sütunlar | Kreatinin kopyasıyla önem bölüşüldü | "Önemsiz" ≠ "bilgisiz" |

**Ders sonrası (isteğe bağlı):** BVYZ-01 projesi bu veriyle çalışıyor; bu defter doğrudan `02_model.ipynb` için başlangıç olabilir.
Herkes için: kendi proje verinizde "gelecekten gelen" bir sütun var mı? Varsa raporun Yöntem bölümüne yazın.
"""),
]

# --------------------------------------------------------------------------
# HAFTA 6 — Denetimsiz öğrenme (sıkıştırılmış; 4 Kasım'da 7. haftayla birlikte)
# --------------------------------------------------------------------------
WEEK06 = [
md("""# Hafta 6 · Etiketsiz Veride Yapı Aramak: Kümeleme ve Anomali

**SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka** · Fırat Üniversitesi Yazılım ve Bilişim Araştırma Enstitüsü

Bu defter kısa; ders 7. haftayla birlikte işleniyor. Üç bölüm: k-means ile hasta kümeleri, "kaç küme?" sorusu ve kümelerin gerçek olup
olmadığını sınamak, son olarak Isolation Forest ile anomali. Veri: Breast Cancer (569 hasta). Etiketi **saklıyoruz**; sonunda açıp bakacağız."""),
code('''import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_breast_cancer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

ds = load_breast_cancer(as_frame=True)
X = ds.frame[ds.feature_names]; y_gizli = ds.frame["target"]     # 0 = malign, 1 = benign — şimdilik bakmıyoruz
Xs = StandardScaler().fit_transform(X)
Z = PCA(2).fit_transform(Xs)                                       # yalnızca çizim için
print(X.shape, "— etiketi kullanmıyoruz")'''),
md("""## 1 · k-means: k merkez seç, herkesi en yakına ata, merkezleri taşı, tekrarla

k-means'e kaç küme istediğinizi söylersiniz; o kadar küme bulur. Her zaman. Veride küme olmasa bile. Bu yüzden asıl iş, bulunan kümelerin
gerçek olup olmadığını sınamaktır."""),
code('''from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
for a, k in zip(ax, [2, 3, 4]):
    etiket = KMeans(k, n_init=10, random_state=0).fit_predict(Xs)
    a.scatter(Z[:, 0], Z[:, 1], c=etiket, cmap="viridis", s=12, alpha=.7)
    a.set_title(f"k = {k} · silhouette = {silhouette_score(Xs, etiket):.2f}"); a.set_xticks([]); a.set_yticks([])
plt.suptitle("Aynı veri, üç farklı k: hepsi 'küme' buldu", y=1.03); plt.tight_layout()'''),
md("""## 2 · Kaç küme? Silhouette ve kararlılık

**Silhouette** her hastanın kendi kümesine, komşu kümeye göre ne kadar yakın olduğunu ölçer (−1 ile 1; yüksek iyi).
**Kararlılık** ise şu soru: veriden rastgele bir yarısını alıp tekrar kümelesem aynı hastalar yine birlikte mi düşüyor?"""),
code('''from sklearn.metrics import adjusted_rand_score
rng = np.random.default_rng(0)
print("k   silhouette   kararlılık (ARI, 20 alt-örneklem)")
for k in range(2, 7):
    sil = silhouette_score(Xs, KMeans(k, n_init=10, random_state=0).fit_predict(Xs))
    ref = KMeans(k, n_init=10, random_state=0).fit(Xs)
    aris = []
    for _ in range(20):
        idx = rng.choice(len(Xs), len(Xs) // 2, replace=False)
        alt = KMeans(k, n_init=10, random_state=int(rng.integers(1e6))).fit(Xs[idx])
        aris.append(adjusted_rand_score(ref.predict(Xs[idx]), alt.labels_))
    print(f"{k}   {sil:.3f}        {np.mean(aris):.3f}")'''),
md("""**Okuyun:** k = 2 hem silhouette hem kararlılıkta öne çıkıyor mu? Çıkıyorsa veri gerçekten iki parçalı olabilir.
Ama bu hâlâ iç kanıt. Dış kanıt, kümelemede kullanmadığımız bir bilgiyle örtüşme. Şimdi sakladığımız etiketi açıyoruz."""),
code('''etiket2 = KMeans(2, n_init=10, random_state=0).fit_predict(Xs)
tablo = pd.crosstab(pd.Series(etiket2, name="küme"), y_gizli.map({0: "malign", 1: "benign"}))
print(tablo, "\\n")
print(f"Küme ile tanı uyumu (ARI): {adjusted_rand_score(y_gizli, etiket2):.3f}")'''),
md("""Kümeler tanıyla büyük ölçüde örtüşüyor; model tanıyı hiç görmeden, yalnızca hücre morfolojisinden iki grubu ayırdı. Gerçek alt-tiplendirme
çalışmasında "dış kanıt" bu tabloya benzer: sağkalım, tedavi yanıtı ya da kümelemede kullanılmamış bir klinik değişken.

> **Deneyin:** `KMeans` yerine `AgglomerativeClustering(2)` ve `GaussianMixture(2)` deneyin. Üç yöntem aynı hastaları mı ayırıyor?"""),
md("""## 3 · Anomali: ağaçla kolayca izole edilen nokta tuhaftır

Isolation Forest rastgele sorularla veriyi böler. Sıradan bir hasta çok soru sonra tek kalır; tuhaf bir hasta birkaç soruda. Skor, kaç soruda
tek kaldığıdır. Tuhaf = hatalı giriş mi, nadir ama gerçek vaka mı? Bunu yöntem değil, alan bilgisi söyler."""),
code('''from sklearn.ensemble import IsolationForest
iso = IsolationForest(n_estimators=300, contamination=0.03, random_state=0).fit(Xs)
skor = -iso.score_samples(Xs); anom = iso.predict(Xs) == -1
plt.figure(figsize=(6, 4.2))
plt.scatter(Z[~anom, 0], Z[~anom, 1], s=12, c="#bcc6d9", label="sıradan")
plt.scatter(Z[anom, 0], Z[anom, 1], s=40, c="#be3a5a", label=f"anomali ({anom.sum()})")
plt.legend(); plt.xticks([]); plt.yticks([]); plt.title("Isolation Forest: en tuhaf %3"); plt.tight_layout()
X.loc[anom, ["mean radius", "mean area", "worst area", "mean concave points"]].describe().loc[["min", "50%", "max"]].round(1)'''),
md("""**Okuyun:** Anomali olarak işaretlenen hastaların tümör alanı sıradan hastalardan ne kadar farklı? Bunlar hata mı, ileri evre vaka mı?

## 4 · Bugün ne gördük?

| Soru | Araç | Alışkanlık |
|---|---|---|
| Benzer hastalar kimler? | k-means | k'yi siz seçersiniz; her zaman k küme bulur |
| Kaç küme gerçek? | silhouette + kararlılık | İç kanıt yetmez |
| Kümeler anlamlı mı? | kümelemede kullanılmayan değişkenle çapraz tablo | Dış kanıt şart |
| Tuhaf hasta kim? | Isolation Forest | Hata mı nadir vaka mı: alan bilgisi karar verir |
"""),
]

# --------------------------------------------------------------------------
# HAFTA 7 — Biyomedikal sinyal analizi (EKG)
# --------------------------------------------------------------------------
WEEK07 = [
md("""# Hafta 7 · Sinyal: Zaman Taşıyan Veri — EKG ile Filtreleme, Spektrum, Öznitelik ve Dürüst Doğrulama

**SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka** · Fırat Üniversitesi Yazılım ve Bilişim Araştırma Enstitüsü

Veri: PhysioNet **MIT-BIH Arrhythmia** veri tabanından gerçek EKG kayıtları (`wfdb` ile doğrudan indirilir; her atım kardiyolog tarafından etiketli).
Beş bölüm: sinyale bakmak ve Nyquist, filtreleme, spektrum, R tepeleri ve HRV öznitelikleri, atım sınıflandırmasında kayıt-bazlı doğrulama.
BVYZ-03 ve BVYZ-04 projeleri bu kodu doğrudan kullanabilir."""),
code('''import warnings; warnings.filterwarnings("ignore")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

KAYITLAR = ["100", "101", "103", "106", "119", "200", "208", "223"]   # normal ağırlıklı + ektopik atımı bol kayıtlar
try:
    import wfdb
    kayit = {}
    for r in KAYITLAR:
        rec = wfdb.rdrecord(r, pn_dir="mitdb"); ann = wfdb.rdann(r, "atr", pn_dir="mitdb")
        kayit[r] = dict(x=rec.p_signal[:, 0], fs=rec.fs, r_idx=ann.sample, sembol=np.array(ann.symbol))
    fs = kayit["100"]["fs"]; print(f"{len(kayit)} kayıt indirildi · örnekleme hızı {fs} Hz · 30 dk/kayıt")
except Exception as e:
    print("İndirme başarısız, sentetik EKG üretiliyor:", e)
    fs = 360; rng = np.random.default_rng(0); kayit = {}
    for i, r in enumerate(KAYITLAR):
        t = np.arange(0, 600, 1 / fs); x = np.zeros_like(t); hr = 60 + 10 * i
        rr = np.cumsum(rng.normal(60 / hr, 0.03, int(600 * hr / 60)))
        r_idx = (rr[rr < 600] * fs).astype(int)
        for k in r_idx: x += np.exp(-((t - k / fs) / 0.012) ** 2) + 0.25 * np.exp(-((t - k / fs - 0.3) / 0.06) ** 2)
        sembol = rng.choice(["N", "V"], len(r_idx), p=[0.9, 0.1])
        kayit[r] = dict(x=x + 0.05 * rng.standard_normal(t.size) + 0.3 * np.sin(2 * np.pi * 50 * t), fs=fs, r_idx=r_idx, sembol=sembol)'''),
md("""## 1 · Sinyale bakmak

Saniyede 360 ölçüm. Beş saniyelik pencerede yaklaşık altı atım görmeliyiz. Örnekleme hızı neden önemli? Saniyede 360 fotoğraf çekiyorsanız
saniyede en fazla 180 kez titreyen bir şeyi yakalayabilirsiniz; bunun üstü yanlış frekansa "katlanır" (Nyquist). EKG için 360 fazlasıyla yeter."""),
code('''x = kayit["100"]["x"]; t = np.arange(len(x)) / fs
plt.figure(figsize=(12, 3)); plt.plot(t[:5*fs], x[:5*fs], lw=.9, c="#0b1526"); plt.xlabel("saniye"); plt.ylabel("mV"); plt.title("Kayıt 100 · ilk 5 saniye (ham)"); plt.tight_layout()'''),
md("""## 2 · Filtreleme: gürültüyü süzmek

EKG'de iki tipik gürültü var: solunum ve hareketten gelen yavaş taban çizgisi kayması (< 0.5 Hz) ve şebeke uğultusu (50 Hz).
Bant geçiren filtre 0.5–40 Hz arasını bırakır, gerisini süzer. `filtfilt` ileri-geri uygulandığı için sinyali kaydırmaz."""),
code('''def bant_gecir(x, fs, lo=0.5, hi=40, n=4):
    b, a = signal.butter(n, [lo, hi], btype="band", fs=fs)
    return signal.filtfilt(b, a, x)

# kasıtlı olarak gürültü ekleyip süzüyoruz, ki fark görünsün
rng = np.random.default_rng(1)
kirli = x + 0.3 * np.sin(2 * np.pi * 50 * t) + 0.4 * np.sin(2 * np.pi * 0.2 * t)
temiz = bant_gecir(kirli, fs)
fig, ax = plt.subplots(2, 1, figsize=(12, 5), sharex=True)
ax[0].plot(t[:5*fs], kirli[:5*fs], lw=.8, c="#6b7a92"); ax[0].set_title("Şebeke (50 Hz) + taban çizgisi kayması eklenmiş")
ax[1].plot(t[:5*fs], temiz[:5*fs], lw=.9, c="#0f9b8e"); ax[1].set_title("0.5–40 Hz bant geçiren filtre sonrası"); ax[1].set_xlabel("saniye")
plt.tight_layout()'''),
md("""## 3 · Spektrum: sinyali notalarına ayırmak

Welch yöntemi, sinyalde hangi frekansın ne kadar güç taşıdığını gösterir. 50 Hz'deki sivri çizgi şebekedir; filtre sonrası kaybolmalı.
EEG'de aynı grafik delta/teta/alfa/beta bantlarını, HRV'de LF/HF oranını verir."""),
code('''f1, P1 = signal.welch(kirli, fs=fs, nperseg=4096); f2, P2 = signal.welch(temiz, fs=fs, nperseg=4096)
plt.figure(figsize=(9, 3.6)); plt.semilogy(f1, P1, c="#6b7a92", label="kirli"); plt.semilogy(f2, P2, c="#0f9b8e", label="filtreli")
plt.axvline(50, ls="--", c="#be3a5a", lw=1, label="50 Hz"); plt.xlim(0, 80); plt.xlabel("Hz"); plt.ylabel("güç"); plt.legend(); plt.title("Güç spektral yoğunluğu (Welch)"); plt.tight_layout()'''),
md("""## 4 · R tepeleri, RR aralıkları ve HRV

Atımı bulmak için R tepesini ararız. Burada iki yol var: kendimiz tepe bulmak (`find_peaks`) ya da kardiyologun anotasyonunu kullanmak.
İkisini karşılaştırıyoruz. Ardışık R tepeleri arasındaki süre (RR) kalp hızı değişkenliğini (HRV) verir: RMSSD, pNN50 gibi sayılar."""),
code('''temiz100 = bant_gecir(x, fs)
tepe, _ = signal.find_peaks(temiz100, distance=int(0.4 * fs), height=np.percentile(temiz100, 98) * 0.5)
r_ann = kayit["100"]["r_idx"]; r_ann = r_ann[(r_ann > 0) & (r_ann < len(x))]
print(f"find_peaks: {len(tepe)} tepe · anotasyon: {len(r_ann)} atım  (30 dakika)")

plt.figure(figsize=(12, 3)); seg = slice(0, 5 * fs)
plt.plot(t[seg], temiz100[seg], lw=.9, c="#0b1526")
plt.plot(t[tepe[tepe < 5*fs]], temiz100[tepe[tepe < 5*fs]], "v", c="#be3a5a", label="find_peaks")
plt.plot(t[r_ann[r_ann < 5*fs]], temiz100[r_ann[r_ann < 5*fs]] + 0.15, "^", c="#0f9b8e", label="kardiyolog anotasyonu")
plt.legend(); plt.xlabel("saniye"); plt.title("R tepeleri"); plt.tight_layout()

rr = np.diff(r_ann) / fs * 1000                      # ms
hrv = {"ortalama RR (ms)": rr.mean(), "kalp hızı (bpm)": 60000 / rr.mean(), "SDNN (ms)": rr.std(),
       "RMSSD (ms)": np.sqrt(np.mean(np.diff(rr) ** 2)), "pNN50 (%)": 100 * np.mean(np.abs(np.diff(rr)) > 50)}
pd.Series(hrv).round(1)'''),
md("""## 5 · Atım sınıflandırması ve dürüst doğrulama

Her atım için bir pencere (R tepesinin 90 ms öncesi, 160 ms sonrası) ve birkaç RR özniteliği çıkarıyoruz. Hedef: normal (N) mi, ventriküler
ektopik (V) mi? Sonra 2. haftanın sorusunu soruyoruz: pencereleri rastgele bölersek aynı kaydın atımları iki kümeye düşer. **Kayıt-bazlı**
bölünce ne oluyor?"""),
code('''def atim_oznitelik(kayit, r, once=0.09, sonra=0.16):
    x = bant_gecir(kayit["x"], kayit["fs"]); fs_ = kayit["fs"]; n1, n2 = int(once * fs_), int(sonra * fs_)
    r_idx, sem = kayit["r_idx"], kayit["sembol"]
    rows, ys, gr = [], [], []
    for i in range(2, len(r_idx) - 2):
        if sem[i] not in ("N", "V"): continue
        k = r_idx[i]
        if k - n1 < 0 or k + n2 >= len(x): continue
        pencere = x[k - n1 : k + n2]
        rr_on, rr_son = (r_idx[i] - r_idx[i-1]) / fs_, (r_idx[i+1] - r_idx[i]) / fs_
        rr_yerel = np.mean(np.diff(r_idx[i-2:i+3])) / fs_
        rows.append(np.concatenate([pencere[::3], [rr_on, rr_son, rr_on / rr_yerel, pencere.max() - pencere.min(), np.abs(np.diff(pencere)).mean()]]))
        ys.append(1 if sem[i] == "V" else 0); gr.append(r)
    return np.array(rows), np.array(ys), np.array(gr)

parcalar = [atim_oznitelik(kayit[r], r) for r in kayit]
Xb = np.vstack([p[0] for p in parcalar]); yb = np.concatenate([p[1] for p in parcalar]); gb = np.concatenate([p[2] for p in parcalar])
print(f"{len(yb)} atım · V oranı %{100*yb.mean():.1f} · kayıt sayısı {len(set(gb))}")
pd.Series(yb).groupby(gb).agg(["count", "mean"]).rename(columns={"count": "atım", "mean": "V oranı"}).round(3).T'''),
code('''from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold, GroupKFold, cross_val_score

rf = RandomForestClassifier(n_estimators=300, class_weight="balanced", random_state=0, n_jobs=-1)
rastgele = cross_val_score(rf, Xb, yb, cv=StratifiedKFold(4, shuffle=True, random_state=0), scoring="f1").mean()
grup     = cross_val_score(rf, Xb, yb, cv=GroupKFold(4), groups=gb, scoring="f1").mean()
print(f"Rastgele bölme (aynı kayıt iki kümede): F1 = {rastgele:.3f}")
print(f"Kayıt-bazlı bölme (GroupKFold):         F1 = {grup:.3f}   <- yeni hastaya genelleme")'''),
md("""**Okuyun:** Fark ne kadar? Rastgele bölmede model her hastanın "normal" atımının şeklini ezberleyip V'yi ona göre ayırıyor. Yeni bir hastaya
geçince o şablon yok; başarım düşüyor. Makalelerde "atım-içi" (intra-patient) ile "hasta-arası" (inter-patient) sonuçlar bu yüzden ayrı raporlanır.

> **Deneyin:** `KAYITLAR` listesine "207" ve "233" ekleyin (zor kayıtlar). Kayıt-bazlı F1 ne oldu? Öznitelik olarak yalnızca RR oranlarını bırakıp
> pencereyi çıkarın; hangi öznitelikler yeni hastaya daha iyi genelliyor?

## 6 · Bugün ne gördük?

| Adım | Araç | Alışkanlık |
|---|---|---|
| Örnekleme ve Nyquist | `fs`, sinyalin yarısı | Hangi frekansı görebildiğinizi bilin |
| Filtreleme | Butterworth bant geçiren, `filtfilt` | Önce/sonra spektrumunu çizin |
| Spektrum | Welch PSD | 50 Hz çizgisi gitti mi? EEG bantları, HRV LF/HF |
| Öznitelik | R tepe, RR, HRV, pencere | Pencere + RR oranları birlikte |
| Doğrulama | GroupKFold(kayıt) | Hasta-arası sonuç raporlanır |

**Projeler:** BVYZ-03 bu defterin Bölüm 5'ini doğrudan genişletebilir (AAMI sınıfları, makro-F1). BVYZ-04 Bölüm 2–3'ü PPG'ye uyarlar.
BVYZ-08 Bölüm 3'ü EEG bantlarına taşır.
"""),
]

NOTEBOOKS = {"hafta-01": ("Hafta 1 · Uçtan Uca İlk Tur", WEEK01),
             "hafta-02": ("Hafta 2 · Eksik Veri, Sızıntı ve Hasta-Bazlı Bölme", WEEK02),
             "hafta-03": ("Hafta 3 · Veriyi Tanımak: Keşif, Öznitelik, PCA ve UMAP", WEEK03),
             "hafta-04": ("Hafta 4 · İlk Model ve Klinik Metrikler", WEEK04),
             "hafta-05": ("Hafta 5 · Ağaç Toplulukları, SVM ve Öznitelik Önemi", WEEK05),
             "hafta-06": ("Hafta 6 · Kümeleme ve Anomali", WEEK06),
             "hafta-07": ("Hafta 7 · EKG: Filtreleme, Spektrum, HRV ve Kayıt-Bazlı Doğrulama", WEEK07)}


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
