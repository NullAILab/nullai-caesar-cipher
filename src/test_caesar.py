"""
test_caesar.py — Unit tests for the Caesar cipher module.

Run with:  python -m pytest src/test_caesar.py -v
"""

import pytest
from caesar import caesar_encrypt, caesar_decrypt, rot13, crack


# ---------------------------------------------------------------------------
# Encrypt / decrypt round-trip
# ---------------------------------------------------------------------------

class TestEncryptDecrypt:
    def test_basic_encrypt(self):
        assert caesar_encrypt("Hello", 3) == "Khoor"

    def test_basic_decrypt(self):
        assert caesar_decrypt("Khoor", 3) == "Hello"

    def test_round_trip(self):
        for shift in range(0, 26):
            original = "The quick brown fox jumps over the lazy dog"
            assert caesar_decrypt(caesar_encrypt(original, shift), shift) == original

    def test_preserves_case(self):
        assert caesar_encrypt("AbCd", 1) == "BcDe"

    def test_non_alpha_untouched(self):
        assert caesar_encrypt("Hello, World! 123", 13) == "Uryyb, Jbeyq! 123"

    def test_shift_zero(self):
        assert caesar_encrypt("Hello", 0) == "Hello"

    def test_shift_26_identity(self):
        # shift 26 should be same as shift 0 for alpha mode
        assert caesar_encrypt("Hello", 26) == "Hello"

    def test_wrap_around(self):
        assert caesar_encrypt("xyz", 3) == "abc"
        assert caesar_encrypt("XYZ", 3) == "ABC"

    def test_negative_shift(self):
        assert caesar_encrypt("Hello", -3) == caesar_decrypt("Hello", 3)

    def test_decrypt_is_inverse(self):
        ct = caesar_encrypt("Attack at dawn", 17)
        assert caesar_decrypt(ct, 17) == "Attack at dawn"


# ---------------------------------------------------------------------------
# Full ASCII mode
# ---------------------------------------------------------------------------

class TestFullAscii:
    def test_full_ascii_round_trip(self):
        for shift in [1, 7, 47, 94]:
            original = "Hello, World! 42 #test"
            ct = caesar_encrypt(original, shift, full_ascii=True)
            assert caesar_decrypt(ct, shift, full_ascii=True) == original

    def test_full_ascii_differs_from_alpha(self):
        # For non-letter chars, full_ascii should differ from alpha
        assert caesar_encrypt("!", 1, full_ascii=True) != caesar_encrypt("!", 1)


# ---------------------------------------------------------------------------
# ROT13
# ---------------------------------------------------------------------------

class TestRot13:
    def test_rot13_known(self):
        assert rot13("Hello") == "Uryyb"

    def test_rot13_self_inverse(self):
        texts = ["Hello World", "ABCDEFGhijklmnop", "The quick brown fox"]
        for t in texts:
            assert rot13(rot13(t)) == t


# ---------------------------------------------------------------------------
# Crack
# ---------------------------------------------------------------------------

class TestCrack:
    def test_crack_finds_correct_shift(self):
        plaintext = (
            "To be or not to be that is the question whether tis nobler "
            "in the mind to suffer the slings and arrows of outrageous fortune"
        )
        shift = 7
        ciphertext = caesar_encrypt(plaintext, shift)
        results = crack(ciphertext, top_n=5)
        # The correct shift should appear in the top-5 candidates
        shifts_found = [r[0] for r in results]
        assert shift in shifts_found

    def test_crack_returns_sorted_by_score(self):
        ct = caesar_encrypt("Hello World from the earth", 11)
        results = crack(ct)
        scores = [r[1] for r in results]
        assert scores == sorted(scores)

    def test_crack_top_n_respected(self):
        ct = caesar_encrypt("short text", 5)
        assert len(crack(ct, top_n=3)) == 3
        assert len(crack(ct, top_n=1)) == 1

    def test_crack_empty_input(self):
        # Should not crash on empty or whitespace-only input
        results = crack("", top_n=3)
        assert isinstance(results, list)
