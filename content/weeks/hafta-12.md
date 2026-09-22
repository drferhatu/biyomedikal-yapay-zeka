---
week: 12
title: "Açıklanabilir Yapay Zeka I: Yorumlanabilirlik, İçsel Modeller ve Post-hoc Yöntemler"
topic: "Açıklanabilir yapay zeka (XAI) I: yorumlanabilirlik kavramı, içsel yorumlanabilirlik ve post-hoc yöntemler (permütasyon önemi, PDP/ICE)"
description: "Yorumlanabilirlik–açıklanabilirlik ayrımı ve taksonomi; içsel yorumlanabilir modeller (GAM, EBM, kural listeleri); permütasyon önemi, kısmi bağımlılık ve ICE eğrileri; açıklamaların değerlendirilmesi."
module: m5
exam: false
status: taslak
changeNote: ""
tags:
  - "XAI"
  - "yorumlanabilirlik"
  - "GAM"
  - "EBM"
  - "permütasyon önemi"
  - "PDP"
  - "ICE"
  - "ALE"
  - "post-hoc"
  - "Rudin"
objectives:
  - "Yorumlanabilirlik ile açıklanabilirliği ayırır; küresel/yerel, model-bağımlı/bağımsız, içsel/post-hoc eksenlerinde yöntemleri sınıflar."
  - "Genelleştirilmiş toplamsal modeller (GAM/EBM) ve seyrek doğrusal modelleri yüksek riskli kararlar için savunur ve kurar."
  - "Permütasyon önemi, kısmi bağımlılık (PDP), bireysel koşullu beklenti (ICE) ve ALE eğrilerini hesaplar ve yorumlar."
  - "Açıklamaların sadakat (fidelity), kararlılık ve insan-anlaşılırlık ölçütlerini tartışır; Rudin'in kara kutu eleştirisini değerlendirir."
methods:
  - "İçsel yorumlanabilir modeller (GAM/EBM)"
  - "Permütasyon önemi"
  - "PDP"
  - "ICE"
  - "ALE"
tools:
  - "scikit-learn (inspection)"
  - "interpret (EBM)"
  - "PyALE"
  - "matplotlib"
datasets:
  - name: "UCI Heart Failure Clinical Records"
    url: "https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records"
  - name: "5. haftanın XGBoost modeli"
    note: "Post-hoc yöntemler için kara kutu."
resources:
  - title: "Molnar C. Interpretable Machine Learning, Bölüm: Interpretability, Interpretable Models, Global Model-Agnostic Methods."
    url: "https://christophm.github.io/interpretable-ml-book/"
    kind: kitap
    note: "Ana kaynak."
  - title: "Rudin C. Stop explaining black box machine learning models for high stakes decisions. Nat Mach Intell 2019."
    url: "https://www.nature.com/articles/s42256-019-0048-x"
    kind: makale
  - title: "Caruana R ve ark. Intelligible models for healthcare: predicting pneumonia risk and hospital 30-day readmission. KDD 2015."
    url: "https://dl.acm.org/doi/10.1145/2783258.2788613"
    kind: makale
  - title: "Apley DW, Zhu J. Visualizing the effects of predictor variables in black box supervised learning models (ALE). JRSS-B 2020."
    url: "https://arxiv.org/abs/1612.08468"
    kind: makale
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Açıklanabilir yapay zeka (XAI) I: yorumlanabilirlik kavramı, içsel yorumlanabilirlik ve post-hoc yöntemler (permütasyon önemi, PDP/ICE)**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Yorumlanabilirlik vs açıklanabilirlik** — Yorumlanabilir model kendi başına anlaşılır (seyrek lojistik, GAM); açıklanabilirlik kara kutuyu sonradan (post-hoc) açıklamaktır.
- **Küresel vs yerel** — Küresel: modelin genel davranışı (hangi öznitelik önemli); yerel: tek bir hastanın tahmini neden böyle.
- **Kısmi bağımlılık (PDP)** — Bir özniteliğin diğerleri üzerinden ortalanmış marjinal etkisi; ilişkili özniteliklerde yanıltıcı olabilir, ALE bunu düzeltir.
- **ICE** — PDP'nin bireysel hasta eğrileri; heterojen etkileri ve etkileşimleri ortaya çıkarır.
- **Sadakat (fidelity)** — Açıklamanın modelin gerçek davranışını ne kadar doğru yansıttığı; açıklama ≠ nedensel gerçek.

## Biyomedikal Uygulama Örnekleri

- Caruana ve ark. (2015): Pnömoni mortalite modelinde 'astım → düşük risk' kuralının GAM ile yakalanması ve klinik açıklaması (astımlılar yoğun bakıma alınıyor).
- Kardiyovasküler risk modelinde yaşın PDP'si: monoton beklenirken 80+ yaşta düşen eğri, sağkalım yanlılığının işareti.

## Uygulama / Laboratuvar

5. haftadaki XGBoost modeline permütasyon önemi, PDP, ICE ve ALE uygulayın; ilişkili öznitelik çiftinde PDP ile ALE farkını gösterin. Aynı veriyi EBM ile modelleyip başarım kaybını ve kazanılan yorumlanabilirliği tabloya dökün. Bir klinisyene sunacağınız iki paragraflık 'model nasıl karar veriyor' özeti yazın.

## Tartışma Soruları

1. Rudin'in 'yüksek riskli kararlarda kara kutuyu açıklamayı bırakın, yorumlanabilir model kullanın' tezi biyomedikal görüntü için de geçerli midir?
2. PDP'de görülen ilişki nedensel midir? Hangi koşullarda nedensel yoruma yaklaşır?

## Haftanın Özeti

Açıklanabilirliğin kavram haritasını çizdik ve küresel post-hoc yöntemleri uyguladık. Gelecek hafta yerel açıklamalara (SHAP, LIME, Grad-CAM) ve adalete geçiyoruz.
