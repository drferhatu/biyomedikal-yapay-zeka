# <Proje başlığı>

> SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka · Fırat Üniversitesi YBAE · 2026–2027 Güz
> Proje kodu: **BVYZ-XX** · Öğrenci: <Ad Soyad>

Bu depo, dönem projesinin tüm kodunu, çalıştırılabilir defterlerini ve LaTeX raporunu içerir.
**Veri dosyaları depoya konmaz**; `data/README.md` verinin nereden ve nasıl indirileceğini anlatır.

## Klinik soru

Bir–iki cümleyle: Hangi hastalar için, hangi sonucu, hangi veriyle tahmin ediyorsunuz ve bu neden önemli?

## Veri

| | |
|---|---|
| Kaynak | <ad ve bağlantı> |
| Örnek sayısı | <n hasta / n kayıt> |
| Öznitelik sayısı | <p> |
| Hedef | <değişken ve tanımı> |
| Sınıf oranı | <%> |
| Lisans / erişim | <açık, kayıt gerekli vb.> |

## Yöntem (kısaca)

Ön işleme → model → değerlendirme → açıklama zincirini üç–dört cümleyle yazın. Ayrıntı raporda.

## Sonuçlar (kısaca)

| Model | ROC-AUC | PR-AUC | Kalibrasyon (Brier) |
|---|---|---|---|
| Temel (lojistik) | | | |
| <Model 2> | | | |

Bir cümle: en önemli bulgu ne?

## Nasıl çalıştırılır

```bash
# Colab: notebooks/ altındaki defterleri sırayla açın; her defterin ilk hücresi veriyi indirir.
# Yerel:
conda create -n proje python=3.12 -y && conda activate proje
pip install -r requirements.txt
jupyter lab
```

## Depo yapısı

```
notebooks/   01_veri_kesif.ipynb · 02_model.ipynb · 03_aciklama.ipynb
src/         yeniden kullanılan fonksiyonlar (ön işleme, metrikler, çizimler)
rapor/       main.tex, kaynaklar.bib, sekiller/ ve derlenmiş rapor.pdf
data/        README.md (indirme talimatı) — veri dosyası YOK
```

## Tekrarlanabilirlik

- Rastgelelik tohumu: `SEED = 42` (tüm defterlerde)
- Bölme stratejisi: <StratifiedKFold / GroupKFold(hasta) / zaman-farkında>
- Ortam: `requirements.txt` (sürümler sabit)

## Kaynaklar

Raporun kaynakçasıyla aynı; en az üç hakemli makale.
