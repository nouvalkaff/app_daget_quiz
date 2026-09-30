import base64
from pathlib import Path

import streamlit as st

from config import JUMLAH_SOAL
from services.ujian_siswa_app import UjianSiswaApp

GAMBAR_DAGET = (
    Path(__file__).parent / "assets" / "images" / "daget_icon_source_dana_id.png"
)

TAMPILAN = """
<style>
  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 10% 8%, rgba(75, 148, 109, .35), transparent 29%),
      radial-gradient(circle at 93% 88%, rgba(213, 171, 82, .22), transparent 34%),
      linear-gradient(135deg, #062a24 0%, #0a4438 52%, #0b2d28 100%);
  }
  [data-testid="stHeader"] { background: transparent; }
  .block-container {
    max-width: 880px;
    margin: 3rem auto;
    padding: 2.8rem 3rem 3.2rem;
    background: linear-gradient(145deg, rgba(10, 54, 45, .97), rgba(5, 35, 31, .98));
    border: 1px solid rgba(224, 190, 113, .3);
    border-radius: 24px;
    box-shadow: 0 30px 80px rgba(1, 20, 16, .48), inset 0 1px rgba(255, 244, 209, .1);
  }
  .quiz-brand { display: flex; align-items: flex-start; gap: 1.15rem; margin-bottom: .15rem; }
  .quiz-brand img {
    width: 106px; height: 106px; object-fit: cover; flex-shrink: 0;
    border-radius: 17px; border: none;
    box-shadow: 0 10px 30px rgba(0, 20, 15, .34);
  }
  .quiz-brand-copy {
    display: flex; flex-direction: column; justify-content: center; gap: .3rem;
  }
  .quiz-brand-copy span {
    display: block; color: #f0ca73; font-size: 1.4rem; font-weight: 700;
    letter-spacing: .15em; text-transform: uppercase; line-height: 1.2;
  }
  .quiz-brand h1 {
    color: #fffaf0; font-size: 36px; font-weight: 700;
    letter-spacing: -.035em; margin: 0; line-height: 1.08;
  }
  .block-container h2, .block-container h3, .block-container p,
  .block-container label { color: #f8f4e9; }
  [data-testid="stCaptionContainer"] { color: #c7d7c5; }
  [data-testid="stRadio"] label[data-baseweb="radio"] {
    width: 100%; padding: .65rem .9rem; border-radius: 12px;
    border: 1px solid rgba(185, 213, 193, .26);
    background: rgba(3, 35, 29, .52); transition: border-color .2s, background .2s;
  }
  [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    border-color: #e1bb66; background: rgba(24, 83, 65, .8);
  }
  div.stButton > button {
    border: 1px solid #f0d187; border-radius: 10px;
    background: linear-gradient(135deg, #f4d889, #c99a3d);
    color: #12362e; font-weight: 700; box-shadow: 0 7px 22px rgba(0, 22, 16, .28);
  }
  div.stButton > button p, div.stButton > button span { color: #12362e; font-weight: 700; }
  div.stButton > button:hover {
    border-color: #fff0bd; background: #ffe6a0; color: #082d25;
  }
  div.stButton > button:hover p, div.stButton > button:hover span { color: #082d25; }
  div.stButton > button:disabled {
    background: #54756a; border-color: #73958a; box-shadow: none;
  }
  div.stButton > button:disabled p, div.stButton > button:disabled span { color: #eef5ee; }
  div.stLinkButton > a {
    border: 1px solid #f0d187; border-radius: 10px;
    background: linear-gradient(135deg, #e4bc61, #b7862d);
    color: #12362e; font-weight: 700; box-shadow: 0 7px 22px rgba(0, 22, 16, .28);
  }
  div.stLinkButton > a p, div.stLinkButton > a span { color: #12362e; font-weight: 700; }
  div.stLinkButton > a:hover {
    border-color: #fff0bd; background: linear-gradient(135deg, #f2d17d, #c9983e);
    color: #082d25;
  }
  div.stLinkButton > a:hover p, div.stLinkButton > a:hover span { color: #082d25; }
  div.stButton > button:focus-visible, div.stLinkButton > a:focus-visible {
    outline: 3px solid #ffe8a5; outline-offset: 2px;
  }
  [data-testid="stExpander"] {
    border: 1px solid rgba(185, 213, 193, .26); border-radius: 12px;
    background: rgba(3, 35, 29, .42);
  }
  @media (max-width: 700px) {
    .block-container { margin: 1rem .7rem; padding: 1.5rem 1.2rem 2rem; border-radius: 18px; }
    .quiz-brand { gap: .9rem; }
    .quiz-brand img { width: 86px; height: 86px; border-radius: 14px; }
  }
</style>
"""


def gambar_daget_data_uri() -> str:
    """Kembalikan ikon Daget lokal sebagai data URI untuk header HTML."""
    encoded_image = base64.b64encode(GAMBAR_DAGET.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded_image}"


def main() -> None:
    st.set_page_config(page_title="Kuis Daget", page_icon="💎", layout="centered")
    st.markdown(TAMPILAN, unsafe_allow_html=True)
    st.markdown(
        f'<div class="quiz-brand"><img src="{gambar_daget_data_uri()}" alt="Ikon DANA Kaget">'
        '<div class="quiz-brand-copy"><span>Kuis berhadiah</span>'
        "<h1>Dana Kaget</h1></div></div>",
        unsafe_allow_html=True,
    )
    st.caption("Semua benar, link DAGET muncul. Tidak ada batas waktu.")
    st.caption("Dipersembahkan oleh: Nouval Alkaf")

    ujian = UjianSiswaApp()
    if "soal_list" not in st.session_state:
        if not ujian.siapkan_sesi():
            st.error(
                f"Bank soal harus berisi setidaknya {JUMLAH_SOAL} soal yang valid."
            )
            return

    if st.session_state.selesai:
        ujian.tampilkan_hasil_web()
        return

    index = st.session_state.index
    soal = st.session_state.soal_list[index]
    st.progress(index / JUMLAH_SOAL)
    st.write(f"Soal {index + 1}/{JUMLAH_SOAL}")
    st.subheader(soal["pertanyaan"])

    pilihan_idx = st.radio(
        "Pilih jawaban:",
        range(len(soal["opsi"])),
        index=None,
        key=f"pilihan_{index}",
        disabled=st.session_state.sudah_jawab,
        format_func=lambda i: f"{chr(65 + i)}. {soal['opsi'][i]}",
    )

    if not st.session_state.sudah_jawab:
        if st.button("Jawab", disabled=pilihan_idx is None):
            jawaban = soal["opsi"][pilihan_idx]
            soal["jawaban_user"] = jawaban
            st.session_state.sudah_jawab = True
            if jawaban == soal["jawaban_benar"]:
                st.session_state.jumlah_benar += 1
            st.rerun()
        return

    if soal["jawaban_user"] == soal["jawaban_benar"]:
        st.success("Jawaban benar! 🎉")
    else:
        st.error("Jawaban salah.")

    if st.button("Lihat hasil" if index == JUMLAH_SOAL - 1 else "Lanjut"):
        st.session_state.index += 1
        st.session_state.sudah_jawab = False
        st.session_state.selesai = st.session_state.index == JUMLAH_SOAL
        st.rerun()


if __name__ == "__main__":
    main()
