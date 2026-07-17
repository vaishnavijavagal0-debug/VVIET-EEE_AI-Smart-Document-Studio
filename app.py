import streamlit as st
from pypdf import PdfReader, PdfWriter
from docx import Document
from googletrans import Translator
from gtts import gTTS
from PIL import Image
import os

st.set_page_config(page_title="AI Smart Document Studio")

st.title("📄 AI Smart Document Studio")

menu = st.sidebar.selectbox(
    "Select Feature",
    [
        "Merge PDFs",
        "Extract PDF Pages",
        "Read Word File",
        "Translate Text",
        "Generate Audio"
    ]
)

# ---------------- MERGE PDF ----------------
if menu == "Merge PDFs":
    files = st.file_uploader(
        "Upload PDFs",
        type="pdf",
        accept_multiple_files=True
    )

    if st.button("Merge"):
        writer = PdfWriter()

        for pdf in files:
            reader = PdfReader(pdf)
            for page in reader.pages:
                writer.add_page(page)

        with open("merged.pdf", "wb") as f:
            writer.write(f)

        st.success("Merged Successfully")

        with open("merged.pdf", "rb") as f:
            st.download_button(
                "Download PDF",
                f,
                "merged.pdf"
            )

# ---------------- EXTRACT ----------------
elif menu == "Extract PDF Pages":

    pdf = st.file_uploader("Upload PDF", type="pdf")

    if pdf:
        page = st.number_input("Page Number", 1, 100, 1)

        if st.button("Extract"):

            reader = PdfReader(pdf)
            writer = PdfWriter()

            writer.add_page(reader.pages[page-1])

            with open("page.pdf", "wb") as f:
                writer.write(f)

            st.success("Page Extracted")

# ---------------- WORD ----------------
elif menu == "Read Word File":

    doc = st.file_uploader("Upload Word File", type="docx")

    if doc:
        document = Document(doc)

        text = ""

        for para in document.paragraphs:
            text += para.text + "\n"

        st.text_area("Content", text, height=300)

# ---------------- TRANSLATE ----------------
elif menu == "Translate Text":

    text = st.text_area("Enter Text")

    lang = st.selectbox(
        "Language",
        ["hi", "kn", "ta", "te", "fr", "es"]
    )

    if st.button("Translate"):

        translator = Translator()

        result = translator.translate(text, dest=lang)

        st.success(result.text)

# ---------------- AUDIO ----------------
elif menu == "Generate Audio":

    text = st.text_area("Enter Text")

    if st.button("Generate Audio"):

        tts = gTTS(text)

        tts.save("audio.mp3")

        audio = open("audio.mp3", "rb")

        st.audio(audio.read())

        audio.seek(0)

        st.download_button(
            "Download MP3",
            audio,
            "audio.mp3"
        )
