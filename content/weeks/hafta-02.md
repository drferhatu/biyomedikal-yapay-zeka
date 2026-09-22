---
week: 2
title: "Biyomedikal Verinin Doğası ve Ön İşleme"
topic: "Biyomedikal verinin doğası ve ön işleme: eksik veri, gürültü, normalizasyon, dengesiz sınıflar, veri sızıntısı ve hasta-bazlı veri bölme"
description: "Eksik veri mekanizmaları ve imputasyon, gürültü ve aykırı değer, ölçekleme, dengesiz sınıf stratejileri, veri sızıntısı ve GroupKFold ile hasta-bazlı bölme."
module: m1
exam: false
status: taslak
changeNote: ""
tags:
  - "eksik veri"
  - "imputasyon"
  - "normalizasyon"
  - "dengesiz sınıf"
  - "veri sızıntısı"
  - "GroupKFold"
  - "SMOTE"
objectives:
  - "Eksik veri mekanizmalarını (MCAR, MAR, MNAR) ayırt eder ve uygun imputasyon stratejisini gerekçelendirir."
  - "Ölçekleme ve normalizasyonu yalnızca eğitim kümesine uydurup test kümesine uygulayarak sızıntıyı önler."
  - "Dengesiz sınıflarda yeniden örnekleme, sınıf ağırlığı ve eşik ayarı seçeneklerini karşılaştırır."
  - "Hasta-bazlı (grup) bölme ve zaman-farkında bölmeyi scikit-learn `Pipeline` ve `GroupKFold` ile uygular."
methods:
  - "MCAR/MAR/MNAR"
  - "İmputasyon"
  - "StandardScaler"
  - "SMOTE / ağırlıklandırma"
  - "GroupKFold"
tools:
  - "pandas"
  - "scikit-learn"
  - "imbalanced-learn"
datasets:
  - name: "Pima Indians Diabetes"
    url: "https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database"
    note: "Sıfırla kodlanmış eksik değerler; imputasyon alıştırması."
  - name: "MIMIC-III Clinical Database Demo"
    url: "https://physionet.org/content/mimiciii-demo/"
    note: "100 hastalık açık demo; hasta-bazlı bölme için."
resources:
  - title: "Kaufman S ve ark. Leakage in data mining: formulation, detection, and avoidance. ACM TKDD 2012."
    url: "https://dl.acm.org/doi/10.1145/2382577.2382579"
    kind: makale
    note: "Sızıntının sistematik sınıflaması."
  - title: "van Buuren S. Flexible Imputation of Missing Data (2. baskı, çevrimiçi)."
    url: "https://stefvanbuuren.name/fimd/"
    kind: kitap
    note: "İmputasyon için açık erişimli referans."
  - title: "scikit-learn: Pipelines and composite estimators"
    url: "https://scikit-learn.org/stable/modules/compose.html"
    kind: dokuman
---

## Ön Okuma ve Hazırlık

scikit-learn dokümantasyonunda 'Cross-validation: evaluating estimator performance' bölümündeki GroupKFold ve TimeSeriesSplit kısımlarını okuyun.

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Biyomedikal verinin doğası ve ön işleme: eksik veri, gürültü, normalizasyon, dengesiz sınıflar, veri sızıntısı ve hasta-bazlı veri bölme**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Eksik veri mekanizması** — MCAR: rastgele; MAR: gözlenen değişkenlere bağlı; MNAR: eksikliğin kendisi bilgi taşır (ağır hasta → daha çok test).
- **Veri sızıntısı** — Test bilgisinin eğitime karışması: ölçekleyicinin tüm veriye uydurulması, aynı hastanın iki kümede olması, gelecekteki bilginin özniteliğe girmesi.
- **Dengesiz sınıf** — Nadir hastalıkta pozitif oranının %1–5 olması; doğruluğun anlamsızlaştığı, PR-AUC'nin öne çıktığı rejim.
- **Pipeline** — Ön işleme ve modelin tek nesnede zincirlenmesi; çapraz doğrulamada her katlamada yeniden uydurulur.

## Biyomedikal Uygulama Örnekleri

- Yoğun bakım laboratuvar verisinde laktat ölçümünün eksikliği, hastanın stabil olduğunun göstergesidir (MNAR): eksiklik göstergesi (indicator) eklemek başarımı artırır.
- EEG nöbet veri setinde kayıt-bazlı bölme yerine rastgele bölme yapıldığında AUC 0.98'den 0.82'ye düşer: sızıntının maskelediği gerçek başarım.

## Uygulama / Laboratuvar

Pima veri setinde sıfırların aslında eksik değer olduğunu saptayın; medyan, KNN ve MICE imputasyonunu bir `Pipeline` içinde karşılaştırın. Ardından aynı veriyi (1) rastgele `KFold`, (2) `StratifiedKFold`, (3) hasta kimliği ile `GroupKFold` kullanarak çapraz doğrulayın ve farkı raporlayın.

## Tartışma Soruları

1. Eksik değer göstergesi (missing indicator) eklemek ne zaman bilgi kazandırır, ne zaman bir tür sızıntıdır?
2. SMOTE gibi sentetik örnekleme yöntemleri klinik veride hangi riskleri taşır?

## Haftanın Özeti

Modelden önce veriyle uğraştık: eksik veri mekanizmaları, sızıntı kaynakları, dengesiz sınıflar ve hasta-bazlı bölme. Bu hafta öğrenilen disiplin dersin geri kalanındaki her modelin ön koşulu.
