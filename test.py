import streamlit as st
import os
import shutil

from utils import chunk_text_with_langchain, get_pdf_content_from_doc_folder, get_summaries_for_chunks

DOC_FOLDER = "doc"

def prepare_doc_folder(folder_path):
    if os.path.exists(folder_path):
        # Clear the folder
        shutil.rmtree(folder_path)
    os.makedirs(folder_path)

def save_uploaded_file(uploaded_file, folder_path):
    file_path = os.path.join(folder_path, uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return file_path

def main():
    # Configure page for responsive design
    st.set_page_config(
        page_title="PDF Summarization App",
        page_icon="📄",
        layout="wide",
        initial_sidebar_state="auto"
    )
    
    # Custom CSS for mobile responsiveness
    st.markdown("""
    <style>
    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }
    
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
        .stButton > button {
            width: 100%;
        }
    }
    
    .stFileUploader > div {
        margin-bottom: 1rem;
    }
    
    .refresh-button {
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header section
    col1, col2 = st.columns([3, 1])
    with col1:
        st.title("📄 Doc Summarization App")
    with col2:
        if st.button("🔄 Refresh", key="refresh_btn", help="Refresh the app"):
            st.rerun()
    
    st.caption("Created By: Anurag Patil / co-founder of Neway Software Corporation")
    
    # File upload section
    st.markdown("---")
    uploaded_file = st.file_uploader(
        "Upload a PDF document", 
        type=["pdf"],
        help="Select a PDF file to upload and summarize"
    )
    
    if uploaded_file is not None:
        with st.spinner("Processing your PDF..."):
            prepare_doc_folder(DOC_FOLDER)
            file_path = save_uploaded_file(uploaded_file, DOC_FOLDER)
            st.success(f"✅ File saved successfully!")
            
            # Progress bar for better UX
            progress_bar = st.progress(0)
            
            # Extract text
            progress_bar.progress(25)
            pdf_directory = file_path
            text = get_pdf_content_from_doc_folder(pdf_directory)
            
            # Chunk text
            progress_bar.progress(50)
            chunks = chunk_text_with_langchain(text)
            st.info(f"📊 Document split into {len(chunks)} chunks")
            
            # Generate summaries
            progress_bar.progress(75)
            summaries = get_summaries_for_chunks(chunks)
            
            progress_bar.progress(100)
            progress_bar.empty()
            
            # Display summary
            st.markdown("---")
            st.subheader("📋 Summary of Uploaded Document")
            
            # Responsive container for summary
            with st.container():
                st.markdown(
                    f"""
                    <div style="
                        background-color: #f0f2f6;
                        padding: 1rem;
                        border-radius: 0.5rem;
                        border-left: 5px solid #1f77b4;
                        margin: 1rem 0;
                    ">
                        {summaries[1]}
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    
    # Footer
    st.markdown("---")
    st.caption("© 2025 Neway Software Corporation. All rights reserved.")

if __name__ == "__main__":
    main()