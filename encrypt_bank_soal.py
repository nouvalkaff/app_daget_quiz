"""Enkripsi setiap soal pada bank soal ke file bank_soal_secured.txt."""

from pathlib import Path

from services.crypto import encrypt

ROOT = Path(__file__).resolve().parent
INPUT_FILE = ROOT / "question_bank" / "ind" / "bank_soal.txt"
OUTPUT_FILE = ROOT / "question_bank" / "ind" / "bank_soal_secured.txt"


def encrypt_question_bank(
    input_file: Path = INPUT_FILE, output_file: Path = OUTPUT_FILE
) -> int:
    """Enkripsi setiap baris soal yang tidak kosong lalu perbarui file output."""
    if not input_file.is_file():
        raise FileNotFoundError(f"File bank soal tidak ditemukan: {input_file}")

    encrypted_lines = [
        encrypt(line) if line else ""
        for line in input_file.read_text(encoding="utf-8-sig").splitlines()
    ]
    output_file.parent.mkdir(parents=True, exist_ok=True)
    output_file.write_text("\n".join(encrypted_lines) + "\n", encoding="utf-8")
    return len(encrypted_lines)


if __name__ == "__main__":
    total_lines = encrypt_question_bank()
    print(f"{total_lines} baris telah dienkripsi ke {OUTPUT_FILE}")
