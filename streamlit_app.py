from bs4 import BeautifulSoup
import streamlit as st
import requests
import validators
import PyPDF2
from io import BytesIO

API_URL = "http://77.68.97.97:5000"  # Replace with your API's base URL

def main():
    st.title("Scrape a website and chat to it")

    api_key = st.text_input("OPENAI API Key - https://platform.openai.com/account/", value='', max_chars=100)

    if st.button("Submit API Key"):
        if api_key:
            data = {"api_key": api_key}
            response = requests.post(f"{API_URL}/api/set-api-key", json=data)

            if response.status_code == 200:
                st.success("API Key submitted successfully.")
            else:
                error_message = response.json().get("error", "Failed to submit API Key.")
                st.error(error_message)
        else:
            st.error("Please fill in the API Key field before submitting.")
            
    url = st.text_input("URL (Some Websites dont work - I'm working on the problem)", value='', max_chars=1000)
    
    if st.button("Submit URL"):
        if url:
            if not validators.url(url):
                st.warning("Please enter a valid URL.")
                return
            
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {"url": url}
            
            with st.spinner("Scraping URLs..."):
                response = requests.post(f"{API_URL}/api/update-loader", json=data, headers=headers)

            if response.status_code == 200:
                scraped_urls = response.json().get("scraped_urls", [])
                st.success("URL submitted successfully.")
                st.write("Scraped URLs:")
                for scraped_url in scraped_urls:
                    st.write(scraped_url)
            else:
                error_message = response.json().get("error", "Failed to submit URL.")
                st.error(error_message)
        else:
            st.error("Please fill in the URL field before submitting.")

    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if uploaded_file is not None:
        with st.spinner("Uploading PDF..."):
            file_bytes = BytesIO(uploaded_file.getvalue())
            pdf_reader = PyPDF2.PdfFileReader(file_bytes)

            pdf_text = []
            for page_num in range(pdf_reader.numPages):
                page = pdf_reader.getPage(page_num)
                text = page.extractText()
                pdf_text.append(text)

            pdf_content = " ".join(pdf_text)

            headers = {"Authorization": f"Bearer {api_key}"}
            data = {"text": pdf_content}

            response = requests.post(f"{API_URL}/api/update-loader", json=data, headers=headers)

            if response.status_code == 200:
                st.success("PDF uploaded successfully.")
            else:
                error_message = response.json().get("error", "Failed to upload PDF.")
                st.error(error_message)

    question = st.text_input("Question", value='', max_chars=1000)
    
    if st.button("Ask Question"):
        if question:
            if not api_key:
                st.warning("Please enter an API Key before asking a question.")
                return
                
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {"question": question}
            
            with st.spinner("Generating response..."):
                response = requests.post(f"{API_URL}/api/ask", json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                st.write(f"Response: {response_data['response']}")
            else:
                error_message = response.json().get("error", "Failed to get a response for the question.")
                st.error(error_message)
        else:
            st.error("Please fill in the Question field before submitting.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        st.error("An error occurred: " + str(e))
