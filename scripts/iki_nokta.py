"""İki noktadan sonra küçük harfle başlayan yerleri listeler ya da düzeltir.

Kullanım:
  python scripts/iki_nokta.py liste DOSYA...            # adayları numaralı listeler
  python scripts/iki_nokta.py duzelt DOSYA --atla 3,7   # atlananlar dışındakileri büyütür
  python scripts/iki_nokta.py duzelt DOSYA --yalniz 1,4 # yalnızca verilenleri büyütür
"""
import re
import sys

KUCUK = "abcçdefgğhıijklmnoöprsştuüvyzqwx"
DESEN = re.compile(r": ([" + KUCUK + r"])")
YAML_ANAHTAR = re.compile(r"^\s*(- )?[A-Za-z_]+:\s")
KOD = re.compile(r"^\s*(const|let|var|if|for|function|return|import|export|//|/\*|\*|<|\.|@|\}|\{)|[;{]\s*$|=>|\bclass=|^\s*[a-z-]+: [^.]*;$")


def buyut(h):
    return {"i": "İ", "ı": "I"}.get(h, h.upper())


def adaylar(yol):
    with open(yol, encoding="utf-8") as f:
        satirlar = f.read().split("\n")
    sonuc = []
    for no, satir in enumerate(satirlar):
        anahtar = YAML_ANAHTAR.match(satir)
        for m in DESEN.finditer(satir):
            if anahtar and m.start() < anahtar.end():
                continue
            sonuc.append((no, m.start(1)))
    return satirlar, sonuc


def main():
    kip, args = sys.argv[1], sys.argv[2:]
    if kip == "liste":
        for yol in args:
            satirlar, a = adaylar(yol)
            for i, (no, k) in enumerate(a):
                s = satirlar[no]
                print(f"{yol.split('/')[-1]}#{i} L{no + 1}: …{s[max(0, k - 45):k + 40]}…")
    elif kip == "duzelt":
        yol = args[0]
        atla = set()
        if "--atla" in args:
            deger = args[args.index("--atla") + 1]
            atla = {int(x) for x in deger.split(",") if x}
        satirlar, a = adaylar(yol)
        if "--yalniz" in args:
            deger = args[args.index("--yalniz") + 1]
            sec = {int(x) for x in deger.split(",") if x}
            atla = set(range(len(a))) - sec
        n = 0
        for i, (no, k) in enumerate(a):
            if i in atla:
                continue
            s = satirlar[no]
            satirlar[no] = s[:k] + buyut(s[k]) + s[k + 1:]
            n += 1
        with open(yol, "w", encoding="utf-8") as f:
            f.write("\n".join(satirlar))
        print(f"{yol}: {n} düzeltme, {len(atla)} atlandı")


if __name__ == "__main__":
    main()
