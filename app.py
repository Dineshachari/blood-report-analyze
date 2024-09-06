import streamlit as st
import os
import pytesseract
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
from io import BytesIO
from database import save_to_database, get_report_from_database
from analysis import generate_report_stats, create_visualizations

# Load environment variables from .env file
load_dotenv()

# Configure the Gemini API
genai.configure(api_key=os.getenv("API_KEY"))
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

st.title("Blood Test Report Analyzer")

uploaded_file = st.file_uploader("Choose a file", type=["pdf", "jpg", "png"])

def extract_text_from_pdf(pdf_file):
    import fitz  # PyMuPDF
    pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in pdf_document:
        text += page.get_text()
    return text

def extract_text_from_image(image_file):
    import pytesseract
    image = Image.open(image_file)
    return pytesseract.image_to_string(image)

def convert_text_to_json(text):
    prompt = f"Convert the following blood test report to a JSON format with key-value pairs:\n\n{text}"
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text  # Adjust this line based on the response format

if uploaded_file:
    if uploaded_file.type == "application/pdf":
        text = extract_text_from_pdf(uploaded_file)
    else:
        text = extract_text_from_image(uploaded_file)
    
    json_data = convert_text_to_json(text)
    save_to_database(json_data)
    st.success("Report saved successfully!")

report_id = st.number_input("Enter Report ID to Retrieve", min_value=1)

if st.button("Get Report"):
    json_data = get_report_from_database(report_id)
    if json_data:
        stats = generate_report_stats(json_data)
        create_visualizations(stats)
        st.image('visualization.png')
        st.write("Report Analysis:")
        st.write(stats)
    else:
        st.error("Report not found.")
