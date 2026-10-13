#!/usr/bin/env python
"""Yoklama listesindeki öğrencilere dönem projelerini atar ve content/data/projects.json üretir.

Gizlilik: Siteye ne isim ne numara ne de açık proje bilgisi yazılır. Her kartın içeriği
(maskeli isim, başlık, veri seti, adımlar...) öğrenci numarasından PBKDF2 ile türetilen anahtarla
AES-256-GCM kullanılarak şifrelenir; sayfada yalnızca şifreli metin bulunur. Öğrenci "Projemi bul"
kutusuna numarasını yazar, tarayıcı aynı anahtarı türetir ve yalnızca kendi kartını çözebilir.
Kaynak görüntüleme ("incele") ile diğer kartlar okunamaz.

Yerel kayıt: Yoklama/projeler-atama.json (açık liste, depoya girmez) öğretim üyesi içindir.

Atama deterministiktir: öğrenciler numaraya göre sıralanır, havuzdaki projeler sırayla verilir.
Belirli bir öğrenciye belirli projeyi vermek için OVERRIDES sözlüğünü kullanın.

Kullanım:
  /opt/miniconda3/envs/ferhat_ml/bin/python scripts/assign_projects.py "Yoklama/DersKatilim_SON.xlsx"
"""
import base64
import hashlib
import json
import os
import re
import sys
from pathlib import Path

import pandas as pd
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "content" / "data" / "projects.json"
SALT = "SVY5430-2026"          # src/pages/proje.astro içindeki değerle aynı olmalı
KDF_ITER = 300_000             # PBKDF2 tur sayısı; proje.astro ile aynı olmalı
OVERRIDES: dict[str, str] = {}  # {"261137101": "P3"} gibi

POOL = [
  dict(id="P1", code="BVYZ-01", dataType="Klinik tablo", title="Kalp yetmezliğinde ölüm riski tahmini",
       dataset="Heart Failure Clinical Records (UCI)", url="https://archive.ics.uci.edu/dataset/519/heart+failure+clinical+records",
       size="299 hasta · 12 öznitelik · 1 ikili hedef", access="Açık; tek CSV, doğrudan indirilir",
       task="İkili sınıflandırma: takip süresi içinde ölüm olayı",
       question="Serum kreatinin, ejeksiyon fraksiyonu ve diğer klinik değişkenlerden kalp yetmezliği hastasının ölüm riski tahmin edilebilir mi, hangi değişkenler kararı belirliyor?",
       steps=["Eksik yok ama 'time' (takip süresi) değişkeni sızıntı tartışması gerektirir: modele verilmeli mi?",
              "Lojistik regresyon temel model; Random Forest ve XGBoost ile karşılaştırma; iç içe çapraz doğrulama.",
              "ROC ve kalibrasyon eğrileri, Brier; eşiği klinik maliyetle seçin.",
              "SHAP özet ve iki hasta için şelale grafiği; serum kreatinin–ejeksiyon fraksiyonu etkileşimi."],
       pitfalls="Küçük veri: güven aralıklarını (bootstrap) raporlayın. 'time' sızıntısına dikkat.",
       refs=["Chicco D, Jurman G. BMC Med Inform Decis Mak 2020 (bu veri setinin özgün makalesi)"]),
  dict(id="P2", code="BVYZ-02", dataType="Elektronik sağlık kaydı", title="Diyabet hastalarında 30 gün içinde yeniden yatış",
       dataset="Diabetes 130-US Hospitals 1999–2008 (UCI)", url="https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008",
       size="~100.000 yatış · ~50 öznitelik", access="Açık; ZIP içinde CSV",
       task="İkili sınıflandırma: <30 gün yeniden yatış (dengesiz sınıf)",
       question="Yatış özelliklerinden, ilaç değişikliklerinden ve demografiden 30 gün içinde yeniden yatış öngörülebilir mi; model farklı ırk ve cinsiyet gruplarında eşit mi çalışıyor?",
       steps=["Aynı hasta birden çok yatışla görünür: GroupKFold(patient_nbr) zorunlu.",
              "Yüksek kardinaliteli kategoriler (tanı kodları) için gruplama; dengesiz sınıf için ağırlık ve eşik.",
              "PR-AUC ve kalibrasyon; alt-grup (ırk, cinsiyet, yaş) başarımı tablosu.",
              "SHAP ile küresel önem; adalet metrikleri (eşit fırsat farkı)."],
       pitfalls="Büyük veri: Colab'de bellek için gerekirse örneklem alın ama bunu raporda belirtin.",
       refs=["Strack B ve ark. BioMed Res Int 2014", "Obermeyer Z ve ark. Science 2019 (adalet tartışması için)"]),
  dict(id="P3", code="BVYZ-03", dataType="Biyomedikal sinyal (EKG)", title="EKG atımlarından aritmi sınıflandırması",
       dataset="MIT-BIH Arrhythmia Database (PhysioNet)", url="https://physionet.org/content/mitdb/1.0.0/",
       size="48 kayıt · ~110.000 etiketli atım", access="Açık; `wfdb` kütüphanesiyle doğrudan indirilir",
       task="Çok sınıflı sınıflandırma: normal / SVEB / VEB / füzyon (AAMI sınıfları)",
       question="Tek atım penceresinden (R tepesi etrafı) ve RR aralığı özniteliklerinden ventriküler ve supraventriküler ektopik atımlar güvenilir biçimde ayrılabilir mi; kayıt-bazlı bölmede başarım ne kadar düşüyor?",
       steps=["0.5–40 Hz filtre, R tepe tespiti (anotasyonlar hazır), atım penceresi ve RR öznitelikleri.",
              "Kayıt-içi rastgele bölme ile kayıt-bazlı (GroupKFold) bölmeyi karşılaştırın; farkı raporun ana bulgusu yapın.",
              "Random Forest / XGBoost; isteğe bağlı 1D-CNN (9–11. hafta).",
              "Sınıf başına duyarlılık; karışıklık matrisi; permütasyon önemi ile hangi öznitelikler."],
       pitfalls="AAMI sınıf dengesizliği çok yüksek; makro-F1 raporlayın. Hastalar arası genelleme asıl soru.",
       refs=["Moody GB, Mark RG. IEEE Eng Med Biol 2001", "de Chazal P ve ark. IEEE TBME 2004"]),
  dict(id="P4", code="BVYZ-04", dataType="Biyomedikal sinyal (PPG)", title="PPG sinyalinden solunum hızı kestirimi",
       dataset="BIDMC PPG and Respiration Dataset (PhysioNet)", url="https://physionet.org/content/bidmc/1.0.0/",
       size="53 kayıt · 8 dk · PPG, EKG, solunum referansı", access="Açık; `wfdb` ile indirilir",
       task="Regresyon: dakikadaki solunum sayısı (referans: impedans solunum sinyali)",
       question="Parmaktan alınan PPG sinyalindeki solunum kaynaklı dalgalanmalardan solunum hızı, referans ölçümle klinik olarak kabul edilebilir hata payında kestirilebilir mi?",
       steps=["PPG'den solunum kaynaklı üç bileşen (genlik, frekans, taban çizgisi modülasyonu) çıkarımı; 32 s pencereler.",
              "Spektral tepe (klasik yöntem) ile öznitelik-temelli regresyon (Random Forest / gradyan artırma) karşılaştırması.",
              "Kayıt-bazlı çapraz doğrulama; MAE, Bland–Altman grafiği.",
              "Hangi pencerelerde hata büyük? Sinyal kalitesi indeksiyle ilişkilendirin."],
       pitfalls="Pencereler aynı kayıttan gelir; GroupKFold(kayıt) olmadan sonuç şişer.",
       refs=["Pimentel MAF ve ark. IEEE TBME 2017", "Charlton PH ve ark. Physiol Meas 2016"]),
  dict(id="P5", code="BVYZ-05", dataType="Tıbbi görüntü", title="Göğüs röntgeninde pnömoni tespiti ve modelin baktığı yer",
       dataset="PneumoniaMNIST (MedMNIST v2)", url="https://medmnist.com/",
       size="5.856 görüntü · 28×28 (isteğe bağlı 64/128 px) · 2 sınıf", access="Açık; `pip install medmnist` ile indirilir",
       task="İkili görüntü sınıflandırma + Grad-CAM ile görsel açıklama",
       question="Küçük bir CNN ve ImageNet ön-eğitimli bir ağ pnömoniyi ne kadar iyi ayırıyor; Grad-CAM haritaları akciğer alanına mı, yoksa görüntü kenarlarındaki ipuçlarına mı bakıyor?",
       steps=["Sıfırdan küçük CNN ile ResNet-18 transfer öğrenme karşılaştırması; veri artırmanın etkisi.",
              "Hazır eğitim/doğrulama/test bölmesini kullanın; test kümesine yalnızca bir kez bakın.",
              "ROC-AUC, duyarlılık/özgüllük, kalibrasyon; sınıf dengesizliğine dikkat.",
              "Grad-CAM (Captum ya da pytorch-grad-cam); doğru ve yanlış sınıflanan 8 örnek için ısı haritası."],
       pitfalls="Colab GPU'yu açın. 28×28 çözünürlükte Grad-CAM kaba olur; 64 px sürümünü tercih edin.",
       refs=["Yang J ve ark. Sci Data 2023 (MedMNIST v2)", "Selvaraju RR ve ark. ICCV 2017 (Grad-CAM)"]),
  dict(id="P6", code="BVYZ-06", dataType="Klinik tablo (yoğun eksik veri)", title="Serviks kanseri risk faktörleri ve biyopsi sonucu",
       dataset="Cervical Cancer (Risk Factors) (UCI)", url="https://archive.ics.uci.edu/dataset/383/cervical+cancer+risk+factors",
       size="858 hasta · 36 öznitelik · 4 hedef (Hinselmann, Schiller, sitoloji, biyopsi)", access="Açık; tek CSV ('?' = eksik)",
       task="İkili sınıflandırma (biyopsi) — eksik veri mekanizması ve kalibrasyon odaklı",
       question="Hastaların cevaplamadığı (eksik) sorular rastgele mi; eksikliğin kendisi riskle ilişkili mi? Bu yapı altında kalibre ve dürüst bir risk modeli kurulabilir mi?",
       steps=["Eksiklik deseni analizi (hangi sütunlar birlikte eksik, hedefle ilişkisi); MCAR/MAR/MNAR tartışması.",
              "Göstergeli ve göstergesiz imputasyonun Pipeline içinde karşılaştırması.",
              "Pozitif oranı çok düşük: PR-AUC, kalibrasyon, karar eğrisi analizi.",
              "SHAP ile eksiklik göstergelerinin katkısı; etik tartışma (hassas sorular)."],
       pitfalls="Çok nadir pozitif (~%6): bootstrap güven aralığı şart. Dört hedef var; birini seçip gerekçelendirin.",
       refs=["Fernandes K ve ark. 2017 (veri setinin kaynağı)", "Sterne JAC ve ark. BMJ 2009 (çoklu imputasyon)"]),
  dict(id="P7", code="BVYZ-07", dataType="Omik (RNA-Seq)", title="Gen ifadesinden kanser tipi sınıflandırması: p ≫ n",
       dataset="Gene Expression Cancer RNA-Seq / TCGA PANCAN (UCI)", url="https://archive.ics.uci.edu/dataset/401/gene+expression+cancer+rna+seq",
       size="801 örnek · 20.531 gen · 5 kanser tipi", access="Açık; ZIP içinde CSV (~200 MB)",
       task="Çok sınıflı sınıflandırma + boyut indirgeme ve özellik seçimi",
       question="Yirmi bin genden beş kanser tipi ayrılabilir mi ve bunu kaç genle yapabiliriz; özellik seçimi çapraz doğrulamanın dışında yapıldığında sonuç ne kadar şişiyor?",
       steps=["PCA açıklanan varyans ve UMAP haritası; kümeler kanser tipiyle örtüşüyor mu?",
              "Özellik seçimi (varyans filtresi + SelectKBest / L1-lojistik) Pipeline içinde; dışında yapıldığında farkı gösterin (2. hafta deneyi).",
              "Lojistik regresyon (L1), Random Forest; makro-F1 ve karışıklık matrisi.",
              "Seçilen genlerin biyolojik anlamı: literatürde bilinen belirteçler mi?"],
       pitfalls="Bellek: CSV'yi float32 olarak okuyun. 801 örnekte 20 bin gen; sızıntı en büyük risk.",
       refs=["Weinstein JN ve ark. Nat Genet 2013 (TCGA PANCAN)", "Guyon I, Elisseeff A. JMLR 2003 (özellik seçimi)"]),
]


def mask_name(name: str) -> str:
    parts = re.split(r"\s+", name.strip())
    return " ".join(p[0] + "*" * max(len(p) - 1, 1) for p in parts if p)


def key_for(number: str) -> bytes:
    """Tarayıcıdaki Web Crypto ile birebir aynı türetme: PBKDF2-HMAC-SHA256(parola=numara, tuz=SALT)."""
    return hashlib.pbkdf2_hmac("sha256", number.encode(), SALT.encode(), KDF_ITER, dklen=32)


def encrypt(payload: dict, number: str) -> dict:
    iv = os.urandom(12)
    ct = AESGCM(key_for(number)).encrypt(iv, json.dumps(payload, ensure_ascii=False).encode(), None)
    return {"iv": base64.b64encode(iv).decode(), "ct": base64.b64encode(ct).decode()}


def read_students(xlsx: Path) -> list[tuple[str, str]]:
    df = pd.read_excel(xlsx, header=None)
    rows = []
    for _, r in df.iterrows():
        vals = [str(v).strip() for v in r.tolist() if str(v) != "nan"]
        num = next((v for v in vals if re.fullmatch(r"\d{9}", v)), None)
        if not num:
            continue
        i = vals.index(num)
        name = vals[i + 1] if i + 1 < len(vals) else ""
        rows.append((num, name))
    return sorted(rows)


def main():
    xlsx = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "Yoklama" / "DersKatilim_SON.xlsx"
    students = read_students(xlsx)
    if not students:
        sys.exit("Öğrenci bulunamadı")
    if len(students) > len(POOL):
        sys.exit(f"{len(students)} öğrenci için {len(POOL)} proje var; POOL'u genişletin")
    pool_by_id = {p["id"]: p for p in POOL}
    used = set(OVERRIDES.values())
    free = [p["id"] for p in POOL if p["id"] not in used]
    out, local = [], []
    for num, name in students:
        pid = OVERRIDES.get(num) or free.pop(0)
        p = dict(pool_by_id[pid])
        p["student"] = mask_name(name)
        out.append({"id": pid, **encrypt(p, num)})
        local.append({"ogrenci_no": num, "ad": name, **p})
        print(f"{pid}  {mask_name(name):22s}  {p['title']}")
    OUT.write_text(json.dumps({"salt": SALT, "iter": KDF_ITER, "projects": out}, ensure_ascii=False, indent=2), encoding="utf-8")
    loc = xlsx.parent / "projeler-atama.json"
    loc.write_text(json.dumps(local, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n✓ {OUT.relative_to(ROOT)} ({len(out)} şifreli kart)\n✓ {loc} (açık liste, yalnızca yerel)")


if __name__ == "__main__":
    main()
