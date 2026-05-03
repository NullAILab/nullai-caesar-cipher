# Architecture Notes — Caesar Cipher

## Why chi-squared for cracking?

The simplest crack approach is to check which shift produces the highest
frequency of 'E' (most common English letter). That works but is brittle on
short texts. Chi-squared is more robust: it compares the *entire* letter
distribution against expected English frequencies, penalising any deviation.
Lower score = more English-like.

Formula used:
    χ² = Σ (O_i - E_i)² / E_i   for each letter i ∈ a-z

Where O_i = observed count, E_i = expected count given text length × EN_FREQ[i].

## Why two shift modes (alpha vs full-ASCII)?

A plain Caesar cipher on A-Z only is educational but trivially restrictive.
Adding a full-printable-ASCII mode (95-character alphabet) makes the tool
directly applicable to CTF challenges where punctuation and digits are also
shifted. The same modular arithmetic works — mod 26 becomes mod 95.

## Module separation

caesar.py  — pure library: no I/O, no argparse, fully testable
main.py    — thin CLI wrapper calling caesar.py functions
test_caesar.py — pytest unit tests; zero dependency on main.py

This separation is intentional. The library can be imported by other scripts
(e.g. a Vigenère cipher built on top of Caesar shifts) without pulling in
the CLI machinery.

## ROT13 as a special case

ROT13 is Caesar-13, but it deserves its own named function because:
1. It is self-inverse (applying it twice returns the original)
2. It is the most common Caesar variant encountered in practice (usenet,
   Reddit spoilers, base references in CTFs)
3. Having a named entry point makes intent explicit in code
