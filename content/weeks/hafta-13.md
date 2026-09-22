---
week: 13
title: "Açıklanabilir Yapay Zeka II: SHAP, LIME, Grad-CAM, Karşıt-Olgusal Açıklamalar ve Adalet"
topic: "Açıklanabilir yapay zeka (XAI) II: SHAP, LIME, Grad-CAM ve karşıt-olgusal (counterfactual) açıklamalar; tıp ve mühendislikte vaka çalışmaları, yanlılık ve adalet"
description: "Shapley değerlerinin oyun kuramsal temeli ve SHAP (Tree/Deep/Kernel), LIME'ın yerel vekil yaklaşımı, Grad-CAM ile görsel açıklama, karşıt-olgusal açıklamalar, açıklama tuzakları ve algoritmik adalet ölçütleri."
module: m5
exam: false
status: taslak
changeNote: ""
tags:
  - "SHAP"
  - "Shapley"
  - "LIME"
  - "Grad-CAM"
  - "Integrated Gradients"
  - "karşıt-olgusal"
  - "yanlılık"
  - "adalet"
  - "eşit fırsat"
  - "DiCE"
objectives:
  - "Shapley değerlerinin aksiyomlarını açıklar; TreeSHAP, DeepSHAP ve KernelSHAP'ın ne zaman kullanıldığını ayırt eder; SHAP özet, bağımlılık ve şelale grafiklerini yorumlar."
  - "LIME'ın yerel vekil model mantığını kurar; kararsızlık ve komşuluk tanımı sorunlarını tartışır."
  - "Grad-CAM ve Integrated Gradients ile CNN kararlarını görselleştirir; tıbbi görüntüde 'doğru yere bakma' değerlendirmesi yapar."
  - "Karşıt-olgusal açıklamalar üretir (DiCE); geçerlilik, yakınlık ve eyleme dönüştürülebilirlik ölçütlerini uygular."
  - "Demografik parite, eşit fırsat ve kalibrasyon eşitliği gibi adalet ölçütlerini hesaplar; alt-grup analizini rapor standardı hâline getirir."
methods:
  - "SHAP (Tree/Deep/Kernel)"
  - "LIME"
  - "Grad-CAM / IG"
  - "Karşıt-olgusal açıklama"
  - "Adalet metrikleri"
tools:
  - "shap"
  - "lime"
  - "captum"
  - "dice-ml"
  - "fairlearn"
datasets:
  - name: "5. ve 9. haftaların modelleri (XGBoost, MLP)"
    note: "SHAP/LIME uygulaması."
  - name: "10. haftanın PneumoniaMNIST CNN'i"
    note: "Grad-CAM."
  - name: "MIMIC-III Demo (demografi ile)"
    url: "https://physionet.org/content/mimiciii-demo/"
    note: "Alt-grup adalet analizi."
resources:
  - title: "Lundberg SM, Lee S-I. A Unified Approach to Interpreting Model Predictions. NeurIPS 2017."
    url: "https://arxiv.org/abs/1705.07874"
    kind: makale
  - title: "Ribeiro MT, Singh S, Guestrin C. 'Why Should I Trust You?' Explaining the Predictions of Any Classifier. KDD 2016."
    url: "https://arxiv.org/abs/1602.04938"
    kind: makale
  - title: "Selvaraju RR ve ark. Grad-CAM. ICCV 2017."
    url: "https://arxiv.org/abs/1610.02391"
    kind: makale
  - title: "Wachter S, Mittelstadt B, Russell C. Counterfactual explanations without opening the black box. Harvard JOLT 2018."
    url: "https://arxiv.org/abs/1711.00399"
    kind: makale
  - title: "Obermeyer Z ve ark. Dissecting racial bias in an algorithm used to manage the health of populations. Science 2019."
    url: "https://www.science.org/doi/10.1126/science.aax2342"
    kind: makale
  - title: "Ghassemi M, Oakden-Rayner L, Beam AL. The false hope of current approaches to explainable AI in health care. Lancet Digit Health 2021."
    url: "https://www.thelancet.com/journals/landig/article/PIIS2589-7500(21)00208-9/fulltext"
    kind: makale
    note: "Eleştirel karşı görüş."
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Açıklanabilir yapay zeka (XAI) II: SHAP, LIME, Grad-CAM ve karşıt-olgusal (counterfactual) açıklamalar; tıp ve mühendislikte vaka çalışmaları, yanlılık ve adalet**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Shapley değeri** — Özniteliğin tüm koalisyonlardaki ortalama marjinal katkısı; verimlilik, simetri, sahte oyuncu ve toplamsallık aksiyomlarını sağlayan tek çözüm.
- **SHAP** — Shapley değerlerinin yerel açıklamaya uyarlanması; TreeSHAP ağaç modellerinde polinom zamanda kesin hesap yapar.
- **LIME** — Tek gözlemin çevresinde bozulmuş örneklerle eğitilen seyrek doğrusal vekil model; hızlı ama komşuluk seçimine duyarlı.
- **Grad-CAM** — Son evrişim katmanının sınıf-özel gradyanlarla ağırlıklandırılmış ısı haritası; modelin 'baktığı' bölgeyi gösterir.
- **Karşıt-olgusal açıklama** — 'Şu öznitelikler şöyle olsaydı karar değişirdi': hastaya eyleme dönük öneri üretir; tıbbi olarak mümkün olmalıdır.
- **Adalet ölçütleri** — Demografik parite (pozitif oranı eşit), eşit fırsat (duyarlılık eşit), kalibrasyon eşitliği; aynı anda hepsini sağlamak genelde imkânsızdır.

## Biyomedikal Uygulama Örnekleri

- Sepsis modelinde hasta düzeyinde SHAP şelale grafiği: laktat ve solunum sayısının katkısı; klinisyenin 'ama bu hasta KOAH' itirazı ve etkileşim değerleri.
- Göğüs röntgeni pnömoni modelinde Grad-CAM'in akciğer dışına (cihaz etiketine) yoğunlaşması: 10. haftadaki kısayol öğrenmenin görsel kanıtı.
- Obermeyer ve ark. (2019): Sağlık harcamasını hastalık şiddetinin vekili olarak kullanan algoritmanın Siyah hastaları sistematik olarak düşük riske atması.
- Pulse oksimetre ve deri rengi: girdi ölçümündeki yanlılığın modele taşınması.

## Uygulama / Laboratuvar

XGBoost modeline TreeSHAP uygulayın: özet, bağımlılık ve üç hasta için şelale grafikleri. Aynı hastaları LIME ile açıklayıp tutarlılığı ölçün. CNN'e Grad-CAM uygulayıp radyolojik olarak anlamlı bölgeyle örtüşmeyi değerlendirin. DiCE ile iki hastaya karşıt-olgusal öneri üretin. Son olarak fairlearn ile cinsiyet/yaş alt-gruplarında duyarlılık, özgüllük ve kalibrasyonu karşılaştırın.

## Tartışma Soruları

1. SHAP değerleri yüksek çıkan bir öznitelik 'nedensel' midir? Klinisyene bunu nasıl anlatırsınız?
2. Alt-grupta duyarlılığı eşitlemek için eşik farklılaştırmak adil midir? Hangi adalet tanımına göre?

## Haftanın Özeti

Yerel açıklama yöntemlerinin tamamını uyguladık ve adaleti ölçülebilir bir rapor bileşeni hâline getirdik. Son hafta bu araçları klinik uygulamaya hazır bir sistemin parçası olarak ele alıyor.
