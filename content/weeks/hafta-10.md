---
week: 10
title: "Evrişimli Sinir Ağları ve Tıbbi Görüntü Analizi"
topic: "Evrişimli sinir ağları ve tıbbi görüntü analizi: sınıflandırma, segmentasyon (U-Net) ve transfer öğrenme"
description: "Evrişim, havuzlama ve alıcı alan; klasik mimariler (ResNet); transfer öğrenme ve ince ayar; U-Net ile segmentasyon; Dice/IoU; tıbbi görüntüye özgü tuzaklar."
module: m4
exam: false
status: taslak
changeNote: ""
tags:
  - "CNN"
  - "ResNet"
  - "U-Net"
  - "segmentasyon"
  - "transfer öğrenme"
  - "Dice"
  - "IoU"
  - "veri artırma"
  - "kısayol öğrenme"
  - "MedMNIST"
objectives:
  - "Evrişim, adım, dolgu ve havuzlamanın alıcı alan ve parametre sayısına etkisini hesaplar."
  - "ImageNet ön-eğitimli bir ağı tıbbi görüntüye transfer eder; dondurma/ince ayar stratejilerini karşılaştırır."
  - "U-Net'in kodlayıcı–kod çözücü ve atlama bağlantılarını açıklar; Dice ve IoU ile segmentasyon başarımını değerlendirir."
  - "Tıbbi görüntüde kısayol öğrenme (cihaz etiketi, hastane imzası) ve dağıtım kayması risklerini tanır; hasta-bazlı bölmeyi uygular."
methods:
  - "CNN"
  - "ResNet transfer öğrenme"
  - "U-Net"
  - "Dice / IoU"
  - "Veri artırma"
tools:
  - "PyTorch"
  - "torchvision"
  - "MONAI"
  - "MedMNIST"
datasets:
  - name: "MedMNIST v2"
    url: "https://medmnist.com/"
    note: "Hafif, standart tıbbi görüntü setleri (Path, Derma, Pneumonia, OrganA)."
  - name: "ISIC Archive"
    url: "https://www.isic-archive.com/"
    note: "Dermatoskopik görüntü."
  - name: "Kaggle: Chest X-Ray Images (Pneumonia)"
    url: "https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia"
    note: "Kısayol öğrenme tartışması için."
resources:
  - title: "Ronneberger O, Fischer P, Brox T. U-Net: Convolutional Networks for Biomedical Image Segmentation. MICCAI 2015."
    url: "https://arxiv.org/abs/1505.04597"
    kind: makale
  - title: "Zech JR ve ark. Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs. PLOS Med 2018."
    url: "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683"
    kind: makale
    note: "Kısayol öğrenme."
  - title: "Yang J ve ark. MedMNIST v2. Sci Data 2023."
    url: "https://www.nature.com/articles/s41597-022-01721-8"
    kind: makale
  - title: "Goodfellow ve ark. Deep Learning, Bölüm 9 (Convolutional Networks)."
    url: "https://www.deeplearningbook.org/contents/convnets.html"
    kind: kitap
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Evrişimli sinir ağları ve tıbbi görüntü analizi: sınıflandırma, segmentasyon (U-Net) ve transfer öğrenme**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Evrişim** — Öğrenilen küçük filtrelerin görüntü üzerinde kaydırılması; öteleme eşdeğerliği ve parametre paylaşımı sağlar.
- **Transfer öğrenme** — Büyük doğal görüntü kümesinde öğrenilen filtrelerin tıbbi görüntüde yeniden kullanımı; az veride başarımın anahtarı.
- **U-Net** — Piksel düzeyinde sınıflandırma için simetrik kodlayıcı–kod çözücü; atlama bağlantıları ince ayrıntıyı korur.
- **Dice katsayısı** — Tahmin ve referans maskelerinin örtüşmesi (2|A∩B|/(|A|+|B|)); küçük lezyonlarda doğruluktan çok daha bilgilendirici.
- **Kısayol öğrenme** — Modelin hastalık yerine görüntüdeki ilgisiz ipucunu (portatif cihaz etiketi) öğrenmesi; dış veride çöküşün ana nedeni.

## Biyomedikal Uygulama Örnekleri

- Zech ve ark. (2018): Göğüs röntgeninde pnömoni modelinin hastane kaynağını öğrenmesi ve dış hastanede AUC düşüşü.
- MedMNIST PathMNIST'te ResNet-18 ince ayarı; DermaMNIST'te sınıf dengesizliği ve makro-F1.
- Kardiyak MR'da sol ventrikül segmentasyonu için U-Net: Dice 0.90'ın klinik olarak yeterli olduğu ve olmadığı durumlar.

## Uygulama / Laboratuvar

PneumoniaMNIST'te (1) sıfırdan küçük bir CNN, (2) dondurulmuş ResNet-18 + yeni baş, (3) tam ince ayar stratejilerini karşılaştırın; veri artırmanın etkisini ölçün. Ardından küçük bir segmentasyon setinde U-Net eğitip Dice/IoU raporlayın. Colab GPU kullanın.

## Tartışma Soruları

1. Radyoloji görüntüsünde %95 doğru bir sınıflandırıcı neden dış hastanede %70'e düşebilir? Bunu dağıtımdan önce nasıl öngörürsünüz?
2. Segmentasyonda piksel doğruluğu yerine Dice kullanmanın gerekçesi nedir?

## Haftanın Özeti

Görüntüden öğrenen ağları kurduk, transfer ettik ve segmentasyon yaptık; tıbbi görüntünün özgün tuzaklarını gördük. 13. haftada Grad-CAM ile bu ağların 'nereye baktığını' göstereceğiz.
