# SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka — Ders Web Sitesi

Fırat Üniversitesi Yazılım ve Bilişim Araştırma Enstitüsü lisansüstü dersi **SVY 5430 Biyomedikal Verilerin Analizi ve Yapay Zeka** (2026–2027 Güz) için 14 haftalık ders web sitesi.
Site tamamen statiktir, GitHub Pages üzerinde yayımlanır ve tüm ders içeriği koddan ayrı Markdown/JSON dosyalarında tutulur.

Canlı adres (depo oluşturulduktan sonra): `https://drferhatu.github.io/biyomedikal-yapay-zeka/`

Aynı mimari, Tıp Fakültesi **Yapay Zeka ve Sağlık** dersinin sitesinden (`../../TIP`) uyarlanmıştır; farklar: tek yarıyıl (14 hafta, 5 modül), lisansüstü tona uygun bölüm adları (Ön Okuma, Yöntemler, Okuma Listesi, Veri Setleri), yeni görsel kimlik ve ek uyarı kutusu türleri (`makale`, `formul`).

## Teknoloji

| Katman | Seçim | Neden |
|---|---|---|
| Çatı | [Astro 5](https://astro.build) | Sıfır istemci JavaScript varsayılanı, içerik koleksiyonları, statik çıktı |
| Stil | [Tailwind CSS 4](https://tailwindcss.com) | Tasarım sistemini tek CSS dosyasında token olarak tutar |
| İçerik | Markdown/MDX + JSON | Haftalar Markdown, ders künyesi/modüller/takvim JSON |
| Arama | [Pagefind](https://pagefind.app) | Derleme sonrası tamamen statik arama dizini, sunucu gerekmez |
| Defterler | Jupyter + nbconvert | `notebooks/*.ipynb` → Colab bağlantısı ve sitede gömülü HTML |
| Dağıtım | GitHub Actions → GitHub Pages | `main` dalına her push'ta otomatik derleme ve yayın |

## Klasör yapısı

```
content/
  data/course.json        ders künyesi, amaç, kazanımlar, değerlendirme, kaynaklar, iletişim kanalları
  data/modules.json       5 modül (başlık, haftalar, renk, özet)
  data/schedule.json      haftalık tarihler ve durumlar (tatil/ertelendi/sınav)
  weeks/hafta-01.mdx …    14 haftalık ders dosyası (her hafta tek dosya; .md veya .mdx)
  guides/*.md             kurulum rehberleri (/rehber/<ad>)
  announcements/*.md      duyurular
notebooks/                Jupyter/Colab defterleri (hafta-XX.ipynb)
src/
  pages/                  rotalar (index, ders-hakkinda, ders-akisi, haftalar/, rehber/, kaynaklar, duyurular, arama)
  components/             yeniden kullanılabilir parçalar (Roadmap, WeekCard, Toc, WeekPager, NotebookEmbed, Channels …)
  layouts/BaseLayout.astro
  lib/site.ts             yardımcılar (href, modül/takvim erişimi, tarih biçimi, REPO sabiti)
  lib/remark-callouts.mjs Markdown uyarı kutuları
  lib/rehype-base-links.mjs  Markdown'daki /haftalar/... bağlantılarına base yolunu ekler
  styles/global.css       tasarım sistemi (renk, yazı tipi, prose stilleri)
scripts/
  extract_course_docx.py  DOCX izlence formunu düz metin/JSON'a çıkarır (iç içe tablolar için XML yedeği)
  generate_week_files.py  14 haftalık Markdown iskeletini üretir (mevcut dosyaları ezmez)
  validate_content.py     içerik + derleme doğrulaması (haftalar, modüller, takvim, defter, kırık bağlantı)
  build_notebooks.py      defterleri (ister tanımdan üretir) çalıştırır ve HTML'e çevirir
  make_qr.py              iletişim kanalları için karekodlar
  make_assets.py          og.png ve apple-touch-icon.png üretir
public/                   favicon, og.png, robots.txt, .nojekyll, qr/
.github/workflows/deploy.yml  GitHub Pages dağıtımı
```

Kaynak belge (`*DersIzlenceFormu.docx`) çalışma klasöründe olduğu gibi durur; `.gitignore` ile depoya ve siteye dâhil edilmez.

## Yerel geliştirme

Gereksinim: Node.js 22+ (`/opt/homebrew/bin/node`).

```bash
npm install
npm run dev        # http://localhost:4321/biyomedikal-yapay-zeka/  (arama dev'de çalışmaz)
npm run build      # dist/ üretir ve Pagefind dizinini oluşturur
npm run preview    # dist/ klasörünü yerelde sunar (arama dâhil)
```

Python scriptleri için `ferhat_ml` conda ortamı kullanılır:

```bash
/opt/miniconda3/envs/ferhat_ml/bin/python scripts/validate_content.py
```

## İçerik düzenleme

### Bir haftanın konusunu veya notlarını değiştirmek

`content/weeks/hafta-XX.md` dosyasını açın. Üst kısım (frontmatter) haftanın kimliğidir:

```yaml
---
week: 4
title: "Klasik Makine Öğrenmesi I: Denetimli Öğrenme ve Klinik Metrikler"  # sitede görünen başlık
topic: "Klasik makine öğrenmesi I: ..."                                    # izlencedeki özgün satır
description: "Lojistik regresyon ve k-NN ..."                              # kart ve meta açıklaması
module: m2              # modules.json'daki modül kimliği
exam: false             # true ise "Ara sınav" etiketi
status: taslak          # taslak → "Hazırlık aşamasında" kutusu; notlar bitince hazir yapın
changeNote: ""          # dolu ise sayfada "Program değişikliği" uyarısı çıkar
tags: [...]             # arama ve etiketler
objectives: [...]       # öğrenme hedefleri (numaralı kutular)
methods: [...]          # yöntem rozetleri (kartta ve sayfa üstünde)
tools: [...]            # "Araçlar ve kütüphaneler"
datasets:               # "Bu haftanın veri setleri"
  - { name: "…", url: "https://…", note: "…" }
resources:              # "Okuma listesi"; kind: makale | kitap | dokuman | video | diger
  - { title: "…", url: "https://…", kind: makale, note: "…" }
---
```

Alt kısım serbest Markdown'dır. Önerilen başlıklar: `## Ön Okuma ve Hazırlık`, `## Ders Notları`,
`## Temel Kavramlar`, `## Biyomedikal Uygulama Örnekleri`, `## Uygulama / Laboratuvar`, `## Tartışma Soruları`, `## Haftanın Özeti`.
Boş bırakılan bölümleri silmekte serbestsiniz; içindekiler tablosu `##` başlıklarından otomatik oluşur.

Uyarı kutuları:

```markdown
> [!neden] Neden önemli?
> Kalibrasyon, ayırt edicilik kadar önemlidir çünkü ...

> [!ornek]
> Sepsis modelinde SHAP şelale grafiği ...

> [!makale] Okuma önerisi
> Rudin (2019), Nat Mach Intell.

> [!formul]
> Dice = 2|A∩B| / (|A|+|B|)
```

Türler: `not`, `uyari`, `ornek`, `neden`, `nerede`, `tanim`, `makale`, `formul`. Başlık verilmezse varsayılan kullanılır.

Başka bir haftaya bağlantı vermek için kök yol yazın; base otomatik eklenir: `[4. hafta](/haftalar/hafta-04)`.

**Defteri notların arasına yerleştirmek** için dosyayı `.mdx` yapın, frontmatter'a `placement: inline` ekleyin ve gövdede istediğiniz yere koyun (bkz. `hafta-01.mdx`):

```mdx
import NotebookEmbed from '@/components/NotebookEmbed.astro';

... notlar ...

<NotebookEmbed file="notebooks/hafta-01.ipynb" title="Hafta 1 · Uçtan Uca İlk Tur" />
```

`placement: auto` (varsayılan) ise defter, notların bittiği yere sayfa tarafından eklenir.

### Haftaların tarihini değiştirmek, tatil veya erteleme işlemek

`content/data/schedule.json` içindeki ilgili satırı düzenleyin:

```json
{ "week": 5, "date": "2026-10-28", "status": "tatil", "note": "Cumhuriyet Bayramı; konu 6. haftaya kaydı" }
```

- `date` boşsa yalnızca hafta numarası görünür.
- `status`: `normal` | `tatil` | `ertelendi` | `sinav`.
- `note` kısa açıklama olarak gösterilir.

İki haftanın konusunu yer değiştirmek için iki Markdown dosyasının içeriğini takas edin (sadece `week` alanını koruyun) ve `changeNote` ile açıklayın.

### Haftaya Colab defteri eklemek

1. Defteri `notebooks/hafta-XX.ipynb` olarak kaydedin (Colab'den Dosya → İndir → .ipynb, ya da `scripts/build_notebooks.py` içindeki `NOTEBOOKS` sözlüğüne hücre listesi ekleyin).
2. Sitede gömülü görünümü üretin:

```bash
/opt/miniconda3/envs/ferhat_ml/bin/python scripts/build_notebooks.py --execute
```

`--execute` tüm defterleri çalıştırır ve çıktılarıyla HTML'e çevirir. Kaynak `.ipynb` dosyası **değiştirilmez** (`--save` verilmedikçe). `--force` scriptteki tanımdan defteri yeniden üretir ve elle yapılan değişiklikleri **ezer**; Colab'de düzenlediğiniz defterlerde kullanmayın.

**Otomatik akış:** Colab'da *Dosya → GitHub'a kopya kaydet* ile `notebooks/hafta-XX.ipynb` dosyasını `main` dalına kaydettiğinizde GitHub Actions defteri çalıştırır, gömülü görünümü üretir ve siteyi yeniden yayımlar. PyTorch gerektiren defterler CI'da çalıştırılmak istenirse `scripts/requirements-notebooks.txt` dosyasına `torch` eklenir (derleme süresi uzar); aksi hâlde defteri Colab'da çalıştırıp çıktılarıyla kaydedin, CI hata hücrelerini olduğu gibi gösterir.

3. Haftanın Markdown dosyasına ekleyin:

```yaml
notebook:
  file: notebooks/hafta-04.ipynb
  title: "Hafta 4 · Klinik Metrikler"
  embed: true       # false ise yalnızca "Colab'de aç" düğmesi görünür
```

"Colab'de aç" bağlantısı GitHub'daki `main` dalındaki dosyayı açar; öğrenci kendi Drive'ına kopyalayıp çalıştırır.

### Yeni duyuru eklemek

`content/announcements/` altına yeni bir dosya:

```markdown
---
title: "Ara sınav tarihi"
date: 2026-11-10
pinned: true        # üstte sabit
kind: sinav         # bilgi | onemli | sinav
---
Ara sınav 12 Kasım Perşembe 10.00'da Seminer Salonu'nda ...
```

### Ders künyesi, kazanımlar, kaynaklar, iletişim

`content/data/course.json` içinde. Kazanımların `weeks` alanı, Ders Hakkında sayfasındaki hafta bağlantılarını ve hafta sayfalarındaki "Ders kazanımları" kutusunu üretir. Ders günü/saati kesinleşince `classTime` alanını güncelleyin.

İletişim kanalları `channels` dizisindedir. Bağlantı değişirse karekodu yeniden üretin:

```bash
/opt/miniconda3/envs/ferhat_ml/bin/python scripts/make_qr.py
```

### Kurulum rehberi eklemek

`content/guides/<ad>.md` dosyası oluşturun (`title`, `description`, `order`). Sayfa `/rehber/<ad>` adresinde açılır ve Kaynaklar sayfasında listelenir.

### Modül eklemek/değiştirmek

`content/data/modules.json`. Her haftanın tam olarak bir modülde yer alması gerekir; `validate_content.py` bunu denetler.

## Scriptler

| Script | İş |
|---|---|
| `scripts/extract_course_docx.py "<dosya.docx>" [--json çıktı.json]` | DOCX'teki paragraf ve tabloları düz metin/JSON'a çıkarır |
| `scripts/generate_week_files.py [--force]` | 14 haftalık iskeleti üretir; `--force` olmadan var olan dosyalara dokunmaz |
| `scripts/validate_content.py` | Hafta sayısı, modül eşleşmesi, takvim formatı, defter dosyaları ve (dist varsa) kırık bağlantıları denetler |
| `scripts/build_notebooks.py [--execute] [--save] [--force]` | Defterleri üretir/çalıştırır ve `public/notebooks/` altına HTML üretir |
| `scripts/make_qr.py` | `public/qr/<id>.svg` karekodları |
| `scripts/make_assets.py` | `public/og.png` ve `public/apple-touch-icon.png` |

## GitHub Pages dağıtımı

1. Depoyu oluşturun ve gönderin:

```bash
gh repo create drferhatu/biyomedikal-yapay-zeka --public --source=. --remote=origin --push
```

2. Depo ayarları → Pages → Source: **GitHub Actions**.
3. `main` dalına push edildiğinde `.github/workflows/deploy.yml` çalışır: Python bağımlılıkları, defterlerin çalıştırılıp HTML'e çevrilmesi, `npm ci`, `npm run build`, içerik doğrulaması ve `dist/` yayını.
4. Base yolu `astro.config.mjs` içinde `/biyomedikal-yapay-zeka` olarak ayarlıdır. Depo adı değişirse bu değeri, `public/robots.txt`, `src/lib/site.ts` içindeki `REPO` sabitini, `scripts/build_notebooks.py` içindeki `REPO` ve `scripts/validate_content.py` içindeki `BASE` değerini güncelleyin. Özel alan adına geçilirse `SITE_URL` ve `BASE_PATH=/` ortam değişkenleriyle derleyin.

İçeriği doğrudan GitHub web arayüzünden de düzenleyebilirsiniz; kaydettiğinizde site birkaç dakika içinde yenilenir.

## Bakım notları

- Yayına almadan önce: `npm run build && /opt/miniconda3/envs/ferhat_ml/bin/python scripts/validate_content.py`.
- Ders notları tamamlanan haftada `status: hazir` yapın; "Hazırlık aşamasında" kutusu kalkar.
- Yazı tipleri Google Fonts'tan yüklenir (Space Grotesk, IBM Plex Sans, IBM Plex Mono). Çevrimdışı kullanım gerekirse `public/fonts/` altına alıp `BaseLayout.astro` içindeki bağlantıyı değiştirin.
- Bağımlılık güncellemeleri: `npm outdated` / `npm update`; büyük sürüm değişimlerinde derlemeyi yerelde doğrulayın.
