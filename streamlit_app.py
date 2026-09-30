import streamlit as st

from config import JUMLAH_SOAL
from services.ujian_siswa_app import UjianSiswaApp

GAMBAR_DAGET = "https://assets.jabarekspres.com/main/2023/05/DANA-Kaget-buatmu-1.png"

TAMPILAN = """
<style>
  [data-testid="stAppViewContainer"] {
    background:
      radial-gradient(circle at 12% 12%, rgba(28, 129, 202, .23), transparent 32%),
      radial-gradient(circle at 87% 84%, rgba(199, 151, 68, .13), transparent 35%),
      linear-gradient(135deg, #091321 0%, #0d1d30 53%, #0a1423 100%);
  }
  [data-testid="stHeader"] { background: transparent; }
  .block-container {
    max-width: 880px;
    margin: 3rem auto;
    padding: 2.8rem 3rem 3.2rem;
    background: linear-gradient(145deg, rgba(23, 43, 67, .97), rgba(12, 25, 43, .98));
    border: 1px solid rgba(174, 203, 226, .16);
    border-radius: 24px;
    box-shadow: 0 30px 80px rgba(0, 0, 0, .32), inset 0 1px rgba(255, 255, 255, .06);
  }
  .quiz-brand { display: flex; align-items: center; gap: 1.15rem; margin-bottom: .15rem; }
  .quiz-brand img {
    width: 88px; height: 88px; object-fit: cover; flex-shrink: 0;
    border-radius: 17px; border: 1px solid rgba(222, 238, 255, .3);
    box-shadow: 0 10px 30px rgba(0, 0, 0, .28);
  }
  .quiz-brand-copy {
    display: flex; flex-direction: column; justify-content: center; gap: .3rem;
  }
  .quiz-brand-copy span {
    display: block; color: #ddbb77; font-size: .9rem; font-weight: 700;
    letter-spacing: .15em; text-transform: uppercase; line-height: 1.2;
  }
  .quiz-brand h1 {
    color: #f7f9ff; font-size: 36px; font-weight: 700;
    letter-spacing: -.035em; margin: 0; line-height: 1.08;
  }
  .block-container h2, .block-container h3, .block-container p,
  .block-container label { color: #f2f6fb; }
  [data-testid="stCaptionContainer"] { color: #aebfd2; }
  [data-testid="stRadio"] label[data-baseweb="radio"] {
    width: 100%; padding: .65rem .9rem; border-radius: 12px;
    border: 1px solid rgba(164, 195, 218, .2);
    background: rgba(7, 18, 32, .42); transition: border-color .2s, background .2s;
  }
  [data-testid="stRadio"] label[data-baseweb="radio"]:hover {
    border-color: #d8b873; background: rgba(22, 49, 75, .8);
  }
  div.stButton > button {
    border: 1px solid #e6c985; border-radius: 10px;
    background: linear-gradient(135deg, #f5dfaa, #d5aa59);
    color: #142337; font-weight: 700; box-shadow: 0 7px 22px rgba(0, 0, 0, .2);
  }
  div.stButton > button p, div.stButton > button span { color: #142337; font-weight: 700; }
  div.stButton > button:hover {
    border-color: #ffe9b1; background: #ffe5a1; color: #0d1d30;
  }
  div.stButton > button:hover p, div.stButton > button:hover span { color: #0d1d30; }
  div.stButton > button:disabled {
    background: #57677b; border-color: #718398; box-shadow: none;
  }
  div.stButton > button:disabled p, div.stButton > button:disabled span { color: #f2f6fb; }
  div.stLinkButton > a {
    border: 1px solid #e26470; border-radius: 10px;
    background: linear-gradient(135deg, #c83d4e, #a51e30);
    color: #ffffff; font-weight: 700; box-shadow: 0 7px 22px rgba(92, 9, 22, .28);
  }
  div.stLinkButton > a p, div.stLinkButton > a span { color: #ffffff; font-weight: 700; }
  div.stLinkButton > a:hover {
    border-color: #f48c96; background: linear-gradient(135deg, #dc5261, #b7283b);
    color: #ffffff;
  }
  div.stLinkButton > a:hover p, div.stLinkButton > a:hover span { color: #ffffff; }
  div.stButton > button:focus-visible, div.stLinkButton > a:focus-visible {
    outline: 3px solid #9bd7ff; outline-offset: 2px;
  }
  [data-testid="stExpander"] {
    border: 1px solid rgba(164, 195, 218, .2); border-radius: 12px;
    background: rgba(7, 18, 32, .3);
  }
  @media (max-width: 700px) {
    .block-container { margin: 1rem .7rem; padding: 1.5rem 1.2rem 2rem; border-radius: 18px; }
    .quiz-brand { gap: .9rem; }
    .quiz-brand img { width: 72px; height: 72px; border-radius: 14px; }
  }
</style>
"""


def main() -> None:
    st.set_page_config(page_title="Kuis Daget", page_icon="💎", layout="centered")
    st.markdown(TAMPILAN, unsafe_allow_html=True)
    st.markdown(
        f'<div class="quiz-brand"><img src="{GAMBAR_DAGET}" alt="Ilustrasi DANA Kaget">'
        '<div class="quiz-brand-copy"><span>Kuis berhadiah</span>'
        "<h1>Kuis Daget</h1></div></div>",
        unsafe_allow_html=True,
    )
    st.caption(
        f"Jawab {JUMLAH_SOAL} soal pilihan ganda. Link daget muncul jika semuanya benar."
    )

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
