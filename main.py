import os
import openai
import streamlit as st
headers={
    openai.api_key = st.secrets[“auth_key”]
}

from PyPDF2 import PdfReader
from dotenv import load_dotenv
load_dotenv()

openai.api_key=os.getenv("OPENAI_API_KEY")
def load_files():
    text=""
    data_dir=os.path.join(os.getcwd(), "data")
    for filename in os.listdir(data_dir):
        if filename.endswith(".txt"):
            with open(os.path.join(data_dir,filename),"r")as f:
                text+=f.read()
    return text

def extract_text_from_pdf(pdf_file):
    reader=PdfReader(pdf_file)
    raw_text=""
    for page in reader.pages:
        content=page.extract_text()
        if content:
            raw_text+=content
    return raw_text

def get_response(text):
    prompt= f"""
            You are a Health Consultant expert. Upon receiving a text enclosed by four backquotes, 
            provide optimal recommendations for resolving the stated problem and include an uplifting quote to inspire positive energy.

            text: ''''{text}'''' 
            """
    response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role":"system",
                "content":prompt,
            },
        ],
    )
    return response["choices"][0]["message"]["content"]
def main():

    st.set_page_config(
        page_title="SpeakWithout Limits",
        page_icon="🤝"
        
    )
    st.title("SpeakWithout Limits app")
    st.write("This app utilizes OpenAI's GPT-3 to empower users to freely express their thoughts and problems within a given text or PDF file.")
    st.divider()

    option=st.radio("Select Input Type",("Text","PDF"))
    if option =="Text":
        user_input=st.text_area("Write your feelings","")

        if st.button("Submit")and user_input !="":
            response=get_response(user_input)
            st.subheader("You are free now")
            st.markdown(f">{response}")
        else:
            st.error("Please enter text.")
    else:
        uploaded_file=st.file_uploader("Choose a PDF file", type="pdf")
        if st.button("Submit")and uploaded_file is not None:
            text=extract_text_from_pdf(uploaded_file)

            response=get_response(text=text)
            st.subheader("You are free now")
            st.markdown(f">{response}")
        else:
            st.error("Please upload a PDF file.")


if __name__=="__main__":
    main()
