#!/usr/bin/env node
/* Proje ara sunumu (vize) için PowerPoint şablonunu üretir:
     public/proje/ara-sunum-sablonu.pptx
   Slayt sırası /proje#ara-sunum sayfasındaki iskeletle aynıdır.

   Kullanım (proje kökünden):
     npm i --no-save pptxgenjs
     node scripts/make_sunum_sablonu.cjs [apply_theme.js yolu]
*/
const path = require('path');
const pptxgen = require('pptxgenjs');

const ROOT = path.resolve(__dirname, '..');
const OUT = path.join(ROOT, 'public', 'proje', 'ara-sunum-sablonu.pptx');

const THEME = {
  name: 'SVY 5430',
  headFontFace: 'Arial',
  bodyFontFace: 'Arial',
  colors: {
    dk1: '0B1526', lt1: 'FFFFFF', dk2: '2F4058', lt2: 'F5F7FB',
    accent1: '2F3FA3', accent2: '0F9B8E', accent3: '4A5BD1',
    accent4: 'E3E7FB', accent5: 'D8F1EE', accent6: '6B7A92',
    hlink: '2F3FA3', folHlink: '4A5BD1',
  },
};

const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.33 x 7.5 inç
pres.theme = { headFontFace: THEME.headFontFace, bodyFontFace: THEME.bodyFontFace };
pres.title = 'Proje ara sunumu şablonu';
pres.author = 'SVY 5430';
pres.company = 'Fırat Üniversitesi';
const C = pres.SchemeColor;

const W = 13.333, MX = 0.6;
const DERS = 'SVY 5430 · Biyomedikal Verilerin Analizi ve Yapay Zeka';
const ADIMLAR = [
  'Klinik soru', 'Veri', 'Keşif', 'Ön işleme kararları',
  'Doğrulama tasarımı', 'Temel model ve eğriler', 'Sorunlar ve plan', 'Depo turu',
];

/* ---------- Düzenler ---------- */
pres.defineSlideMaster({
  title: 'KAPAK',
  background: { color: C.text1 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', align: 'left', x: MX, y: 2.2, w: 6.6, h: 2.2, fontSize: 38, bold: true, color: C.background1, valign: 'top', margin: 0 }, text: '' } },
    { placeholder: { options: { name: 'body', type: 'body', align: 'left', x: MX, y: 4.6, w: 6.6, h: 1.3, fontSize: 18, color: C.accent4, valign: 'top', margin: 0 }, text: '' } },
    { text: { text: 'Fırat Üniversitesi · Yazılım ve Bilişim Araştırma Enstitüsü · 2026–2027 Güz', options: { x: MX, y: 6.7, w: 8, h: 0.3, fontSize: 11, color: C.accent4, margin: 0 } } },
  ],
});

pres.defineSlideMaster({
  title: 'ICERIK',
  background: { color: C.background1 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', align: 'left', x: MX, y: 0.8, w: 9.6, h: 0.8, fontSize: 36, bold: true, color: C.text1, valign: 'middle', margin: 0 }, text: '' } },
    { text: { text: DERS + ' · Proje ara sunumu', options: { x: MX, y: 6.98, w: 9, h: 0.3, fontSize: 10, color: C.accent6, margin: 0 } } },
  ],
  slideNumber: { x: W - MX - 0.8, y: 6.98, w: 0.8, h: 0.3, fontSize: 10, color: C.accent6, align: 'right' },
});

pres.defineSlideMaster({
  title: 'KAPANIS',
  background: { color: C.text1 },
  objects: [
    { placeholder: { options: { name: 'title', type: 'title', align: 'left', x: MX, y: 2.3, w: 7, h: 1.2, fontSize: 44, bold: true, color: C.background1, valign: 'top', margin: 0 }, text: '' } },
    { placeholder: { options: { name: 'body', type: 'body', align: 'left', x: MX, y: 3.7, w: 7, h: 2, fontSize: 18, color: C.accent4, valign: 'top', margin: 0 }, text: '' } },
    { text: { text: DERS, options: { x: MX, y: 6.7, w: 8, h: 0.3, fontSize: 11, color: C.accent4, margin: 0 } } },
  ],
});

/* ---------- Yardımcılar ---------- */
const iki = (n) => String(n).padStart(2, '0');

function icerik(n, not) {
  const s = pres.addSlide({ masterName: 'ICERIK' });
  s.addText(`ADIM ${iki(n)} / 08`, { x: MX, y: 0.45, w: 3, h: 0.3, fontSize: 11, bold: true, color: C.accent1, charSpacing: 2, margin: 0, isTextBox: true, objectName: 'Adım etiketi' });
  // sekiz noktalı ilerleme göstergesi
  ADIMLAR.forEach((_, i) => {
    s.addShape(pres.ShapeType.ellipse, {
      x: W - MX - (8 - i) * 0.3 + 0.12, y: 0.5, w: 0.18, h: 0.18,
      fill: { color: i + 1 === n ? C.accent1 : C.accent4 }, line: { type: 'none' },
      objectName: `İlerleme ${i + 1}`,
    });
  });
  s.addText(ADIMLAR[n - 1], { placeholder: 'title' });
  s.addNotes(not);
  return s;
}

function kart(s, x, y, w, h, baslik, ipucu, o = {}) {
  s.addText(
    [
      { text: baslik, options: { bold: true, fontSize: 12, color: o.vurgu || C.accent1, charSpacing: 1, breakLine: true } },
      { text: ipucu, options: { fontSize: o.fontSize || 15, color: o.renk || C.text2 } },
    ],
    {
      x, y, w, h, shape: pres.ShapeType.roundRect, rectRadius: 0.12,
      fill: { color: o.fill || C.background2 }, line: { type: 'none' },
      valign: 'top', margin: [12, 14, 12, 14], paraSpaceAfter: 6, isTextBox: true, objectName: baslik,
    },
  );
}

function sekil(s, x, y, w, h, metin) {
  s.addText(metin, {
    x, y, w, h, shape: pres.ShapeType.rect,
    fill: { color: C.background1 }, line: { color: C.accent6, width: 1, dashType: 'dash' },
    align: 'center', valign: 'middle', fontSize: 14, color: C.accent6, margin: 14, isTextBox: true, objectName: 'Şekil alanı',
  });
}

const hucre = (text, o = {}) => ({ text, options: { fontSize: 14, color: C.text2, valign: 'middle', margin: [6, 10, 6, 10], ...o } });
const baslikHucre = (text) => hucre(text, { bold: true, color: C.background1, fill: { color: C.accent1 } });
const etiketHucre = (text) => hucre(text, { bold: true, color: C.text1, fill: { color: C.background2 } });
const kenar = { type: 'solid', color: 'D9DFEB', pt: 0.75 };

/* ---------- Kapak ---------- */
{
  const s = pres.addSlide({ masterName: 'KAPAK' });
  s.addText('PROJE ARA SUNUMU · 18 KASIM 2026', { x: MX, y: 1.5, w: 6.6, h: 0.3, fontSize: 12, bold: true, color: C.accent5, charSpacing: 2, margin: 0, isTextBox: true, objectName: 'Üst etiket' });
  s.addText('Proje başlığınızı buraya yazın', { placeholder: 'title' });
  s.addText([
    { text: 'Ad Soyad', options: { breakLine: true } },
    { text: 'Proje kodu: BVYZ-00 · github.com/kullanici/depo' },
  ], { placeholder: 'body' });
  // sağda sunumun akışı
  s.addText('SUNUMUN AKIŞI', { x: 8.2, y: 1.5, w: 4.5, h: 0.3, fontSize: 12, bold: true, color: C.accent5, charSpacing: 2, margin: 0, isTextBox: true, objectName: 'Akış etiketi' });
  ADIMLAR.forEach((ad, i) => {
    const y = 2.05 + i * 0.56;
    s.addText(iki(i + 1), { x: 8.2, y, w: 0.42, h: 0.42, shape: pres.ShapeType.roundRect, rectRadius: 0.08, fill: { color: C.accent1 }, line: { type: 'none' }, align: 'center', valign: 'middle', fontSize: 12, bold: true, color: C.background1, margin: 0, isTextBox: true, objectName: `Adım ${i + 1} no` });
    s.addText(ad, { x: 8.8, y, w: 3.9, h: 0.42, fontSize: 16, color: C.background1, valign: 'middle', margin: 0, isTextBox: true, objectName: `Adım ${i + 1}` });
  });
  s.addNotes('Kapak. Proje başlığını, adınızı, proje kodunuzu ve depo adresinizi yazın. Sağdaki akış listesine dokunmayın; herkes aynı sırayla sunar. Süre: 10 dakika sunum, 5 dakika soru. Kapak ve kapanış dışında sekiz slayt vardır; slayt eklemeyin, sıra değiştirmeyin.');
}

/* ---------- 1. Klinik soru ---------- */
{
  const s = icerik(1, 'Yaklaşık 1 dakika. Soruyu tek cümleyle söyleyin, sonra üç kutuyu doldurun. Etiketin veri setinde nasıl tanımlandığını mutlaka belirtin.');
  kart(s, MX, 1.95, W - 2 * MX, 1.35, 'KLİNİK SORU, TEK CÜMLE', 'Örnek: "Kalp yetmezliği ile yatan bir hastanın takip süresi içinde ölüp ölmeyeceğini, yatıştaki ölçümlerden tahmin edebilir miyiz?"', { fill: C.accent4, fontSize: 18 });
  const w = (W - 2 * MX - 0.8) / 3;
  kart(s, MX, 3.7, w, 2.9, 'HASTA', 'Kim? Hangi klinikte, hangi anda? Bir satır neyi temsil ediyor: bir hastayı mı, bir başvuruyu mu, bir sinyal parçasını mı?');
  kart(s, MX + w + 0.4, 3.7, w, 2.9, 'SONUÇ (ETİKET)', 'Neyi tahmin ediyorsunuz? Etiket veri setinde nasıl tanımlanmış, kim ya da ne belirlemiş?');
  kart(s, MX + 2 * (w + 0.4), 3.7, w, 2.9, 'NEDEN ÖNEMLİ', 'Bu tahmin doğru çıkarsa hangi klinik karar değişir? Yanlış çıkarsa bedeli nedir?');
}

/* ---------- 2. Veri ---------- */
{
  const s = icerik(2, 'Yaklaşık 1 dakika. Dört kutudaki sayıları kendi verinizle değiştirin. Sınıflandırma dışı bir görevde dördüncü kutuya hedef değişkenin dağılımını yazın.');
  const w = (W - 2 * MX - 3 * 0.3) / 4;
  [['KAYIT', '0000', 'satır / örnek'], ['HASTA', '000', 'tekil hasta / denek'], ['ÖZNİTELİK', '00', 'sütun ya da kanal'], ['POZİTİF SINIF', '%00', 'sınıf oranı']].forEach(([et, sayi, alt], i) => {
    s.addText([
      { text: et, options: { fontSize: 12, bold: true, color: C.accent1, charSpacing: 1, breakLine: true } },
      { text: sayi, options: { fontSize: 44, bold: true, color: C.text1, breakLine: true } },
      { text: alt, options: { fontSize: 12, color: C.accent6 } },
    ], { x: MX + i * (w + 0.3), y: 1.95, w, h: 2.0, shape: pres.ShapeType.roundRect, rectRadius: 0.12, fill: { color: C.background2 }, line: { type: 'none' }, valign: 'middle', margin: [10, 14, 10, 14], isTextBox: true, objectName: et });
  });
  const w2 = (W - 2 * MX - 0.4) / 2;
  kart(s, MX, 4.3, w2, 2.3, 'KAYNAK', 'Veri setinin adı, kim topladı, hangi yıllar, hangi merkez? Bağlantısı ve lisansı.');
  kart(s, MX + w2 + 0.4, 4.3, w2, 2.3, 'VERİNİN TUZAKLARI', 'Bir hastanın birden çok satırı var mı? Eksik değerler nerede yoğun? Yinelenen kayıt, tutarsız birim, şüpheli sütun gördünüz mü?', { fill: C.accent5, vurgu: C.accent2 });
}

/* ---------- 3. Keşif ---------- */
{
  const s = icerik(3, 'Yaklaşık 1,5 dakika. En çok iki grafik. Her grafik deponuzdaki bir defterden üretilmiş olmalı; alt yazıya defterin adını yazın. Eksenler ve yazılar arka sıradan okunabilmeli.');
  const w = (W - 2 * MX - 0.4) / 2;
  sekil(s, MX, 1.95, w, 3.1, 'Şekil 1\nDefterden ürettiğiniz grafiği buraya yerleştirin');
  sekil(s, MX + w + 0.4, 1.95, w, 3.1, 'Şekil 2\nDefterden ürettiğiniz grafiği buraya yerleştirin');
  s.addText('Şekil 1: Ne gösteriyor? (notebooks/01_kesif.ipynb)', { x: MX, y: 5.1, w, h: 0.3, fontSize: 11, color: C.accent6, margin: 0, isTextBox: true, objectName: 'Alt yazı 1' });
  s.addText('Şekil 2: Ne gösteriyor? (notebooks/01_kesif.ipynb)', { x: MX + w + 0.4, y: 5.1, w, h: 0.3, fontSize: 11, color: C.accent6, margin: 0, isTextBox: true, objectName: 'Alt yazı 2' });
  kart(s, MX, 5.6, W - 2 * MX, 1.1, 'BENİ ŞAŞIRTAN', 'Veride beklemediğiniz tek bir şeyi bir cümleyle yazın.', { fill: C.accent5, vurgu: C.accent2 });
}

/* ---------- 4. Ön işleme kararları ---------- */
{
  const s = icerik(4, 'Yaklaşık 1,5 dakika. Her satır bir karar. "Ne yaptım" kısa olsun, asıl önemli olan gerekçe sütunudur. Size uymayan satırı silin, gerekiyorsa kendi kararınızı ekleyin.');
  const satirlar = [
    ['Eksik veri', 'Hangi sütunlar, hangi yöntem?', 'Neden bu yöntem? Eksiklik rastgele mi?'],
    ['Ölçekleme', 'Hangi ölçekleyici, hangi sütunlara?', 'Modeliniz ölçeğe duyarlı mı?'],
    ['Kategorik değişkenler', 'Kodlama yöntemi', 'Kategori sayısı, seyrek sınıflar'],
    ['Aykırı değer / gürültü', 'Sildim mi, kırptım mı, bıraktım mı?', 'Klinik olarak mümkün bir değer mi?'],
    ['Çıkardığım sütunlar', 'Hangileri?', 'Tahmin anında bilinemez ya da kimlik taşıyor'],
  ];
  s.addTable(
    [[baslikHucre('Karar'), baslikHucre('Ne yaptım'), baslikHucre('Gerekçe')],
      ...satirlar.map(([a, b, c]) => [etiketHucre(a), hucre(b), hucre(c)])],
    { x: MX, y: 1.95, w: W - 2 * MX, colW: [2.9, 4.4, 4.833], rowH: 0.74, border: kenar, objectName: 'Karar tablosu' },
  );
}

/* ---------- 5. Doğrulama tasarımı ---------- */
{
  const s = icerik(5, 'Yaklaşık 1,5 dakika. Vize ölçütlerinde en yüksek puan bu slayttadır. Oranları ve bölme birimini yazın; sağdaki üç soruya "evet / hayır, çünkü…" diye yanıt verin.');
  s.addText('TÜM VERİ', { x: MX, y: 1.95, w: 6.6, h: 0.55, shape: pres.ShapeType.roundRect, rectRadius: 0.1, fill: { color: C.text1 }, line: { type: 'none' }, align: 'center', valign: 'middle', fontSize: 14, bold: true, color: C.background1, charSpacing: 1, isTextBox: true, objectName: 'Tüm veri' });
  [['EĞİTİM', '%00', 3.3, C.accent1, C.background1], ['DOĞRULAMA', '%00', 1.5, C.accent3, C.background1], ['TEST', '%00', 1.5, C.accent2, C.background1]].reduce((x, [ad, oran, w, fill, renk]) => {
    s.addText([
      { text: ad, options: { fontSize: 12, bold: true, charSpacing: 1, breakLine: true } },
      { text: oran, options: { fontSize: 24, bold: true } },
    ], { x, y: 2.7, w, h: 1.3, shape: pres.ShapeType.roundRect, rectRadius: 0.1, fill: { color: fill }, line: { type: 'none' }, align: 'center', valign: 'middle', color: renk, isTextBox: true, objectName: ad });
    return x + w + 0.15;
  }, MX);
  kart(s, MX, 4.3, 6.6, 2.4, 'BÖLME STRATEJİSİ', 'Bölme birimi: hasta mı, kayıt mı? Katmanlı mı, zamana göre mi? Çapraz doğrulama kullandıysanız kaç kat? Tohum değeri.');
  s.addText('SIZINTI KONTROLÜ', { x: 7.6, y: 1.95, w: 5.1, h: 0.3, fontSize: 12, bold: true, color: C.accent2, charSpacing: 1, margin: 0, isTextBox: true, objectName: 'Sızıntı etiketi' });
  [
    ['Aynı hasta hem eğitimde hem testte var mı?', 'Yanıt ve nasıl denetlediğiniz'],
    ['Ön işleme yalnızca eğitim verisinde mi öğrenildi?', 'Ölçekleyici, doldurucu, öznitelik seçimi'],
    ['Tahmin anında bilinemeyecek sütun kaldı mı?', 'Hangi sütunları bu yüzden çıkardınız?'],
  ].forEach(([soru, ipucu], i) => {
    s.addText([
      { text: soru, options: { fontSize: 15, bold: true, color: C.text1, breakLine: true } },
      { text: ipucu, options: { fontSize: 14, color: C.text2 } },
    ], { x: 7.6, y: 2.4 + i * 1.47, w: 5.1, h: 1.32, shape: pres.ShapeType.roundRect, rectRadius: 0.12, fill: { color: C.accent5 }, line: { type: 'none' }, valign: 'middle', margin: [8, 14, 8, 14], paraSpaceAfter: 4, isTextBox: true, objectName: `Sızıntı sorusu ${i + 1}` });
  });
}

/* ---------- 6. Temel model ve eğriler ---------- */
{
  const s = icerik(6, 'Yaklaşık 1,5 dakika. Verinize uygun en basit modeli gösterin. Sınıflandırmada ROC, PR ve kalibrasyon; sinir ağı eğittiyseniz eğitim ve doğrulama eğrisi yan yana. Ölçütleri görevinize göre değiştirin. Yüksek sayı değil, doğru yorum puan getirir.');
  sekil(s, MX, 1.95, 6.6, 4.3, 'Eğriler\nROC / PR / kalibrasyon ya da\neğitim ve doğrulama eğrisi');
  s.addText('Şekil: Hangi model, hangi veri bölümü? (notebooks/02_model.ipynb)', { x: MX, y: 6.3, w: 6.6, h: 0.3, fontSize: 11, color: C.accent6, margin: 0, isTextBox: true, objectName: 'Alt yazı' });
  s.addText([
    { text: 'TEMEL MODEL', options: { fontSize: 12, bold: true, color: C.accent1, charSpacing: 1, breakLine: true } },
    { text: 'Model adı ve temel ayarları', options: { fontSize: 15, color: C.text2 } },
  ], { x: 7.6, y: 1.95, w: 5.1, h: 0.75, valign: 'top', margin: 0, paraSpaceAfter: 4, isTextBox: true, objectName: 'Model' });
  s.addTable(
    [[baslikHucre('Ölçüt'), baslikHucre('Eğitim'), baslikHucre('Doğrulama')],
      ...['AUROC', 'AUPRC', 'Brier skoru'].map((m) => [etiketHucre(m), hucre('0,00'), hucre('0,00')])],
    { x: 7.6, y: 2.85, w: 5.1, colW: [2.1, 1.5, 1.5], rowH: 0.5, border: kenar, objectName: 'Ölçüt tablosu' },
  );
  kart(s, 7.6, 5.1, 5.1, 1.5, 'YORUM', 'Eğriniz hangi tabloya benziyor: sağlıklı mı, ezberci mi, emekleyen mi?', { fill: C.accent4 });
}

/* ---------- 7. Sorunlar ve plan ---------- */
{
  const s = icerik(7, 'Yaklaşık 1,5 dakika. Üstteki şeritte her aşama için tek bir durumu bırakın, diğerlerini silin. Sorunları açıkça anlatın; takıldığınız yeri söylemek puan kaybettirmez. Planı tarihleriyle yazın (son rapor: 23 Aralık).');
  const asamalar = ['Veri', 'Keşif', 'Ön işleme', 'Doğrulama', 'Temel model', 'Açıklanabilirlik', 'Rapor'];
  const w = (W - 2 * MX - 6 * 0.15) / 7;
  asamalar.forEach((ad, i) => {
    s.addText([
      { text: ad, options: { fontSize: 14, bold: true, color: C.text1, breakLine: true } },
      { text: 'tamam / sürüyor / başlamadı', options: { fontSize: 10, color: C.text2 } },
    ], { x: MX + i * (w + 0.15), y: 1.95, w, h: 0.95, shape: pres.ShapeType.roundRect, rectRadius: 0.1, fill: { color: C.accent4 }, line: { type: 'none' }, align: 'center', valign: 'middle', margin: 4, isTextBox: true, objectName: `Aşama ${ad}` });
  });
  const w3 = (W - 2 * MX - 0.8) / 3;
  kart(s, MX, 3.25, w3, 3.4, 'KARŞILAŞTIĞIM SORUNLAR', 'Veri, kod, donanım ya da yöntem: sizi en çok ne uğraştırdı? En çok iki ya da üç madde.');
  kart(s, MX + w3 + 0.4, 3.25, w3, 3.4, 'NASIL ÇÖZDÜM', 'Çözdükleriniz ve hâlâ açık olanlar. Yardıma ihtiyaç duyduğunuz nokta varsa buraya yazın.', { fill: C.accent5, vurgu: C.accent2 });
  kart(s, MX + 2 * (w3 + 0.4), 3.25, w3, 3.4, 'SON RAPORA KADAR PLAN', 'Deneyeceğiniz model, kullanacağınız açıklanabilirlik yöntemi ve tarihleri.');
}

/* ---------- 8. Depo turu ---------- */
{
  const s = icerik(8, 'Yaklaşık 1 dakika. README ekran görüntüsünü yerleştirin ya da depoyu canlı açın. Sağdaki listede eksik olanı dürüstçe söyleyin. Depoda veri bulunmamalı; yalnızca veriyi indirme talimatı.');
  sekil(s, MX, 1.95, 6.6, 4.7, 'README ekran görüntüsü');
  s.addText([
    { text: 'DEPO', options: { fontSize: 12, bold: true, color: C.accent1, charSpacing: 1, breakLine: true } },
    { text: 'github.com/kullanici/depo', options: { fontSize: 18, bold: true, color: C.text1 } },
  ], { x: 7.6, y: 1.95, w: 5.1, h: 0.85, valign: 'top', margin: 0, paraSpaceAfter: 4, isTextBox: true, objectName: 'Depo adresi' });
  s.addTable(
    [[baslikHucre('Depoda ne var'), baslikHucre('Durum')],
      ...['README: proje, kurulum, çalıştırma', 'data/README: veriyi indirme talimatı', 'requirements.txt ve sabit tohum', 'Defterler baştan sona çalışıyor', 'sunum/ara-sunum.pdf'].map((m) => [hucre(m), hucre('var / yok')])],
    { x: 7.6, y: 3.0, w: 5.1, colW: [3.7, 1.4], rowH: 0.6, border: kenar, objectName: 'Depo listesi' },
  );
}

/* ---------- Kapanış ---------- */
{
  const s = pres.addSlide({ masterName: 'KAPANIS' });
  s.addText('Sorular', { placeholder: 'title' });
  s.addText([
    { text: 'Ad Soyad · BVYZ-00', options: { breakLine: true } },
    { text: 'github.com/kullanici/depo' },
  ], { placeholder: 'body' });
  kart(s, 8.2, 2.3, 4.5, 2.6, 'TEK CÜMLEYLE', 'Dinleyenin aklında kalmasını istediğiniz tek şeyi yazın.', { fill: C.accent1, vurgu: C.accent5, renk: C.background1, fontSize: 18 });
  s.addNotes('Kapanış. Beş dakika soru. "Bilmiyorum, şöyle bakarım" geçerli bir yanıttır. Teslim: Dosya > Dışa Aktar > PDF ile kaydedip deponuza sunum/ara-sunum.pdf olarak yükleyin (17 Kasım Salı gün sonuna kadar).');
}

(async () => {
  await pres.writeFile({ fileName: OUT });
  const tema = process.argv[2];
  if (tema) {
    const { applyTheme } = require(path.resolve(tema));
    await applyTheme(OUT, THEME);
  } else {
    console.warn('! apply_theme.js yolu verilmedi; tema renkleri Office varsayılanı kalır.');
  }
  console.log('✓ ' + path.relative(ROOT, OUT));
})();
