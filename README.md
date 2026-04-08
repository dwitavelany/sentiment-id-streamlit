---
title: Sentiment Analysis Indonesia
emoji: 🤖
colorFrom: blue
colorTo: green
sdk: docker
app_port: 7860
pinned: false
---

# Sentiment Analysis Bahasa Indonesia (Streamlit)

Aplikasi ini melakukan analisis sentimen teks bahasa Indonesia dengan tiga kelas:

- Positif
- Netral
- Negatif

Model yang digunakan:
`w11wo/indonesian-roberta-base-sentiment-classifier`

## Jalankan Lokal

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Deploy ke Hugging Face Spaces

### Opsi 1: Upload Manual

1. Login ke https://huggingface.co dan buat Space baru.
2. Pilih `SDK: Docker`.
3. Upload file berikut ke root Space:
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. Tunggu build selesai, aplikasi akan aktif otomatis.

### Opsi 2: Push via Git (Direkomendasikan)

```bash
source .venv/bin/activate
pip install huggingface_hub

git init
git add .
git commit -m "Initial Streamlit Indonesian sentiment app"

.venv/bin/hf auth login
.venv/bin/hf repos create sentiment-id-streamlit --type space --space-sdk docker

git remote add hf https://huggingface.co/spaces/<username>/sentiment-id-streamlit
git branch -M main
git push -u hf main
```

Catatan: Hugging Face CLI terbaru tidak lagi menerima `streamlit` sebagai `--space-sdk` saat create repo. Solusi resminya adalah pakai `docker` dan jalankan Streamlit dari `Dockerfile`.
Untuk `git push` ke `huggingface.co`, password akun tidak didukung. Gunakan User Access Token (role `write`) dari https://huggingface.co/settings/tokens.
Saat prompt Git muncul:
- Username: username Hugging Face Anda
- Password: token Hugging Face (contoh diawali `hf_...`)

Jika muncul error `externally-managed-environment`, pastikan semua perintah pip dijalankan setelah `source .venv/bin/activate`.
Jika muncul `hf: command not found`, gunakan `.venv/bin/hf ...` seperti contoh di atas.

## Catatan

- Teks panjang dipotong otomatis hingga 256 token.
- Untuk analisis banyak teks sekaligus, gunakan tab **Analisis Banyak Teks**.
- Jika log Space menampilkan warning `unauthenticated requests`, tambahkan Secret `HF_TOKEN` di Settings -> Variables and secrets pada Space Anda.
- Pesan `roberta.embeddings.position_ids | UNEXPECTED` saat load model umumnya tidak fatal dan aplikasi tetap bisa jalan.
