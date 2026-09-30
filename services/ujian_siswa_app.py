import random

import streamlit as st

from config import JUMLAH_SOAL, ambil_link_daget
from models.soal_app import SoalApp
from repositories.bank_soal_app import BankSoalApp
from services.nilai import evaluasi_nilai


class UjianSiswaApp:
    def siapkan_sesi(self) -> bool:
        raw = BankSoalApp().ambil_soal()
        if len(raw) < JUMLAH_SOAL:
            return False

        soal_list = []
        for baris in random.sample(raw, JUMLAH_SOAL):
            soal = SoalApp(baris)
            pertanyaan, jawaban_benar = soal.parse_soal()
            soal_list.append({
                "pertanyaan": pertanyaan,
                "opsi": soal.acak_opsi(),
                "jawaban_benar": jawaban_benar,
                "jawaban_user": None,
            })

        st.session_state.soal_list = soal_list
        st.session_state.index = 0
        st.session_state.jumlah_benar = 0
        st.session_state.sudah_jawab = False
        st.session_state.selesai = False
        return True

    def tampilkan_hasil_web(self) -> None:
        benar = st.session_state.jumlah_benar
        st.progress(1.0)
        st.subheader(f"Hasil: {benar}/{JUMLAH_SOAL} benar")
        st.write(evaluasi_nilai(benar))

        if benar == JUMLAH_SOAL:
            link = ambil_link_daget()
            if link:
                st.link_button("Buka link daget", link)
            else:
                st.error("DAGET_LINK belum berisi URL http/https yang valid. Hubungi pengelola kuis.")

        with st.expander("Review jawaban"):
            for i, soal in enumerate(st.session_state.soal_list, start=1):
                benar_soal = soal["jawaban_user"] == soal["jawaban_benar"]
                st.write(f"{'✅' if benar_soal else '❌'} Soal {i}: {soal['pertanyaan']}")
                st.write(f"Jawabanmu: {soal['jawaban_user']}")
                if not benar_soal:
                    st.write(f"Jawaban benar: {soal['jawaban_benar']}")

        if st.button("Coba lagi"):
            for key in ("soal_list", "index", "jumlah_benar", "sudah_jawab", "selesai"):
                st.session_state.pop(key, None)
            st.rerun()
