---
week: 6
title: "Denetimsiz Öğrenme: Hasta Alt-Tiplendirme, Kümeleme ve Anomali Tespiti"
topic: "Denetimsiz öğrenme: hasta alt-tiplendirme (subtyping), kümeleme ve anomali tespiti"
description: "k-means, hiyerarşik ve GMM kümeleme; küme sayısı seçimi ve kararlılık; hasta alt-tiplerinin klinik doğrulanması; Isolation Forest ve otokodlayıcı ile anomali."
module: m2
exam: false
status: taslak
changeNote: ""
tags:
  - "kümeleme"
  - "k-means"
  - "hiyerarşik"
  - "GMM"
  - "alt-tipleme"
  - "anomali tespiti"
  - "Isolation Forest"
  - "silhouette"
objectives:
  - "k-means, hiyerarşik ve Gauss karışım modellerinin varsayımlarını ve hangi veri geometrisine uyduklarını açıklar."
  - "Küme sayısını silhouette, gap istatistiği ve konsensüs/kararlılık analiziyle seçer; keyfî seçimden kaçınır."
  - "Bulunan hasta alt-tiplerini klinik değişkenler ve sonlanımlarla (sağkalım, yanıt) dışsal olarak doğrular."
  - "Isolation Forest ve yoğunluk-temelli yöntemlerle anomali tespiti yapar; anomaliyi hata mı, nadir fenotip mi diye ayırır."
methods:
  - "k-means"
  - "Hiyerarşik kümeleme"
  - "GMM"
  - "Konsensüs kümeleme"
  - "Isolation Forest"
tools:
  - "scikit-learn"
  - "scipy"
  - "umap-learn"
datasets:
  - name: "UCI Wisconsin Breast Cancer (etiketler saklanarak)"
    url: "https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic"
    note: "Kümeleme sonuçlarının dışsal doğrulaması."
  - name: "PhysioNet MIT-BIH Arrhythmia"
    url: "https://physionet.org/content/mitdb/"
    note: "Anomali tespiti."
resources:
  - title: "Seymour CW ve ark. Derivation, validation, and potential treatment implications of novel clinical phenotypes for sepsis. JAMA 2019."
    url: "https://jamanetwork.com/journals/jama/fullarticle/2733996"
    kind: makale
  - title: "Liu FT, Ting KM, Zhou Z-H. Isolation Forest. ICDM 2008."
    url: "https://ieeexplore.ieee.org/document/4781136"
    kind: makale
  - title: "Monti S ve ark. Consensus clustering. Machine Learning 2003."
    url: "https://link.springer.com/article/10.1023/A:1023949509487"
    kind: makale
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Denetimsiz öğrenme: hasta alt-tiplendirme (subtyping), kümeleme ve anomali tespiti**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Hasta alt-tiplendirme** — Aynı tanı altındaki hastaların veri-güdümlü biçimde klinik olarak farklı gruplara ayrılması (ör. sepsis fenotipleri α–δ).
- **Küme kararlılığı** — Alt-örneklemeler veya farklı başlangıçlarda aynı kümelerin yeniden bulunması; kararsız küme yapay bulgudur.
- **Dışsal doğrulama** — Kümelemede kullanılmayan değişkenlerle (sonlanım, tedavi yanıtı) kümelerin anlamlılığını sınamak.
- **Anomali** — Çoğunluk dağılımından uzak gözlem; sensör hatası, veri giriş hatası veya gerçek nadir vaka olabilir.

## Biyomedikal Uygulama Örnekleri

- Seymour ve ark. (JAMA 2019): 20.000+ sepsis hastasında dört klinik fenotip ve farklı mortalite profilleri.
- Holter EKG kayıtlarında Isolation Forest ile aritmik segment tespiti: anomali skoru ile kardiyolog etiketinin karşılaştırılması.

## Uygulama / Laboratuvar

Etiketleri saklayarak Breast Cancer verisini k-means, hiyerarşik ve GMM ile kümeleyin; silhouette ve konsensüs matrisleriyle k seçin. Kümeleri saklanan etiket ve klinik değişkenlerle karşılaştırın. MIT-BIH'ten çıkarılan RR aralığı özniteliklerinde Isolation Forest ile anomali skoru üretip aritmi etiketleriyle ROC hesaplayın.

## Tartışma Soruları

1. k-means her zaman k küme bulur; bulduğu kümelerin gerçek olduğunu nasıl kanıtlarsınız?
2. Anomali tespiti modeli tıbbi bir cihazda uyarı üretiyorsa yanlış alarm ile kaçırılan olay arasındaki dengeyi kim, nasıl belirler?

## Haftanın Özeti

Etiketsiz veriden yapı çıkarmayı ve bulduğumuz yapıyı klinik olarak doğrulamayı öğrendik. Modül 2 tamamlandı.
