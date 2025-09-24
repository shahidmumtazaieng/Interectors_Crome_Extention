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
    const summarizeBtn = document.getElementById("summarizeBtn");
    summarizeBtn.disabled = true;
    summarizeBtn.innerHTML = 'Generating...';
    
    showLoading('summary');
    const url = await getCurrentTabUrl();
    
    // Send message to background script
    const response = await chrome.runtime.sendMessage({
      action: "summarize",
      url: url
    });
    
    if (!response.success) {
      throw new Error(response.error);
    }
    
    document.getElementById("summary").innerHTML = `<p>${response.data.summary}</p>`;
  } catch (error) {
    handleApiError('summary', error);
  } finally {
    const summarizeBtn = document.getElementById("summarizeBtn");
    summarizeBtn.disabled = false;
    summarizeBtn.innerHTML = 'Regenerate Summary';
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
    
    const qaBtn = document.getElementById("qa-btn");
    const qaInput = document.getElementById("qa-input");
    
    qaBtn.disabled = true;
    qaBtn.innerHTML = '...';
    qaInput.disabled = true;
    
    showLoading('qa-content');
    const url = await getCurrentTabUrl();
    
    // Send message to background script
    const response = await chrome.runtime.sendMessage({
      action: "askQuestion",
      url: url,
      question: question
    });
    
    if (!response.success) {
      throw new Error(response.error);
    }
    
    // Add the Q&A response to the content
    const currentContent = document.getElementById("qa-content").innerHTML;
    const emptyState = document.getElementById("qa-content").querySelector('.empty-state');
    
    if (emptyState) {
      document.getElementById("qa-content").innerHTML = '';
    }
    
    const responseDiv = document.createElement('div');
    responseDiv.className = 'qa-response';
    responseDiv.innerHTML = `
      <div class="qa-question">Q: ${question}</div>
      <div>A: ${response.data.answer}</div>
    `;
    document.getElementById("qa-content").insertBefore(responseDiv, document.getElementById("qa-content").firstChild);
    
    // Clear input and reset button
    document.getElementById("qa-input").value = '';
  } catch (error) {
    handleApiError('qa-content', error);
  } finally {
    const qaBtn = document.getElementById("qa-btn");
    const qaInput = document.getElementById("qa-input");
    qaBtn.disabled = false;
    qaBtn.innerHTML = 'Ask';
    qaInput.disabled = false;
    qaInput.focus();
  }
}

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("summarizeBtn").addEventListener("click", summarizePage);
  document.getElementById("qa-btn").addEventListener("click", askQuestion);
  
  // Allow Enter key to submit question
  document.getElementById("qa-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      askQuestion();
    }
  });
});