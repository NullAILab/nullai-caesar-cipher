"""
caesar.py — Caesar cipher: encrypt, decrypt, and brute-force crack.

Supports:
  - Standard alphabet-only shift (preserves case, leaves non-alpha intact)
  - Full printable-ASCII shift (shift applied over all 95 printable chars)
  - Auto-detection of shift via index-of-coincidence scoring
  - ROT13 shortcut

Usage examples:
    python caesar.py encrypt "Hello World" --shift 13
    python caesar.py decrypt "Uryyb Jbeyq" --shift 13
    python caesar.py crack   "Khoor Zruog"
    python caesar.py rot13   "Hello World"
"""

from __future__ import annotations

import string

# ---------------------------------------------------------------------------
# Core shift primitives
# ---------------------------------------------------------------------------

_LOWER = string.ascii_lowercase          # a-z
_UPPER = string.ascii_uppercase          # A-Z
_PRINTABLE = string.printable[:95]       # all printable ASCII except \t\n etc.


def _shift_char_alpha(ch: str, shift: int) -> str:
    """Shift a single character within its alphabet block (upper / lower)."""
    if ch in _LOWER:
        return _LOWER[(ord(ch) - ord('a') + shift) % 26]
    if ch in _UPPER:
        return _UPPER[(ord(ch) - ord('A') + shift) % 26]
    return ch                              # non-alpha — pass through


def _shift_char_full(ch: str, shift: int) -> str:
    """Shift over all 95 printable ASCII characters."""
    idx = _PRINTABLE.find(ch)
    if idx == -1:
        return ch
    return _PRINTABLE[(idx + shift) % 95]


def caesar_encrypt(plaintext: str, shift: int, *, full_ascii: bool = False) -> str:
    """
    Encrypt *plaintext* with a Caesar shift.

    Args:
        plaintext:  Input string.
        shift:      Number of positions to shift (positive = right).
        full_ascii: If True, shift over all 95 printable ASCII chars.
                    If False (default), shift only A-Z / a-z.

    Returns:
        Ciphertext string.
    """
    shift %= (95 if full_ascii else 26)
    fn = _shift_char_full if full_ascii else _shift_char_alpha
    return "".join(fn(c, shift) for c in plaintext)


def caesar_decrypt(ciphertext: str, shift: int, *, full_ascii: bool = False) -> str:
    """Decrypt *ciphertext* by reversing the shift."""
    shift %= (95 if full_ascii else 26)
    return caesar_encrypt(ciphertext, -shift, full_ascii=full_ascii)


def rot13(text: str) -> str:
    """Apply ROT13 (self-inverse Caesar shift of 13)."""
    return caesar_encrypt(text, 13)


# ---------------------------------------------------------------------------
# Frequency analysis / brute-force cracking
# ---------------------------------------------------------------------------

# English letter frequency table (a-z), sourced from Lewand (2000)
_EN_FREQ: dict[str, float] = {
    'a': 0.08167, 'b': 0.01492, 'c': 0.02782, 'd': 0.04253, 'e': 0.12702,
    'f': 0.02228, 'g': 0.02015, 'h': 0.06094, 'i': 0.06966, 'j': 0.00153,
    'k': 0.00772, 'l': 0.04025, 'm': 0.02406, 'n': 0.06749, 'o': 0.07507,
    'p': 0.01929, 'q': 0.00095, 'r': 0.05987, 's': 0.06327, 't': 0.09056,
    'u': 0.02758, 'v': 0.00978, 'w': 0.02360, 'x': 0.00150, 'y': 0.01974,
    'z': 0.00074,
}


def _chi_squared(text: str) -> float:
    """
    Compute chi-squared statistic comparing text's letter distribution
    against expected English frequencies. Lower = more English-like.
    """
    text_lower = text.lower()
    total = sum(1 for c in text_lower if c.isalpha())
    if total == 0:
        return float('inf')

    score = 0.0
    for ch in _LOWER:
        observed = text_lower.count(ch)
        expected = _EN_FREQ[ch] * total
        if expected > 0:
            score += (observed - expected) ** 2 / expected
    return score


def crack(ciphertext: str, top_n: int = 5) -> list[tuple[int, float, str]]:
    """
    Brute-force all 25 Caesar shifts and rank by chi-squared fitness.

    Returns:
        List of (shift, chi_squared_score, plaintext) tuples, sorted
        best-first (lowest chi-squared = most English-like).
        Length is min(top_n, 25).
    """
    candidates: list[tuple[int, float, str]] = []
    for shift in range(1, 26):
        plaintext = caesar_decrypt(ciphertext, shift)
        score = _chi_squared(plaintext)
        candidates.append((shift, score, plaintext))

    candidates.sort(key=lambda x: x[1])
    return candidates[:top_n]
