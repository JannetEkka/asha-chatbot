def setup_utils_directory():
    """Create the utils directory structure and files."""
    
    # Define paths
    current_dir = os.getcwd()
    utils_dir = os.path.join(current_dir, "utils")
    
    # Create the directory if it doesn't exist
    os.makedirs(utils_dir, exist_ok=True)
    print(f"Ensuring utils directory exists at: {utils_dir}")
    
    # Create __init__.py file
    init_file = os.path.join(utils_dir, "__init__.py")
    with open(init_file, 'w') as f:
        f.write("""# Utils package for Asha Chatbot
# Contains various utility modules for the chatbot functionality

# Import modules for easier access
try:
    from .herkey_search import HerkeyJobSearch
except ImportError:
    pass  # Handle missing modules gracefully
""")
    
    # Create herkey_search.py file
    search_file = os.path.join(utils_dir, "herkey_search.py")
    with open(search_file, 'w') as f:
        f.write("""import os
import requests
import json
import random

class HerkeyJobSearch:
    # Class content here...
""")
    
    print("Utils directory structure and files created successfully!")
    print(f"Created utils directory at: {utils_dir}")