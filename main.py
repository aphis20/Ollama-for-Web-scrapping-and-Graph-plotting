import streamlit as st
from scrape import (
    scrape_website,
    extract_body_content,
    clean_body_content,
    split_dom_content,
)
from parse import parse_with_ollama

# Streamlit UI
st.title("AI Web Scraper")

url = st.text_input("Enter Website URL")

# Step 1: Scrape the Website
if st.button("Scrape Website"):
    if url:
        st.write("Scraping the website...")
        
        try:
            # Scrape the website
            dom_content = scrape_website(url)
            body_content = extract_body_content(dom_content)
            cleaned_content = clean_body_content(body_content)

            # Store the DOM content in Streamlit session state
            st.session_state.dom_content = cleaned_content

            # Display the DOM content in an expandable text box
            with st.expander("View DOM Content"):
                st.text_area("DOM Content", cleaned_content, height=300)

        except Exception as e:
            st.error(f"An error occurred while scraping: {str(e)}")
    else:
        st.warning("Please enter a valid URL!")

# Step 2: Ask Questions About the DOM Content
if "dom_content" in st.session_state:
    parse_description = st.text_area("Describe what you want to parse")

    if st.button("Parse Content"):
        if parse_description:
            st.write("Parsing the content...")

            try:
                # Parse the content with Ollama
                dom_chunks = split_dom_content(st.session_state.dom_content)
                
                # Add a progress bar
                progress_bar = st.progress(0)
                parsed_results = []

                for i, chunk in enumerate(dom_chunks, start=1):
                    parsed_result = parse_with_ollama([chunk], parse_description)
                    parsed_results.append(parsed_result)

                    # Update the progress bar
                    progress_bar.progress(i / len(dom_chunks))

                st.write("\n".join(parsed_results))

            except Exception as e:
                st.error(f"An error occurred while parsing: {str(e)}")
        else:
            st.warning("Please provide a parse description.")
