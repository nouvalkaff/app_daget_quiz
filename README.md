# Kuis Daget

Aplikasi kuis berbasis Streamlit dengan hadiah DANA Kaget. Setiap sesi terdiri dari lima soal pilihan ganda yang dipilih secara acak. Tautan hadiah hanya diberikan jika seluruh soal dijawab dengan benar.

## Fitur

- Lima soal dipilih secara acak untuk setiap sesi, termasuk pengacakan pilihan jawaban.
- Jawaban dikunci setelah dikirim dan peserta dapat melihat hasil serta review jawaban di akhir sesi.
- Tautan hadiah hanya ditampilkan untuk peserta dengan nilai sempurna.
- Bank soal disimpan dalam format terenkripsi menggunakan AES-256-GCM.

## Struktur Project

```text
.
|-- assets/images/                          # Ikon Daget untuk header
|-- models/soal_app.py                      # Parsing dan pengacakan soal
|-- question_bank/ind/bank_soal_secured.txt # Bank soal terenkripsi
|-- repositories/bank_soal_app.py           # Pembacaan dan validasi bank soal
|-- services/
|   |-- crypto.py                           # Enkripsi/dekripsi AES-256-GCM
|   |-- nilai.py                            # Pesan hasil kuis
|   `-- ujian_siswa_app.py                  # Alur sesi kuis
|-- config.py                               # Konfigurasi aplikasi dan link hadiah
|-- encrypt_bank_soal.py                    # Enkripsi bank soal
|-- streamlit_app.py                        # Entry point Streamlit
`-- requirements.txt                        # Dependensi aplikasi
```

## Persyaratan

- Python 3.10 atau lebih baru.
- `pip` untuk memasang dependensi.
- `SECRET_KEY` dan `DAGET_LINK` yang valid.

## Menjalankan Secara Lokal

### 1. Buat virtual environment

Virtual environment bersifat opsional, tetapi disarankan agar dependensi project tetap terisolasi.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Install dependensi

```powershell
python -m pip install -r requirements.txt
```

### 3. Buat file `.env`

Buat `.env` di root project:

```dotenv
SECRET_KEY="ganti_dengan_key_base64_url_safe_32_byte"
DAGET_LINK="https://alamat-hadiah-anda"
```

### 4. Jalankan aplikasi

```powershell
python -m streamlit run streamlit_app.py
```

`requirements.txt` digunakan sebagai manifest dependensi untuk Streamlit Community Cloud. `requirements_app.txt` tetap disimpan untuk menjaga kompatibilitas dengan workflow lokal sebelumnya.

## Konfigurasi Rahasia

| Variabel     | Kegunaan                                       | Ketentuan                                                         |
| ------------ | ---------------------------------------------- | ----------------------------------------------------------------- |
| `SECRET_KEY` | Membuka bank soal terenkripsi                  | Base64 URL-safe yang setelah di-decode menghasilkan tepat 32 byte |
| `DAGET_LINK` | URL hadiah untuk peserta dengan nilai sempurna | URL HTTP atau HTTPS yang valid                                    |

Untuk membuat `SECRET_KEY` baru:

```powershell
python -c "import base64, secrets; print(base64.urlsafe_b64encode(secrets.token_bytes(32)).decode())"
```

Urutan pembacaan `DAGET_LINK` adalah:

1. Environment variable
2. Streamlit secrets
3. `.env`

`SECRET_KEY` dibaca dari environment variable atau `.env`.

Jangan commit `.env` atau `.streamlit/secrets.toml` ke repository. Keduanya berisi informasi sensitif dan sudah dimasukkan ke `.gitignore`.

## Mengelola Bank Soal

Bank soal sumber disimpan di:

```text
question_bank/ind/bank_soal.txt
```

Setiap baris mewakili satu soal dengan format:

```text
Teks pertanyaan?|Jawaban benar#Opsi salah 1#Opsi salah 2#Opsi salah 3
```

Setiap soal harus memenuhi ketentuan berikut:

- Teks pertanyaan tidak boleh kosong.
- Harus terdapat tepat empat pilihan jawaban.
- Semua pilihan harus berbeda.
- Pilihan pertama merupakan jawaban yang benar.
- Minimal tersedia lima soal valid, sesuai nilai `JUMLAH_SOAL` di `config.py`.

Setelah bank soal diperbarui, jalankan:

```powershell
python encrypt_bank_soal.py
```

Script tersebut akan membuat atau memperbarui:

```text
question_bank/ind/bank_soal_secured.txt
```

File terenkripsi inilah yang dibaca oleh aplikasi saat berjalan.

Pastikan `SECRET_KEY` yang digunakan saat mengenkripsi bank soal sama dengan key yang digunakan oleh aplikasi.

## Deploy ke Streamlit Community Cloud

1. Push project ke repository GitHub. Sertakan `requirements.txt`, bank soal terenkripsi, dan aset yang dibutuhkan aplikasi.
2. Buat aplikasi baru di Streamlit Community Cloud dan gunakan `streamlit_app.py` sebagai entry point.
3. Buka **App settings → Secrets** dan tambahkan:

```toml
SECRET_KEY = "key-base64-url-safe-anda"
DAGET_LINK = "https://alamat-hadiah-anda"
```

4. Deploy aplikasi.

Lakukan redeploy setelah mengubah kode, dependensi, atau bank soal terenkripsi.


## Lisensi

Project ini didistribusikan di bawah [MIT License](LICENSE).
