import streamlit as st
from PIL import Image
import pytesseract
import google.generativeai as genai

genai.configure(api_key="AIzaSyD7fq_XHMUY3CkOlD6vRmYKiFzRIuoiook")
model = genai.GenerativeModel("gemini-2.5-flash")
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="MCQ Solver", layout="wide")
st.title("📚 Real-Time MCQ Solver")

img_file = st.camera_input("Capture your MCQ question")
prompt_text = st.text_area("Extra instructions (optional)", placeholder="E.g., solve the MCQ and return answer letter + option")

if img_file:
    img = Image.open(img_file)

    question_text = pytesseract.image_to_string(img).strip()


    if not question_text:
        st.error("No text detected")
    else:
            prompt = f"You are an MCQ solver. Answer the following question concisely. Only return the correct answer letter and option.\n\nQuestion: {question_text}\nInstructions: {prompt_text}"
            with st.spinner("Solving..."):
                response = model.generate_content(prompt)
                st.subheader("Answer")
                st.success(response.text.strip())
