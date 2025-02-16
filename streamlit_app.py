from bs4 import BeautifulSoup
import streamlit as st
import requests
import validators

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
            
    st.title("Choose either a URL to scrape or upload a PDF (depending on the size of the PDF it can take a while)")
            
    url = st.text_input("URL (Some Websites dont work - I'm working on the problem)", value='', max_chars=1000)
    uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

    if st.button("Submit URL"):
        if url:
            if not validators.url(url):
                st.warning("Please enter a valid URL.")
            else:
                headers = {"Authorization": f"Bearer {api_key}"}
                data = {"url": url}

                with st.spinner("Scraping URLs..."):
                    response = requests.post(f"{API_URL}/api/update-loader", data=data, headers=headers)

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
            st.warning("Please enter a URL before submitting.")

    if st.button("Upload PDF"):
        if uploaded_file is not None:
            headers = {"Authorization": f"Bearer {api_key}"}
            files = {"pdf": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}

            with st.spinner("Uploading PDF..."):
                response = requests.post(f"{API_URL}/api/update-loader", files=files, headers=headers)

            if response.status_code == 200:
                scraped_urls = response.json().get("scraped_urls", [])
                st.success("PDF uploaded successfully.")
                st.write("Scraped URLs:")
                for scraped_url in scraped_urls:
                    st.write(scraped_url)
            else:
                error_message = response.json().get("error", "Failed to upload PDF.")
                st.error(error_message)
        else:
            st.warning("Please choose a PDF file to upload.")


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
