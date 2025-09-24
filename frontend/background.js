// Background script to handle API requests without CORS issues

// API URL Configuration - Using localhost for local development
const API_SERVER_URL = "http://localhost:8000";  // Changed to localhost

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
  // Removed extractSemanticKeywords handling
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
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
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
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API error: ${response.status} ${response.statusText}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error("Q&A API Error:", error);
    throw error;
  }
}

// Removed extractSemanticKeywords function