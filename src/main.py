"""
main.py — CLI entry point for the Caesar cipher toolkit.

Subcommands:
    encrypt   Encrypt plaintext with a given shift
    decrypt   Decrypt ciphertext with a known shift
    crack     Brute-force all 25 shifts and rank by English frequency
    rot13     Apply ROT13 (Caesar-13, self-inverse)

Options (all subcommands):
    --full-ascii  Shift over all 95 printable ASCII chars instead of A-Z only

Usage:
    python main.py encrypt "Attack at dawn" --shift 3
    python main.py decrypt "Dwwdfn dw gdzq" --shift 3
    python main.py crack   "Khoor Zruog" --top 3
    python main.py rot13   "Hello World"
    python main.py encrypt "Hello!" --shift 7 --full-ascii
"""

import argparse
import sys

from caesar import caesar_encrypt, caesar_decrypt, rot13, crack


# ---------------------------------------------------------------------------
# Formatting
# ---------------------------------------------------------------------------

def _header(title: str) -> str:
    return f"\n{'─' * 50}\n  {title}\n{'─' * 50}"


def cmd_encrypt(args: argparse.Namespace) -> None:
    ct = caesar_encrypt(args.text, args.shift, full_ascii=args.full_ascii)
    print(_header("ENCRYPT"))
    print(f"  Shift      : {args.shift}")
    print(f"  Plaintext  : {args.text}")
    print(f"  Ciphertext : {ct}\n")


def cmd_decrypt(args: argparse.Namespace) -> None:
    pt = caesar_decrypt(args.text, args.shift, full_ascii=args.full_ascii)
    print(_header("DECRYPT"))
    print(f"  Shift      : {args.shift}")
    print(f"  Ciphertext : {args.text}")
    print(f"  Plaintext  : {pt}\n")


def cmd_rot13(args: argparse.Namespace) -> None:
    result = rot13(args.text)
    print(_header("ROT13"))
    print(f"  Input  : {args.text}")
    print(f"  Output : {result}\n")


def cmd_crack(args: argparse.Namespace) -> None:
    results = crack(args.text, top_n=args.top)
    print(_header(f"BRUTE-FORCE CRACK  (top {args.top})"))
    print(f"  Ciphertext : {args.text}\n")
    print(f"  {'Rank':>4}  {'Shift':>5}  {'χ² Score':>10}  Plaintext")
    print(f"  {'─'*4}  {'─'*5}  {'─'*10}  {'─'*30}")
    for rank, (shift, score, plaintext) in enumerate(results, 1):
        print(f"  {rank:>4}  {shift:>5}  {score:>10.3f}  {plaintext}")
    print()


# ---------------------------------------------------------------------------
# Argument parser
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="caesar",
        description="Caesar cipher — encrypt, decrypt, crack, ROT13",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    sub = p.add_subparsers(dest="command", required=True)

    # shared options
    def add_text_arg(subp: argparse.ArgumentParser) -> None:
        subp.add_argument("text", help="Input text (quote multi-word strings)")
        subp.add_argument(
            "--full-ascii", action="store_true",
            help="Shift all 95 printable ASCII chars, not just A-Z"
        )

    def add_shift_arg(subp: argparse.ArgumentParser) -> None:
        subp.add_argument("--shift", "-s", type=int, required=True,
                          help="Shift amount (0–25 for alpha mode)")

    # encrypt
    enc_p = sub.add_parser("encrypt", help="Encrypt plaintext")
    add_text_arg(enc_p)
    add_shift_arg(enc_p)
    enc_p.set_defaults(func=cmd_encrypt)

    # decrypt
    dec_p = sub.add_parser("decrypt", help="Decrypt ciphertext")
    add_text_arg(dec_p)
    add_shift_arg(dec_p)
    dec_p.set_defaults(func=cmd_decrypt)

    # rot13
    rot_p = sub.add_parser("rot13", help="Apply ROT13 (shift-13, self-inverse)")
    add_text_arg(rot_p)
    rot_p.set_defaults(func=cmd_rot13)

    # crack
    crack_p = sub.add_parser("crack", help="Brute-force all 25 shifts")
    add_text_arg(crack_p)
    crack_p.add_argument(
        "--top", "-n", type=int, default=5,
        help="Show top N candidates (default: 5)"
    )
    crack_p.set_defaults(func=cmd_crack)

    return p


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
