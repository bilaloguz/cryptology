Cryptology – Classical Ciphers (EN)

Overview
- Dual-language, dual-runtime cryptology toolkit (Python and C)
- Focus: classical ciphers with a composable key/square/table system
- Alphabets: English and Turkish (Standard and Extended), all lowercase, UTF‑8 safe

Alphabets and Normalization
- English: 26 letters (lowercase)
- Turkish Standard: 29 letters (ç ğ ı ö ş ü included)
- Turkish Extended: 32 letters (+ q w x)
- All I/O normalized to lowercase; spaces/punctuation typically omitted by cipher rules
- UTF‑8 preserved for Turkish across Python and C

Square/Cube/Table Formation (Composable System)
- Monoalphabetic producers (Caesar/Atbash/Affine/Keyword/Custom) can create:
  - Polybius squares (5×5 EN, 6×6 TR)
  - Trifid cubes (3×3×3 EN; 3×3×4 TR)
  - Polyalphabetic tables (tabula recta)
- Custom option: supply your alphabet; system pads/truncates to target size without replacing Turkish letters

Letter Combination Rules
- English 5×5 Polybius family (Playfair, Bifid, Two-/Four-Square, Nihilist, ADFGX): combine i/j
- Turkish 6×6: no letter combinations, no replacements
- Trifid: EN maps j→i (26→27), TR uses 3×3×4 cube; no Turkish replacements

Cipher Catalog and Key Material
Substitution – Monoalphabetic
- Caesar, Atbash, Keyword, Affine, ROT13

Substitution – Polyalphabetic
- Vigenère: tabula recta via produce_table (26×26 EN, 29×29 TR); random key available
- Beaufort: reuses Vigenère table; self‑reciprocal tests
- Auto‑key: table reuse; auto‑key stream logic
- Porta: pairing strategy; supports mono‑based pairing; Turkish supported
- Gronsfeld: numeric key shifts
- Reihenschieber: shift direction (forward/backward), repetition, progressive/custom shifts
- Chaocipher: user‑defined left/right alphabets via mono producers

Substitution – Polygraphic/Fractionated
- Playfair: 5×5 EN; 6×6 TR preserves all Turkish; dynamic padding
- Bifid: Polybius square (5×5 EN, 6×6 TR); corrected defractionation
- Trifid: block/period‑based fractionation (default period 5); cube sizes above
- Two‑Square / Four‑Square: keyword/custom squares; EN 5×5, TR 6×6

Transposition
- Simple: Scytale, Rail Fence
- Columnar: Single, Double, Disrupted, Myszkowski
- Route/Path: Spiral Route, Boustrophedon, Knight’s Move
- Compound: Rasterschlüssel 44
- All transpositions support Turkish (UTF‑8 helpers in C)

Composite
- Straddling Checkerboard: produce_checkerboard (Frequency EN/TR, Alphabetical, Vowel–Consonant, Custom)
- Nihilist: Polybius options (Standard, Keyword, Custom, Caesar, Atbash, Affine) – EN 5×5, TR 6×6
- ADFGVX/ADFGVZX: Polybius 6×6; same mono options; Turkish supported
- VIC: Multi‑stage (Polybius, Fractionation, Checkerboard, Columnar, Numeric/Chain Addition); random key

Custom Square/Table/Cube
- Use square_type="custom" and mono_params={"alphabet": "<your alphabet>"}
- The provided alphabet is used as fill order; system pads/truncates only to reach exact size
- English i/j merging is only applied in standard English 5×5 paths; custom preserves as given

Testing and Roundtrip Guarantees
- Comprehensive suite validates EN/TR/TRX for all ciphers
- Roundtrip (encrypt→decrypt) equals normalized plaintext
- Trifid: verified period‑based blocks for EN (3×3×3) and TR/TRX (3×3×4)

Python/C Parity
- Shared design decisions across languages
- C implementations use UTF‑8 helpers (strlen/char access) where needed for Turkish

Examples (Python)
```python
from cryptology.classical.substitution.fractionated import trifid
import cryptology.alphabets as A

pt = "pijamalı hasta yağız şoföre çabucak güvendi"
ct = trifid.encrypt(pt, key="test", alphabet=A.TURKISH_ALPHABET)
rt = trifid.decrypt(ct, key="test", alphabet=A.TURKISH_ALPHABET)
assert ''.join(c for c in pt.lower() if c.isalpha() or c in 'çğıöşüı') \
    == ''.join(c for c in rt.lower() if c.isalpha() or c in 'çğıöşüı')
```

Notes
- All inputs should be lowercase; Turkish preserved; tests tolerate spacing removal per cipher rules
- When using 5×5 English squares, avoid 'j' in test text (i/j combined); Turkish has no such restriction


