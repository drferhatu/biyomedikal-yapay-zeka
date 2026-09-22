---
title: "Yerel Python Ortamı: conda, PyTorch ve SHAP"
description: "Windows ve macOS için Miniconda kurulumu, ders ortamının (scikit-learn, PyTorch, SHAP, MNE) oluşturulması, JupyterLab ve GPU kontrolü."
order: 1
---

## Neden yerel kurulum?

Dersin tüm uygulamaları Google Colab'de yapılabilir; Colab ücretsiz GPU sağlar ve kurulum gerektirmez. Yerel kurulum şu durumlarda gerekir:

- **Tez verinizle** çalışacaksanız: kurum izniyle alınmış veri, kişisel bilgisayara değil kurumun onayladığı makineye kurulur; oradaki ortamı bu rehberle hazırlarsınız.
- **Uzun eğitimler** (saatler süren CNN/Transformer eğitimi) için Colab oturum sınırları yetersiz kalıyorsa.
- Yapay zeka kod asistanlarının (Claude Code, Cursor vb.) sizin adınıza bir klasörde kod yazıp çalıştırmasını istiyorsanız.

> [!not] Süre
> Kurulum 15–25 dakika sürer (PyTorch indirmesi büyük olduğu için bağlantı hızına bağlı) ve bir kez yapılır.

## Adım 1 · Miniconda'yı kur

**Conda**, Python sürümlerini ve kütüphaneleri birbirinden ayrı "ortamlarda" tutar; bir projede bozulan bir şey diğerini etkilemez. **Miniconda** bunun küçük kurulum paketidir.

İndirme sayfası: [docs.conda.io → Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Windows

1. "Miniconda3 Windows 64-bit" kurulum dosyasını indirip çalıştırın.
2. Kurulumda **"Just Me"** seçin; "Add Miniconda3 to my PATH" kutusunu işaretlemeyin (varsayılan).
3. Kurulum bitince Başlat menüsünden **Anaconda Prompt (miniconda3)** uygulamasını açın.

### macOS

1. İşlemcinize göre indirin: Apple Silicon için "arm64", Intel Mac için "x86_64" (sol üst  → Bu Mac Hakkında → "Çip").
2. `.pkg` dosyasını çalıştırın ve varsayılanlarla ilerleyin.
3. **Terminal** uygulamasını açın. Komut satırının başında `(base)` görünüyorsa kurulum tamam.

### Kontrol

```bash
conda --version
```

## Adım 2 · Ders ortamını oluştur

Ders için `biomed` adında bir ortam oluşturup temel kütüphaneleri kuruyoruz:

```bash
conda create -n biomed python=3.12 numpy pandas scipy matplotlib seaborn scikit-learn jupyterlab -y
conda activate biomed
```

Ardından derin öğrenme ve açıklanabilirlik kütüphaneleri:

```bash
pip install torch torchvision xgboost shap lime umap-learn mne neurokit2 captum
```

> [!uyari] GPU'lu Windows/Linux bilgisayarlar
> NVIDIA ekran kartınız varsa PyTorch'u CUDA destekli sürümle kurun; doğru komutu [pytorch.org/get-started](https://pytorch.org/get-started/locally/) sayfasındaki seçiciden alın. Apple Silicon Mac'lerde `torch` doğrudan MPS (Metal) hızlandırmasıyla gelir; ek işlem gerekmez.

### Kontrol

```bash
python -c "import torch, sklearn, shap; print(torch.__version__, sklearn.__version__, shap.__version__); print('GPU:', torch.cuda.is_available() or torch.backends.mps.is_available())"
```

## Adım 3 · JupyterLab'i çalıştır

```bash
jupyter lab
```

Tarayıcınızda JupyterLab açılır. Colab'den indirdiğiniz `.ipynb` dosyalarını (Dosya → İndir → .ipynb) buraya sürükleyip çalıştırabilirsiniz. Kapatmak için terminalde `Ctrl + C`.

## Adım 4 · Tekrarlanabilirlik alışkanlıkları

Lisansüstü çalışmada sonuçlarınızın başkası (ve altı ay sonra siz) tarafından yeniden üretilebilmesi gerekir:

1. **Ortamı dışa aktarın** ve tez/makale deposuna ekleyin:
   ```bash
   conda env export --from-history > environment.yml
   ```
2. **Rastgelelik tohumunu** sabitleyin: `numpy`, `torch` ve `random` için aynı tohum; `train_test_split(random_state=...)`.
3. **Hasta-bazlı bölme** yapın: aynı hastanın kayıtları hem eğitim hem test kümesine düşmesin (`GroupKFold`). Bu, 2. haftanın ana konusudur.
4. Kod ve defterleri **Git** ile sürümleyin; veri dosyalarını depoya koymayın.

> [!uyari] Hasta verisi
> Yerel kurulum, hasta verisini kişisel bilgisayarınıza almanız için gerekçe değildir. Gerçek hasta verisi yalnızca etik kurul onayı ve kurum izniyle, kurumun belirlediği ortamda ve KVKK çerçevesinde işlenir. Derste açık ve anonim veri setleri kullanıyoruz.

## Sık karşılaşılan sorunlar

| Belirti | Olası neden | Çözüm |
|---|---|---|
| `conda: command not found` | Terminal Miniconda'yı tanımıyor | Windows'ta Anaconda Prompt kullanın; macOS'ta Terminal'i kapatıp açın |
| `ModuleNotFoundError` | Yanlış ortam ya da kütüphane kurulmamış | `conda activate biomed`, sonra `pip install <paket>` |
| `torch.cuda.is_available()` → `False` | CPU sürümü kurulmuş ya da sürücü eski | pytorch.org seçicisinden CUDA sürümünü kurun; NVIDIA sürücüsünü güncelleyin |
| SHAP çok yavaş | `KernelExplainer` kullanılıyor | Ağaç modellerinde `TreeExplainer`, PyTorch'ta `DeepExplainer`/`GradientExplainer` |
| Kurulum çok yer kaplıyor | Normal; PyTorch ile ~5 GB | Gereksiz ortamları `conda env remove -n <ad>` ile silin |

## Yararlı komutlar

```bash
conda env list                    # tüm ortamları listele
conda activate biomed             # ortama gir
conda deactivate                  # ortamdan çık
pip install -U <paket>            # paketi güncelle
conda run -n biomed python x.py   # ortamı etkinleştirmeden bir dosyayı çalıştır
```
