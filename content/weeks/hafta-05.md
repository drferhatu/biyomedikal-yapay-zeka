---
week: 5
title: "Klasik Makine Öğrenmesi II: Topluluk Yöntemleri, SVM ve Öznitelik Önemi"
topic: "Klasik makine öğrenmesi II: topluluk yöntemleri (Random Forest, XGBoost), destek vektör makineleri ve öznitelik önemi"
description: "Torbalama ve artırma ilkeleri, Random Forest ve XGBoost hiperparametreleri, SVM ve çekirdek hilesi, öznitelik önemi türleri ve tuzakları."
module: m2
exam: false
status: taslak
changeNote: ""
tags:
  - "Random Forest"
  - "XGBoost"
  - "gradyan artırma"
  - "SVM"
  - "çekirdek"
  - "öznitelik önemi"
  - "hiperparametre"
objectives:
  - "Torbalama (bagging) ile artırmanın (boosting) varyans–yanlılık açısından farkını açıklar."
  - "Random Forest ve XGBoost'u iç içe (nested) çapraz doğrulamayla ayarlar; erken durdurma ve düzenlileştirme parametrelerini kullanır."
  - "SVM'de marj, çekirdek ve C parametresinin rolünü açıklar; ölçeklemenin zorunluluğunu gerekçelendirir."
  - "Safsızlık-temelli, permütasyon-temelli ve SHAP-temelli öznitelik önemini karşılaştırır; ilişkili özniteliklerde tuzakları tanır."
methods:
  - "Random Forest"
  - "XGBoost / LightGBM"
  - "SVM (RBF)"
  - "Bayes hiperparametre arama"
  - "Permütasyon önemi"
tools:
  - "scikit-learn"
  - "xgboost"
  - "optuna"
datasets:
  - name: "UCI Heart Failure Clinical Records"
    url: "https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records"
  - name: "Kaggle: Stroke Prediction"
    url: "https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset"
    note: "Dengesiz sınıf."
resources:
  - title: "Chen T, Guestrin C. XGBoost: A Scalable Tree Boosting System. KDD 2016."
    url: "https://arxiv.org/abs/1603.02754"
    kind: makale
  - title: "Grinsztajn L ve ark. Why do tree-based models still outperform deep learning on tabular data? NeurIPS 2022."
    url: "https://arxiv.org/abs/2207.08815"
    kind: makale
  - title: "Strobl C ve ark. Bias in random forest variable importance measures. BMC Bioinformatics 2007."
    url: "https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-25"
    kind: makale
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Klasik makine öğrenmesi II: topluluk yöntemleri (Random Forest, XGBoost), destek vektör makineleri ve öznitelik önemi**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Torbalama vs artırma** — Torbalama bağımsız ağaçların ortalamasıyla varyansı düşürür; artırma önceki hataları ardışık düzeltir ve yanlılığı azaltır.
- **Gradyan artırma** — Kayıp fonksiyonunun gradyanına küçük ağaçlar uydurma; öğrenme oranı, derinlik ve düzenlileştirme ile denetlenir.
- **Çekirdek hilesi** — Veriyi açıkça dönüştürmeden yüksek boyutlu uzayda iç çarpım hesaplama; RBF çekirdeği en yaygını.
- **Öznitelik önemi tuzağı** — Safsızlık-temelli önem yüksek kardinaliteli ve ilişkili özniteliklere yanlıdır; permütasyon önemi ilişkili öznitelikler arasında bölünür.

## Biyomedikal Uygulama Örnekleri

- Tablo hâlindeki klinik veride XGBoost'un çoğu zaman derin öğrenmeyi geçmesi ve bunun nedenleri.
- Kalp yetmezliği yeniden yatış modelinde 'ilaç sayısı' özniteliğinin yüksek önemi: nedensel mi, hastalık şiddetinin vekili mi?

## Uygulama / Laboratuvar

Aynı veri setinde lojistik regresyon, Random Forest, XGBoost ve RBF-SVM'yi iç içe çapraz doğrulama ile karşılaştırın (ROC-AUC, PR-AUC, Brier). XGBoost için Optuna ile hiperparametre arayın. Üç öznitelik önemi yöntemini yan yana çizip uyuşmayan öznitelikleri tartışın.

## Tartışma Soruları

1. Model başarımı %1 artınca ek karmaşıklık ve yorumlanabilirlik kaybı klinik olarak ne zaman kabul edilir?
2. İki yüksek korelasyonlu öznitelikten birini çıkardığınızda diğerinin önemi neden aniden artar?

## Haftanın Özeti

Tablo verisi için güçlü klasik yöntemleri ve onları sorumlu biçimde ayarlamayı öğrendik. Öznitelik önemi ile açıklanabilirliğin ilk kapısını araladık; 12. haftada derinleşecek.
