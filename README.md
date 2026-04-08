---
title: Sentiment Analysis Indonesia
emoji: 🇮🇩
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.44.1
app_file: app.py
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
2. Pilih `SDK: Streamlit`.
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
.venv/bin/hf repo create sentiment-id-streamlit --type space --space_sdk streamlit

git remote add origin https://huggingface.co/spaces/<username>/sentiment-id-streamlit
git branch -M main
git push -u origin main
```

Jika muncul error `externally-managed-environment`, pastikan semua perintah pip dijalankan setelah `source .venv/bin/activate`.
Jika muncul `hf: command not found`, gunakan `.venv/bin/hf ...` seperti contoh di atas.

## Catatan

- Teks panjang dipotong otomatis hingga 256 token.
- Untuk analisis banyak teks sekaligus, gunakan tab **Analisis Banyak Teks**.
