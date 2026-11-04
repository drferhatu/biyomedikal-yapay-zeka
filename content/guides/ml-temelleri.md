---
title: "Sıfırdan Makine Öğrenmesi: Tamamlayıcı Yol Haritası"
description: "Bu derse makine öğrenmesi, istatistik ya da Python temeli olmadan gelenler için haftalara bağlı, ücretsiz kaynaklardan kurulu bir yetişme planı. Hangi haftadan önce neyi bitirmeli, kaç saat sürer."
order: 0
---

## Bu rehber kimin için?

Bu ders lisansüstü düzeyde ve bazı şeyleri temelden almıyor. Lojistik regresyonun ne olduğunu, bir DataFrame'in nasıl filtrelendiğini, olasılığın ne anlama geldiğini bildiğinizi varsayıyor. Mühendislik ya da sağlık kökenli olup bu temelleri hiç almamış ya da yıllar önce almış olmanız çok normal; sınıfın yarısı öyle. Bu rehber o açığı kapatmak için var.

Aşağıdaki kaynakların hepsi ücretsiz, çoğu tarayıcıda çalışıyor ve hiçbiri "önce şu kitabı bitirin" demiyor. Yol haritası dersin haftalarına bağlı: her aşamanın yanında "şu haftadan önce" yazıyor. Toplam yük yaklaşık 25–35 saat; dönem boyunca haftada iki üç saat ayırmak yeterli.

> [!not] Nasıl kullanmalı?
> Hepsini baştan sona yapmanız gerekmiyor. Hangi haftada zorlandıysanız o aşamaya gidin. Aşağıdaki tabloyu yazdırıp yanınızda tutmak işe yarar; bitirdiğiniz kutuyu işaretleyin.

## Tek bakışta: hangi haftadan önce ne?

| Aşama | Konu | Şu haftadan önce | Süre |
|---|---|---|---|
| 0 | Python ve pandas ile veri | Hafta 2 | 6–8 saat |
| 1 | Makine öğrenmesi sezgisi | Hafta 4 | 6–8 saat |
| 2 | Olasılık, istatistik ve metrikler | Hafta 4 | 3–4 saat |
| 3 | scikit-learn ile uygulama | Hafta 5 | 4–6 saat |
| 4 | Sinyal işleme temelleri | Hafta 7 | 2–3 saat |
| 5 | Sinir ağları ve derin öğrenme | Hafta 9 | 5–8 saat |
| 6 | Açıklanabilirlik | Hafta 12 | 2–3 saat |
| — | Matematik tazeleme (isteğe bağlı) | İhtiyaç oldukça | 3–5 saat |

## Aşama 0 · Python ve pandas ile veri (Hafta 2'den önce)

Dersteki her defter pandas DataFrame'leriyle başlar. "Sütun seç, filtrele, grupla, ortalama al" diyebilmeniz yeterli; program yazmayı öğrenmeniz gerekmiyor.

- **Kaggle Learn – Python** · [kaggle.com/learn/python](https://www.kaggle.com/learn/python) · Yedi kısa ders, tarayıcıda çalışır, yaklaşık 5 saat. Daha önce hiç kod yazmadıysanız buradan başlayın; yazdıysanız atlayın.
- **Kaggle Learn – Pandas** · [kaggle.com/learn/pandas](https://www.kaggle.com/learn/pandas) · Altı ders, yaklaşık 4 saat. Dersin 2. ve 3. haftalarında yaptığımız her şeyin temeli. Bunu atlamayın.
- **Python for Data Analysis**, Wes McKinney · [wesmckinney.com/book](https://wesmckinney.com/book/) · Pandas'ın yazarından, çevrimiçi ve ücretsiz. Başvuru kaynağı; baştan okumayın, takıldığınız fonksiyonu arayın.

Ne zaman hazırsınız? 2. haftanın defterindeki "eksik oranı" ve "sınıfa göre eksiklik" hücrelerini okuyup ne yaptığını söyleyebiliyorsanız.

## Aşama 1 · Makine öğrenmesi sezgisi (Hafta 4'ten önce)

"Model" dediğimiz şey ne, "öğrenmek" ne demek, eğitim ve test neden ayrı? Bu soruların cevabını sezgisel olarak bilmek, 4. haftadan sonrasını çok rahatlatır.

- **Google Machine Learning Crash Course** · [developers.google.com/machine-learning/crash-course](https://developers.google.com/machine-learning/crash-course) · Google'ın ücretsiz giriş kursu; kısa videolar ve etkileşimli alıştırmalar. Yalnızca şu modülleri yapın: *Introduction to ML*, *Linear regression*, *Logistic regression*, *Classification*, *Overfitting*. Yaklaşık 5 saat. "Classification" modülü dersin 4. haftasıyla birebir örtüşür: duyarlılık, özgüllük, ROC, AUC.
- **Kaggle Learn – Intro to Machine Learning** · [kaggle.com/learn/intro-to-machine-learning](https://www.kaggle.com/learn/intro-to-machine-learning) · Yedi ders, 3 saat; karar ağacı ve Random Forest'ı tek bir veri setinde kurarsınız. 5. haftaya iyi bir ön hazırlık.
- **StatQuest (Josh Starmer)** · [statquest.org](https://statquest.org/video-index/) · YouTube'daki en iyi "sıfırdan" anlatımlar; her video 10–20 dakika. Önerilen sıra: *Machine Learning Fundamentals: Bias and Variance*, *Logistic Regression*, *ROC and AUC*, *Decision Trees*, *Random Forests Part 1*, *Gradient Boost Part 1*. Derste bir kavramı anlamadıysanız önce buraya bakın.

> [!ornek] Hangisini seçmeli?
> Vaktiniz kısıtlıysa yalnızca Google kursunun beş modülünü ve StatQuest'in ROC videosunu yapın. Bu ikisi 4. haftayı taşır. Gerisi sonraya kalabilir.

## Aşama 2 · Olasılık, istatistik ve metrikler (Hafta 4'ten önce)

Dersin en çok döndüğü kavramlar: olasılık, koşullu olasılık (prevalans tuzağı), dağılım, ortalama ile medyan farkı. Derin istatistik gerekmiyor; sezgi gerekiyor.

- **Seeing Theory** · [seeing-theory.brown.edu](https://seeing-theory.brown.edu/) · Olasılık ve istatistiği etkileşimli görsellerle anlatan ücretsiz site. *Basic Probability*, *Compound Probability* (koşullu olasılık ve Bayes) ve *Frequentist Inference* bölümleri yeterli; 2 saat.
- **StatQuest** · *Sensitivity and Specificity*, *Confusion Matrix*, *Bayes' Theorem*. Toplam 40 dakika; 4. haftanın "yüzde doksan beş doğru test" örneğini anlamak için.
- **Khan Academy – Statistics and Probability** · [khanacademy.org/math/statistics-probability](https://www.khanacademy.org/math/statistics-probability) · Daha sistemli isteyenler için; yalnızca *Probability* ve *Random variables* üniteleri.

## Aşama 3 · scikit-learn ile uygulama (Hafta 5'ten önce)

Dersteki kodun neredeyse tamamı scikit-learn. `Pipeline`, `cross_val_score`, `GroupKFold` gibi adlar size yabancı geliyorsa bu aşama o yabancılığı giderir.

- **scikit-learn MOOC (Inria)** · [inria.github.io/scikit-learn-mooc](https://inria.github.io/scikit-learn-mooc/) · Kütüphanenin geliştiricilerinden ücretsiz, çevrimiçi kurs. Yalnızca ilk iki modülü yapın: *The predictive modeling pipeline* ve *Selecting the best model*. Yaklaşık 6 saat. Dersin 2. haftasında anlattığımız "her şey Pipeline içinde" ilkesini burada derinlemesine görürsünüz.
- **scikit-learn – Getting Started** · [scikit-learn.org/stable/getting_started.html](https://scikit-learn.org/stable/getting_started.html) · 20 dakikalık resmî başlangıç; MOOC'a vakit yoksa en azından bu.
- **Kaggle Learn – Intermediate Machine Learning** · [kaggle.com/learn/intermediate-machine-learning](https://www.kaggle.com/learn/intermediate-machine-learning) · Eksik veri, kategorik değişken, Pipeline, çapraz doğrulama, XGBoost ve veri sızıntısı. 4 saat. Dersin 2. ve 5. haftalarının Kaggle versiyonu; sızıntı dersi özellikle iyi.

## Aşama 4 · Sinyal işleme temelleri (Hafta 7'den önce)

Yalnızca sinyal projesi olanlar (EKG, PPG, EEG) ve 7. haftada "frekans" kelimesinde kaybolanlar için.

- **The Scientist and Engineer's Guide to DSP**, Steven Smith · [dspguide.com](https://www.dspguide.com/pdfbook.htm) · Ücretsiz PDF; mühendis olmayanlar için yazılmış en iyi sinyal işleme kitabı. Yalnızca 2. bölüm (*Statistics, Probability and Noise*), 3. bölüm (*ADC and DAC*: örnekleme ve Nyquist) ve 8. bölüm (*The Discrete Fourier Transform*) yeterli; 3 saat.
- **SciPy – Signal processing tutorial** · [docs.scipy.org/doc/scipy/tutorial/signal.html](https://docs.scipy.org/doc/scipy/tutorial/signal.html) · Derste kullandığımız `butter`, `filtfilt`, `welch`, `find_peaks` fonksiyonlarının belgesi.
- **NeuroKit2 belgeleri** · [neuropsychology.github.io/NeuroKit](https://neuropsychology.github.io/NeuroKit/) · EKG, PPG ve EEG için hazır işleme hatları; projelerde kısayol.

## Aşama 5 · Sinir ağları ve derin öğrenme (Hafta 9'dan önce)

Dersin ikinci yarısı burada başlıyor. Sinir ağının ne olduğunu "görmüş" olmak, 9. haftanın matematiğini çok kolaylaştırır.

- **3Blue1Brown – Neural Networks** · [3blue1brown.com/topics/neural-networks](https://www.3blue1brown.com/topics/neural-networks) · Dört video, yaklaşık 1 saat. Sinir ağının ve geri yayılımın ne yaptığını görsel olarak anlatan en iyi kaynak. 9. haftadan önce mutlaka.
- **Kaggle Learn – Intro to Deep Learning** · [kaggle.com/learn/intro-to-deep-learning](https://www.kaggle.com/learn/intro-to-deep-learning) · Altı ders, 4 saat; ilk ağınızı kurarsınız (Keras ile; derste PyTorch kullanıyoruz ama kavramlar aynı).
- **PyTorch – Learn the Basics** · [pytorch.org/tutorials/beginner/basics/intro.html](https://pytorch.org/tutorials/beginner/basics/intro.html) · Derste kullanacağımız kütüphanenin resmî başlangıcı; 2 saat.
- **fast.ai – Practical Deep Learning for Coders** · [course.fast.ai](https://course.fast.ai/) · Daha fazlasını isteyenler için; ücretsiz, uygulama odaklı, tıbbi görüntü örnekleri içeriyor. İlk iki ders 10. haftanın (CNN, transfer öğrenme) iyi bir hazırlığı.

## Aşama 6 · Açıklanabilirlik (Hafta 12'den önce)

- **Kaggle Learn – Machine Learning Explainability** · [kaggle.com/learn/machine-learning-explainability](https://www.kaggle.com/learn/machine-learning-explainability) · Permütasyon önemi, kısmi bağımlılık ve SHAP; dört ders, 3 saat. Dersin 12. ve 13. haftalarının neredeyse birebir ön hazırlığı.
- **Interpretable Machine Learning**, Christoph Molnar · [christophm.github.io/interpretable-ml-book](https://christophm.github.io/interpretable-ml-book/) · Dersin ana kitabı, ücretsiz. 1. haftada ilk iki bölümünü okumuştunuz; 12. haftadan önce *Global Model-Agnostic Methods* bölümüne göz atın.

## Matematik tazeleme (isteğe bağlı)

Derste türetim yapmıyoruz ama "vektör", "matris", "gradyan" kelimeleri geçiyor. Bunlar rahatsız ediyorsa:

- **3Blue1Brown – Essence of Linear Algebra** · [3blue1brown.com/topics/linear-algebra](https://www.3blue1brown.com/topics/linear-algebra) · İlk altı video yeterli; PCA'yı (3. hafta) gerçekten anlamak için.
- **Khan Academy – Linear Algebra** ve **Calculus** · [khanacademy.org/math](https://www.khanacademy.org/math) · Türev ve zincir kuralı (9. hafta geri yayılım) için yalnızca *Derivatives: chain rule* ünitesi.

## Türkçe kaynaklar

- **BTK Akademi** · [btkakademi.gov.tr](https://www.btkakademi.gov.tr/) · Ücretsiz Türkçe kurslar; "Python ile Makine Öğrenmesi" ve "Veri Bilimi" başlıklarını arayın. Hız ve derinlik yukarıdakilerden düşük ama dil engeli olanlar için iyi bir başlangıç.
- **StatQuest videolarının Türkçe altyazısı** · YouTube'da çoğu videoda otomatik Türkçe altyazı açılabiliyor; kalite değişken ama izlenebilir.

> [!uyari] Yapay zeka asistanlarını öğretmen olarak kullanın, cevap anahtarı olarak değil
> Bir kavramı anlamadığınızda ChatGPT, Claude ya da Gemini'ye "bunu hiç bilmeyen birine anlat, sonra bana bir soru sor" demek çok etkilidir. Ama yukarıdaki kaynaklardaki alıştırmaları asistana çözdürürseniz hiçbir şey öğrenmezsiniz. Kod yazdırın, ama çıkan kodu satır satır açıklattırın.

## Takıldığınızda

Rehberdeki hiçbir kaynak bir kavramı açmıyorsa ofis saatine gelin ya da e-posta yazın; hangi aşamada takıldığınızı söylemeniz yeterli. Sınıfta birkaç kişi aynı yerde takılıyorsa dersin başında on dakika ayırıp birlikte bakarız.
