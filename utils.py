import os
import fitz
from langchain.text_splitter import RecursiveCharacterTextSplitter
from openai import AzureOpenAI
from config import ENDPOINT, DEPLOYMENT, SUBSCRIPTION_KEY, API_VERSION
from dotenv import load_dotenv

load_dotenv()

client = AzureOpenAI(
    api_version=API_VERSION,
    azure_endpoint=ENDPOINT,
    api_key=SUBSCRIPTION_KEY,
)

def get_pdf_content_from_doc_folder(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The specified file does not exist: {file_path}")
    if not file_path.endswith('.pdf'):
        raise ValueError("The specified file is not a PDF document.")
    try:
        plain_text = ""
        with fitz.open(file_path) as doc:
            for page in doc:
                text = page.get_text("text")
                plain_text += " ".join(text.splitlines()) + "\n"
        return plain_text.strip()
    except Exception as e:
        raise RuntimeError(f"An error occurred while reading the PDF file: {e}")

def chunk_text_with_langchain(text, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    return text_splitter.split_text(text)

def get_summaries_for_chunks(chunks, model=DEPLOYMENT, max_tokens=200):
    prompt = """
        You are an expert document analyst trained in legal, technical, financial, medical, and business document analysis. Given a document enclosed in triple quotes, extract every possible key and highly important detail from it, including but not limited to:

            1. Named Entities: List all people, organizations, locations, laws, companies, and products mentioned.

            2. Dates & Timelines: Capture all relevant dates, deadlines, timelines, and durations.

            3. Numerical Data: Extract all financial figures, percentages, units, and any numerical metrics with their context.

            4. Critical Events & Actions: Identify decisions, actions taken, responsibilities, and events with high impact.

            5. Stakeholders & Roles: Identify all involved parties and their roles or responsibilities.

            6. Conditions & Requirements: Note any rules, conditions, constraints, terms, or eligibility criteria.

            7. Risks or Warnings: Extract any warnings, limitations, disclaimers, penalties, or risk-related content.

            8. Outcomes or Deliverables: Identify expected outputs, conclusions, approvals, or deliverables.

            9. Hidden or Implied Information: Surface any implications, assumptions, or unstated insights.

            10. Summary of Intent: Give a one-paragraph summary of the document's main goal or purpose.

        Output must be structured under clear headings with bullet points for each category. Prioritize accuracy, completeness, and clarity. If the document is incomplete or ambiguous, infer conservatively and label assumptions clearly.
        
        Follow above instructions carefully and provide a comprehensive analysis.
        """
        
    summaries = []
    for chunk in chunks:
        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": chunk}
                ],
                max_tokens=max_tokens,
                temperature=0.5,
            )
            summary = response.choices[0].message.content.strip()
            summaries.append(summary)
        except Exception as e:
            summaries.append(f"Error: {e}")

    # Final summary of all chunk summaries
    final_prompt = """
        You are an expert summarizer. Given the following multiple detailed analyses of document chunks, synthesize them into a single, concise, and comprehensive summary. 
        - Remove redundancies.
        - Highlight the most important and recurring points.
        - Structure the output under clear headings as before.
        - Provide a one-paragraph summary of the overall document's main goal or purpose at the end.
        Here are the chunk analyses:
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": final_prompt},
                {"role": "user", "content": "\n\n".join(summaries)}
            ],
            max_tokens=max_tokens * 2,
            temperature=0.5,
        )
        final_summary = response.choices[0].message.content.strip()
    except Exception as e:
        final_summary = f"Error during final summarization: {e}"

    return summaries, final_summary

# # Example usage:
# pdf_directory = 'call_doc_ai/doc'
# pdf_paths = [os.path.join(pdf_directory, file) for file in os.listdir(pdf_directory) if file.endswith('.pdf')]
# text = get_pdf_content_from_doc_folder(pdf_paths[0])  # Assuming you want to read the first PDF file
# print(text)

# chunks = chunk_text_with_langchain(text)
# print(f"Number of chunks: {len(chunks)}")
# for i in chunks:
#     print(i)
    
# # Summarize the chunks
# summaries = get_summaries_for_chunks(chunks)
# print(f"Number of summaries: {len(summaries)}")
# for summary in summaries:
#     print(summary)