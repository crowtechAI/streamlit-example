import streamlit as st

def main():
    st.title("API Key and URL Input App")

    api_key = st.text_input("API Key", value='', max_chars=50, type='password')
    url = st.text_input("URL", value='', max_chars=1000)

    if st.button("Submit"):
        if api_key and url:
            st.success("API Key and URL submitted successfully.")
            st.write(f"API Key: {api_key}")
            st.write(f"URL: {url}")
        else:
            st.error("Please fill in both input fields before submitting.")

if __name__ == "__main__":
    main()
