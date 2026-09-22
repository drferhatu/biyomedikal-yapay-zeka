---
week: 7
title: "Biyomedikal Sinyal ve Zaman Serisi Analizi: EEG, EKG, EMG"
topic: "Biyomedikal sinyal ve zaman serisi analizi (EEG/ECG/EMG): filtreleme, öznitelik çıkarımı ve zaman-frekans yöntemleri"
description: "Örnekleme ve Nyquist, sayısal filtreler, artefakt giderme, zaman/frekans/doğrusal-olmayan öznitelikler, STFT ve dalgacık dönüşümü, kayıt-bazlı doğrulama."
module: m3
exam: false
status: taslak
changeNote: ""
tags:
  - "EEG"
  - "EKG"
  - "EMG"
  - "filtreleme"
  - "FFT"
  - "STFT"
  - "dalgacık"
  - "HRV"
  - "zaman-frekans"
  - "MNE"
objectives:
  - "Örnekleme frekansı, Nyquist sınırı ve örtüşmenin (aliasing) sinyal kalitesine etkisini açıklar."
  - "Bant geçiren ve çentik filtreleri tasarlar; EEG'de göz/kas artefaktını, EKG'de taban çizgisi kaymasını giderir."
  - "Zaman alanı (RR, HRV), frekans alanı (bant güçleri) ve doğrusal olmayan (entropi) öznitelikler çıkarır."
  - "STFT ve sürekli dalgacık dönüşümüyle zaman–frekans temsili üretir; kayıt-bazlı çapraz doğrulama ile sınıflandırıcı eğitir."
methods:
  - "Butterworth / notch filtre"
  - "FFT & Welch PSD"
  - "STFT"
  - "Dalgacık dönüşümü"
  - "HRV öznitelikleri"
tools:
  - "scipy.signal"
  - "MNE-Python"
  - "NeuroKit2"
  - "wfdb"
  - "PyWavelets"
datasets:
  - name: "PhysioNet MIT-BIH Arrhythmia"
    url: "https://physionet.org/content/mitdb/"
    note: "EKG; etiketli atımlar."
  - name: "Bonn EEG / CHB-MIT Scalp EEG"
    url: "https://physionet.org/content/chbmit/"
    note: "Nöbet tespiti."
  - name: "PhysioNet AF Classification Challenge 2017"
    url: "https://physionet.org/content/challenge-2017/"
    note: "Tek derivasyon EKG."
resources:
  - title: "Rajpurkar P ve ark. Cardiologist-level arrhythmia detection with convolutional neural networks. Nat Med 2019."
    url: "https://www.nature.com/articles/s41591-018-0268-3"
    kind: makale
    note: "Uçtan uca öğrenme karşıtı olarak öznitelik-temelli yaklaşımı tartışın."
  - title: "Gramfort A ve ark. MEG and EEG data analysis with MNE-Python. Front Neurosci 2013."
    url: "https://www.frontiersin.org/articles/10.3389/fnins.2013.00267/full"
    kind: makale
  - title: "Shaffer F, Ginsberg JP. An overview of heart rate variability metrics and norms. Front Public Health 2017."
    url: "https://www.frontiersin.org/articles/10.3389/fpubh.2017.00258/full"
    kind: makale
---

## Ön Okuma ve Hazırlık

Ara sınav gelecek hafta: 1–7. haftaların içeriğini kapsar. Bu hafta işlenen sinyal işleme kavramları da dâhildir.

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Biyomedikal sinyal ve zaman serisi analizi (EEG/ECG/EMG): filtreleme, öznitelik çıkarımı ve zaman-frekans yöntemleri**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Nyquist frekansı** — Örnekleme frekansının yarısı; üzerindeki bileşenler yanlış frekansa katlanır (aliasing).
- **Güç spektral yoğunluğu (PSD)** — Sinyal gücünün frekansa dağılımı; EEG bantları (delta–gama) ve HRV LF/HF oranı buradan okunur.
- **Zaman–frekans temsili** — STFT sabit pencereyle, dalgacık dönüşümü ölçeğe göre değişen pencereyle geçici olayları (nöbet, aritmi) yakalar.
- **Kayıt-bazlı doğrulama** — Aynı kaydın segmentlerinin eğitim ve teste dağılmaması; aksi hâlde başarım yapay olarak şişer.

## Biyomedikal Uygulama Örnekleri

- EEG'de epileptik nöbet tespiti: 2 saniyelik pencerelerde bant güçleri + entropi → Random Forest; hasta-bazlı AUC ile pencere-bazlı AUC farkı.
- EKG'den atriyal fibrilasyon tespiti: RR aralığı düzensizliği (RMSSD, pNN50) ve P dalgası yokluğu.

## Uygulama / Laboratuvar

MIT-BIH'ten bir kaydı yükleyin; 0.5–40 Hz bant geçiren ve 50 Hz çentik filtre uygulayıp öncesi/sonrası PSD çizin. R tepe tespiti ile RR serisi ve HRV öznitelikleri üretin. CHB-MIT'ten bir hastanın EEG'sinde STFT spektrogramında nöbeti işaretleyin; bant güçleriyle kayıt-bazlı çapraz doğrulamalı sınıflandırıcı eğitin.

## Tartışma Soruları

1. Aynı hastanın nöbet ve nöbet-dışı segmentleri hem eğitim hem test kümesine düşerse model neyi öğrenir?
2. Öznitelik çıkarımı + klasik ML ile ham sinyalden uçtan uca öğrenen CNN arasında ne zaman hangisini seçersiniz?

## Haftanın Özeti

Fizyolojik sinyalleri temizleyip anlamlı özniteliklere dönüştürdük ve zaman–frekans temsillerini gördük. Bu temsiller 9–11. haftalardaki derin öğrenme modellerinin girdisi olacak.
