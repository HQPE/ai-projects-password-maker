# 🔐 AI Projects · Password Maker

Güvenli şifre ve parola cümlesi (passphrase) üreten basit bir araç. İki şekilde kullanılabilir:

- **Web sürümü** (`index.html`): Tarayıcıda çalışır, kurulum gerektirmez. GitHub Pages ile yayınlanabilir.
- **Komut satırı sürümü** (`password_maker.py`): Python 3.8+ ile çalışır, ek paket gerektirmez.

## ✨ Özellikler

- Kriptografik olarak güvenli rastgelelik (Python `secrets`, tarayıcıda `crypto.getRandomValues`)
- Uzunluk ve karakter türü seçimi (küçük/büyük harf, rakam, sembol)
- Seçilen her türden en az bir karakter garantisi
- Karışabilen karakterleri (`I l 1 O 0 o`) çıkarma seçeneği
- Türkçe kelimelerle akılda kalıcı parola cümlesi üretme
- Şifre gücü göstergesi (entropi hesabı)
- Tek tıkla kopyalama (web)

## 🌐 Web sürümü

`index.html` dosyasını tarayıcıda açman yeterli.

GitHub Pages ile yayınlamak için: repo **Settings → Pages → Branch: `main` / root → Save**.
Birkaç dakika sonra `https://hqpe.github.io/ai-projects-password-maker/` adresinde açılır.

## 💻 Komut satırı kullanımı

```bash
python password_maker.py                      # 16 karakterlik şifre
python password_maker.py -l 24 -n 5           # 24 karakterlik 5 şifre
python password_maker.py --no-symbols         # sembolsüz
python password_maker.py --no-ambiguous       # karışan karakterler olmadan
python password_maker.py -p                   # parola cümlesi: kedi-deniz-fener-bahar
python password_maker.py -p -w 5 --capitalize --add-number
python password_maker.py --show-strength      # güç bilgisiyle
```

| Seçenek | Açıklama |
|---|---|
| `-l, --length` | Şifre uzunluğu (varsayılan 16) |
| `-n, --count` | Üretilecek şifre sayısı |
| `--no-lower` / `--no-upper` / `--no-digits` / `--no-symbols` | İlgili karakter türünü çıkarır |
| `--no-ambiguous` | `I l 1 O 0 o` karakterlerini çıkarır |
| `-p, --passphrase` | Kelimelerden parola cümlesi üretir |
| `-w, --words` | Parola cümlesindeki kelime sayısı |
| `-s, --separator` | Kelime ayırıcı (varsayılan `-`) |
| `--capitalize` | Kelimelerin ilk harfini büyütür |
| `--add-number` | Sona 0–99 arası sayı ekler |
| `--show-strength` | Güç ve entropi bilgisini gösterir |

## 🧪 Testler

```bash
python -m unittest discover tests
```

## 📁 Proje yapısı

```
ai-projects-password-maker/
├── index.html              # Web sürümü
├── password_maker.py       # Komut satırı aracı
├── tests/
│   └── test_password_maker.py
├── README.md
├── LICENSE
└── .gitignore
```

## 📄 Lisans

MIT
