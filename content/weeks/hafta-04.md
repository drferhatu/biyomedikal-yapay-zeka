---
week: 4
title: "Klasik Makine Öğrenmesi I: Denetimli Öğrenme ve Klinik Metrikler"
topic: "Klasik makine öğrenmesi I: denetimli öğrenme ve klinik değerlendirme metrikleri (ROC-AUC, duyarlılık/özgüllük, kalibrasyon)"
description: "Lojistik regresyon ve k-NN ile denetimli öğrenme; karışıklık matrisi, duyarlılık/özgüllük, PPV/NPV, ROC ve PR eğrileri, kalibrasyon ve karar eğrisi analizi."
module: m2
exam: false
status: taslak
changeNote: ""
tags:
  - "lojistik regresyon"
  - "ROC-AUC"
  - "PR-AUC"
  - "duyarlılık"
  - "özgüllük"
  - "kalibrasyon"
  - "Brier"
  - "karar eğrisi"
objectives:
  - "Lojistik regresyonu olasılıksal model olarak kurar; katsayıları odds oranı biçiminde yorumlar."
  - "Karışıklık matrisinden duyarlılık, özgüllük, PPV, NPV ve F1 hesaplar; prevalansın PPV üzerindeki etkisini açıklar."
  - "ROC-AUC ile PR-AUC'yi karşılaştırır; dengesiz sınıflarda hangisinin bilgilendirici olduğunu gerekçelendirir."
  - "Kalibrasyon eğrisi, Brier skoru ve Platt/izotonik kalibrasyonu uygular; karar eğrisi analiziyle net faydayı yorumlar."
methods:
  - "Lojistik regresyon"
  - "k-NN"
  - "ROC / PR eğrisi"
  - "Kalibrasyon"
  - "Karar eğrisi analizi"
tools:
  - "scikit-learn"
  - "matplotlib"
datasets:
  - name: "UCI Breast Cancer Wisconsin (Diagnostic)"
    url: "https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic"
  - name: "Kaggle: Sepsis (PhysioNet 2019 Challenge)"
    url: "https://physionet.org/content/challenge-2019/"
    note: "Dengesiz sınıf ve PR-AUC."
resources:
  - title: "Steyerberg EW ve ark. Assessing the performance of prediction models: a framework. Epidemiology 2010."
    url: "https://journals.lww.com/epidem/fulltext/2010/01000/assessing_the_performance_of_prediction_models__a.22.aspx"
    kind: makale
    note: "Ayırt edicilik, kalibrasyon ve klinik fayda çerçevesi."
  - title: "Vickers AJ, Elkin EB. Decision curve analysis. Med Decis Making 2006."
    url: "https://journals.sagepub.com/doi/10.1177/0272989X06295361"
    kind: makale
  - title: "Van Calster B ve ark. Calibration: the Achilles heel of predictive analytics. BMC Med 2019."
    url: "https://bmcmedicine.biomedcentral.com/articles/10.1186/s12916-019-1466-7"
    kind: makale
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Klasik makine öğrenmesi I: denetimli öğrenme ve klinik değerlendirme metrikleri (ROC-AUC, duyarlılık/özgüllük, kalibrasyon)**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Ayırt edicilik (discrimination)** — Modelin hastayı sağlıklıdan sıralama gücü; ROC-AUC bunun eşikten bağımsız özetidir.
- **Kalibrasyon** — Modelin %30 dediği hastaların gerçekten yaklaşık %30'unun olay yaşaması; klinik kararda ayırt edicilik kadar önemlidir.
- **Eşik seçimi** — Yanlış pozitif ve yanlış negatifin klinik maliyetine göre belirlenir; Youden indeksi tek başına yeterli değildir.
- **Karar eğrisi analizi (DCA)** — Farklı eşik olasılıklarında modelin 'herkesi tedavi et / kimseyi tedavi etme' stratejilerine göre net faydasını gösterir.

## Biyomedikal Uygulama Örnekleri

- Sepsis erken uyarı skorunun ROC-AUC'si 0.85 iken alarm başına gerçek pozitif oranı %8: yüksek AUC, düşük PPV ve alarm yorgunluğu.
- Kardiyovasküler risk modelinin dış popülasyonda iyi ayırt edici ama kötü kalibre olması (riski sistematik abartma).

## Uygulama / Laboratuvar

Lojistik regresyon ve k-NN'yi hasta-bazlı çapraz doğrulamayla eğitin. ROC ve PR eğrilerini aynı grafikte çizin; kalibrasyon eğrisi ve Brier skorunu raporlayın. Üç farklı eşik için karışıklık matrislerini çıkarıp klinik senaryoya (tarama vs. doğrulama) göre birini savunun. Karar eğrisi analizi ekleyin.

## Tartışma Soruları

1. Prevalansı %1 olan bir hastalıkta %95 duyarlı ve %95 özgül bir testin PPV'si kaçtır? Bu model raporlarında neden sık göz ardı edilir?
2. Kalibrasyonu bozuk ama ROC-AUC'si yüksek bir model klinik karar destek için kullanılabilir mi?

## Haftanın Özeti

Denetimli öğrenmeyi klinik metrik diliyle kurduk: ayırt edicilik, kalibrasyon, eşik ve net fayda. Bu haftanın değerlendirme çerçevesi dönemin tüm modellerinde tekrarlanacak.
