---
week: 8
title: "Proje Atölyesi: Veriden İlk Modele"
topic: "Ara sınav (izlencede) — öğretim üyesi kararıyla dönem projesi atölyesi olarak işlenir"
description: "Ara sınav yerine uygulamalı proje atölyesi: herkes kendi veri setiyle çalışır; ön işleme kararları, doğrulama tasarımı ve ilk model birlikte gözden geçirilir."
module: m3
exam: false
status: hazir
changeNote: "İzlencedeki ara sınav yapılmayacak; dönem notunun %50'si proje ile belirlenir. Bu derste herkes kendi proje verisiyle çalışır."
tags:
  - "proje"
  - "atölye"
  - "doğrulama tasarımı"
objectives:
  - "Kendi proje verisinde eksik veri, sızıntı ve bölme stratejisi kararlarını gerekçelendirir."
  - "Temel modeli (lojistik regresyon) kurup dört klinik grafiği (ROC, PR, kalibrasyon, karar eğrisi) üretir."
  - "Ara rapor için Yöntem ve Sonuçlar bölümlerinin iskeletini çıkarır."
methods:
  - "Pipeline"
  - "GroupKFold"
  - "Klinik metrikler"
tools:
  - "Google Colab"
  - "scikit-learn"
  - "GitHub"
datasets:
  - name: "Herkesin kendi proje veri seti"
    note: "Proje sayfasındaki kartınız."
resources:
  - title: "Proje sayfası: teslimler, şablonlar, değerlendirme"
    url: "https://drferhatu.github.io/biyomedikal-yapay-zeka/proje/"
    kind: dokuman
---

## Ön Okuma ve Hazırlık

Bilgisayarınızla ve ilk teslimde gönderdiğiniz depo ile gelin. Verinizin indirilmiş ve defterin ilk hücresinin çalışır durumda olması yeterli. Şu üç soruya bir cümlelik cevabınız hazır olsun: pozitif sınıf oranı kaç, bir hastanın kaç satırı var, "tahmin anında bilinemeyecek" bir sütun var mı?

## Ders Notları

Bu hafta anlatım yok; çalışma var. İzlencede ara sınav olarak görünen hafta, dönem projesine ayrıldı. Ders boyunca herkes kendi verisinde ilerler, ben masalara uğrarım. Hedef, dersin sonunda her deponun şu üç şeyi içermesi: sızıntısız bir boru hattı, hasta-bazlı ya da gerekçeli bir bölme stratejisi ve dört klinik grafiğiyle temel bir model. Bunlar ara raporun (2 Aralık) Yöntem ve Sonuçlar bölümlerinin iskeletidir.

Ders şu sırayla ilerler. İlk yarım saat herkes 2. haftanın kontrol listesini kendi verisine uygular: eksikler, sızıntı adayları, grup sütunu. Sonraki saat temel model ve dört grafik; şablondaki başlangıç defteri bunun için yeterli. Son saatte her öğrenci üç dakikada kendi dört grafiğini gösterir ve bir soru sorar.

> [!not] Hangi haftaya bakmalıyım?
> Eksik veri ve bölme için 2. hafta, keşif ve öznitelik için 3. hafta, dört grafik için 4. hafta, modeller ve öznitelik önemi için 5. hafta. Sinyal projeleri (BVYZ-03, 04, 08) için 7. hafta, görüntü projesi (BVYZ-05) için 10. haftayı bekleyin; o güne kadar tablo biçimindeki özniteliklerle ilerleyin.

## Uygulama / Laboratuvar

Kendi deponuzdaki başlangıç defterini açın ve sırayla ilerleyin: veri indirme hücresi çalışıyor mu, hedef ve grup sütunu tanımlı mı, boru hattı kuruldu mu, dört grafik üretildi mi, grafikler `rapor/sekiller/` altına kaydedildi mi? Takıldığınız yerde elinizi kaldırın.

## Tartışma Soruları

1. Verinizde grup sütunu yoksa bunun nedeni gerçekten her hastanın tek satırı olması mı, yoksa hasta kimliğinin veride bulunmaması mı? İkincisiyse bu, raporun sınırlılıklar bölümüne girer.
2. Temel modelinizin kalibrasyon eğrisi köşegenden sapıyorsa bunun bir sonraki adımdaki anlamı ne?

## Haftanın Özeti

Dönemin ilk yarısını sınavla değil, herkesin kendi verisinde kurduğu ilk modelle kapattık. İkinci yarı derin öğrenme ile başlıyor; sinyal ve görüntü projeleri orada hız kazanacak.
