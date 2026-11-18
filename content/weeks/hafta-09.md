---
week: 9
title: "Proje Ara Sunumları (Vize)"
topic: "Ara sınav (izlencede 8. hafta); yazılı sınav yerine proje ara sunumları olarak yapılır"
description: "Vize notu için proje ara sunumları: her öğrenci on dakikada klinik sorusunu, veri kararlarını, doğrulama tasarımını ve temel modelinin eğrilerini sunar. Hikâye köşesinde hesap yapan at Akıllı Hans."
module: m4
exam: true
status: hazir
changeNote: "Bu hafta ders işlenmez; vize notu için proje ara sunumları yapılır. İzlencede 9. haftada görünen derin öğrenmeye giriş konusu 11 Kasım'da işlendi."
tags:
  - "proje"
  - "sunum"
  - "vize"
  - "Akıllı Hans"
  - "kısayol öğrenme"
objectives:
  - "Projesinin klinik sorusunu, veri kararlarını ve doğrulama tasarımını on dakikada gerekçeleriyle sunar."
  - "Temel modelinin eğrilerini gösterir ve hangi tabloya benzediğini (sağlıklı, ezberci, emekleyen) söyler."
  - "Sorulara dürüst yanıt verir; bilmediği yerde nasıl bakacağını anlatır."
methods: []
tools:
  - "GitHub"
  - "PDF slayt"
datasets: []
resources:
  - title: "Clever Hans (Akıllı Hans): Pfungst'un 1907 tarihli incelemesinin özeti, Wikipedia"
    url: "https://en.wikipedia.org/wiki/Clever_Hans"
    kind: diger
  - title: "Lapuschkin S ve ark. Unmasking Clever Hans predictors and assessing what machines really learn. Nat Commun 2019."
    url: "https://doi.org/10.1038/s41467-019-08987-4"
    kind: makale
  - title: "Proje sayfası: ara sunum düzeni, slayt iskeleti ve vize ölçütleri"
    url: "https://drferhatu.github.io/biyomedikal-yapay-zeka/proje/#ara-sunum"
    kind: dokuman
---

## Sunum Günü

Yazılı ara sınav yok. Vize notu, bugünkü proje ara sunumu ve bugünkü depo durumu üzerinden verilir. Bitmiş bir proje beklenmiyor; şimdiye kadar verdiğiniz kararları ve gerekçelerini dinlemek istiyoruz.

| | |
|---|---|
| Ne zaman | 18 Kasım Çarşamba, ders saatinde (13.15) |
| Süre | 10 dakika sunum, 5 dakika soru |
| Sıra | Proje koduna göre: BVYZ-01'den başlayarak |
| Slayt | [Ortak şablon](/proje#ara-sunum) üzerinden: kapak, sekiz slayt ve kapanış; PDF |
| Teslim | Deponuzda `sunum/ara-sunum.pdf` olarak; 17 Kasım Salı gün sonuna kadar |

Slayt iskeleti ve yüz puanlık vize ölçütleri [proje sayfasının ara sunum bölümünde](/proje#ara-sunum).

## Hikâye Köşesi: Akıllı Hans

Bugün ders anlatmıyoruz, sunum dinliyoruz. Sayfa boş kalmasın diye size yüz yirmi yıllık bir hikâye bıraktım. Yapay zekâ tarihinde en çok anılan atın hikâyesi bu, ve bugün birbirinize soracağınız soruların hepsi aslında bu hikâyenin içinden çıkıyor.

### Berlin'de hesap yapan at

1900'lerin başında Berlin'de Wilhelm von Osten adında emekli bir matematik öğretmeni yaşıyordu. Hayvanların sanıldığından çok daha zeki olduğuna inanıyordu ve bunu kanıtlamak için yıllarını Hans adlı atına verdi. Karatahtanın önünde, bir çocuğa öğretir gibi sabırla çalıştı. Sonunda Hans, sorulan soruları ön ayağını yere vurarak yanıtlamaya başladı. Üç ile dördü topluyor ve yedi kez vuruyordu. Kesirlerle uğraşıyor, ayın kaçının hangi güne geldiğini buluyor, saati söylüyordu.

Von Osten gösterilerinden para almıyordu; bir şarlatan değildi, gördüğüne içtenlikle inanan bir öğretmendi. Avlusu her gün doluyor, gazeteler attan "Akıllı Hans" diye söz ediyordu.

### Kurul ne dedi?

Mesele o kadar büyüdü ki 1904'te bir kurul toplandı. Başında dönemin önde gelen psikologlarından Carl Stumpf vardı; yanında bir veteriner, bir sirk yöneticisi, süvari subayları, öğretmenler ve hayvanat bahçesinin müdürü oturuyordu. Hile aradılar. Gizli bir işaret, bir ip, bir yardımcı var mı diye baktılar. Bulamadılar, çünkü gerçekten yoktu. Kurulun vardığı sonuç şuydu: ortada bir hile yok.

Buraya kadar hikâye, bugün "modelimiz test verisinde çok başarılı" diyen bir makaleye benziyor. Sonuç etkileyici, hakemler ikna olmuş, kimse yalan söylemiyor.

### Pfungst'un iki sorusu

Stumpf'un genç öğrencisi Oskar Pfungst işin peşini bırakmadı ve iki basit şeyi değiştirdi. Önce soruyu, cevabını kendisi de bilmeyen birine sordurdu. Sonra atın soruyu soran kişiyi görmesini engelledi.

Sonuç çarpıcıydı. Soran kişi cevabı biliyorsa Hans soruların onda dokuzuna yakınını doğru yanıtlıyordu. Soran kişi cevabı bilmiyorsa ya da at onu göremiyorsa, Hans neredeyse hiçbir soruyu bilemiyordu.

Hans hesap yapmıyordu. İnsanı okuyordu. Soruyu soran kişi, at vurmaya başladığında farkında olmadan hafifçe öne eğiliyor, doğru sayıya yaklaşıldıkça geriliyor, doğru vuruşta ise başını belli belirsiz kaldırıp rahatlıyordu. Hans bu küçücük hareketi yakalıyor ve tam o anda duruyordu. İşin en ilginç yanı şu: von Osten bu işareti verdiğinin farkında değildi, Pfungst da kendini tutmaya çalıştığında bile işareti vermekten kendini alamadı.

Pfungst bulgularını 1907'de yayımladı. Von Osten sonuca hiçbir zaman ikna olmadı.

### Hans gerçekten "akılsız" mıydı?

Bana kalırsa hayır, ve hikâyenin bize en çok öğreten yeri burası. Hans çok iyi bir öğrenciydi. Yalnızca kendisine sorulduğunu sandığımız soruyu değil, ödüle giden en kısa yolu öğrenmişti. Havuç doğru sayıda vurunca geliyordu; doğru sayıyı bulmanın en kolay yolu da aritmetik değil, karşısındaki insanın yüzüydü.

Sinir ağları da tam olarak böyle öğrenir. Biz "zatürreyi bul" deriz; ağ, kaybı düşüren en kolay ipucunu bulur. O ipucu bazen akciğerde, bazen de görüntünün köşesinde durur.

### Yüz yıl sonra aynı at

2019'da bir araştırma ekibi, at fotoğraflarını çok iyi tanıyan bir görüntü sınıflandırıcısının nereye baktığını inceledi. Model ata bakmıyordu. Veri setindeki at fotoğraflarının çoğu aynı kaynaktan geliyordu ve sol alt köşelerinde küçük bir kaynak yazısı vardı; model o yazıyı tanımayı öğrenmişti. Araştırmacılar makalelerinin başlığına Hans'ın adını koydular (Lapuschkin ve ark., 2019). Bir at sınıflandırıcısının Akıllı Hans çıkması, bu alanın en güzel tesadüflerinden biridir.

Sağlıkta bedeli daha ağır. Göğüs röntgeninden zatürre tanıyan bir modelin, hastalığın yanında görüntünün hangi hastaneden geldiğini de öğrendiği gösterildi; model başka bir hastanenin verisine götürüldüğünde başarımı düştü (Zech ve ark., 2018). [8. haftada](/haftalar/hafta-08) konuştuğumuz COVID-19 modellerinin hikâyesi de aynı hikâyedir. Bu yüzden alanda, kısayoldan öğrenen modellere bugün de "Akıllı Hans" denir.

### Bugün salonda Pfungst olun

Kurul hile aradı ve bulamadı. Pfungst ise başka bir şey sordu: at cevabı nereden biliyor? Bugün her sunumda arkadaşınıza soracağınız soru budur.

- Modelin cevabı nereden biliyor? Tahmin anında elinde olmayacak bir sütun veriye karışmış olabilir mi?
- Aynı hasta hem eğitimde hem testte var mı? Varsa model hastalığı değil, hastayı tanıyor olabilir.
- Sonuç, veri başka bir merkezden ya da başka bir cihazdan gelseydi de aynı kalır mıydı?
- Model neye bakıyor? Açıklanabilirlik yöntemleri, Pfungst'un atın gözüne taktığı perdenin bugünkü karşılığıdır.

Sunan arkadaşınız için de aynı şey geçerli. "Bunu denemedim, şöyle bakarım" demek, von Osten gibi sonuca inanmakta diretmekten çok daha değerlidir.

> [!not] Hikâyenin özü
> Hans'ı ele veren şey daha zor sorular olmadı. Onu ele veren, soruyu soranın cevabı bilmediği tek bir deneydi. İyi bir doğrulama tasarımı tam olarak budur: modelin cevabı başka bir yerden okuyamayacağı bir sınav kurmak.

## Sunumda Ne Anlatılır?

Sekiz başlık, yaklaşık birer slayt: klinik soru, veri, keşif, ön işleme kararları, doğrulama tasarımı, temel model ve eğrileri, karşılaştığınız sorunlar ve kalan plan, kısa bir depo turu. Her kararın yanında bir cümlelik gerekçesi olsun. "Medyanla doldurdum" bir karardır; "eksiklik sınıfla ilişkili olduğu için gösterge sütunu da ekledim" gerekçeli bir karardır.

> [!neden] Yüksek AUC puan getirmez
> Puanı gerekçeli karar getirir. Sızıntıyı fark edip düzelttiğini ve bu yüzden başarımının düştüğünü anlatan bir sunum, şişmiş bir sonuçtan daha yüksek not alır.

## Sık Yapılan Hatalar

- **Yalnızca eğitim sonucunu göstermek.** [8. haftadaki](/haftalar/hafta-08) ezberci vakayı hatırlayın; eğitim ve doğrulama sonuçları yan yana gösterilir.
- **Bölme stratejisini atlamak.** "Veriyi yüzde seksen, yüzde yirmi böldüm" yeterli değildir. Bir hastanın kaç satırı var, satırlar nasıl bölündü?
- **Doğruluk raporlamak.** Sınıflar dengesizse doğruluk bir şey söylemez; görevinize uygun ölçütü kullanın.
- **Grafiği okumamak.** Her grafiğin altında bir cümle olsun: bu grafik ne söylüyor?
- **Süreyi aşmak.** On dakika, sekiz slayttır. Prova yapın.

## Sunumdan Sonra

Sorular ve geri bildirim, son rapora kadar yapacaklarınızın listesidir; not alın ve deponuzda bir yapılacaklar dosyasına yazın. 25 Kasım'da derse tıbbi görüntü ve evrişimli ağlarla devam ediyoruz.
