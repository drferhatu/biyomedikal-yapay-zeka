---
week: 11
title: "Dizisel Modeller: RNN/LSTM, Transformer ve Klinik Metin Analizi"
topic: "Dizisel modeller: RNN/LSTM ve Transformer'ların biyomedikal uygulamaları; klinik metin (NLP) analizine giriş"
description: "Tekrarlayan ağlar ve LSTM, dikkat mekanizması ve Transformer, ham sinyal ve düzensiz EHR zaman serileri, klinik metin için BERT-tabanlı modeller ve de-identifikasyon."
module: m4
exam: false
status: taslak
changeNote: ""
tags:
  - "RNN"
  - "LSTM"
  - "GRU"
  - "Transformer"
  - "dikkat"
  - "BERT"
  - "klinik NLP"
  - "ClinicalBERT"
  - "EHR zaman serisi"
  - "de-identifikasyon"
objectives:
  - "RNN/LSTM'in dizisel bağımlılığı nasıl modellediğini ve uzun bağımlılık sorununu açıklar."
  - "Öz-dikkat mekanizmasını matris biçiminde türetir; Transformer'ın RNN'e göre avantajlarını sıralar."
  - "Düzensiz örneklenmiş EHR zaman serilerini (eksik, farklı aralıklı) dizisel modele hazırlar; maske ve zaman kodlaması kullanır."
  - "Ön-eğitimli biyomedikal dil modelleriyle (ClinicalBERT, BioBERT) klinik not sınıflandırması yapar; de-identifikasyon ve mahremiyet gereklerini tanır."
methods:
  - "LSTM / GRU"
  - "1D-CNN"
  - "Transformer / dikkat"
  - "BERT ince ayarı"
  - "Klinik NLP"
tools:
  - "PyTorch"
  - "Hugging Face transformers"
  - "scikit-learn"
datasets:
  - name: "PhysioNet AF Classification Challenge 2017"
    url: "https://physionet.org/content/challenge-2017/"
    note: "Ham EKG dizisi."
  - name: "MIMIC-III Demo (notlar ve zaman serisi)"
    url: "https://physionet.org/content/mimiciii-demo/"
    note: "Düzensiz EHR serisi."
  - name: "MTSamples (açık klinik transkript örnekleri)"
    url: "https://mtsamples.com/"
    note: "Klinik metin sınıflandırma alıştırması."
resources:
  - title: "Vaswani A ve ark. Attention Is All You Need. NeurIPS 2017."
    url: "https://arxiv.org/abs/1706.03762"
    kind: makale
  - title: "Hochreiter S, Schmidhuber J. Long Short-Term Memory. Neural Computation 1997."
    url: "https://www.bioinf.jku.at/publications/older/2604.pdf"
    kind: makale
  - title: "Alsentzer E ve ark. Publicly Available Clinical BERT Embeddings. 2019."
    url: "https://arxiv.org/abs/1904.03323"
    kind: makale
  - title: "Goodfellow ve ark. Deep Learning, Bölüm 10 (Sequence Modeling)."
    url: "https://www.deeplearningbook.org/contents/rnn.html"
    kind: kitap
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Dizisel modeller: RNN/LSTM ve Transformer'ların biyomedikal uygulamaları; klinik metin (NLP) analizine giriş**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Tekrarlayan ağ (RNN)** — Gizli durumu her zaman adımında güncelleyen ağ; LSTM/GRU kapılarla uzun bağımlılığı korur.
- **Öz-dikkat** — Her konumun diğer tüm konumlarla ilişkisini sorgu–anahtar–değer çarpımıyla ağırlıklandırma; paralel ve uzun menzilli.
- **Düzensiz zaman serisi** — EHR'de ölçümlerin farklı zamanlarda ve sıklıkta olması; eksiklik deseni bilgi taşır.
- **Klinik metin** — Serbest metin notlar, radyoloji raporları; kısaltma, olumsuzlama ('pnömoni yok') ve mahremiyet zorlukları.
- **De-identifikasyon** — Kişisel tanımlayıcıların metinden çıkarılması; NLP çalışmasının yasal ön koşulu.

## Biyomedikal Uygulama Örnekleri

- Yoğun bakım vital ve laboratuvar serilerinden 6 saat önceden sepsis tahmini: GRU ile öznitelik-temelli XGBoost karşılaştırması.
- Ham tek derivasyon EKG'den atriyal fibrilasyon tespiti: 1D-CNN + LSTM (PhysioNet 2017).
- Radyoloji raporlarından bulgu çıkarımı: ClinicalBERT ince ayarı ve olumsuzlama hataları.

## Uygulama / Laboratuvar

PhysioNet 2017 EKG verisinde 1D-CNN ve LSTM modellerini kayıt-bazlı bölme ile eğitip 7. haftanın öznitelik-temelli modeliyle karşılaştırın. Hugging Face'ten bir biyomedikal BERT modelini indirip küçük bir klinik metin sınıflandırma görevinde ince ayar yapın; olumsuzlama içeren örneklerde hataları inceleyin.

## Tartışma Soruları

1. Dikkat ağırlıkları bir 'açıklama' sayılır mı? 12–13. haftalarda bu soruya geri döneceğiz.
2. Klinik notlarla çalışırken de-identifikasyon yeterli midir; yeniden tanımlama riski nereden gelir?

## Haftanın Özeti

Zamanı ve dili modelleyen ağları biyomedikal dizilere uyguladık. Modül 4 tamamlandı; artık elimizde açıklanması gereken güçlü kara kutular var.
