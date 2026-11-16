#!/usr/bin/env python3
"""
Password Maker - Güvenli şifre ve parola cümlesi üretici.

Kriptografik olarak güvenli rastgelelik için Python'un `secrets` modülünü kullanır.
"""

from __future__ import annotations

import argparse
import math
import secrets
import string
import sys

LOWER = string.ascii_lowercase
UPPER = string.ascii_uppercase
DIGITS = string.digits
SYMBOLS = "!@#$%^&*()-_=+[]{};:,.<>?/"
AMBIGUOUS = set("Il1O0o")

# Parola cümlesi (passphrase) için kısa, akılda kalıcı kelime listesi
WORDS = [
    "elma", "armut", "deniz", "bulut", "kalem", "kitap", "orman", "nehir",
    "dağ", "yıldız", "güneş", "ay", "rüzgar", "kartal", "aslan", "kaplan",
    "çiçek", "toprak", "ateş", "buz", "kum", "taş", "yol", "köprü",
    "kale", "kapı", "pencere", "masa", "sandalye", "lamba", "saat", "zil",
    "gemi", "tren", "uçak", "bisiklet", "balık", "kedi", "köpek", "kuş",
    "limon", "kiraz", "üzüm", "portakal", "çay", "kahve", "şeker", "tuz",
    "mavi", "yeşil", "kırmızı", "sarı", "mor", "beyaz", "siyah", "turuncu",
    "hızlı", "sessiz", "parlak", "derin", "yüksek", "eski", "yeni", "sıcak",
    "robot", "gezegen", "kuyruklu", "pusula", "harita", "fener", "çapa", "yelken",
    "bahar", "yaz", "güz", "kış", "sabah", "akşam", "gece", "şafak",
]


def build_pool(lower: bool, upper: bool, digits: bool, symbols: bool,
               no_ambiguous: bool) -> list[str]:
    """Seçilen karakter gruplarını döndürür (her biri ayrı string)."""
    groups = []
    if lower:
        groups.append(LOWER)
    if upper:
        groups.append(UPPER)
    if digits:
        groups.append(DIGITS)
    if symbols:
        groups.append(SYMBOLS)
    if no_ambiguous:
        groups = ["".join(c for c in g if c not in AMBIGUOUS) for g in groups]
    groups = [g for g in groups if g]
    if not groups:
        raise ValueError("En az bir karakter türü seçmelisin.")
    return groups


def generate_password(length: int = 16, lower: bool = True, upper: bool = True,
                      digits: bool = True, symbols: bool = True,
                      no_ambiguous: bool = False) -> str:
    """Her seçili gruptan en az bir karakter içeren rastgele şifre üretir."""
    groups = build_pool(lower, upper, digits, symbols, no_ambiguous)
    if length < len(groups):
        raise ValueError(
            f"Uzunluk en az {len(groups)} olmalı (seçili karakter türü sayısı)."
        )
    pool = "".join(groups)
    # Her gruptan bir karakter garanti et, kalanı tüm havuzdan seç
    chars = [secrets.choice(g) for g in groups]
    chars += [secrets.choice(pool) for _ in range(length - len(groups))]
    # Kriptografik olarak güvenli karıştırma (Fisher-Yates)
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]
    return "".join(chars)


def generate_passphrase(words: int = 4, separator: str = "-",
                        capitalize: bool = False, add_number: bool = False) -> str:
    """Kelime listesinden rastgele parola cümlesi üretir."""
    if words < 1:
        raise ValueError("Kelime sayısı en az 1 olmalı.")
    chosen = [secrets.choice(WORDS) for _ in range(words)]
    if capitalize:
        chosen = [w.capitalize() for w in chosen]
    if add_number:
        chosen.append(str(secrets.randbelow(100)))
    return separator.join(chosen)


def entropy_bits(password: str) -> float:
    """Şifrenin içerdiği karakter türlerine göre yaklaşık entropiyi hesaplar."""
    size = 0
    if any(c in LOWER for c in password):
        size += len(LOWER)
    if any(c in UPPER for c in password):
        size += len(UPPER)
    if any(c in DIGITS for c in password):
        size += len(DIGITS)
    if any(c in SYMBOLS for c in password):
        size += len(SYMBOLS)
    other = {c for c in password if c not in LOWER + UPPER + DIGITS + SYMBOLS}
    size += len(other)
    if size == 0:
        return 0.0
    return len(password) * math.log2(size)


def strength_label(bits: float) -> str:
    if bits < 40:
        return "Zayıf"
    if bits < 60:
        return "Orta"
    if bits < 80:
        return "Güçlü"
    return "Çok güçlü"


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(
        prog="password_maker",
        description="Güvenli şifre ve parola cümlesi üretici.",
    )
    p.add_argument("-l", "--length", type=int, default=16,
                   help="Şifre uzunluğu (varsayılan: 16)")
    p.add_argument("-n", "--count", type=int, default=1,
                   help="Kaç şifre üretilsin (varsayılan: 1)")
    p.add_argument("--no-lower", action="store_true", help="Küçük harf kullanma")
    p.add_argument("--no-upper", action="store_true", help="Büyük harf kullanma")
    p.add_argument("--no-digits", action="store_true", help="Rakam kullanma")
    p.add_argument("--no-symbols", action="store_true", help="Sembol kullanma")
    p.add_argument("--no-ambiguous", action="store_true",
                   help="Karışabilen karakterleri çıkar (I, l, 1, O, 0, o)")
    p.add_argument("-p", "--passphrase", action="store_true",
                   help="Şifre yerine kelimelerden parola cümlesi üret")
    p.add_argument("-w", "--words", type=int, default=4,
                   help="Parola cümlesindeki kelime sayısı (varsayılan: 4)")
    p.add_argument("-s", "--separator", default="-",
                   help="Kelime ayırıcı (varsayılan: -)")
    p.add_argument("--capitalize", action="store_true",
                   help="Kelimelerin ilk harfini büyüt")
    p.add_argument("--add-number", action="store_true",
                   help="Parola cümlesinin sonuna sayı ekle")
    p.add_argument("--show-strength", action="store_true",
                   help="Her şifrenin gücünü göster")
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    if args.count < 1:
        print("Hata: --count en az 1 olmalı.", file=sys.stderr)
        return 2
    try:
        for _ in range(args.count):
            if args.passphrase:
                pw = generate_passphrase(args.words, args.separator,
                                         args.capitalize, args.add_number)
            else:
                pw = generate_password(
                    length=args.length,
                    lower=not args.no_lower,
                    upper=not args.no_upper,
                    digits=not args.no_digits,
                    symbols=not args.no_symbols,
                    no_ambiguous=args.no_ambiguous,
                )
            if args.show_strength:
                if args.passphrase:
                    bits = args.words * math.log2(len(WORDS))
                else:
                    bits = entropy_bits(pw)
                print(f"{pw}  [{strength_label(bits)} · ~{bits:.0f} bit]")
            else:
                print(pw)
    except ValueError as e:
        print(f"Hata: {e}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
