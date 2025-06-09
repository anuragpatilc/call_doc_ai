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
        page_title="DOC Summarization App",
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
            padding-left: 0.5rem;
            padding-right: 0.5rem;
            padding-top: 0.5rem;
        }
        .stButton > button {
            width: 100%;
            font-size: 14px;
        }
        .stFileUploader {
            font-size: 14px;
        }
        h1 {
            font-size: 1.5rem !important;
        }
        h2 {
            font-size: 1.2rem !important;
        }
    }
    
    @media (max-width: 480px) {
        .main .block-container {
            padding-left: 0.25rem;
            padding-right: 0.25rem;
        }
        h1 {
            font-size: 1.3rem !important;
        }
    }
    
    .stFileUploader > div {
        margin-bottom: 1rem;
    }
    
    .refresh-button {
        margin-bottom: 1rem;
    }
    
    /* Mobile-friendly summary container */
    .summary-container {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
        word-wrap: break-word;
        overflow-wrap: break-word;
    }
    
    @media (max-width: 768px) {
        .summary-container {
            padding: 0.75rem;
            font-size: 14px;
            line-height: 1.4;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header section - responsive columns
    if st.session_state.get('is_mobile', False) or st.get_option('browser.gatherUsageStats'):
        # Stack vertically on mobile
        st.title("📄 DOC Summarization App")
        if st.button("🔄 Refresh", key="refresh_btn", help="Refresh the app"):
            st.rerun()
    else:
        # Side by side on desktop
        col1, col2 = st.columns([3, 1])
        with col1:
            st.title("📄 DOC Summarization App")
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
            
            # Mobile-friendly summary display
            st.markdown(
                f"""
                <div class="summary-container">
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