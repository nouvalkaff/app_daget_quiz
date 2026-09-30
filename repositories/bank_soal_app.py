from config import DIR_PATH_IDN
from services.crypto import decrypt


class BankSoalApp:
    def ambil_soal(self) -> list[str]:
        try:
            with DIR_PATH_IDN.open(encoding="utf-8") as file:
                encrypted_lines = (baris.strip() for baris in file)
                decrypted_lines = (decrypt(baris) for baris in encrypted_lines if baris)
                return [baris for baris in decrypted_lines if self._valid(baris)]
        except FileNotFoundError:
            return []

    @staticmethod
    def _valid(baris: str) -> bool:
        bagian = baris.split("|", 1)
        if len(bagian) != 2 or not bagian[0].strip():
            return False
        opsi = [pilihan.strip() for pilihan in bagian[1].split("#")]
        return len(opsi) == 4 and all(opsi) and len(set(opsi)) == 4
