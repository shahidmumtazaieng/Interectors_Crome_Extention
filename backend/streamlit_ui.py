import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
import asyncio
from dotenv import load_dotenv
import json
import sys
import os

# Load environment variables
load_dotenv()

# Check if this is an API request (when running as a module)
if "STREAMLIT_API_MODE" in os.environ:
    # API mode - handle requests directly
    import sys
    import json
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    
    app = Flask(__name__)
    CORS(app, origins=["chrome-extension://*"])
    
    # Initialize with API key from environment
    API_KEY = os.getenv("GOOGLE_API_KEY", True)
    
    # Function to load and process web page
    async def process_web_page(url: str) -> str:
        """Load and extract text from a web page"""
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()
            return "\n".join([doc.page_content for doc in documents])
        except Exception as e:
            raise Exception(f"Error loading page: {str(e)}")

    # Function to summarize text
    def summarize_text(text: str) -> str:
        """Generate a summary of the provided text"""
        try:
            if not API_KEY:
                raise Exception("Google API key not configured")
                
            model = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=API_KEY
            )
            summary_prompt = PromptTemplate(
                template="Summarize the following web page content in under 200 words:\n\n{text}",
                input_variables=['text']
            )
            summarize_chain = summary_prompt | model | StrOutputParser()
            return summarize_chain.invoke({"text": text})
        except Exception as e:
            raise Exception(f"Error summarizing text: {str(e)}")

    # Function to answer questions
    def answer_question(text: str, question: str) -> str:
        """Answer a question based on the provided text"""
        try:
            if not API_KEY:
                raise Exception("Google API key not configured")
                
            model = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=API_KEY
            )
            qa_prompt = PromptTemplate(
                template="Use the following content to answer the question.\n\nContent:\n{text}\n\nQuestion: {question}\n\nAnswer:",
                input_variables=['text', 'question']
            )
            qa_chain = qa_prompt | model | StrOutputParser()
            return qa_chain.invoke({"text": text, "question": question})
        except Exception as e:
            raise Exception(f"Error answering question: {str(e)}")

    @app.route('/summarize', methods=['POST'])
    def summarize_endpoint():
        """API endpoint for summarizing web pages"""
        try:
            data = request.get_json()
            url = data.get('url')
            
            if not url:
                return jsonify({"error": "URL is required"}), 400
            
            # Process the web page
            page_text = asyncio.run(process_web_page(url))
            if not page_text:
                return jsonify({"error": "Failed to load page content"}), 500
            
            # Generate summary
            summary = summarize_text(page_text)
            return jsonify({"summary": summary})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/qa', methods=['POST'])
    def qa_endpoint():
        """API endpoint for answering questions about web pages"""
        try:
            data = request.get_json()
            url = data.get('url')
            question = data.get('question')
            
            if not url or not question:
                return jsonify({"error": "URL and question are required"}), 400
            
            # Process the web page
            page_text = asyncio.run(process_web_page(url))
            if not page_text:
                return jsonify({"error": "Failed to load page content"}), 500
            
            # Generate answer
            answer = answer_question(page_text, question)
            return jsonify({"answer": answer})
        
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    @app.route('/health', methods=['GET'])
    def health_check():
        """Health check endpoint"""
        return jsonify({"status": "healthy"}), 200

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 8000))
        app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Streamlit UI mode
    import streamlit as st
    from langchain_community.document_loaders import WebBaseLoader
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain_core.prompts import PromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    import asyncio
    from dotenv import load_dotenv

    # Load environment variables
    load_dotenv()

    # Set page config
    st.set_page_config(
        page_title="Interectors API",
        page_icon="🤖",
        layout="centered"
    )

    # Title
    st.title("🤖 Interectors - Web Page Analysis API")

    # Initialize session state
    if "api_key" not in st.session_state:
        st.session_state.api_key = ""

    # Try to get API key from environment variables (for Streamlit deployment)
    if not st.session_state.api_key:
        st.session_state.api_key = True

    # Sidebar for API key
    with st.sidebar:
        st.header("🔑 API Configuration")
        st.session_state.api_key = st.text_input("Google Generative AI API Key", type="password")
        st.markdown("[Get your API key here](https://makersuite.google.com/app/apikey)")
        
        st.divider()
        st.header("📚 How to Use")
        st.markdown("""
        1. Enter your Google API key
        2. Deploy this app to Streamlit
        3. Update your Chrome extension with the Streamlit URL
        4. Install and use the extension!
        """)

    # Main content
    st.markdown("This API provides web page summarization and Q&A capabilities for the Interectors Chrome extension.")

    # Add CORS information
    st.markdown(
        """
        <style>
        .cors-info {
            background-color: #f0f8ff;
            border: 1px solid #1e90ff;
            border-radius: 5px;
            padding: 10px;
            margin: 10px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="cors-info">
        <h3>🔧 CORS Configuration</h3>
        <p>To use this API with your Chrome extension, ensure your requests include these headers:</p>
        <pre>
        headers: {
            "Content-Type": "application/json",
        }
        </pre>
        </div>
        """,
        unsafe_allow_html=True
    )

    # API endpoints documentation
    st.header("🌐 API Endpoints")

    # Summarization endpoint
    with st.expander("📄 Summarization Endpoint"):
        st.markdown("""
        **Endpoint:** `/summarize`
        
        **Method:** POST
        
        **Request Body:**
        ```json
        {
            "url": "https://example.com"
        }
        ```
        
        **Response:**
        ```json
        {
            "summary": "Page summary here..."
        }
        ```
        """)

    # QA endpoint
    with st.expander("❓ Q&A Endpoint"):
        st.markdown("""
        **Endpoint:** `/qa`
        
        **Method:** POST
        
        **Request Body:**
        ```json
        {
            "url": "https://example.com",
            "question": "Your question here?"
        }
        ```
        
        **Response:**
        ```json
        {
            "answer": "Answer to your question..."
        }
        ```
        """)

    # Function to load and process web page
    async def process_web_page(url: str) -> str:
        """Load and extract text from a web page"""
        try:
            loader = WebBaseLoader(url)
            documents = loader.load()
            return "\n".join([doc.page_content for doc in documents])
        except Exception as e:
            st.error(f"Error loading page: {str(e)}")
            return ""

    # Function to summarize text
    def summarize_text(text: str) -> str:
        """Generate a summary of the provided text"""
        try:
            model = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=st.session_state.api_key
            )
            summary_prompt = PromptTemplate(
                template="Summarize the following web page content in under 200 words:\n\n{text}",
                input_variables=['text']
            )
            summarize_chain = summary_prompt | model | StrOutputParser()
            return summarize_chain.invoke({"text": text})
        except Exception as e:
            st.error(f"Error summarizing text: {str(e)}")
            return "Failed to generate summary."

    # Function to answer questions
    def answer_question(text: str, question: str) -> str:
        """Answer a question based on the provided text"""
        try:
            model = ChatGoogleGenerativeAI(
                model="gemini-pro",
                google_api_key=st.session_state.api_key
            )
            qa_prompt = PromptTemplate(
                template="Use the following content to answer the question.\n\nContent:\n{text}\n\nQuestion: {question}\n\nAnswer:",
                input_variables=['text', 'question']
            )
            qa_chain = qa_prompt | model | StrOutputParser()
            return qa_chain.invoke({"text": text, "question": question})
        except Exception as e:
            st.error(f"Error answering question: {str(e)}")
            return "Failed to generate answer."

    # Test section
    st.header("🧪 Test the API")

    # Test URL input
    test_url = st.text_input("Enter a URL to test:", "https://example.com")

    if st.session_state.api_key:
        if st.button("Test Summarization"):
            if test_url:
                with st.spinner("Loading and summarizing page..."):
                    page_text = asyncio.run(process_web_page(test_url))
                    if page_text:
                        summary = summarize_text(page_text)
                        st.subheader("Summary")
                        st.write(summary)
            else:
                st.warning("Please enter a URL")

        # Test QA
        test_question = st.text_input("Enter a question about the page:")
        if st.button("Test Q&A"):
            if test_url and test_question:
                with st.spinner("Loading page and generating answer..."):
                    page_text = asyncio.run(process_web_page(test_url))
                    if page_text:
                        answer = answer_question(page_text, test_question)
                        st.subheader("Answer")
                        st.write(answer)
            else:
                st.warning("Please enter both a URL and a question")

    else:
        st.warning("Please enter your Google Generative AI API key in the sidebar to test the functionality.")

    # Instructions for deployment
    st.header("🚀 Deployment Instructions")

    st.markdown("""
    1. **Get your Google API Key:**
       - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
       - Create an API key and copy it

    2. **Deploy to Streamlit:**
       - Push this code to a GitHub repository
       - Go to [Streamlit Community Cloud](https://streamlit.io/cloud)
       - Create a new app and connect it to your GitHub repository
       - Deploy the app

    3. **Configure Chrome Extension:**
       - Update the API URLs in `popup.js` with your Streamlit app URL
       - Package the extension and upload to Chrome Web Store

    4. **Using the Extension:**
       - Install the extension from Chrome Web Store
       - Navigate to any webpage
       - Click the extension icon
       - Use the summary and Q&A features
    """)

    # Footer
    st.divider()
    st.markdown(
        """
        <div style="text-align: center; padding: 10px;">
            Made with ❤️ using Langchain, Streamlit, and Google Gemini
        </div>
        """,
        unsafe_allow_html=True
    )