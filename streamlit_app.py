from bs4 import BeautifulSoup
import streamlit as st
import requests
import validators

API_URL = "http://77.68.97.97:5000"  # Replace with your API's base URL

def main():
    st.title("API Key and URL Input App")

    api_key = st.text_input("API Key", value='', max_chars=100)

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
            
    url = st.text_input("URL", value='', max_chars=1000)
    
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
