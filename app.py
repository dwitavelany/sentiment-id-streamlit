import os
import re
from typing import List, Dict

# Avoid Streamlit module watcher probing transformers optional vision modules.
os.environ.setdefault("STREAMLIT_SERVER_FILE_WATCHER_TYPE", "none")

import streamlit as st
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from transformers.utils import logging as hf_logging


MODEL_NAME = "w11wo/indonesian-roberta-base-sentiment-classifier"
MAX_LENGTH = 256

# Keep runtime logs clean in Spaces; model still loads the same way.
hf_logging.set_verbosity_error()

LABEL_MAP = {
    "LABEL_0": "Positif",
    "LABEL_1": "Netral",
    "LABEL_2": "Negatif",
}
EMOJI_MAP = {
    "Negatif": "😕",
    "Netral": "😐",
    "Positif": "😄",
}


@st.cache_resource(show_spinner="Memuat model bahasa Indonesia...")
def load_model():
    hf_token = os.getenv("HF_TOKEN")
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, token=hf_token)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, token=hf_token)
    return tokenizer, model


def clean_text(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    return text


def predict_sentiment(texts: List[str], tokenizer, model) -> List[Dict[str, float]]:
    inputs = tokenizer(
        texts,
        return_tensors="pt",
        truncation=True,
        padding=True,
        max_length=MAX_LENGTH,
    )

    with torch.no_grad():
        logits = model(**inputs).logits

    probs = torch.nn.functional.softmax(logits, dim=-1)
    results = []
    for prob in probs:
        score_map = {
            LABEL_MAP[f"LABEL_{idx}"]: float(prob[idx].item())
            for idx in range(prob.shape[0])
        }
        top_label = max(score_map, key=score_map.get)
        results.append(
            {
                "label": top_label,
                "confidence": score_map[top_label],
                "scores": score_map,
            }
        )
    return results


def main():
    st.set_page_config(
        page_title="Sentimen Bahasa Indonesia",
        page_icon="🇮🇩",
        layout="centered",
    )

    st.title("Sentiment Analysis Bahasa Indonesia")
    st.caption(
        "Aplikasi ini menganalisis sentimen teks berbahasa Indonesia menjadi Positif, Netral, atau Negatif."
    )

    with st.expander("Tentang model", expanded=False):
        st.write(f"Model: `{MODEL_NAME}`")
        st.write("Teks akan dipotong otomatis hingga 256 token untuk menjaga performa.")

    tokenizer, model = load_model()

    tab_single, tab_batch = st.tabs(["Analisis Satu Teks", "Analisis Banyak Teks"])

    with tab_single:
        input_text = st.text_area(
            "Masukkan teks Indonesia",
            placeholder="Contoh: Pelayanan aplikasi ini cepat dan sangat membantu!",
            height=140,
        )

        if st.button("Analisis Sentimen", use_container_width=True):
            cleaned = clean_text(input_text)
            if not cleaned:
                st.warning("Teks tidak boleh kosong.")
            else:
                result = predict_sentiment([cleaned], tokenizer, model)[0]
                label = result["label"]
                confidence = result["confidence"]

                st.success(f"Hasil: {EMOJI_MAP[label]} **{label}**")
                st.metric("Tingkat keyakinan", f"{confidence * 100:.2f}%")
                st.write("Distribusi skor:")
                st.bar_chart(result["scores"])

    with tab_batch:
        st.write(
            "Masukkan beberapa teks, satu baris per teks. Cocok untuk analisis cepat beberapa komentar sekaligus."
        )
        batch_text = st.text_area(
            "Input batch",
            placeholder="Aplikasi ini sangat bagus\nBiasa saja menurut saya\nFiturnya sering error",
            height=180,
            key="batch_input",
        )

        if st.button("Analisis Batch", use_container_width=True):
            lines = [clean_text(line) for line in batch_text.splitlines()]
            texts = [line for line in lines if line]

            if not texts:
                st.warning("Mohon isi minimal satu baris teks.")
            else:
                results = predict_sentiment(texts, tokenizer, model)
                output_rows = []
                for original, pred in zip(texts, results):
                    output_rows.append(
                        {
                            "teks": original,
                            "sentimen": pred["label"],
                            "keyakinan": f"{pred['confidence'] * 100:.2f}%",
                            "negatif": f"{pred['scores']['Negatif'] * 100:.2f}%",
                            "netral": f"{pred['scores']['Netral'] * 100:.2f}%",
                            "positif": f"{pred['scores']['Positif'] * 100:.2f}%",
                        }
                    )

                st.dataframe(output_rows, use_container_width=True)

                positives = sum(1 for r in results if r["label"] == "Positif")
                neutrals = sum(1 for r in results if r["label"] == "Netral")
                negatives = sum(1 for r in results if r["label"] == "Negatif")

                st.write("Ringkasan batch:")
                st.bar_chart(
                    {
                        "Positif": positives,
                        "Netral": neutrals,
                        "Negatif": negatives,
                    }
                )

    st.divider()
    st.caption("Dibuat dengan Streamlit dan Hugging Face Transformers.")


if __name__ == "__main__":
    main()
