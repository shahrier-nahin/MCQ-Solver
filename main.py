import streamlit as st
from PIL import Image
import google.generativeai as genai

# Configure API


genai.configure(api_key=st.secrets["GENAI_API_KEY"])
model = genai.GenerativeModel("gemini-2.0-flash")

st.set_page_config(page_title="MCQ Solver", layout="wide")
st.title("📚 MCQ Solver")

# Camera input
img_file = st.camera_input("Capture your MCQ question")

# Extra instructions
prompt_text = st.text_area("Extra instructions (optional)",
                           placeholder="E.g., solve the MCQ and return answer letter + option")

if img_file:
    img = Image.open(img_file)
   # st.image(img, caption="Captured Image", use_container_width=True)

    # Extract text using Gemini Vision
    with st.spinner("Extracting text..."):
        extraction_prompt = "Extract and read ALL text from this image. Return only the text content exactly as it appears."
        extraction_response = model.generate_content([extraction_prompt, img])
        question_text = extraction_response.text.strip()

    if not question_text:
        st.error("No text detected")
    else:
        st.success("✅ Text extracted successfully")

        # Solve the MCQ
        with st.spinner("Solving..."):
            solve_prompt = f"You are an MCQ solver. Answer the following question concisely. Only return the correct answer letter and option.\n\nQuestion: {question_text}\nInstructions: {prompt_text}"
            response = model.generate_content(solve_prompt)

            st.subheader("Answer")
            st.success(response.text.strip())