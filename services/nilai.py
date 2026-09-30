from config import JUMLAH_SOAL


def evaluasi_nilai(jawaban_benar: int) -> str:
    responses = {
        JUMLAH_SOAL: "Alhamdulillah benar semua! Ini yang ditunggu-tunggu:",
        4: "4 dari 5, hampir? Nyaris nyaris. Wkwk sabar.",
        3: "Setengah jalan, lumayan lah. Lanjut belajar.",
        2: "Dua doang, nanggung banget sih. Coba lagi!",
        1: "Satu? hehehe. Semangat! Coba lagi.",
        0: "Nol? Oops, harus belajar lagi nih.",
    }
    return responses.get(jawaban_benar, "Coba lagi!")
