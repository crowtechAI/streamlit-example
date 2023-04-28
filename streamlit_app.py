from dotenv import load_dotenv
import streamlit as st
import requests

API_BASE_URL=http://77.68.97.97:5000

def main():
    st.title("Query Your Website")

    api_key = st.text_input("API Key", value='', max_chars=100)
    
    

    if st.button("Submit API Key"):
        if api_key:
            data = {"api_key": api_key}
            response = requests.post(f"{API_URL}/api/set-api-key", json=data)

            if response.status_code == 200:
                st.success("API Key submitted successfully.")
            else:
                st.error("Failed to submit API Key.")
        else:
            st.error("Please fill in the API Key field before submitting.")
            
    url = st.text_input("URL", value='', max_chars=1000)
    
    if st.button("Submit URL"):
        if url:
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {"url": url}
            response = requests.post(f"{API_URL}/api/update-loader", json=data, headers=headers)

            if response.status_code == 200:
                st.success("URL submitted successfully.")
            else:
                st.error("Failed to submit URL.")
        else:
            st.error("Please fill in the URL field before submitting.")
            
    question = st.text_input("Question", value='', max_chars=1000)
    
    if st.button("Ask Question"):
        if question:
            headers = {"Authorization": f"Bearer {api_key}"}
            data = {"question": question}
            response = requests.post(f"{API_URL}/api/ask", json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                st.write(f"Response: {response_data['response']}")
            else:
                st.error("Failed to get a response for the question.")
        else:
            st.error("Please fill in the Question field before submitting.")

if __name__ == "__main__":
    main()
