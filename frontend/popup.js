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

// Function to show copy notification
function showCopyNotification(message) {
  const notification = document.getElementById('copyNotification');
  notification.textContent = message;
  notification.style.display = 'block';
  
  setTimeout(() => {
    notification.style.display = 'none';
  }, 2000);
}

// Function to convert markdown-like formatting to HTML
function convertMarkdownToHtml(text) {
  if (!text) return '';
  
  // Convert headings (# Heading)
  text = text.replace(/^### (.*$)/gm, '<h3>$1</h3>');
  text = text.replace(/^## (.*$)/gm, '<h2>$1</h2>');
  text = text.replace(/^# (.*$)/gm, '<h1>$1</h1>');
  
  // Convert bold (**text** or __text__)
  text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  text = text.replace(/__(.*?)__/g, '<strong>$1</strong>');
  
  // Convert italic (*text* or _text_)
  text = text.replace(/(?<!\*)\*(?!\*)(.*?)\*(?!\*)/g, '<em>$1</em>');
  text = text.replace(/(?<!_)_(?!_)(.*?)_(?!_)/g, '<em>$1</em>');
  
  // Convert unordered lists (* item)
  text = text.replace(/^\* (.*$)/gm, '<li>$1</li>');
  text = text.replace(/(<li>.*<\/li>)/gs, '<ul>$1</ul>');
  
  // Convert ordered lists (1. item)
  text = text.replace(/^\d+\. (.*$)/gm, '<li>$1</li>');
  text = text.replace(/(<li>.*<\/li>)/gs, '<ol>$1</ol>');
  
  // Convert line breaks to paragraphs
  const paragraphs = text.split('\n\n');
  const formattedParagraphs = paragraphs.map(p => {
    // If paragraph is already wrapped in HTML tags, don't wrap in <p>
    if (p.startsWith('<h') || p.startsWith('<ul') || p.startsWith('<ol')) {
      return p;
    }
    // If paragraph contains list items, don't wrap in <p>
    if (p.includes('<li>')) {
      return p;
    }
    // Wrap in <p> tag
    return `<p>${p}</p>`;
  });
  
  return formattedParagraphs.join('');
}

// Function to create HTML5-based visualization for QA response
function createVisualization(features, probability) {
  // Create visualization container
  const vizContainer = document.createElement('div');
  vizContainer.className = 'visualization-container';
  
  // Add title
  const title = document.createElement('div');
  title.className = 'visualization-title';
  title.textContent = `Relevance Probability: ${(probability * 100).toFixed(1)}%`;
  vizContainer.appendChild(title);
  
  // Create chart container
  const chartContainer = document.createElement('div');
  chartContainer.className = 'chart-container';
  
  // Create chart bars
  const chartData = [
    { label: 'Content-Question', value: features.content_question_similarity, color: '#36a2eb' },
    { label: 'Content-Answer', value: features.content_answer_similarity, color: '#ffce56' },
    { label: 'Question-Answer', value: features.question_answer_similarity, color: '#4bc0c0' }
  ];
  
  chartData.forEach(data => {
    const barContainer = document.createElement('div');
    barContainer.className = 'chart-bar';
    
    const label = document.createElement('div');
    label.className = 'chart-label';
    label.textContent = data.label;
    barContainer.appendChild(label);
    
    const barWrapper = document.createElement('div');
    barWrapper.className = 'chart-bar-container';
    
    const barFill = document.createElement('div');
    barFill.className = 'chart-bar-fill';
    barFill.style.width = `${data.value * 100}%`;
    barFill.style.backgroundColor = data.color;
    barWrapper.appendChild(barFill);
    
    barContainer.appendChild(barWrapper);
    
    const value = document.createElement('div');
    value.className = 'chart-value';
    value.textContent = `${(data.value * 100).toFixed(1)}%`;
    barContainer.appendChild(value);
    
    chartContainer.appendChild(barContainer);
  });
  
  vizContainer.appendChild(chartContainer);
  
  // Create keywords container
  const keywordsContainer = document.createElement('div');
  keywordsContainer.className = 'keywords-container';
  
  // Add top keywords
  const keywordsTitle = document.createElement('div');
  keywordsTitle.className = 'keywords-title';
  keywordsTitle.textContent = 'Top Keywords:';
  keywordsContainer.appendChild(keywordsTitle);
  
  const keywordsList = document.createElement('div');
  keywordsList.className = 'keywords-list';
  
  // Combine and deduplicate keywords
  const allKeywords = [...new Set([
    ...features.top_content_keywords, 
    ...features.top_question_keywords, 
    ...features.top_answer_keywords
  ])].slice(0, 10); // Limit to top 10
  
  allKeywords.forEach(keyword => {
    const keywordTag = document.createElement('span');
    keywordTag.className = 'keyword-tag';
    keywordTag.textContent = keyword;
    keywordsList.appendChild(keywordTag);
  });
  
  keywordsContainer.appendChild(keywordsList);
  vizContainer.appendChild(keywordsContainer);
  
  return vizContainer;
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
    
    // Convert markdown to HTML and render
    const formattedSummary = convertMarkdownToHtml(response.data.summary);
    document.getElementById("summary").innerHTML = `<div class="summary-content">${formattedSummary}</div>`;
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
    
    // Convert markdown to HTML and render
    const formattedAnswer = convertMarkdownToHtml(response.data.answer);
    
    const responseDiv = document.createElement('div');
    responseDiv.className = 'qa-response';
    responseDiv.innerHTML = `
      <div class="qa-question">Q: ${question}</div>
      <div class="qa-answer">${formattedAnswer}</div>
    `;
    
    // Add visualization if features are available
    if (response.data.features && response.data.probability !== undefined) {
      const vizContainer = createVisualization(response.data.features, response.data.probability);
      responseDiv.appendChild(vizContainer);
    }
    
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

// Removed extractSemanticKeywords function

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
  document.getElementById("summarizeBtn").addEventListener("click", summarizePage);
  document.getElementById("qa-btn").addEventListener("click", askQuestion);
  // Removed semanticKeywordsBtn event listener
  
  // Allow Enter key to submit question
  document.getElementById("qa-input").addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
      askQuestion();
    }
  });
});