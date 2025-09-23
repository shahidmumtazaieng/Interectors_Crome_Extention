// Configuration - Set to false for production deployment
const IS_LOCAL_DEVELOPMENT = false;

// API URL Configuration - Update this with your actual Streamlit app URL after deployment
const STREAMLIT_APP_URL = IS_LOCAL_DEVELOPMENT 
  ? "http://localhost:8000" 
  : "https://your-streamlit-app-url.streamlit.app";

// Function to get the current tab URL
async function getCurrentTabUrl() {
  return new Promise((resolve, reject) => {
    chrome.tabs.query({active: true, currentWindow: true}, function(tabs) {
      if (chrome.runtime.lastError) {
        reject(chrome.runtime.lastError);
      } else if (tabs && tabs[0]) {
        resolve(tabs[0].url);
      } else {
        reject(new Error("No active tab found"));
      }
    });
  });
}

// Function to show loading indicator
function showLoading(elementId) {
  document.getElementById(elementId).innerHTML = '<div class="loading">Processing...</div>';
}

// Function to handle API errors
function handleApiError(elementId, error) {
  console.error("API Error:", error);
  document.getElementById(elementId).innerHTML = `<div class="error">Error: ${error.message || 'Failed to process request'}</div>`;
}

// Function to summarize the current page
async function summarizePage() {
  try {
    showLoading('summary');
    const url = await getCurrentTabUrl();
    
    const response = await fetch(`${STREAMLIT_APP_URL}/summarize`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({url: url})
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    if (data.error) {
      throw new Error(data.error);
    }
    
    document.getElementById("summary").innerHTML = `<p>${data.summary}</p>`;
  } catch (error) {
    handleApiError('summary', error);
  }
}

// Function to ask questions about the current page
async function askQuestion() {
  try {
    const question = document.getElementById("qa-input").value.trim();
    if (!question) {
      alert("Please enter a question");
      return;
    }
    
    showLoading('qa-content');
    const url = await getCurrentTabUrl();
    
    const response = await fetch(`${STREAMLIT_APP_URL}/qa`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        url: url,
        question: question
      })
    });
    
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    if (data.error) {
      throw new Error(data.error);
    }
    
    document.getElementById("qa-content").innerHTML = `<p><strong>Q:</strong> ${question}</p><p><strong>A:</strong> ${data.answer}</p>`;
  } catch (error) {
    handleApiError('qa-content', error);
  }
}

// Event listeners
document.getElementById("summarizeBtn").addEventListener("click", summarizePage);
document.getElementById("qa-btn").addEventListener("click", askQuestion);

// Allow Enter key to submit question
document.getElementById("qa-input").addEventListener("keypress", function(event) {
  if (event.key === "Enter") {
    askQuestion();
  }
});