import torch
# Safe workaround: try accessing it in a dummy try/except
try:
    _ = dir(torch.classes)  # Don't print or return this!
except Exception:
    pass

import streamlit as st
from summarizer.text_summarizer import summarize_text
from summarizer.document_parser import extract_text_from_pdf, extract_text_from_docx
from summarizer.video_summarizer import get_video_id, get_transcript

st.set_page_config(page_title="Text & Video Summarizer", layout="centered")

st.title("📄🎥 Text & Video Summarizer")

# Upload document
uploaded_file = st.file_uploader("Upload a document (PDF, DOCX, TXT)", type=["pdf", "docx", "txt"])

input_text = ""

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        input_text = extract_text_from_pdf(uploaded_file)
    elif uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        input_text = extract_text_from_docx(uploaded_file)
    elif uploaded_file.type == "text/plain":
        input_text = str(uploaded_file.read(), "utf-8")

if input_text:
    st.subheader("📝 Extracted Text")
    st.write(input_text[:1000])

    if st.button("Summarize Document"):
        with st.spinner("Summarizing..."):
            summary = summarize_text(input_text)
            st.subheader("📌 Summary")
            st.write(summary)

# YouTube Video Input
st.markdown("---")
st.subheader("📺 Summarize YouTube Video")

video_url = st.text_input("Enter YouTube Video URL")

if video_url:
    video_id = get_video_id(video_url)
    if video_id:
        try:
            transcript = get_transcript(video_id)
            st.subheader("🗒 Transcript Preview")
            st.write(transcript[:1000])
            if st.button("Summarize Video"):
                with st.spinner("Summarizing..."):
                    summary = summarize_text(transcript)
                    st.subheader("📌 Video Summary")
                    st.write(summary)
        except Exception as e:
            st.error(f"Error fetching transcript: {e}")
    else:
        st.error("Invalid YouTube URL")
