#!/usr/bin/env python
"""Site görsellerini üretir: public/og.png (1200×630) ve public/apple-touch-icon.png (180×180).

Tasarım sistemiyle aynı renkler kullanılır; yazı tipi olarak sistemde bulunan bir sans-serif seçilir.
Kullanım: /opt/miniconda3/envs/ferhat_ml/bin/python scripts/make_assets.py
"""
import json
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
course = json.loads((ROOT / "content" / "data" / "course.json").read_text(encoding="utf-8"))
PUB = ROOT / "public"

INK, PAPER, BRAND, ACCENT, INK3, LINE = "#0b1526", "#f5f7fb", "#2f3fa3", "#0f9b8e", "#6b7a92", "#d9dfeb"


def font(size, bold=False):
    cands = [
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf" if bold else "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
    ]
    for c in cands:
        if Path(c).exists():
            return ImageFont.truetype(c, size)
    return ImageFont.load_default()


def signal(draw, x0, y, w, color, width=5):
    """Basit EKG benzeri çizgi."""
    pts = [(x0, y), (x0 + w * .18, y), (x0 + w * .22, y - 14), (x0 + w * .26, y + 10), (x0 + w * .30, y),
           (x0 + w * .34, y), (x0 + w * .37, y - 90), (x0 + w * .40, y + 60), (x0 + w * .43, y),
           (x0 + w * .60, y), (x0 + w * .66, y - 22), (x0 + w * .72, y), (x0 + w, y)]
    draw.line(pts, fill=color, width=width, joint="curve")


def og():
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(im)
    for x in range(0, W, 22):          # nokta ızgarası
        for yy in range(0, H, 22):
            if (x + yy) % 44 == 0:
                d.ellipse([x, yy, x + 2, yy + 2], fill="#dfe4ee")
    d.rectangle([0, 0, W, 8], fill=ACCENT)
    d.text((72, 64), f"{course['code']}  ·  {course['university']} {course['faculty']}", font=font(24), fill=INK3)
    title_font = font(64, bold=True)
    d.text((72, 120), "Biyomedikal Verilerin", font=title_font, fill=INK)
    d.text((72, 196), "Analizi ve Yapay Zeka", font=title_font, fill=BRAND)
    d.text((72, 300), "Makine öğrenmesi · Derin öğrenme · Açıklanabilir YZ (XAI)", font=font(28), fill=INK3)
    d.text((72, 344), f"{course['semester']} · Lisansüstü · {course['credits']['ects']} AKTS", font=font(24), fill=INK3)
    # sinyal → düğüm → çubuklar
    signal(d, 72, 500, 520, ACCENT, 6)
    for i, (cx, cy) in enumerate([(680, 460), (680, 500), (680, 540), (760, 480), (760, 520), (840, 500)]):
        d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], outline=BRAND, width=3, fill=PAPER if i < 5 else BRAND)
    for a in [(680, 460), (680, 500), (680, 540)]:
        for b in [(760, 480), (760, 520)]:
            d.line([a, b], fill="#c9d1e3", width=2)
    for b in [(760, 480), (760, 520)]:
        d.line([b, (840, 500)], fill="#c9d1e3", width=2)
    for i, w in enumerate([120, 84, 50, -40, -22]):
        y = 440 + i * 30
        color = ACCENT if w > 0 else "#be3a5a"
        d.rectangle([960 + min(0, w), y, 960 + max(0, w), y + 18], fill=color)
    d.line([(960, 430), (960, 590)], fill=LINE, width=2)
    d.text((72, 576), course["instructor"]["name"], font=font(22), fill=INK3)
    im.save(PUB / "og.png", optimize=True)
    print("✓ public/og.png")


def touch_icon():
    S = 180
    im = Image.new("RGB", (S, S), INK)
    d = ImageDraw.Draw(im)
    signal(d, 22, 100, 118, PAPER, 11)
    d.ellipse([136, 86, 164, 114], fill=ACCENT)
    im.save(PUB / "apple-touch-icon.png", optimize=True)
    print("✓ public/apple-touch-icon.png")


if __name__ == "__main__":
    og()
    touch_icon()
