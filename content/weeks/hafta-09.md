---
week: 9
title: "Derin Öğrenmeye Giriş: Yapay Sinir Ağları, Geri Yayılım ve Eğitim Pratiği"
topic: "Derin öğrenmeye giriş: yapay sinir ağları, geri yayılım ve eğitim pratiği"
description: "Perceptron'dan çok katmanlı ağa, aktivasyon ve kayıp fonksiyonları, geri yayılım ve otomatik türev, optimizasyon, düzenlileştirme ve PyTorch ile eğitim döngüsü."
module: m4
exam: false
status: taslak
changeNote: ""
tags:
  - "YSA"
  - "MLP"
  - "geri yayılım"
  - "PyTorch"
  - "Adam"
  - "dropout"
  - "batch norm"
  - "erken durdurma"
  - "öğrenme oranı"
objectives:
  - "Çok katmanlı algılayıcıyı bileşimsel fonksiyon olarak kurar; aktivasyon ve kayıp fonksiyonlarını probleme göre seçer."
  - "Geri yayılımı zincir kuralı olarak türetir; PyTorch autograd ile bağlantısını kurar."
  - "Öğrenme oranı, yığın boyutu, düzenlileştirme (L2, dropout) ve erken durdurmanın etkisini deneyle gösterir."
  - "Eğitim/doğrulama eğrilerinden aşırı/eksik öğrenmeyi tanır; tekrarlanabilir bir PyTorch eğitim döngüsü yazar."
methods:
  - "MLP"
  - "Geri yayılım"
  - "SGD / Adam"
  - "Dropout & BatchNorm"
  - "Erken durdurma"
tools:
  - "PyTorch"
  - "torchmetrics"
  - "scikit-learn"
datasets:
  - name: "UCI Heart Disease / Breast Cancer"
    url: "https://archive.ics.uci.edu/"
    note: "Tablo verisinde MLP."
  - name: "7. haftanın EEG öznitelik matrisi"
    note: "Kendi ürettiğiniz öznitelikler."
resources:
  - title: "Goodfellow, Bengio, Courville. Deep Learning. Bölüm 6 (Deep Feedforward Networks) ve 8 (Optimization)."
    url: "https://www.deeplearningbook.org/"
    kind: kitap
    note: "Ana kaynak."
  - title: "PyTorch: Learn the Basics"
    url: "https://pytorch.org/tutorials/beginner/basics/intro.html"
    kind: dokuman
  - title: "Smith LN. Cyclical learning rates for training neural networks. WACV 2017."
    url: "https://arxiv.org/abs/1506.01186"
    kind: makale
    note: "Öğrenme oranı bulucu."
---

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Derin öğrenmeye giriş: yapay sinir ağları, geri yayılım ve eğitim pratiği**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Evrensel yaklaşım** — Yeterli genişlikte tek gizli katmanlı ağın sürekli fonksiyonlara yaklaşabilmesi; pratikte derinlik daha verimlidir.
- **Geri yayılım** — Kayıp fonksiyonunun her parametreye göre gradyanının zincir kuralıyla çıkıştan girişe hesaplanması.
- **Kaybolan/patlayan gradyan** — Derin ağlarda gradyanın katmanlar boyunca çarpımsal küçülmesi/büyümesi; ReLU, BatchNorm ve artık bağlantılar çözüm sunar.
- **Düzenlileştirme** — Aşırı öğrenmeyi frenleyen her şey: L2 cezası, dropout, veri artırma, erken durdurma.

## Biyomedikal Uygulama Örnekleri

- Klinik tablo verisinde MLP ile XGBoost'un karşılaştırılması: küçük veride ağaçların üstünlüğü, çok-modaliteli veride ağın esnekliği.
- Sinyal özniteliklerinden nöbet tespiti için MLP: öğrenme oranı çok yüksekken kayıp eğrisinin salınımı.

## Uygulama / Laboratuvar

NumPy ile iki katmanlı bir ağın ileri ve geri geçişini elle yazın; aynı ağı PyTorch autograd ile doğrulayın. Ardından PyTorch'ta tam bir eğitim döngüsü (DataLoader, kayıp, optimizer, doğrulama, erken durdurma) kurup Heart Disease verisinde XGBoost ile karşılaştırın. Öğrenme oranı taraması yapıp eğrileri çizin.

## Tartışma Soruları

1. Aynı veri setinde MLP her çalıştırmada farklı sonuç veriyorsa tekrarlanabilirlik için hangi adımlar gerekir?
2. Tablo hâlindeki klinik veride derin öğrenme ne zaman gerçekten haklı çıkar?

## Haftanın Özeti

Derin öğrenmenin çekirdeğini kurduk: ağ, kayıp, gradyan, optimizasyon ve eğitim disiplini. Sonraki iki hafta bu çekirdeği görüntü ve dizilere uyarlıyor.
