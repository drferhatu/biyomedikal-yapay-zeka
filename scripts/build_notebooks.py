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

NOTEBOOKS = {"hafta-01": ("Hafta 1 · Uçtan Uca İlk Tur", WEEK01),
             "hafta-02": ("Hafta 2 · Eksik Veri, Sızıntı ve Hasta-Bazlı Bölme", WEEK02),
             "hafta-03": ("Hafta 3 · Veriyi Tanımak: Keşif, Öznitelik, PCA ve UMAP", WEEK03),
             "hafta-04": ("Hafta 4 · İlk Model ve Klinik Metrikler", WEEK04)}


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
