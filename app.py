from dotenv import load_dotenv

load_dotenv()

import io
import streamlit as st
import os
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai


genai.configure(api_key=os.getenv("Google_API_Key"))


def get_gemini_response(input,pdf_content,prompt):
    model = genai.GenerativeModel('gemini-1.5-flash')
    response= model.generate_content([input,pdf_content[0],prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        ##convert pdf to img
        images =pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        #convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format='JPEG')
        img_byte_arr = img_byte_arr.getvalue()
        
        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # encode to base64
            }
        ]
        return pdf_parts
    else: 
        raise FileNotFoundError("No file uploaded")
    
    
##Steamlit APP

st.set_page_config(page_title="PDF_QueryAI")
st.header("Query your documents using AI")
uploaded_file = st.file_uploader("Upload your document(pdf format)",type=["pdf"])
input_text=st.text_area("Your Query: " ,key="input") #JD input


if uploaded_file is not None:
    st.write("Document Uploaded Successfully")
    
submit1 = st.button("Search")


input_prompt1 = """
 You are an expert AI assistant skilled at reading and understanding documents.
 You will be provided with the text of a PDF file, and your job is to answer any questions based on the content. 
 If the information is not available in the PDF, clearly state so.
"""



if submit1:
    if uploaded_file is not None:
        pdf_content=input_pdf_setup(uploaded_file)
        response=get_gemini_response(input_prompt1,pdf_content,input_text)
        st.subheader("Response")
        st.write(response)
    else:
        st.write("Please upload the document")



    
        