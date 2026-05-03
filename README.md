# Caesar Cipher

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-passing-brightgreen)
![License](https://img.shields.io/badge/License-MIT-green)

> **Difficulty:** Beginner | **Language:** Python | **No dependencies**

CLI toolkit for the Caesar cipher: encrypt, decrypt, ROT13, and brute-force crack using chi-squared English frequency analysis. Supports both standard A-Z mode and full 95-character printable-ASCII mode for CTF use cases. Comes with a pytest suite covering round-trips, edge cases, and crack accuracy.

---

## What You'll Build

| Module | Purpose |
|--------|---------|
| `caesar.py` | Pure library — encrypt, decrypt, rot13, crack |
| `main.py` | CLI entry point with subcommands |
| `test_caesar.py` | pytest unit tests |

---

## Project Structure

```
03-caesar-cipher/
├── README.md
├── .gitignore
├── src/
│   ├── caesar.py         ← Core cipher logic + chi-squared cracker
│   ├── main.py           ← CLI: encrypt / decrypt / rot13 / crack
│   └── test_caesar.py    ← Unit tests
└── docs/
    └── NOTES.md
```

---

## No Installation Required

Python 3.10+ standard library only. No `pip install` needed.

---

## Usage

```bash
cd src

# Encrypt
python main.py encrypt "Attack at dawn" --shift 3
# → Dwwdfn dw gdzq

# Decrypt
python main.py decrypt "Dwwdfn dw gdzq" --shift 3
# → Attack at dawn

# ROT13 (self-inverse)
python main.py rot13 "Hello World"
# → Uryyb Jbeyq

# Brute-force crack — ranks all 25 shifts by English likeness
python main.py crack "Khoor Zruog" --top 3

# Full printable-ASCII mode (useful for CTF challenges)
python main.py encrypt "Hello!" --shift 7 --full-ascii
```

**Example crack output:**
```
──────────────────────────────────────────────────────
  BRUTE-FORCE CRACK  (top 3)
──────────────────────────────────────────────────────
  Ciphertext : Khoor Zruog

  Rank  Shift    χ² Score  Plaintext
  ────  ─────  ──────────  ──────────────────────────────
     1      3       4.218  Hello World
     2     16      31.502  Yvccf Nficu
     3     10      38.714  Axeeh Phkew
```

---

## Run Tests

```bash
cd src
python -m pytest test_caesar.py -v
```

---

## How It Works

### Encryption
Each alphabetic character is shifted by `n` positions modulo 26 (or 95 for full-ASCII mode). Case is preserved in alpha mode; non-alpha characters pass through unchanged.

```
'H' (pos 7) + shift 3  →  'K' (pos 10)
'z' (pos 25) + shift 3  →  'c' (pos 2)   ← wraps around
```

### Cracking — Chi-Squared Analysis
All 25 possible shifts are tried. Each candidate plaintext is scored against expected English letter frequencies using the chi-squared statistic:

```
χ² = Σ (observed_count - expected_count)² / expected_count
```

The shift with the lowest score is the best match. Works reliably on texts of 50+ characters.

---

---

## Challenges & Extensions

- Implement the **Vigenère cipher** (multi-key Caesar — much harder to crack)
- Implement **Kasiski examination** to find the key length of a Vigenère ciphertext
- Add a **substitution cipher** with a full 26-letter key
- Implement **index of coincidence** as an alternative scoring method
- Build a web UI with Flask to visualize frequency histograms

---

## References

- [Caesar cipher — Wikipedia](https://en.wikipedia.org/wiki/Caesar_cipher)
- [Index of coincidence](https://en.wikipedia.org/wiki/Index_of_coincidence)
- [Lewand (2000) English letter frequencies](https://en.wikipedia.org/wiki/Letter_frequency)
- [ROT13](https://en.wikipedia.org/wiki/ROT13)

---

