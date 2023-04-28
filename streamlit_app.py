import streamlit as st
import requests

API_URL = "http://localhost:5000"  # Replace with your API's base URL

def main():
    st.title("API Key and URL Input App")

    api_key = st.text_input("API Key", value='', max_chars=50, type='password')
    url = st.text_input("URL", value='', max_chars=1000)
    question = st.text_input("Question", value='', max_chars=1000)

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
