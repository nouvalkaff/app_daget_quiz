# Kuis Daget

Aplikasi kuis hadiah berbasis Streamlit. Pengguna menjawab tiga soal pilihan
ganda yang dipilih secara acak dari bank soal. Jawaban dikunci setelah dikirim;
tautan DANA Kaget hanya ditampilkan jika ketiga jawaban benar.

## Fitur

- Tiga soal pilihan ganda per sesi, dengan urutan soal dan opsi yang diacak.
- Feedback setelah setiap jawaban serta ringkasan dan review di akhir kuis.
- Tombol hadiah hanya tersedia untuk hasil sempurna.
- Tampilan responsif dengan ilustrasi DANA Kaget, latar navy, aksen emas, dan
  tombol hadiah merah.
- URL hadiah dibaca dari environment variable, Streamlit secrets, atau `.env`.

## Menjalankan aplikasi

```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

`requirements.txt` is also the dependency manifest used by Streamlit Community
Cloud. The legacy `requirements_app.txt` contains the same requirements for
existing local workflows.

## Konfigurasi link hadiah

Untuk Streamlit lokal, buat `.streamlit/secrets.toml` dan isi:

```toml
DAGET_LINK = "https://alamat-hadiah-anda"
```

Pada Streamlit Community Cloud, masukkan baris TOML yang sama di pengaturan
Secrets aplikasi. Secara lokal, `.env` pada root project atau environment
variable `DAGET_LINK` juga dapat digunakan. Urutan prioritasnya adalah
environment variable, Streamlit secrets, kemudian `.env`.

Jangan commit `.env` atau `secrets.toml` ke repository. Keduanya menyimpan URL
hadiah yang sebaiknya hanya diketahui pengelola kuis.

## Bank soal

Bank soal sumber berada di `question_bank/ind/bank_soal.txt`, satu soal per baris.
Jalankan `python encrypt_bank_soal.py` untuk membuat
`question_bank/ind/bank_soal_secured.txt`; aplikasi membaca file secured ini dan
mendekripsi setiap baris sebelum menampilkannya di UI. Format file sumber:

```text
Teks pertanyaan?|Jawaban benar#Opsi salah 1#Opsi salah 2#Opsi salah 3
```

Sediakan setidaknya tiga baris valid. Setiap soal harus memiliki pertanyaan,
empat opsi yang tidak kosong, dan empat opsi yang berbeda. Opsi pertama
dianggap sebagai jawaban benar.
