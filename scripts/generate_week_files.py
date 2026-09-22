#!/usr/bin/env python
"""14 haftalık ders izlencesinden content/weeks/hafta-XX.md dosyalarını üretir.

Bu script yalnızca İLK iskeleti oluşturmak içindir. Var olan bir dosyanın üzerine
yazmaz (--force verilmedikçe); böylece elle düzenlenen ders notları korunur.

Kullanım:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/generate_week_files.py [--force]
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "weeks"
MODULES = json.loads((ROOT / "content" / "data" / "modules.json").read_text(encoding="utf-8"))


def module_of(week):
    for m in MODULES:
        if week in m["weeks"]:
            return m
    raise KeyError(week)


# ---------------------------------------------------------------------------
# Haftalık içerik (DOCX izlencedeki "Konu" sütunu "topic" alanında özgün hâliyle korunur)
# ---------------------------------------------------------------------------
WEEKS = [
 dict(n=1, title="Biyomedikal Veri Bilimi ve Yapay Zekaya Giriş",
  topic="Biyomedikal veri bilimi ve yapay zekaya giriş: veri türleri (klinik, sinyal, görüntü, omik, EHR), problem tipleri, etik ve regülasyon",
  desc="Beş biyomedikal veri türü, denetimli/denetimsiz problem tipleri, dersin uçtan uca iş akışı ve etik–regülasyon çerçevesi.",
  tags=["giriş", "veri türleri", "EHR", "omik", "etik", "regülasyon", "problem tipleri"],
  methods=["Problem çerçeveleme", "İş akışı (pipeline)", "Etik & regülasyon"],
  objectives=["Klinik, sinyal, görüntü, omik ve EHR verilerinin yapısal farklarını ve her birine özgü analiz zorluklarını açıklar.",
              "Bir biyomedikal soruyu sınıflandırma, regresyon, kümeleme, segmentasyon veya zaman serisi tahmini olarak çerçeveler.",
              "Veri → ön işleme → model → klinik metrik → açıklama → güven iş akışını tanımlar ve dersin modülleriyle eşler.",
              "Sağlıkta yapay zeka için etik ilkeleri (mahremiyet, adalet, hesap verebilirlik) ve temel regülasyon çerçevelerini (KVKK, AB YZ Yasası, FDA) tanır."],
  concepts=[("Biyomedikal veri", "Klinik ölçüm, fizyolojik sinyal, tıbbi görüntü, moleküler (omik) profil ve elektronik sağlık kaydından oluşan, heterojen ve çoğu zaman eksik veri."),
            ("Problem tipi", "Sorunun makine öğrenmesi diline çevirisi: ikili sınıflandırma (hasta/sağlıklı), regresyon (yatış süresi), kümeleme (alt-tip), segmentasyon (lezyon maskesi), tahmin (zaman serisi)."),
            ("Etiket kalitesi", "Referans standardın (altın standart) güvenilirliği; gürültülü etiket, modelin tavan başarımını sınırlar."),
            ("Yüksek riskli YZ", "AB Yapay Zeka Yasası'nda tıbbi cihaz niteliğindeki sistemler; şeffaflık, insan gözetimi ve doğruluk yükümlülükleri getirir.")],
  examples=["MIMIC-IV yoğun bakım kayıtlarından 48 saat içinde mortalite tahmini: hangi veri türleri birleşir, etiket nasıl tanımlanır?",
            "Dermatoskopik görüntüden melanom sınıflandırması: FDA onaylı bir sistemin karşılaması gereken performans ve şeffaflık koşulları."],
  tools=["Python", "Google Colab", "pandas", "scikit-learn"],
  datasets=[("UCI Breast Cancer Wisconsin (Diagnostic)", "https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic", "Dönemin ilk uygulamasında tablo verisine örnek."),
            ("PhysioNet", "https://physionet.org/", "Sinyal ve EHR veri türlerine genel bakış için.")],
  activity="Verilen üç biyomedikal problemi (sepsis erken uyarı, EEG'de nöbet tespiti, patoloji lamında tümör segmentasyonu) veri türü, problem tipi, etiket kaynağı ve klinik metrik açısından tabloya dökün. Ardından Colab'de Breast Cancer veri setini yükleyip boyutlarını, sınıf dağılımını ve eksik değer durumunu raporlayın.",
  questions=["Aynı hastanın verisinin hem eğitim hem test kümesinde bulunması neden 'sızıntı'dır ve bu neden biyomedikal veride diğer alanlardan daha sık görülür?",
             "Yüksek doğruluklu ama açıklanamayan bir model ile daha düşük doğruluklu ama yorumlanabilir bir model arasında klinik seçim hangi koşullara bağlıdır?"],
  summary="Dersin haritasını çizdik: beş veri türü, problem tipleri, uçtan uca iş akışı ve etik–regülasyon çerçevesi. Bundan sonraki her hafta bu haritanın bir bölgesini derinleştirecek.",
  before="Ders öncesi Molnar'ın *Interpretable Machine Learning* kitabının 'Introduction' ve 'Interpretability' bölümlerini (yaklaşık 20 sayfa) okuyun. Google hesabınızla colab.research.google.com adresine giriş yapabildiğinizi kontrol edin.",
  readings=[("Topol E. High-performance medicine: the convergence of human and artificial intelligence. Nat Med 2019.", "https://www.nature.com/articles/s41591-018-0300-7", "makale", "Sağlıkta YZ'nin panoramik derlemesi."),
            ("Rajkomar A, Dean J, Kohane I. Machine Learning in Medicine. NEJM 2019.", "https://www.nejm.org/doi/full/10.1056/NEJMra1814259", "makale", "Klinisyen gözüyle makine öğrenmesi."),
            ("WHO. Ethics and governance of artificial intelligence for health. 2021.", "https://www.who.int/publications/i/item/9789240029200", "dokuman", "Altı etik ilke.")]),

 dict(n=2, title="Biyomedikal Verinin Doğası ve Ön İşleme",
  topic="Biyomedikal verinin doğası ve ön işleme: eksik veri, gürültü, normalizasyon, dengesiz sınıflar, veri sızıntısı ve hasta-bazlı veri bölme",
  desc="Eksik veri mekanizmaları ve imputasyon, gürültü ve aykırı değer, ölçekleme, dengesiz sınıf stratejileri, veri sızıntısı ve GroupKFold ile hasta-bazlı bölme.",
  tags=["eksik veri", "imputasyon", "normalizasyon", "dengesiz sınıf", "veri sızıntısı", "GroupKFold", "SMOTE"],
  methods=["MCAR/MAR/MNAR", "İmputasyon", "StandardScaler", "SMOTE / ağırlıklandırma", "GroupKFold"],
  objectives=["Eksik veri mekanizmalarını (MCAR, MAR, MNAR) ayırt eder ve uygun imputasyon stratejisini gerekçelendirir.",
              "Ölçekleme ve normalizasyonu yalnızca eğitim kümesine uydurup test kümesine uygulayarak sızıntıyı önler.",
              "Dengesiz sınıflarda yeniden örnekleme, sınıf ağırlığı ve eşik ayarı seçeneklerini karşılaştırır.",
              "Hasta-bazlı (grup) bölme ve zaman-farkında bölmeyi scikit-learn `Pipeline` ve `GroupKFold` ile uygular."],
  concepts=[("Eksik veri mekanizması", "MCAR: rastgele; MAR: gözlenen değişkenlere bağlı; MNAR: eksikliğin kendisi bilgi taşır (ağır hasta → daha çok test)."),
            ("Veri sızıntısı", "Test bilgisinin eğitime karışması: ölçekleyicinin tüm veriye uydurulması, aynı hastanın iki kümede olması, gelecekteki bilginin özniteliğe girmesi."),
            ("Dengesiz sınıf", "Nadir hastalıkta pozitif oranının %1–5 olması; doğruluğun anlamsızlaştığı, PR-AUC'nin öne çıktığı rejim."),
            ("Pipeline", "Ön işleme ve modelin tek nesnede zincirlenmesi; çapraz doğrulamada her katlamada yeniden uydurulur.")],
  examples=["Yoğun bakım laboratuvar verisinde laktat ölçümünün eksikliği, hastanın stabil olduğunun göstergesidir (MNAR): eksiklik göstergesi (indicator) eklemek başarımı artırır.",
            "EEG nöbet veri setinde kayıt-bazlı bölme yerine rastgele bölme yapıldığında AUC 0.98'den 0.82'ye düşer: sızıntının maskelediği gerçek başarım."],
  tools=["pandas", "scikit-learn", "imbalanced-learn"],
  datasets=[("Pima Indians Diabetes", "https://www.kaggle.com/datasets/uciml/pima-indians-diabetes-database", "Sıfırla kodlanmış eksik değerler; imputasyon alıştırması."),
            ("MIMIC-III Clinical Database Demo", "https://physionet.org/content/mimiciii-demo/", "100 hastalık açık demo; hasta-bazlı bölme için.")],
  activity="Pima veri setinde sıfırların aslında eksik değer olduğunu saptayın; medyan, KNN ve MICE imputasyonunu bir `Pipeline` içinde karşılaştırın. Ardından aynı veriyi (1) rastgele `KFold`, (2) `StratifiedKFold`, (3) hasta kimliği ile `GroupKFold` kullanarak çapraz doğrulayın ve farkı raporlayın.",
  questions=["Eksik değer göstergesi (missing indicator) eklemek ne zaman bilgi kazandırır, ne zaman bir tür sızıntıdır?",
             "SMOTE gibi sentetik örnekleme yöntemleri klinik veride hangi riskleri taşır?"],
  summary="Modelden önce veriyle uğraştık: eksik veri mekanizmaları, sızıntı kaynakları, dengesiz sınıflar ve hasta-bazlı bölme. Bu hafta öğrenilen disiplin dersin geri kalanındaki her modelin ön koşulu.",
  before="scikit-learn dokümantasyonunda 'Cross-validation: evaluating estimator performance' bölümündeki GroupKFold ve TimeSeriesSplit kısımlarını okuyun.",
  readings=[("Kaufman S ve ark. Leakage in data mining: formulation, detection, and avoidance. ACM TKDD 2012.", "https://dl.acm.org/doi/10.1145/2382577.2382579", "makale", "Sızıntının sistematik sınıflaması."),
            ("van Buuren S. Flexible Imputation of Missing Data (2. baskı, çevrimiçi).", "https://stefvanbuuren.name/fimd/", "kitap", "İmputasyon için açık erişimli referans."),
            ("scikit-learn: Pipelines and composite estimators", "https://scikit-learn.org/stable/modules/compose.html", "dokuman", "")]),

 dict(n=3, title="Keşifçi Veri Analizi, Öznitelik Mühendisliği ve Boyut İndirgeme",
  topic="Keşifçi veri analizi, öznitelik mühendisliği ve boyut indirgeme (PCA, UMAP)",
  desc="Görsel ve istatistiksel keşif, alan bilgisiyle öznitelik türetme, özellik seçimi, PCA'nın doğrusal cebiri ve UMAP ile doğrusal olmayan gömme.",
  tags=["EDA", "öznitelik mühendisliği", "PCA", "UMAP", "t-SNE", "özellik seçimi", "omik"],
  methods=["EDA", "Öznitelik türetme", "PCA", "UMAP", "Özellik seçimi"],
  objectives=["Dağılım, korelasyon ve grup karşılaştırmalarıyla veri setini sistematik biçimde keşfeder ve veri kalitesi sorunlarını raporlar.",
              "Alan bilgisine dayalı öznitelikler (oranlar, zaman pencereleri, klinik skorlar) türetir ve filtre/sarmal/gömülü seçim yöntemlerini uygular.",
              "PCA'yı kovaryans matrisinin özayrışımı olarak açıklar; açıklanan varyans ve yüklemeleri yorumlar.",
              "UMAP ve t-SNE'yi keşif amaçlı kullanır; gömme uzaklıklarının yorum sınırlarını bilir."],
  concepts=[("Öznitelik mühendisliği", "Ham değişkenlerden model için daha bilgilendirici temsiller türetme: kreatinin/eGFR, nabız değişkenliği, son 24 saat maksimumu."),
            ("Boyut laneti", "Öznitelik sayısı örnek sayısına yaklaştıkça uzaklıkların anlamsızlaşması; omik veride (p ≫ n) temel sorun."),
            ("PCA", "Veriyi en yüksek varyanslı ortogonal eksenlere yansıtan doğrusal dönüşüm; bileşenler özvektörler, varyanslar özdeğerlerdir."),
            ("UMAP", "Topolojik komşuluk yapısını koruyarak düşük boyuta gömen doğrusal olmayan yöntem; küme aralıkları ve şekilleri nicel yorum kabul etmez.")],
  examples=["Gen ifadesi (~20.000 gen × 200 hasta) verisinde PCA ile ilk 50 bileşene indirgeme, ardından UMAP ile alt-tip haritası.",
            "Yoğun bakım vital serilerinden 6 saatlik pencerelerde ortalama, eğim ve değişkenlik özniteliklerinin türetilmesi."],
  tools=["pandas", "seaborn", "scikit-learn", "umap-learn"],
  datasets=[("GEO GDS / TCGA örnek ifade matrisi", "https://www.ncbi.nlm.nih.gov/geo/", "p ≫ n rejiminde PCA/UMAP."),
            ("UCI Heart Disease", "https://archive.ics.uci.edu/dataset/45/heart+disease", "Öznitelik türetme alıştırması.")],
  activity="Heart Disease veri setinde tam bir EDA raporu üretin (dağılımlar, korelasyon matrisi, hedefe göre grup karşılaştırmaları). En az üç türetilmiş öznitelik ekleyin ve `SelectKBest` ile `RFE` sonuçlarını karşılaştırın. Bir ifade matrisinde PCA açıklanan varyans eğrisini çizip UMAP gömmesini renklendirin.",
  questions=["UMAP grafiğinde iki kümenin uzak görünmesi biyolojik olarak 'çok farklı' oldukları anlamına gelir mi?",
             "Özellik seçimini çapraz doğrulama döngüsünün dışında yapmak neden sızıntıdır?"],
  summary="Veriyi tanımanın ve yeniden temsil etmenin araçlarını kurduk: keşif, öznitelik türetme, seçim ve boyut indirgeme. Modül 1 tamamlandı; artık model kurmaya hazırız.",
  readings=[("McInnes L, Healy J, Melville J. UMAP: Uniform Manifold Approximation and Projection. 2018.", "https://arxiv.org/abs/1802.03426", "makale", ""),
            ("Chari T, Pachter L. The specious art of single-cell genomics. PLOS Comput Biol 2023.", "https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1011288", "makale", "t-SNE/UMAP gömmelerinin yorum sınırları."),
            ("Guyon I, Elisseeff A. An introduction to variable and feature selection. JMLR 2003.", "https://www.jmlr.org/papers/v3/guyon03a.html", "makale", "")]),

 dict(n=4, title="Klasik Makine Öğrenmesi I: Denetimli Öğrenme ve Klinik Metrikler",
  topic="Klasik makine öğrenmesi I: denetimli öğrenme ve klinik değerlendirme metrikleri (ROC-AUC, duyarlılık/özgüllük, kalibrasyon)",
  desc="Lojistik regresyon ve k-NN ile denetimli öğrenme; karışıklık matrisi, duyarlılık/özgüllük, PPV/NPV, ROC ve PR eğrileri, kalibrasyon ve karar eğrisi analizi.",
  tags=["lojistik regresyon", "ROC-AUC", "PR-AUC", "duyarlılık", "özgüllük", "kalibrasyon", "Brier", "karar eğrisi"],
  methods=["Lojistik regresyon", "k-NN", "ROC / PR eğrisi", "Kalibrasyon", "Karar eğrisi analizi"],
  objectives=["Lojistik regresyonu olasılıksal model olarak kurar; katsayıları odds oranı biçiminde yorumlar.",
              "Karışıklık matrisinden duyarlılık, özgüllük, PPV, NPV ve F1 hesaplar; prevalansın PPV üzerindeki etkisini açıklar.",
              "ROC-AUC ile PR-AUC'yi karşılaştırır; dengesiz sınıflarda hangisinin bilgilendirici olduğunu gerekçelendirir.",
              "Kalibrasyon eğrisi, Brier skoru ve Platt/izotonik kalibrasyonu uygular; karar eğrisi analiziyle net faydayı yorumlar."],
  concepts=[("Ayırt edicilik (discrimination)", "Modelin hastayı sağlıklıdan sıralama gücü; ROC-AUC bunun eşikten bağımsız özetidir."),
            ("Kalibrasyon", "Modelin %30 dediği hastaların gerçekten yaklaşık %30'unun olay yaşaması; klinik kararda ayırt edicilik kadar önemlidir."),
            ("Eşik seçimi", "Yanlış pozitif ve yanlış negatifin klinik maliyetine göre belirlenir; Youden indeksi tek başına yeterli değildir."),
            ("Karar eğrisi analizi (DCA)", "Farklı eşik olasılıklarında modelin 'herkesi tedavi et / kimseyi tedavi etme' stratejilerine göre net faydasını gösterir.")],
  examples=["Sepsis erken uyarı skorunun ROC-AUC'si 0.85 iken alarm başına gerçek pozitif oranı %8: yüksek AUC, düşük PPV ve alarm yorgunluğu.",
            "Kardiyovasküler risk modelinin dış popülasyonda iyi ayırt edici ama kötü kalibre olması (riski sistematik abartma)."],
  tools=["scikit-learn", "matplotlib"],
  datasets=[("UCI Breast Cancer Wisconsin (Diagnostic)", "https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic", ""),
            ("Kaggle: Sepsis (PhysioNet 2019 Challenge)", "https://physionet.org/content/challenge-2019/", "Dengesiz sınıf ve PR-AUC.")],
  activity="Lojistik regresyon ve k-NN'yi hasta-bazlı çapraz doğrulamayla eğitin. ROC ve PR eğrilerini aynı grafikte çizin; kalibrasyon eğrisi ve Brier skorunu raporlayın. Üç farklı eşik için karışıklık matrislerini çıkarıp klinik senaryoya (tarama vs. doğrulama) göre birini savunun. Karar eğrisi analizi ekleyin.",
  questions=["Prevalansı %1 olan bir hastalıkta %95 duyarlı ve %95 özgül bir testin PPV'si kaçtır? Bu model raporlarında neden sık göz ardı edilir?",
             "Kalibrasyonu bozuk ama ROC-AUC'si yüksek bir model klinik karar destek için kullanılabilir mi?"],
  summary="Denetimli öğrenmeyi klinik metrik diliyle kurduk: ayırt edicilik, kalibrasyon, eşik ve net fayda. Bu haftanın değerlendirme çerçevesi dönemin tüm modellerinde tekrarlanacak.",
  readings=[("Steyerberg EW ve ark. Assessing the performance of prediction models: a framework. Epidemiology 2010.", "https://journals.lww.com/epidem/fulltext/2010/01000/assessing_the_performance_of_prediction_models__a.22.aspx", "makale", "Ayırt edicilik, kalibrasyon ve klinik fayda çerçevesi."),
            ("Vickers AJ, Elkin EB. Decision curve analysis. Med Decis Making 2006.", "https://journals.sagepub.com/doi/10.1177/0272989X06295361", "makale", ""),
            ("Van Calster B ve ark. Calibration: the Achilles heel of predictive analytics. BMC Med 2019.", "https://bmcmedicine.biomedcentral.com/articles/10.1186/s12916-019-1466-7", "makale", "")]),

 dict(n=5, title="Klasik Makine Öğrenmesi II: Topluluk Yöntemleri, SVM ve Öznitelik Önemi",
  topic="Klasik makine öğrenmesi II: topluluk yöntemleri (Random Forest, XGBoost), destek vektör makineleri ve öznitelik önemi",
  desc="Torbalama ve artırma ilkeleri, Random Forest ve XGBoost hiperparametreleri, SVM ve çekirdek hilesi, öznitelik önemi türleri ve tuzakları.",
  tags=["Random Forest", "XGBoost", "gradyan artırma", "SVM", "çekirdek", "öznitelik önemi", "hiperparametre"],
  methods=["Random Forest", "XGBoost / LightGBM", "SVM (RBF)", "Bayes hiperparametre arama", "Permütasyon önemi"],
  objectives=["Torbalama (bagging) ile artırmanın (boosting) varyans–yanlılık açısından farkını açıklar.",
              "Random Forest ve XGBoost'u iç içe (nested) çapraz doğrulamayla ayarlar; erken durdurma ve düzenlileştirme parametrelerini kullanır.",
              "SVM'de marj, çekirdek ve C parametresinin rolünü açıklar; ölçeklemenin zorunluluğunu gerekçelendirir.",
              "Safsızlık-temelli, permütasyon-temelli ve SHAP-temelli öznitelik önemini karşılaştırır; ilişkili özniteliklerde tuzakları tanır."],
  concepts=[("Torbalama vs artırma", "Torbalama bağımsız ağaçların ortalamasıyla varyansı düşürür; artırma önceki hataları ardışık düzeltir ve yanlılığı azaltır."),
            ("Gradyan artırma", "Kayıp fonksiyonunun gradyanına küçük ağaçlar uydurma; öğrenme oranı, derinlik ve düzenlileştirme ile denetlenir."),
            ("Çekirdek hilesi", "Veriyi açıkça dönüştürmeden yüksek boyutlu uzayda iç çarpım hesaplama; RBF çekirdeği en yaygını."),
            ("Öznitelik önemi tuzağı", "Safsızlık-temelli önem yüksek kardinaliteli ve ilişkili özniteliklere yanlıdır; permütasyon önemi ilişkili öznitelikler arasında bölünür.")],
  examples=["Tablo hâlindeki klinik veride XGBoost'un çoğu zaman derin öğrenmeyi geçmesi ve bunun nedenleri.",
            "Kalp yetmezliği yeniden yatış modelinde 'ilaç sayısı' özniteliğinin yüksek önemi: nedensel mi, hastalık şiddetinin vekili mi?"],
  tools=["scikit-learn", "xgboost", "optuna"],
  datasets=[("UCI Heart Failure Clinical Records", "https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records", ""),
            ("Kaggle: Stroke Prediction", "https://www.kaggle.com/datasets/fedesoriano/stroke-prediction-dataset", "Dengesiz sınıf.")],
  activity="Aynı veri setinde lojistik regresyon, Random Forest, XGBoost ve RBF-SVM'yi iç içe çapraz doğrulama ile karşılaştırın (ROC-AUC, PR-AUC, Brier). XGBoost için Optuna ile hiperparametre arayın. Üç öznitelik önemi yöntemini yan yana çizip uyuşmayan öznitelikleri tartışın.",
  questions=["Model başarımı %1 artınca ek karmaşıklık ve yorumlanabilirlik kaybı klinik olarak ne zaman kabul edilir?",
             "İki yüksek korelasyonlu öznitelikten birini çıkardığınızda diğerinin önemi neden aniden artar?"],
  summary="Tablo verisi için güçlü klasik yöntemleri ve onları sorumlu biçimde ayarlamayı öğrendik. Öznitelik önemi ile açıklanabilirliğin ilk kapısını araladık; 12. haftada derinleşecek.",
  readings=[("Chen T, Guestrin C. XGBoost: A Scalable Tree Boosting System. KDD 2016.", "https://arxiv.org/abs/1603.02754", "makale", ""),
            ("Grinsztajn L ve ark. Why do tree-based models still outperform deep learning on tabular data? NeurIPS 2022.", "https://arxiv.org/abs/2207.08815", "makale", ""),
            ("Strobl C ve ark. Bias in random forest variable importance measures. BMC Bioinformatics 2007.", "https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-8-25", "makale", "")]),

 dict(n=6, title="Denetimsiz Öğrenme: Hasta Alt-Tiplendirme, Kümeleme ve Anomali Tespiti",
  topic="Denetimsiz öğrenme: hasta alt-tiplendirme (subtyping), kümeleme ve anomali tespiti",
  desc="k-means, hiyerarşik ve GMM kümeleme; küme sayısı seçimi ve kararlılık; hasta alt-tiplerinin klinik doğrulanması; Isolation Forest ve otokodlayıcı ile anomali.",
  tags=["kümeleme", "k-means", "hiyerarşik", "GMM", "alt-tipleme", "anomali tespiti", "Isolation Forest", "silhouette"],
  methods=["k-means", "Hiyerarşik kümeleme", "GMM", "Konsensüs kümeleme", "Isolation Forest"],
  objectives=["k-means, hiyerarşik ve Gauss karışım modellerinin varsayımlarını ve hangi veri geometrisine uyduklarını açıklar.",
              "Küme sayısını silhouette, gap istatistiği ve konsensüs/kararlılık analiziyle seçer; keyfî seçimden kaçınır.",
              "Bulunan hasta alt-tiplerini klinik değişkenler ve sonlanımlarla (sağkalım, yanıt) dışsal olarak doğrular.",
              "Isolation Forest ve yoğunluk-temelli yöntemlerle anomali tespiti yapar; anomaliyi hata mı, nadir fenotip mi diye ayırır."],
  concepts=[("Hasta alt-tiplendirme", "Aynı tanı altındaki hastaların veri-güdümlü biçimde klinik olarak farklı gruplara ayrılması (ör. sepsis fenotipleri α–δ)."),
            ("Küme kararlılığı", "Alt-örneklemeler veya farklı başlangıçlarda aynı kümelerin yeniden bulunması; kararsız küme yapay bulgudur."),
            ("Dışsal doğrulama", "Kümelemede kullanılmayan değişkenlerle (sonlanım, tedavi yanıtı) kümelerin anlamlılığını sınamak."),
            ("Anomali", "Çoğunluk dağılımından uzak gözlem; sensör hatası, veri giriş hatası veya gerçek nadir vaka olabilir.")],
  examples=["Seymour ve ark. (JAMA 2019): 20.000+ sepsis hastasında dört klinik fenotip ve farklı mortalite profilleri.",
            "Holter EKG kayıtlarında Isolation Forest ile aritmik segment tespiti: anomali skoru ile kardiyolog etiketinin karşılaştırılması."],
  tools=["scikit-learn", "scipy", "umap-learn"],
  datasets=[("UCI Wisconsin Breast Cancer (etiketler saklanarak)", "https://archive.ics.uci.edu/dataset/17/breast+cancer+wisconsin+diagnostic", "Kümeleme sonuçlarının dışsal doğrulaması."),
            ("PhysioNet MIT-BIH Arrhythmia", "https://physionet.org/content/mitdb/", "Anomali tespiti.")],
  activity="Etiketleri saklayarak Breast Cancer verisini k-means, hiyerarşik ve GMM ile kümeleyin; silhouette ve konsensüs matrisleriyle k seçin. Kümeleri saklanan etiket ve klinik değişkenlerle karşılaştırın. MIT-BIH'ten çıkarılan RR aralığı özniteliklerinde Isolation Forest ile anomali skoru üretip aritmi etiketleriyle ROC hesaplayın.",
  questions=["k-means her zaman k küme bulur; bulduğu kümelerin gerçek olduğunu nasıl kanıtlarsınız?",
             "Anomali tespiti modeli tıbbi bir cihazda uyarı üretiyorsa yanlış alarm ile kaçırılan olay arasındaki dengeyi kim, nasıl belirler?"],
  summary="Etiketsiz veriden yapı çıkarmayı ve bulduğumuz yapıyı klinik olarak doğrulamayı öğrendik. Modül 2 tamamlandı.",
  readings=[("Seymour CW ve ark. Derivation, validation, and potential treatment implications of novel clinical phenotypes for sepsis. JAMA 2019.", "https://jamanetwork.com/journals/jama/fullarticle/2733996", "makale", ""),
            ("Liu FT, Ting KM, Zhou Z-H. Isolation Forest. ICDM 2008.", "https://ieeexplore.ieee.org/document/4781136", "makale", ""),
            ("Monti S ve ark. Consensus clustering. Machine Learning 2003.", "https://link.springer.com/article/10.1023/A:1023949509487", "makale", "")]),

 dict(n=7, title="Biyomedikal Sinyal ve Zaman Serisi Analizi: EEG, EKG, EMG",
  topic="Biyomedikal sinyal ve zaman serisi analizi (EEG/ECG/EMG): filtreleme, öznitelik çıkarımı ve zaman-frekans yöntemleri",
  desc="Örnekleme ve Nyquist, sayısal filtreler, artefakt giderme, zaman/frekans/doğrusal-olmayan öznitelikler, STFT ve dalgacık dönüşümü, kayıt-bazlı doğrulama.",
  tags=["EEG", "EKG", "EMG", "filtreleme", "FFT", "STFT", "dalgacık", "HRV", "zaman-frekans", "MNE"],
  methods=["Butterworth / notch filtre", "FFT & Welch PSD", "STFT", "Dalgacık dönüşümü", "HRV öznitelikleri"],
  objectives=["Örnekleme frekansı, Nyquist sınırı ve örtüşmenin (aliasing) sinyal kalitesine etkisini açıklar.",
              "Bant geçiren ve çentik filtreleri tasarlar; EEG'de göz/kas artefaktını, EKG'de taban çizgisi kaymasını giderir.",
              "Zaman alanı (RR, HRV), frekans alanı (bant güçleri) ve doğrusal olmayan (entropi) öznitelikler çıkarır.",
              "STFT ve sürekli dalgacık dönüşümüyle zaman–frekans temsili üretir; kayıt-bazlı çapraz doğrulama ile sınıflandırıcı eğitir."],
  concepts=[("Nyquist frekansı", "Örnekleme frekansının yarısı; üzerindeki bileşenler yanlış frekansa katlanır (aliasing)."),
            ("Güç spektral yoğunluğu (PSD)", "Sinyal gücünün frekansa dağılımı; EEG bantları (delta–gama) ve HRV LF/HF oranı buradan okunur."),
            ("Zaman–frekans temsili", "STFT sabit pencereyle, dalgacık dönüşümü ölçeğe göre değişen pencereyle geçici olayları (nöbet, aritmi) yakalar."),
            ("Kayıt-bazlı doğrulama", "Aynı kaydın segmentlerinin eğitim ve teste dağılmaması; aksi hâlde başarım yapay olarak şişer.")],
  examples=["EEG'de epileptik nöbet tespiti: 2 saniyelik pencerelerde bant güçleri + entropi → Random Forest; hasta-bazlı AUC ile pencere-bazlı AUC farkı.",
            "EKG'den atriyal fibrilasyon tespiti: RR aralığı düzensizliği (RMSSD, pNN50) ve P dalgası yokluğu."],
  tools=["scipy.signal", "MNE-Python", "NeuroKit2", "wfdb", "PyWavelets"],
  datasets=[("PhysioNet MIT-BIH Arrhythmia", "https://physionet.org/content/mitdb/", "EKG; etiketli atımlar."),
            ("Bonn EEG / CHB-MIT Scalp EEG", "https://physionet.org/content/chbmit/", "Nöbet tespiti."),
            ("PhysioNet AF Classification Challenge 2017", "https://physionet.org/content/challenge-2017/", "Tek derivasyon EKG.")],
  activity="MIT-BIH'ten bir kaydı yükleyin; 0.5–40 Hz bant geçiren ve 50 Hz çentik filtre uygulayıp öncesi/sonrası PSD çizin. R tepe tespiti ile RR serisi ve HRV öznitelikleri üretin. CHB-MIT'ten bir hastanın EEG'sinde STFT spektrogramında nöbeti işaretleyin; bant güçleriyle kayıt-bazlı çapraz doğrulamalı sınıflandırıcı eğitin.",
  questions=["Aynı hastanın nöbet ve nöbet-dışı segmentleri hem eğitim hem test kümesine düşerse model neyi öğrenir?",
             "Öznitelik çıkarımı + klasik ML ile ham sinyalden uçtan uca öğrenen CNN arasında ne zaman hangisini seçersiniz?"],
  summary="Fizyolojik sinyalleri temizleyip anlamlı özniteliklere dönüştürdük ve zaman–frekans temsillerini gördük. Bu temsiller 9–11. haftalardaki derin öğrenme modellerinin girdisi olacak.",
  before="Ara sınav gelecek hafta: 1–7. haftaların içeriğini kapsar. Bu hafta işlenen sinyal işleme kavramları da dâhildir.",
  readings=[("Rajpurkar P ve ark. Cardiologist-level arrhythmia detection with convolutional neural networks. Nat Med 2019.", "https://www.nature.com/articles/s41591-018-0268-3", "makale", "Uçtan uca öğrenme karşıtı olarak öznitelik-temelli yaklaşımı tartışın."),
            ("Gramfort A ve ark. MEG and EEG data analysis with MNE-Python. Front Neurosci 2013.", "https://www.frontiersin.org/articles/10.3389/fnins.2013.00267/full", "makale", ""),
            ("Shaffer F, Ginsberg JP. An overview of heart rate variability metrics and norms. Front Public Health 2017.", "https://www.frontiersin.org/articles/10.3389/fpubh.2017.00258/full", "makale", "")]),

 dict(n=8, title="Ara Sınav",
  topic="Ara sınav",
  desc="1–7. haftaların içeriğini kapsayan yüz yüze ara sınav; dönem notunun %50'si.",
  tags=["ara sınav", "değerlendirme"],
  methods=[],
  exam=True,
  objectives=["Biyomedikal veri türleri, ön işleme ve sızıntı kaynaklarını kavramsal düzeyde açıklar.",
              "Klinik değerlendirme metriklerini (ROC-AUC, duyarlılık/özgüllük, kalibrasyon) hesaplar ve yorumlar.",
              "Klasik denetimli/denetimsiz yöntemleri ve sinyal işleme temellerini uygun probleme eşler."],
  concepts=[("Kapsam", "Hafta 1–7: veri türleri ve problem tipleri; eksik veri, sızıntı, hasta-bazlı bölme; EDA, öznitelik mühendisliği, PCA/UMAP; lojistik regresyon ve klinik metrikler; topluluk yöntemleri, SVM, öznitelik önemi; kümeleme ve anomali; sinyal filtreleme ve zaman–frekans."),
            ("Biçim", "Yüz yüze, yazılı. Kavramsal sorular, kısa hesaplamalar (karışıklık matrisi, PPV, PSD yorumu) ve bir vaka çözümü (veri → yöntem → metrik seçimi ve gerekçesi)."),
            ("Ağırlık", "Dönem notunun %50'si.")],
  examples=["Örnek soru tipi: 'Yoğun bakımda sepsis tahmini için verilen veri şemasında sızıntı kaynaklarını bulun ve doğru bölme stratejisini önerin.'",
            "Örnek soru tipi: 'ROC-AUC 0.90, kalibrasyon eğrisi diyagonalin üstünde: model klinikte nasıl davranır; nasıl düzeltirsiniz?'"],
  tools=[],
  datasets=[],
  activity="Her haftanın 'Temel Kavramlar' ve 'Tartışma Soruları' bölümlerini gözden geçirin; uygulama defterlerinde metrik hesaplamalarını elle tekrar edin. Ders saatinde sınav öncesi 30 dakikalık soru–cevap yapılır.",
  questions=["Modül 1–3'te öğrendiklerinizi tek bir biyomedikal probleme (kendi tez konunuz olabilir) uçtan uca uygulasanız hangi adımda en çok zorlanırsınız?"],
  summary="Dönemin ilk yarısı ara sınavla kapandı. İkinci yarı derin öğrenme ve açıklanabilir yapay zeka ile devam eder.",
  before="Sınav 1–7. haftaların içeriğini kapsar. Hesap makinesi getirebilirsiniz; formül kâğıdı sınav kâğıdıyla birlikte verilir.",
  readings=[]),

 dict(n=9, title="Derin Öğrenmeye Giriş: Yapay Sinir Ağları, Geri Yayılım ve Eğitim Pratiği",
  topic="Derin öğrenmeye giriş: yapay sinir ağları, geri yayılım ve eğitim pratiği",
  desc="Perceptron'dan çok katmanlı ağa, aktivasyon ve kayıp fonksiyonları, geri yayılım ve otomatik türev, optimizasyon, düzenlileştirme ve PyTorch ile eğitim döngüsü.",
  tags=["YSA", "MLP", "geri yayılım", "PyTorch", "Adam", "dropout", "batch norm", "erken durdurma", "öğrenme oranı"],
  methods=["MLP", "Geri yayılım", "SGD / Adam", "Dropout & BatchNorm", "Erken durdurma"],
  objectives=["Çok katmanlı algılayıcıyı bileşimsel fonksiyon olarak kurar; aktivasyon ve kayıp fonksiyonlarını probleme göre seçer.",
              "Geri yayılımı zincir kuralı olarak türetir; PyTorch autograd ile bağlantısını kurar.",
              "Öğrenme oranı, yığın boyutu, düzenlileştirme (L2, dropout) ve erken durdurmanın etkisini deneyle gösterir.",
              "Eğitim/doğrulama eğrilerinden aşırı/eksik öğrenmeyi tanır; tekrarlanabilir bir PyTorch eğitim döngüsü yazar."],
  concepts=[("Evrensel yaklaşım", "Yeterli genişlikte tek gizli katmanlı ağın sürekli fonksiyonlara yaklaşabilmesi; pratikte derinlik daha verimlidir."),
            ("Geri yayılım", "Kayıp fonksiyonunun her parametreye göre gradyanının zincir kuralıyla çıkıştan girişe hesaplanması."),
            ("Kaybolan/patlayan gradyan", "Derin ağlarda gradyanın katmanlar boyunca çarpımsal küçülmesi/büyümesi; ReLU, BatchNorm ve artık bağlantılar çözüm sunar."),
            ("Düzenlileştirme", "Aşırı öğrenmeyi frenleyen her şey: L2 cezası, dropout, veri artırma, erken durdurma.")],
  examples=["Klinik tablo verisinde MLP ile XGBoost'un karşılaştırılması: küçük veride ağaçların üstünlüğü, çok-modaliteli veride ağın esnekliği.",
            "Sinyal özniteliklerinden nöbet tespiti için MLP: öğrenme oranı çok yüksekken kayıp eğrisinin salınımı."],
  tools=["PyTorch", "torchmetrics", "scikit-learn"],
  datasets=[("UCI Heart Disease / Breast Cancer", "https://archive.ics.uci.edu/", "Tablo verisinde MLP."),
            ("7. haftanın EEG öznitelik matrisi", None, "Kendi ürettiğiniz öznitelikler.")],
  activity="NumPy ile iki katmanlı bir ağın ileri ve geri geçişini elle yazın; aynı ağı PyTorch autograd ile doğrulayın. Ardından PyTorch'ta tam bir eğitim döngüsü (DataLoader, kayıp, optimizer, doğrulama, erken durdurma) kurup Heart Disease verisinde XGBoost ile karşılaştırın. Öğrenme oranı taraması yapıp eğrileri çizin.",
  questions=["Aynı veri setinde MLP her çalıştırmada farklı sonuç veriyorsa tekrarlanabilirlik için hangi adımlar gerekir?",
             "Tablo hâlindeki klinik veride derin öğrenme ne zaman gerçekten haklı çıkar?"],
  summary="Derin öğrenmenin çekirdeğini kurduk: ağ, kayıp, gradyan, optimizasyon ve eğitim disiplini. Sonraki iki hafta bu çekirdeği görüntü ve dizilere uyarlıyor.",
  readings=[("Goodfellow, Bengio, Courville. Deep Learning. Bölüm 6 (Deep Feedforward Networks) ve 8 (Optimization).", "https://www.deeplearningbook.org/", "kitap", "Ana kaynak."),
            ("PyTorch: Learn the Basics", "https://pytorch.org/tutorials/beginner/basics/intro.html", "dokuman", ""),
            ("Smith LN. Cyclical learning rates for training neural networks. WACV 2017.", "https://arxiv.org/abs/1506.01186", "makale", "Öğrenme oranı bulucu.")]),

 dict(n=10, title="Evrişimli Sinir Ağları ve Tıbbi Görüntü Analizi",
  topic="Evrişimli sinir ağları ve tıbbi görüntü analizi: sınıflandırma, segmentasyon (U-Net) ve transfer öğrenme",
  desc="Evrişim, havuzlama ve alıcı alan; klasik mimariler (ResNet); transfer öğrenme ve ince ayar; U-Net ile segmentasyon; Dice/IoU; tıbbi görüntüye özgü tuzaklar.",
  tags=["CNN", "ResNet", "U-Net", "segmentasyon", "transfer öğrenme", "Dice", "IoU", "veri artırma", "kısayol öğrenme", "MedMNIST"],
  methods=["CNN", "ResNet transfer öğrenme", "U-Net", "Dice / IoU", "Veri artırma"],
  objectives=["Evrişim, adım, dolgu ve havuzlamanın alıcı alan ve parametre sayısına etkisini hesaplar.",
              "ImageNet ön-eğitimli bir ağı tıbbi görüntüye transfer eder; dondurma/ince ayar stratejilerini karşılaştırır.",
              "U-Net'in kodlayıcı–kod çözücü ve atlama bağlantılarını açıklar; Dice ve IoU ile segmentasyon başarımını değerlendirir.",
              "Tıbbi görüntüde kısayol öğrenme (cihaz etiketi, hastane imzası) ve dağıtım kayması risklerini tanır; hasta-bazlı bölmeyi uygular."],
  concepts=[("Evrişim", "Öğrenilen küçük filtrelerin görüntü üzerinde kaydırılması; öteleme eşdeğerliği ve parametre paylaşımı sağlar."),
            ("Transfer öğrenme", "Büyük doğal görüntü kümesinde öğrenilen filtrelerin tıbbi görüntüde yeniden kullanımı; az veride başarımın anahtarı."),
            ("U-Net", "Piksel düzeyinde sınıflandırma için simetrik kodlayıcı–kod çözücü; atlama bağlantıları ince ayrıntıyı korur."),
            ("Dice katsayısı", "Tahmin ve referans maskelerinin örtüşmesi (2|A∩B|/(|A|+|B|)); küçük lezyonlarda doğruluktan çok daha bilgilendirici."),
            ("Kısayol öğrenme", "Modelin hastalık yerine görüntüdeki ilgisiz ipucunu (portatif cihaz etiketi) öğrenmesi; dış veride çöküşün ana nedeni.")],
  examples=["Zech ve ark. (2018): Göğüs röntgeninde pnömoni modelinin hastane kaynağını öğrenmesi ve dış hastanede AUC düşüşü.",
            "MedMNIST PathMNIST'te ResNet-18 ince ayarı; DermaMNIST'te sınıf dengesizliği ve makro-F1.",
            "Kardiyak MR'da sol ventrikül segmentasyonu için U-Net: Dice 0.90'ın klinik olarak yeterli olduğu ve olmadığı durumlar."],
  tools=["PyTorch", "torchvision", "MONAI", "MedMNIST"],
  datasets=[("MedMNIST v2", "https://medmnist.com/", "Hafif, standart tıbbi görüntü setleri (Path, Derma, Pneumonia, OrganA)."),
            ("ISIC Archive", "https://www.isic-archive.com/", "Dermatoskopik görüntü."),
            ("Kaggle: Chest X-Ray Images (Pneumonia)", "https://www.kaggle.com/datasets/paultimothymooney/chest-xray-pneumonia", "Kısayol öğrenme tartışması için.")],
  activity="PneumoniaMNIST'te (1) sıfırdan küçük bir CNN, (2) dondurulmuş ResNet-18 + yeni baş, (3) tam ince ayar stratejilerini karşılaştırın; veri artırmanın etkisini ölçün. Ardından küçük bir segmentasyon setinde U-Net eğitip Dice/IoU raporlayın. Colab GPU kullanın.",
  questions=["Radyoloji görüntüsünde %95 doğru bir sınıflandırıcı neden dış hastanede %70'e düşebilir? Bunu dağıtımdan önce nasıl öngörürsünüz?",
             "Segmentasyonda piksel doğruluğu yerine Dice kullanmanın gerekçesi nedir?"],
  summary="Görüntüden öğrenen ağları kurduk, transfer ettik ve segmentasyon yaptık; tıbbi görüntünün özgün tuzaklarını gördük. 13. haftada Grad-CAM ile bu ağların 'nereye baktığını' göstereceğiz.",
  readings=[("Ronneberger O, Fischer P, Brox T. U-Net: Convolutional Networks for Biomedical Image Segmentation. MICCAI 2015.", "https://arxiv.org/abs/1505.04597", "makale", ""),
            ("Zech JR ve ark. Variable generalization performance of a deep learning model to detect pneumonia in chest radiographs. PLOS Med 2018.", "https://journals.plos.org/plosmedicine/article?id=10.1371/journal.pmed.1002683", "makale", "Kısayol öğrenme."),
            ("Yang J ve ark. MedMNIST v2. Sci Data 2023.", "https://www.nature.com/articles/s41597-022-01721-8", "makale", ""),
            ("Goodfellow ve ark. Deep Learning, Bölüm 9 (Convolutional Networks).", "https://www.deeplearningbook.org/contents/convnets.html", "kitap", "")]),

 dict(n=11, title="Dizisel Modeller: RNN/LSTM, Transformer ve Klinik Metin Analizi",
  topic="Dizisel modeller: RNN/LSTM ve Transformer'ların biyomedikal uygulamaları; klinik metin (NLP) analizine giriş",
  desc="Tekrarlayan ağlar ve LSTM, dikkat mekanizması ve Transformer, ham sinyal ve düzensiz EHR zaman serileri, klinik metin için BERT-tabanlı modeller ve de-identifikasyon.",
  tags=["RNN", "LSTM", "GRU", "Transformer", "dikkat", "BERT", "klinik NLP", "ClinicalBERT", "EHR zaman serisi", "de-identifikasyon"],
  methods=["LSTM / GRU", "1D-CNN", "Transformer / dikkat", "BERT ince ayarı", "Klinik NLP"],
  objectives=["RNN/LSTM'in dizisel bağımlılığı nasıl modellediğini ve uzun bağımlılık sorununu açıklar.",
              "Öz-dikkat mekanizmasını matris biçiminde türetir; Transformer'ın RNN'e göre avantajlarını sıralar.",
              "Düzensiz örneklenmiş EHR zaman serilerini (eksik, farklı aralıklı) dizisel modele hazırlar; maske ve zaman kodlaması kullanır.",
              "Ön-eğitimli biyomedikal dil modelleriyle (ClinicalBERT, BioBERT) klinik not sınıflandırması yapar; de-identifikasyon ve mahremiyet gereklerini tanır."],
  concepts=[("Tekrarlayan ağ (RNN)", "Gizli durumu her zaman adımında güncelleyen ağ; LSTM/GRU kapılarla uzun bağımlılığı korur."),
            ("Öz-dikkat", "Her konumun diğer tüm konumlarla ilişkisini sorgu–anahtar–değer çarpımıyla ağırlıklandırma; paralel ve uzun menzilli."),
            ("Düzensiz zaman serisi", "EHR'de ölçümlerin farklı zamanlarda ve sıklıkta olması; eksiklik deseni bilgi taşır."),
            ("Klinik metin", "Serbest metin notlar, radyoloji raporları; kısaltma, olumsuzlama ('pnömoni yok') ve mahremiyet zorlukları."),
            ("De-identifikasyon", "Kişisel tanımlayıcıların metinden çıkarılması; NLP çalışmasının yasal ön koşulu.")],
  examples=["Yoğun bakım vital ve laboratuvar serilerinden 6 saat önceden sepsis tahmini: GRU ile öznitelik-temelli XGBoost karşılaştırması.",
            "Ham tek derivasyon EKG'den atriyal fibrilasyon tespiti: 1D-CNN + LSTM (PhysioNet 2017).",
            "Radyoloji raporlarından bulgu çıkarımı: ClinicalBERT ince ayarı ve olumsuzlama hataları."],
  tools=["PyTorch", "Hugging Face transformers", "scikit-learn"],
  datasets=[("PhysioNet AF Classification Challenge 2017", "https://physionet.org/content/challenge-2017/", "Ham EKG dizisi."),
            ("MIMIC-III Demo (notlar ve zaman serisi)", "https://physionet.org/content/mimiciii-demo/", "Düzensiz EHR serisi."),
            ("MTSamples (açık klinik transkript örnekleri)", "https://mtsamples.com/", "Klinik metin sınıflandırma alıştırması.")],
  activity="PhysioNet 2017 EKG verisinde 1D-CNN ve LSTM modellerini kayıt-bazlı bölme ile eğitip 7. haftanın öznitelik-temelli modeliyle karşılaştırın. Hugging Face'ten bir biyomedikal BERT modelini indirip küçük bir klinik metin sınıflandırma görevinde ince ayar yapın; olumsuzlama içeren örneklerde hataları inceleyin.",
  questions=["Dikkat ağırlıkları bir 'açıklama' sayılır mı? 12–13. haftalarda bu soruya geri döneceğiz.",
             "Klinik notlarla çalışırken de-identifikasyon yeterli midir; yeniden tanımlama riski nereden gelir?"],
  summary="Zamanı ve dili modelleyen ağları biyomedikal dizilere uyguladık. Modül 4 tamamlandı; artık elimizde açıklanması gereken güçlü kara kutular var.",
  readings=[("Vaswani A ve ark. Attention Is All You Need. NeurIPS 2017.", "https://arxiv.org/abs/1706.03762", "makale", ""),
            ("Hochreiter S, Schmidhuber J. Long Short-Term Memory. Neural Computation 1997.", "https://www.bioinf.jku.at/publications/older/2604.pdf", "makale", ""),
            ("Alsentzer E ve ark. Publicly Available Clinical BERT Embeddings. 2019.", "https://arxiv.org/abs/1904.03323", "makale", ""),
            ("Goodfellow ve ark. Deep Learning, Bölüm 10 (Sequence Modeling).", "https://www.deeplearningbook.org/contents/rnn.html", "kitap", "")]),

 dict(n=12, title="Açıklanabilir Yapay Zeka I: Yorumlanabilirlik, İçsel Modeller ve Post-hoc Yöntemler",
  topic="Açıklanabilir yapay zeka (XAI) I: yorumlanabilirlik kavramı, içsel yorumlanabilirlik ve post-hoc yöntemler (permütasyon önemi, PDP/ICE)",
  desc="Yorumlanabilirlik–açıklanabilirlik ayrımı ve taksonomi; içsel yorumlanabilir modeller (GAM, EBM, kural listeleri); permütasyon önemi, kısmi bağımlılık ve ICE eğrileri; açıklamaların değerlendirilmesi.",
  tags=["XAI", "yorumlanabilirlik", "GAM", "EBM", "permütasyon önemi", "PDP", "ICE", "ALE", "post-hoc", "Rudin"],
  methods=["İçsel yorumlanabilir modeller (GAM/EBM)", "Permütasyon önemi", "PDP", "ICE", "ALE"],
  objectives=["Yorumlanabilirlik ile açıklanabilirliği ayırır; küresel/yerel, model-bağımlı/bağımsız, içsel/post-hoc eksenlerinde yöntemleri sınıflar.",
              "Genelleştirilmiş toplamsal modeller (GAM/EBM) ve seyrek doğrusal modelleri yüksek riskli kararlar için savunur ve kurar.",
              "Permütasyon önemi, kısmi bağımlılık (PDP), bireysel koşullu beklenti (ICE) ve ALE eğrilerini hesaplar ve yorumlar.",
              "Açıklamaların sadakat (fidelity), kararlılık ve insan-anlaşılırlık ölçütlerini tartışır; Rudin'in kara kutu eleştirisini değerlendirir."],
  concepts=[("Yorumlanabilirlik vs açıklanabilirlik", "Yorumlanabilir model kendi başına anlaşılır (seyrek lojistik, GAM); açıklanabilirlik kara kutuyu sonradan (post-hoc) açıklamaktır."),
            ("Küresel vs yerel", "Küresel: modelin genel davranışı (hangi öznitelik önemli); yerel: tek bir hastanın tahmini neden böyle."),
            ("Kısmi bağımlılık (PDP)", "Bir özniteliğin diğerleri üzerinden ortalanmış marjinal etkisi; ilişkili özniteliklerde yanıltıcı olabilir, ALE bunu düzeltir."),
            ("ICE", "PDP'nin bireysel hasta eğrileri; heterojen etkileri ve etkileşimleri ortaya çıkarır."),
            ("Sadakat (fidelity)", "Açıklamanın modelin gerçek davranışını ne kadar doğru yansıttığı; açıklama ≠ nedensel gerçek.")],
  examples=["Caruana ve ark. (2015): Pnömoni mortalite modelinde 'astım → düşük risk' kuralının GAM ile yakalanması ve klinik açıklaması (astımlılar yoğun bakıma alınıyor).",
            "Kardiyovasküler risk modelinde yaşın PDP'si: monoton beklenirken 80+ yaşta düşen eğri, sağkalım yanlılığının işareti."],
  tools=["scikit-learn (inspection)", "interpret (EBM)", "PyALE", "matplotlib"],
  datasets=[("UCI Heart Failure Clinical Records", "https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records", ""),
            ("5. haftanın XGBoost modeli", None, "Post-hoc yöntemler için kara kutu.")],
  activity="5. haftadaki XGBoost modeline permütasyon önemi, PDP, ICE ve ALE uygulayın; ilişkili öznitelik çiftinde PDP ile ALE farkını gösterin. Aynı veriyi EBM ile modelleyip başarım kaybını ve kazanılan yorumlanabilirliği tabloya dökün. Bir klinisyene sunacağınız iki paragraflık 'model nasıl karar veriyor' özeti yazın.",
  questions=["Rudin'in 'yüksek riskli kararlarda kara kutuyu açıklamayı bırakın, yorumlanabilir model kullanın' tezi biyomedikal görüntü için de geçerli midir?",
             "PDP'de görülen ilişki nedensel midir? Hangi koşullarda nedensel yoruma yaklaşır?"],
  summary="Açıklanabilirliğin kavram haritasını çizdik ve küresel post-hoc yöntemleri uyguladık. Gelecek hafta yerel açıklamalara (SHAP, LIME, Grad-CAM) ve adalete geçiyoruz.",
  readings=[("Molnar C. Interpretable Machine Learning, Bölüm: Interpretability, Interpretable Models, Global Model-Agnostic Methods.", "https://christophm.github.io/interpretable-ml-book/", "kitap", "Ana kaynak."),
            ("Rudin C. Stop explaining black box machine learning models for high stakes decisions. Nat Mach Intell 2019.", "https://www.nature.com/articles/s42256-019-0048-x", "makale", ""),
            ("Caruana R ve ark. Intelligible models for healthcare: predicting pneumonia risk and hospital 30-day readmission. KDD 2015.", "https://dl.acm.org/doi/10.1145/2783258.2788613", "makale", ""),
            ("Apley DW, Zhu J. Visualizing the effects of predictor variables in black box supervised learning models (ALE). JRSS-B 2020.", "https://arxiv.org/abs/1612.08468", "makale", "")]),

 dict(n=13, title="Açıklanabilir Yapay Zeka II: SHAP, LIME, Grad-CAM, Karşıt-Olgusal Açıklamalar ve Adalet",
  topic="Açıklanabilir yapay zeka (XAI) II: SHAP, LIME, Grad-CAM ve karşıt-olgusal (counterfactual) açıklamalar; tıp ve mühendislikte vaka çalışmaları, yanlılık ve adalet",
  desc="Shapley değerlerinin oyun kuramsal temeli ve SHAP (Tree/Deep/Kernel), LIME'ın yerel vekil yaklaşımı, Grad-CAM ile görsel açıklama, karşıt-olgusal açıklamalar, açıklama tuzakları ve algoritmik adalet ölçütleri.",
  tags=["SHAP", "Shapley", "LIME", "Grad-CAM", "Integrated Gradients", "karşıt-olgusal", "yanlılık", "adalet", "eşit fırsat", "DiCE"],
  methods=["SHAP (Tree/Deep/Kernel)", "LIME", "Grad-CAM / IG", "Karşıt-olgusal açıklama", "Adalet metrikleri"],
  objectives=["Shapley değerlerinin aksiyomlarını açıklar; TreeSHAP, DeepSHAP ve KernelSHAP'ın ne zaman kullanıldığını ayırt eder; SHAP özet, bağımlılık ve şelale grafiklerini yorumlar.",
              "LIME'ın yerel vekil model mantığını kurar; kararsızlık ve komşuluk tanımı sorunlarını tartışır.",
              "Grad-CAM ve Integrated Gradients ile CNN kararlarını görselleştirir; tıbbi görüntüde 'doğru yere bakma' değerlendirmesi yapar.",
              "Karşıt-olgusal açıklamalar üretir (DiCE); geçerlilik, yakınlık ve eyleme dönüştürülebilirlik ölçütlerini uygular.",
              "Demografik parite, eşit fırsat ve kalibrasyon eşitliği gibi adalet ölçütlerini hesaplar; alt-grup analizini rapor standardı hâline getirir."],
  concepts=[("Shapley değeri", "Özniteliğin tüm koalisyonlardaki ortalama marjinal katkısı; verimlilik, simetri, sahte oyuncu ve toplamsallık aksiyomlarını sağlayan tek çözüm."),
            ("SHAP", "Shapley değerlerinin yerel açıklamaya uyarlanması; TreeSHAP ağaç modellerinde polinom zamanda kesin hesap yapar."),
            ("LIME", "Tek gözlemin çevresinde bozulmuş örneklerle eğitilen seyrek doğrusal vekil model; hızlı ama komşuluk seçimine duyarlı."),
            ("Grad-CAM", "Son evrişim katmanının sınıf-özel gradyanlarla ağırlıklandırılmış ısı haritası; modelin 'baktığı' bölgeyi gösterir."),
            ("Karşıt-olgusal açıklama", "'Şu öznitelikler şöyle olsaydı karar değişirdi': hastaya eyleme dönük öneri üretir; tıbbi olarak mümkün olmalıdır."),
            ("Adalet ölçütleri", "Demografik parite (pozitif oranı eşit), eşit fırsat (duyarlılık eşit), kalibrasyon eşitliği; aynı anda hepsini sağlamak genelde imkânsızdır.")],
  examples=["Sepsis modelinde hasta düzeyinde SHAP şelale grafiği: laktat ve solunum sayısının katkısı; klinisyenin 'ama bu hasta KOAH' itirazı ve etkileşim değerleri.",
            "Göğüs röntgeni pnömoni modelinde Grad-CAM'in akciğer dışına (cihaz etiketine) yoğunlaşması: 10. haftadaki kısayol öğrenmenin görsel kanıtı.",
            "Obermeyer ve ark. (2019): Sağlık harcamasını hastalık şiddetinin vekili olarak kullanan algoritmanın Siyah hastaları sistematik olarak düşük riske atması.",
            "Pulse oksimetre ve deri rengi: girdi ölçümündeki yanlılığın modele taşınması."],
  tools=["shap", "lime", "captum", "dice-ml", "fairlearn"],
  datasets=[("5. ve 9. haftaların modelleri (XGBoost, MLP)", None, "SHAP/LIME uygulaması."),
            ("10. haftanın PneumoniaMNIST CNN'i", None, "Grad-CAM."),
            ("MIMIC-III Demo (demografi ile)", "https://physionet.org/content/mimiciii-demo/", "Alt-grup adalet analizi.")],
  activity="XGBoost modeline TreeSHAP uygulayın: özet, bağımlılık ve üç hasta için şelale grafikleri. Aynı hastaları LIME ile açıklayıp tutarlılığı ölçün. CNN'e Grad-CAM uygulayıp radyolojik olarak anlamlı bölgeyle örtüşmeyi değerlendirin. DiCE ile iki hastaya karşıt-olgusal öneri üretin. Son olarak fairlearn ile cinsiyet/yaş alt-gruplarında duyarlılık, özgüllük ve kalibrasyonu karşılaştırın.",
  questions=["SHAP değerleri yüksek çıkan bir öznitelik 'nedensel' midir? Klinisyene bunu nasıl anlatırsınız?",
             "Alt-grupta duyarlılığı eşitlemek için eşik farklılaştırmak adil midir? Hangi adalet tanımına göre?"],
  summary="Yerel açıklama yöntemlerinin tamamını uyguladık ve adaleti ölçülebilir bir rapor bileşeni hâline getirdik. Son hafta bu araçları klinik uygulamaya hazır bir sistemin parçası olarak ele alıyor.",
  readings=[("Lundberg SM, Lee S-I. A Unified Approach to Interpreting Model Predictions. NeurIPS 2017.", "https://arxiv.org/abs/1705.07874", "makale", ""),
            ("Ribeiro MT, Singh S, Guestrin C. 'Why Should I Trust You?' Explaining the Predictions of Any Classifier. KDD 2016.", "https://arxiv.org/abs/1602.04938", "makale", ""),
            ("Selvaraju RR ve ark. Grad-CAM. ICCV 2017.", "https://arxiv.org/abs/1610.02391", "makale", ""),
            ("Wachter S, Mittelstadt B, Russell C. Counterfactual explanations without opening the black box. Harvard JOLT 2018.", "https://arxiv.org/abs/1711.00399", "makale", ""),
            ("Obermeyer Z ve ark. Dissecting racial bias in an algorithm used to manage the health of populations. Science 2019.", "https://www.science.org/doi/10.1126/science.aax2342", "makale", ""),
            ("Ghassemi M, Oakden-Rayner L, Beam AL. The false hope of current approaches to explainable AI in health care. Lancet Digit Health 2021.", "https://www.thelancet.com/journals/landig/article/PIIS2589-7500(21)00208-9/fulltext", "makale", "Eleştirel karşı görüş.")]),

 dict(n=14, title="Güvenilir ve Klinik Uygulamaya Hazır Yapay Zeka",
  topic="Güvenilir ve klinik uygulamaya hazır yapay zeka: dış doğrulama, dağıtım kayması, model kartları/MLOps ve mahremiyet-koruyucu öğrenme (federated learning)",
  desc="İç–dış–zamansal doğrulama hiyerarşisi, dağıtım kayması türleri ve izleme, model kartları ve TRIPOD+AI raporlaması, MLOps yaşam döngüsü, federe öğrenme ve diferansiyel mahremiyet, regülasyon ve dönem değerlendirmesi.",
  tags=["dış doğrulama", "dağıtım kayması", "model kartı", "TRIPOD+AI", "MLOps", "federe öğrenme", "diferansiyel mahremiyet", "regülasyon", "AB YZ Yasası", "FDA"],
  methods=["Dış / zamansal doğrulama", "Kayma tespiti (PSI, KS)", "Model kartı", "Federe öğrenme (FedAvg)", "Diferansiyel mahremiyet"],
  objectives=["İç, zamansal, coğrafi ve alan-dışı doğrulama düzeylerini ayırır; TRIPOD+AI'ye uygun bir doğrulama planı yazar.",
              "Kovaryat, etiket ve kavram kaymasını tanır; üretimde kayma izleme (PSI, KS testi, performans izleme) kurar.",
              "Bir model kartı (kullanım amacı, veri, başarım alt-grupları, sınırlılıklar, etik) hazırlar ve MLOps yaşam döngüsünü (sürümleme, izleme, yeniden eğitim) tanımlar.",
              "Federe öğrenmenin (FedAvg) çalışma ilkesini ve mahremiyet sınırlarını açıklar; diferansiyel mahremiyet ve güvenli toplama kavramlarını tanır.",
              "AB YZ Yasası ve FDA çerçevelerinin bir klinik YZ ürününe getirdiği yükümlülükleri özetler."],
  concepts=[("Dış doğrulama", "Modelin geliştirildiği kurum/zaman dışındaki bağımsız veride sınanması; yayın ve klinik kullanım için asgari kanıt."),
            ("Dağıtım kayması", "Kovaryat kayması (girdi dağılımı değişir), etiket kayması (prevalans değişir), kavram kayması (girdi–çıktı ilişkisi değişir: yeni tedavi kılavuzu)."),
            ("Model kartı", "Modelin 'prospektüsü': amaç, eğitim verisi, alt-grup başarımı, bilinen sınırlılıklar, etik hususlar."),
            ("Federe öğrenme", "Verinin kurumdan çıkmadan, yalnızca model güncellemelerinin paylaşılmasıyla çok merkezli eğitim; mahremiyeti artırır ama tek başına garanti etmez."),
            ("Diferansiyel mahremiyet", "Tek bir bireyin varlığının çıktıyı ölçülebilir sınırın (ε) üzerinde değiştirmemesi garantisi; gürültü ekleme yoluyla sağlanır.")],
  examples=["Epic Sepsis Model'in dış doğrulaması (Wong ve ark., 2021): satıcının bildirdiği AUC 0.76–0.83 yerine bağımsız kurumda 0.63 ve yüksek alarm yükü.",
            "COVID-19 döneminde göğüs röntgeni modellerinde kavram kayması; pandemi öncesi eğitilmiş modellerin çöküşü.",
            "Çok merkezli beyin tümörü segmentasyonunda federe öğrenme (FeTS girişimi): veri paylaşılmadan 70+ kurumla eğitim."],
  tools=["scikit-learn", "evidently / alibi-detect", "Flower (federe öğrenme)", "Opacus", "Model Card Toolkit"],
  datasets=[("İki farklı kaynaktan aynı görev (ör. MIMIC-III Demo + eICU örneği)", "https://physionet.org/content/eicu-crd-demo/", "Coğrafi dış doğrulama."),
            ("10. haftanın CNN'i + farklı hastane röntgenleri", None, "Kovaryat kayması.")],
  activity="Dönem boyunca kurduğunuz bir modeli (tablo veya görüntü) farklı kaynaktan bir veri setinde dış doğrulayın; ayırt edicilik ve kalibrasyon düşüşünü raporlayın. PSI ile öznitelik kaymasını ölçün. Flower ile iki-üç 'kurum' simülasyonunda FedAvg çalıştırıp merkezî eğitimle karşılaştırın. Son teslim: modelinizin TRIPOD+AI uyumlu bir model kartı (2 sayfa).",
  questions=["Bir hastane, satıcının sağladığı yapay zeka modelini kullanmaya başlamadan önce hangi asgari doğrulama kanıtını istemeli?",
             "Federe öğrenme veriyi kurumdan çıkarmıyorsa mahremiyet sorunu çözülmüş sayılır mı? Model güncellemelerinden ne sızabilir?"],
  summary="Dönemi, bir modelin klinik uygulamaya hazır sayılması için gereken kanıt ve süreçlerle kapattık: dış doğrulama, kayma izleme, model kartı, mahremiyet-koruyucu öğrenme ve regülasyon. Genel sınav dönem sonunda; tüm dönem içeriğini kapsar.",
  before="Genel sınav için tüm haftaların 'Temel Kavramlar' bölümleri ve uygulama defterleri kapsam dâhilindedir. Son derste 45 dakikalık genel tekrar ve soru–cevap yapılır.",
  readings=[("Collins GS ve ark. TRIPOD+AI statement. BMJ 2024.", "https://www.bmj.com/content/385/bmj-2023-078378", "dokuman", "Raporlama standardı."),
            ("Mitchell M ve ark. Model Cards for Model Reporting. FAT* 2019.", "https://arxiv.org/abs/1810.03993", "makale", ""),
            ("Wong A ve ark. External validation of a widely implemented proprietary sepsis prediction model. JAMA Intern Med 2021.", "https://jamanetwork.com/journals/jamainternalmedicine/fullarticle/2781307", "makale", ""),
            ("Rieke N ve ark. The future of digital health with federated learning. npj Digit Med 2020.", "https://www.nature.com/articles/s41746-020-00323-1", "makale", ""),
            ("Finlayson SG ve ark. The clinician and dataset shift in artificial intelligence. NEJM 2021.", "https://www.nejm.org/doi/full/10.1056/NEJMc2104626", "makale", "")]),
]

assert [w["n"] for w in WEEKS] == list(range(1, 15)), "14 hafta olmalı"


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def yaml_list(items, indent=2):
    pad = " " * indent
    return "\n".join(f"{pad}- {yaml_str(i)}" for i in items)


def render(w):
    m = module_of(w["n"])
    fm = [
        "---",
        f'week: {w["n"]}',
        f'title: {yaml_str(w["title"])}',
        f'topic: {yaml_str(w["topic"])}',
        f'description: {yaml_str(w["desc"])}',
        f'module: {m["id"]}',
        f'exam: {"true" if w.get("exam") else "false"}',
        "status: taslak",
        'changeNote: ""',
        "tags:",
        yaml_list(w["tags"]),
        "objectives:",
        yaml_list(w["objectives"]),
        "methods:" + (" []" if not w["methods"] else ""),
    ]
    if w["methods"]:
        fm.append(yaml_list(w["methods"]))
    fm.append("tools:" + (" []" if not w["tools"] else ""))
    if w["tools"]:
        fm.append(yaml_list(w["tools"]))
    if w.get("datasets"):
        fm.append("datasets:")
        for name, url, note in w["datasets"]:
            fm.append(f"  - name: {yaml_str(name)}")
            if url:
                fm.append(f"    url: {yaml_str(url)}")
            if note:
                fm.append(f"    note: {yaml_str(note)}")
    else:
        fm.append("datasets: []")
    if w.get("readings"):
        fm.append("resources:")
        for title, url, kind, note in w["readings"]:
            fm.append(f"  - title: {yaml_str(title)}")
            fm.append(f"    url: {yaml_str(url)}")
            fm.append(f"    kind: {kind}")
            if note:
                fm.append(f"    note: {yaml_str(note)}")
    else:
        fm.append("resources: []")
    fm.append("---")

    body = []
    if w.get("before"):
        body += ["## Ön Okuma ve Hazırlık", "", w["before"], ""]
    body += ["## Ders Notları", "",
             f"> [!not] Bu bölüm ders notlarının genişletileceği alandır. İzlencedeki özgün başlık: **{w['topic']}**",
             "", "Ayrıntılı notlar ve türetimler ders yaklaştıkça buraya eklenecektir.", ""]
    body += ["## Temel Kavramlar", ""]
    for term, d in w["concepts"]:
        body.append(f"- **{term}** — {d}")
    body.append("")
    if w["examples"]:
        body += ["## Biyomedikal Uygulama Örnekleri", ""] + [f"- {e}" for e in w["examples"]] + [""]
    body += ["## Uygulama / Laboratuvar", "", w["activity"], ""]
    body += ["## Tartışma Soruları", ""] + [f"{i+1}. {q}" for i, q in enumerate(w["questions"])] + [""]
    body += ["## Haftanın Özeti", "", w["summary"], ""]
    return "\n".join(fm) + "\n\n" + "\n".join(body)


def main():
    force = "--force" in sys.argv
    OUT.mkdir(parents=True, exist_ok=True)
    written = skipped = 0
    for w in WEEKS:
        path = OUT / f"hafta-{w['n']:02d}.md"
        if (path.exists() or path.with_suffix(".mdx").exists()) and not force:
            skipped += 1
            continue
        path.write_text(render(w), encoding="utf-8")
        written += 1
    print(f"Yazıldı: {written}, atlandı (mevcut): {skipped} → {OUT}")


if __name__ == "__main__":
    main()
