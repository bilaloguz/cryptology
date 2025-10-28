Kriptoloji – Klasik Şifreler (TR)

Özet
- Python ve C ikili dil/çalışma zamanı desteği
- Bileşen‑tabanlı anahtar/kare/tablo sistemine odaklı klasik şifreler
- Alfabeler: İngilizce ve Türkçe (Standart ve Genişletilmiş), tümü küçük harf ve UTF‑8

Alfabeler ve Normalizasyon
- İngilizce: 26 harf
- Türkçe Standart: 29 harf (ç ğ ı ö ş ü)
- Türkçe Genişletilmiş: 32 harf (+ q w x)
- Giriş/çıkış küçük harfe normalize edilir; boşluk/noktalama çoğu şifrede ayıklanır
- Türkçe karakterler Python ve C tarafında korunur (UTF‑8)

Kare/Küp/Tablo Üretimi (Bileşen Sistem)
- Monoalfabetik üreticiler (Sezar/Atbash/Affine/Anahtar/Özel) ile:
  - Polybius kareleri (5×5 EN, 6×6 TR)
  - Trifid küpleri (3×3×3 EN; 3×3×4 TR)
  - Polialfabetik tablolar (tabula recta)
- Özel (custom): kendi alfabenizi verin; boyuta ulaşmak için sadece doldurma/kısaltma yapılır, Türkçe harfler asla değiştirilmez

Birleştirme Kuralları
- İngilizce 5×5 Polybius ailesi (Playfair, Bifid, Two-/Four-Square, Nihilist, ADFGX): i/j birleştirilir
- Türkçe 6×6: birleştirme yok, değiştirme yok
- Trifid: EN’de j→i (26→27); TR’de 3×3×4; Türkçe harfler korunur

Şifre Kataloğu ve Anahtar Malzemesi
Yerine Koyma – Monoalfabetik
- Sezar, Atbash, Anahtar (Keyword), Affine, ROT13

Yerine Koyma – Polialfabetik
- Vigenère: produce_table ile tabula recta (26×26 EN, 29×29 TR); rastgele anahtar seçeneği
- Beaufort: Vigenère tablosunu kullanır; öz‑karşılıklı testler
- Auto‑key: tablo yeniden kullanımı; otomatik anahtar akışı
- Porta: eşleştirme stratejisi; mono‑tabanlı eşleştirme; Türkçe desteklenir
- Gronsfeld: sayısal anahtar kaydırmaları
- Reihenschieber: kaydırma yönü (ileri/geri), tekrar, ilerlemeli/özel modlar
- Chaocipher: sol/sağ alfabeler mono üreticilerle tanımlanır

Yerine Koyma – Polygraphic / Kesirlemeli
- Playfair: 5×5 EN; 6×6 TR (Türkçe harfler tam korunur), dinamik dolgu
- Bifid: Polybius (5×5 EN, 6×6 TR); düzeltilmiş defraksiyon
- Trifid: blok/periyot temelli kesirleme (varsayılan periyot 5); küp boyutları yukarıda
- Two‑Square / Four‑Square: anahtar/özel kareler; EN 5×5, TR 6×6

Yer Değiştirme
- Basit: Scytale, Raylı Çit (Rail Fence)
- Sütunlu: Tek, Çift, Bozuntulu, Myszkowski
- Rota/Yol: Spiral, Boustrophedon, Atın L‑Hareketi
- Bileşik: Rasterschlüssel 44
- Tüm yer değiştirmeler Türkçe’yi destekler (C’de UTF‑8 yardımcıları)

Bileşik
- Basamaklı Kontrol Tablosu (Straddling Checkerboard): produce_checkerboard (Sıklık EN/TR, Alfabetik, Ünlü–Ünsüz, Özel)
- Nihilist: Polybius seçenekleri (Standart, Anahtar, Özel, Sezar, Atbash, Affine) – EN 5×5, TR 6×6
- ADFGVX/ADFGVZX: Polybius 6×6; aynı mono seçenekleri; Türkçe destek
- VIC: Çok aşamalı (Polybius, Kesirleme, Kontrol Tablosu, Sütunlu, Sayısal/Chain ekleme); rastgele anahtar

Özel Kare/Tablo/Küp
- square_type="custom", mono_params={"alphabet": "<alfabeniz>"}
- Verdiğiniz alfabe doldurma sırası olarak kullanılır; sadece hedef boyuta ulaşmak için doldurma/kısaltma yapılır
- İngilizce 5×5 i/j birleştirme sadece standart İngilizce yolunda; özel (custom) verildiğinde aynen korunur

Test ve Doğrulama
- Kapsamlı testler: tüm şifreler EN/TR/TRX
- Roundtrip (şifrele→çöz) normalize edilmiş açık metne eşit olmalı
- Trifid: periyot temelli; EN 3×3×3, TR/TRX 3×3×4 doğrulandı

Python/C Paralelliği
- Ortak tasarım kararları iki tarafta da uygulanır
- C tarafında Türkçe için UTF‑8 karakter sayımı ve erişim yardımcıları kullanılır

Örnek (Python)
```python
from cryptology.classical.substitution.fractionated import trifid
import cryptology.alphabets as A

pt = "pijamalı hasta yağız şoföre çabucak güvendi"
ct = trifid.encrypt(pt, key="test", alphabet=A.TURKISH_ALPHABET)
rt = trifid.decrypt(ct, key="test", alphabet=A.TURKISH_ALPHABET)
assert ''.join(c for c in pt.lower() if c.isalpha() or c in 'çğıöşüı') \
    == ''.join(c for c in rt.lower() if c.isalpha() or c in 'çğıöşüı')
```

Notlar
- Girişler küçük harf olmalı; Türkçe korunur; boşluk ayıklama şifre kurallarına göre değişir
- 5×5 İngilizce karelerde i/j birleştiği için test metninde ‘j’ kullanmaktan kaçınmak pratikte faydalıdır; Türkçe için gerek yok


