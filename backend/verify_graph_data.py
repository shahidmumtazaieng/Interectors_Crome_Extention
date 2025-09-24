"""
Test script to verify that the backend returns the correct data structure for graph visualization
"""

import requests
import json

def test_graph_data():
    """Test that the backend returns the correct data structure for graph visualization"""
    base_url = "http://localhost:8000"
    
    print("Testing Graph Data Structure")
    print("=" * 30)
    
    try:
        # Test QA endpoint with a real example
        print("Testing QA endpoint...")
        response = requests.post(
            f"{base_url}/qa",
            json={
                "url": "https://en.wikipedia.org/wiki/Artificial_intelligence",
                "question": "What is artificial intelligence?"
            }
        )
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response Data Structure:")
            print(json.dumps(data, indent=2))
            
            # Check if the required fields are present
            required_fields = ['answer', 'features', 'probability']
            missing_fields = [field for field in required_fields if field not in data]
            
            if missing_fields:
                print(f"Missing fields: {missing_fields}")
            else:
                print("✓ All required fields present")
                
                # Check features structure
                features = data['features']
                required_features = [
                    'content_question_similarity',
                    'content_answer_similarity', 
                    'question_answer_similarity',
                    'top_content_keywords',
                    'top_question_keywords',
                    'top_answer_keywords',
                    'content_length',
                    'answer_length'
                ]
                
                missing_features = [feat for feat in required_features if feat not in features]
                
                if missing_features:
                    print(f"Missing features: {missing_features}")
                else:
                    print("✓ All required features present")
                    print(f"Probability: {data['probability']}")
                    print(f"Content-Question Similarity: {features['content_question_similarity']}")
                    print(f"Content-Answer Similarity: {features['content_answer_similarity']}")
                    print(f"Question-Answer Similarity: {features['question_answer_similarity']}")
        else:
            print(f"Error: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_graph_data()