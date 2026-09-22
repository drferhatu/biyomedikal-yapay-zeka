---
week: 3
title: "Keşifçi Veri Analizi, Öznitelik Mühendisliği ve Boyut İndirgeme"
topic: "Keşifçi veri analizi, öznitelik mühendisliği ve boyut indirgeme (PCA, UMAP)"
description: "Görsel ve istatistiksel keşif, alan bilgisiyle öznitelik türetme, özellik seçimi, PCA'nın doğrusal cebiri ve UMAP ile doğrusal olmayan gömme."
module: m1
exam: false
status: taslak
changeNote: ""
tags:
  - "EDA"
  - "öznitelik mühendisliği"
  - "PCA"
  - "UMAP"
  - "t-SNE"
  - "özellik seçimi"
  - "omik"
objectives:
  - "Dağılım, korelasyon ve grup karşılaştırmalarıyla veri setini sistematik biçimde keşfeder ve veri kalitesi sorunlarını raporlar."
  - "Alan bilgisine dayalı öznitelikler (oranlar, zaman pencereleri, klinik skorlar) türetir ve filtre/sarmal/gömülü seçim yöntemlerini uygular."
  - "PCA'yı kovaryans matrisinin özayrışımı olarak açıklar; açıklanan varyans ve yüklemeleri yorumlar."
  - "UMAP ve t-SNE'yi keşif amaçlı kullanır; gömme uzaklıklarının yorum sınırlarını bilir."
methods:
  - "EDA"
  - "Öznitelik türetme"
  - "PCA"
  - "UMAP"
  - "Özellik seçimi"
tools:
  - "pandas"
  - "seaborn"
  - "scikit-learn"
  - "umap-learn"
datasets:
  - name: "GEO GDS / TCGA örnek ifade matrisi"
    url: "https://www.ncbi.nlm.nih.gov/geo/"
    note: "p ≫ n rejiminde PCA/UMAP."
  - name: "UCI Heart Disease"
    url: "https://archive.ics.uci.edu/dataset/45/heart+disease"
    note: "Öznitelik türetme alıştırması."
resources:
  - title: "McInnes L, Healy J, Melville J. UMAP: Uniform Manifold Approximation and Projection. 2018."
    url: "https://arxiv.org/abs/1802.03426"
    kind: makale
  - title: "Chari T, Pachter L. The specious art of single-cell genomics. PLOS Comput Biol 2023."
    url: "https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011288"
    kind: makale
    note: "t-SNE/UMAP gömmelerinin yorum sınırları."
  - title: "Guyon I, Elisseeff A. An introduction to variable and feature selection. JMLR 2003."
    url: "https://www.jmlr.org/papers/v3/guyon03a.html"
    kind: makale
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Keşifçi veri analizi, öznitelik mühendisliği ve boyut indirgeme (PCA, UMAP)**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Öznitelik mühendisliği** — Ham değişkenlerden model için daha bilgilendirici temsiller türetme: kreatinin/eGFR, nabız değişkenliği, son 24 saat maksimumu.
- **Boyut laneti** — Öznitelik sayısı örnek sayısına yaklaştıkça uzaklıkların anlamsızlaşması; omik veride (p ≫ n) temel sorun.
- **PCA** — Veriyi en yüksek varyanslı ortogonal eksenlere yansıtan doğrusal dönüşüm; bileşenler özvektörler, varyanslar özdeğerlerdir.
- **UMAP** — Topolojik komşuluk yapısını koruyarak düşük boyuta gömen doğrusal olmayan yöntem; küme aralıkları ve şekilleri nicel yorum kabul etmez.

## Biyomedikal Uygulama Örnekleri

- Gen ifadesi (~20.000 gen × 200 hasta) verisinde PCA ile ilk 50 bileşene indirgeme, ardından UMAP ile alt-tip haritası.
- Yoğun bakım vital serilerinden 6 saatlik pencerelerde ortalama, eğim ve değişkenlik özniteliklerinin türetilmesi.

## Uygulama / Laboratuvar

Heart Disease veri setinde tam bir EDA raporu üretin (dağılımlar, korelasyon matrisi, hedefe göre grup karşılaştırmaları). En az üç türetilmiş öznitelik ekleyin ve `SelectKBest` ile `RFE` sonuçlarını karşılaştırın. Bir ifade matrisinde PCA açıklanan varyans eğrisini çizip UMAP gömmesini renklendirin.

## Tartışma Soruları

1. UMAP grafiğinde iki kümenin uzak görünmesi biyolojik olarak 'çok farklı' oldukları anlamına gelir mi?
2. Özellik seçimini çapraz doğrulama döngüsünün dışında yapmak neden sızıntıdır?

## Haftanın Özeti

Veriyi tanımanın ve yeniden temsil etmenin araçlarını kurduk: keşif, öznitelik türetme, seçim ve boyut indirgeme. Modül 1 tamamlandı; artık model kurmaya hazırız.
