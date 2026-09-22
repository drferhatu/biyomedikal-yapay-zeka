---
week: 14
title: "Güvenilir ve Klinik Uygulamaya Hazır Yapay Zeka"
topic: "Güvenilir ve klinik uygulamaya hazır yapay zeka: dış doğrulama, dağıtım kayması, model kartları/MLOps ve mahremiyet-koruyucu öğrenme (federated learning)"
description: "İç–dış–zamansal doğrulama hiyerarşisi, dağıtım kayması türleri ve izleme, model kartları ve TRIPOD+AI raporlaması, MLOps yaşam döngüsü, federe öğrenme ve diferansiyel mahremiyet, regülasyon ve dönem değerlendirmesi."
module: m5
exam: false
status: taslak
changeNote: ""
tags:
  - "dış doğrulama"
  - "dağıtım kayması"
  - "model kartı"
  - "TRIPOD+AI"
  - "MLOps"
  - "federe öğrenme"
  - "diferansiyel mahremiyet"
  - "regülasyon"
  - "AB YZ Yasası"
  - "FDA"
objectives:
  - "İç, zamansal, coğrafi ve alan-dışı doğrulama düzeylerini ayırır; TRIPOD+AI'ye uygun bir doğrulama planı yazar."
  - "Kovaryat, etiket ve kavram kaymasını tanır; üretimde kayma izleme (PSI, KS testi, performans izleme) kurar."
  - "Bir model kartı (kullanım amacı, veri, başarım alt-grupları, sınırlılıklar, etik) hazırlar ve MLOps yaşam döngüsünü (sürümleme, izleme, yeniden eğitim) tanımlar."
  - "Federe öğrenmenin (FedAvg) çalışma ilkesini ve mahremiyet sınırlarını açıklar; diferansiyel mahremiyet ve güvenli toplama kavramlarını tanır."
  - "AB YZ Yasası ve FDA çerçevelerinin bir klinik YZ ürününe getirdiği yükümlülükleri özetler."
methods:
  - "Dış / zamansal doğrulama"
  - "Kayma tespiti (PSI, KS)"
  - "Model kartı"
  - "Federe öğrenme (FedAvg)"
  - "Diferansiyel mahremiyet"
tools:
  - "scikit-learn"
  - "evidently / alibi-detect"
  - "Flower (federe öğrenme)"
  - "Opacus"
  - "Model Card Toolkit"
datasets:
  - name: "İki farklı kaynaktan aynı görev (ör. MIMIC-III Demo + eICU örneği)"
    url: "https://physionet.org/content/eicu-crd-demo/"
    note: "Coğrafi dış doğrulama."
  - name: "10. haftanın CNN'i + farklı hastane röntgenleri"
    note: "Kovaryat kayması."
resources:
  - title: "Collins GS ve ark. TRIPOD+AI statement. BMJ 2024."
    url: "https://www.bmj.com/content/385/bmj-2023-078378"
    kind: dokuman
    note: "Raporlama standardı."
  - title: "Mitchell M ve ark. Model Cards for Model Reporting. FAT* 2019."
    url: "https://arxiv.org/abs/1810.03993"
    kind: makale
  - title: "Wong A ve ark. External validation of a widely implemented proprietary sepsis prediction model. JAMA Intern Med 2021."
    url: "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307"
    kind: makale
  - title: "Rieke N ve ark. The future of digital health with federated learning. npj Digit Med 2020."
    url: "https://www.nature.com/articles/s41746-020-00323-1"
    kind: makale
  - title: "Finlayson SG ve ark. The clinician and dataset shift in artificial intelligence. NEJM 2021."
    url: "https://www.nejm.org/doi/full/10.1056/NEJMc2104626"
    kind: makale
---

## Ön Okuma ve Hazırlık

Genel sınav için tüm haftaların 'Temel Kavramlar' bölümleri ve uygulama defterleri kapsam dâhilindedir. Son derste 45 dakikalık genel tekrar ve soru–cevap yapılır.

## Ders Notları

> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **Güvenilir ve klinik uygulamaya hazır yapay zeka: dış doğrulama, dağıtım kayması, model kartları/MLOps ve mahremiyet-koruyucu öğrenme (federated learning)**

Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.

## Temel Kavramlar

- **Dış doğrulama** — Modelin geliştirildiği kurum/zaman dışındaki bağımsız veride sınanması; yayın ve klinik kullanım için asgari kanıt.
- **Dağıtım kayması** — Kovaryat kayması (girdi dağılımı değişir), etiket kayması (prevalans değişir), kavram kayması (girdi–çıktı ilişkisi değişir: yeni tedavi kılavuzu).
- **Model kartı** — Modelin 'prospektüsü': amaç, eğitim verisi, alt-grup başarımı, bilinen sınırlılıklar, etik hususlar.
- **Federe öğrenme** — Verinin kurumdan çıkmadan, yalnızca model güncellemelerinin paylaşılmasıyla çok merkezli eğitim; mahremiyeti artırır ama tek başına garanti etmez.
- **Diferansiyel mahremiyet** — Tek bir bireyin varlığının çıktıyı ölçülebilir sınırın (ε) üzerinde değiştirmemesi garantisi; gürültü ekleme yoluyla sağlanır.

## Biyomedikal Uygulama Örnekleri

- Epic Sepsis Model'in dış doğrulaması (Wong ve ark., 2021): satıcının bildirdiği AUC 0.76–0.83 yerine bağımsız kurumda 0.63 ve yüksek alarm yükü.
- COVID-19 döneminde göğüs röntgeni modellerinde kavram kayması; pandemi öncesi eğitilmiş modellerin çöküşü.
- Çok merkezli beyin tümörü segmentasyonunda federe öğrenme (FeTS girişimi): veri paylaşılmadan 70+ kurumla eğitim.

## Uygulama / Laboratuvar

Dönem boyunca kurduğunuz bir modeli (tablo veya görüntü) farklı kaynaktan bir veri setinde dış doğrulayın; ayırt edicilik ve kalibrasyon düşüşünü raporlayın. PSI ile öznitelik kaymasını ölçün. Flower ile iki-üç 'kurum' simülasyonunda FedAvg çalıştırıp merkezî eğitimle karşılaştırın. Son teslim: modelinizin TRIPOD+AI uyumlu bir model kartı (2 sayfa).

## Tartışma Soruları

1. Bir hastane, satıcının sağladığı yapay zeka modelini kullanmaya başlamadan önce hangi asgari doğrulama kanıtını istemeli?
2. Federe öğrenme veriyi kurumdan çıkarmıyorsa mahremiyet sorunu çözülmüş sayılır mı? Model güncellemelerinden ne sızabilir?

## Haftanın Özeti

Dönemi, bir modelin klinik uygulamaya hazır sayılması için gereken kanıt ve süreçlerle kapattık: dış doğrulama, kayma izleme, model kartı, mahremiyet-koruyucu öğrenme ve regülasyon. Genel sınav dönem sonunda; tüm dönem içeriğini kapsar.
