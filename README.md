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
pip install -r requirements.txt
streamlit run app.py
```

## Deploy ke Hugging Face Spaces

1. Login ke https://huggingface.co dan buat Space baru.
2. Pilih `SDK: Streamlit`.
3. Upload file berikut ke root Space:
   - `app.py`
   - `requirements.txt`
   - `README.md`
4. Tunggu build selesai, aplikasi akan aktif otomatis.

## Catatan

- Teks panjang dipotong otomatis hingga 256 token.
- Untuk analisis banyak teks sekaligus, gunakan tab **Analisis Banyak Teks**.
