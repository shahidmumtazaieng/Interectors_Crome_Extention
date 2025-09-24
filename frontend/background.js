// Background script to handle API requests without CORS issues

// Configuration - Set to false for production deployment
const IS_LOCAL_DEVELOPMENT = false;

// API URL Configuration - Update this with your actual API server URL after deployment
const API_SERVER_URL = IS_LOCAL_DEVELOPMENT 
  ? "http://localhost:8000" 
  : "https://interectorscromeextention-igrjcyl4beuxpt2xof4kmq.streamlit.app";

// Listen for messages from popup
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.action === "summarize") {
    summarizePage(request.url)
      .then(result => sendResponse({ success: true, data: result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep the message channel open for async response
  } else if (request.action === "askQuestion") {
    askQuestion(request.url, request.question)
      .then(result => sendResponse({ success: true, data: result }))
      .catch(error => sendResponse({ success: false, error: error.message }));
    return true; // Keep the message channel open for async response
  }
});

// Function to summarize the current page
async function summarizePage(url) {
  try {
    const response = await fetch(`${API_SERVER_URL}/summarize`, {
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
    
    return data;
  } catch (error) {
    console.error("Summarize API Error:", error);
    throw error;
  }
}

// Function to ask questions about the current page
async function askQuestion(url, question) {
  try {
    const response = await fetch(`${API_SERVER_URL}/qa`, {
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
    
    return data;
  } catch (error) {
    console.error("Q&A API Error:", error);
    throw error;
  }
}