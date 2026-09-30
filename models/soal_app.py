from random import shuffle


class SoalApp:
    def __init__(self, baris: str) -> None:
        self.baris = baris
        self.pertanyaan = ""
        self.jawaban_benar = ""
        self.opsi = []

    def parse_soal(self) -> tuple[str, str]:
        soal = self.baris.split("|", 1)
        self.pertanyaan = soal[0].strip()
        self.opsi = [opsi.strip() for opsi in soal[1].split("#")]
        self.jawaban_benar = self.opsi[0]
        return self.pertanyaan, self.jawaban_benar

    def acak_opsi(self) -> list[str]:
        opsi_acak = self.opsi[:]
        shuffle(opsi_acak)
        return opsi_acak
