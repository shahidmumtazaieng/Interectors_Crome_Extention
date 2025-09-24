import asyncio
import sys
import os

# Add the backend directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import extract_keywords_optimized

def test_semantic_keywords():
    # Test content
    test_content = """
    Artificial Intelligence and Machine Learning are transforming the technology landscape. 
    AI applications include natural language processing, computer vision, and robotics.
    Machine learning algorithms such as neural networks, decision trees, and support vector machines 
    are widely used in data science and analytics. Deep learning, a subset of machine learning, 
    has revolutionized image and speech recognition systems. Companies are investing heavily in 
    AI research and development to gain competitive advantages in the market.
    """
    
    print("Testing semantic keywords extraction...")
    print("Test content length:", len(test_content))
    
    # Test the optimized keyword extraction
    keywords = extract_keywords_optimized(test_content)
    
    print("\nExtracted keywords:")
    for keyword_obj in keywords:
        print(f"  {keyword_obj['keyword']}: {keyword_obj['frequency']}")
    
    print(f"\nTotal keywords extracted: {len(keywords)}")

if __name__ == "__main__":
    test_semantic_keywords()