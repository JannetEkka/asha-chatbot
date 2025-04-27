"""
Enhanced test script for Gemini API connection.
Run this script to test if your Gemini API key is working correctly.
"""

import os
import json
import requests
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def test_gemini_api():
    """Test the Gemini API connection using the environment variable."""
    api_key = os.getenv("GEMINI_API_KEY", "")
    
    if not api_key:
        logger.error("GEMINI_API_KEY environment variable is not set.")
        logger.info("Please set it using:")
        logger.info("  $env:GEMINI_API_KEY = 'your_api_key_here'  # In PowerShell")
        logger.info("  set GEMINI_API_KEY=your_api_key_here       # In Command Prompt")
        return False
    
    logger.info(f"API Key found: {api_key[:5]}...{api_key[-5:] if len(api_key) > 10 else ''}")
    
    # Test with gemini-1.5-flash (free tier model)
    api_url = "https://generativelanguage.googleapis.com/v1/models/gemini-1.5-flash:generateContent"
    
    # Create a simple test prompt
    prompt = "Generate a test response to confirm the API connection works."
    
    try:
        headers = {
            "Content-Type": "application/json"
        }
        
        data = {
            "contents": [
                {
                    "parts": [
                        {
                            "text": prompt
                        }
                    ]
                }
            ],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        
        url = f"{api_url}?key={api_key}"
        logger.info(f"Making API request to: {api_url}")
        
        response = requests.post(url, headers=headers, json=data)
        
        if response.status_code == 200:
            response_json = response.json()
            text_response = ""
            
            # Extract text from response
            if 'candidates' in response_json and len(response_json['candidates']) > 0:
                candidate = response_json['candidates'][0]
                if 'content' in candidate and 'parts' in candidate['content']:
                    for part in candidate['content']['parts']:
                        if 'text' in part:
                            text_response += part['text']
            
            logger.info("\nAPI CONNECTION SUCCESSFUL!")
            logger.info("Response from Gemini API:")
            logger.info("-" * 40)
            logger.info(text_response[:200] + "..." if len(text_response) > 200 else text_response)
            logger.info("-" * 40)
            return True
        else:
            logger.error("\nAPI REQUEST FAILED")
            logger.error(f"Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            
            # Let's try listing available models to debug
            try:
                models_url = f"https://generativelanguage.googleapis.com/v1/models?key={api_key}"
                logger.info("Attempting to list available models...")
                models_response = requests.get(models_url)
                
                if models_response.status_code == 200:
                    models_data = models_response.json()
                    logger.info("Available models:")
                    for model in models_data.get('models', []):
                        logger.info(f"- {model.get('name')}")
                else:
                    logger.error(f"Failed to list models: {models_response.status_code}")
                    logger.error(models_response.text)
            except Exception as e:
                logger.error(f"Error listing models: {e}")
            
            return False
            
    except Exception as e:
        logger.error(f"\nERROR: {str(e)}")
        return False

def validate_directory_structure():
    """Check if the utils directory structure is set up correctly."""
    # Check for the utils directory in different possible locations
    possible_paths = [
        os.path.join(os.getcwd(), "utils"),
        os.path.join(os.getcwd(), "src", "utils"),
        os.path.join(os.getcwd(), "actions", "utils")
    ]
    
    utils_found = False
    herkey_search_found = False
    
    for path in possible_paths:
        if os.path.exists(path):
            utils_found = True
            logger.info(f"Utils directory found at: {path}")
            
            # Check for herkey_search.py
            search_file = os.path.join(path, "herkey_search.py")
            if os.path.exists(search_file):
                herkey_search_found = True
                logger.info(f"herkey_search.py found at: {search_file}")
                break
    
    if not utils_found:
        logger.warning("Utils directory not found in any of the expected locations.")
        logger.warning("Please run setup_utils.py to create the required directory structure.")
    
    if not herkey_search_found:
        logger.warning("herkey_search.py not found in any of the utils directories.")
        logger.warning("Please run setup_utils.py to create the required files.")
    
    return utils_found and herkey_search_found

if __name__ == "__main__":
    logger.info("Testing Gemini API and directory structure...\n")
    
    # Check directory structure
    structure_valid = validate_directory_structure()
    
    # Test the API
    api_working = test_gemini_api()
    
    logger.info("\nSUMMARY:")
    logger.info(f"Directory structure valid: {'Yes' if structure_valid else 'No'}")
    logger.info(f"Gemini API working: {'Yes' if api_working else 'No'}")
    
    if not structure_valid or not api_working:
        logger.info("\nTROUBLESHOOTING STEPS:")
        if not structure_valid:
            logger.info("1. Run the setup_utils.py script to create the required directories and files.")
        if not api_working:
            logger.info("1. Ensure you've set the GEMINI_API_KEY environment variable correctly.")
            logger.info("2. Check your internet connection.")
            logger.info("3. Verify your API key is valid and has not expired.")
            logger.info("4. Make sure you're using the correct model name (gemini-1.5-flash is recommended for free tier).")