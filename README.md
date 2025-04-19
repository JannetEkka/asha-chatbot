# Asha AI Chatbot

Asha is an AI-powered chatbot designed for the JobsForHer Foundation to assist women in their career journeys. The chatbot provides information about job opportunities, mentorship programs, community events, and career resources.

## Features

- **Job Search**: Find job opportunities based on role, location, and experience with contextual search refinement
- **Events & Sessions**: Get information about upcoming community events and learning sessions
- **Mentorship**: Learn about mentorship programs and how to connect with mentors
- **Career Resources**: Access information about women empowerment initiatives and career advice
- **FAQ Handling**: Get answers to frequently asked questions about JobsForHer

## Technical Stack

- **Rasa Open Source**: For natural language understanding and dialogue management
- **Python 3.9**: Core programming language
- **HTML/CSS/JavaScript**: Web interface with custom chat widget
- **CSV/JSON**: Data storage for job listings and session information

## Recent Updates

- **Improved Job Search**: Enhanced contextual understanding of job search queries
- **Fixed Slot Persistence**: Location and experience values are now retained when changing job roles
- **Better Conversation Flow**: Smoother transitions between different conversation topics
- **Alternative Suggestions**: When no jobs match criteria, the bot now offers helpful alternatives
- **Enhanced NLU Training**: Better recognition of job roles, locations, and experience levels

## Project Structure

```
asha-chatbot/
├── actions/              # Custom actions code
├── data/                 # Training data (NLU, stories, rules)
│   ├── nlu.yml           # Natural language understanding training data  
│   ├── stories.yml       # Conversation flow stories
│   ├── rules.yml         # Conversation rules
│   ├── job_listing_data.csv  # Sample job listings
│   └── Session Details.json  # Event and session information
├── models/               # Trained model files
├── tests/                # Test stories and scripts
├── config.yml            # NLU and policy configuration
├── credentials.yml       # Channel credentials
├── domain.yml            # Domain definition
├── endpoints.yml         # Endpoints configuration
└── index.html            # Web interface
```

## Setup and Installation

1. **Prerequisites**:
   - Python 3.9
   - Rasa Open Source 3.x

2. **Environment Setup**:
   ```bash
   # Create virtual environment
   python3.9 -m venv venv-rasa
   
   # Activate environment
   # On Windows:
   venv-rasa\Scripts\activate
   # On Linux/Mac:
   source venv-rasa/bin/activate
   
   # Install dependencies
   pip install rasa
   ```

3. **Training the Model**:
   ```bash
   rasa train
   ```

4. **Running the Chatbot**:
   ```bash
   # Start Rasa server
   rasa run --enable-api --cors "*"
   
   # In a new terminal, start actions server
   rasa run actions
   ```

5. **Web Interface**:
   - Open `index.html` in a web browser
   - The chat widget will connect to the local Rasa server

## Key Features Implementation

### Job Search with Context Maintenance

The chatbot uses a form to collect user preferences such as job role, location, and experience. It maintains context when users refine their search, allowing for natural conversation flow.

```python
# Example of using a job search form
- intent: search_job
- action: job_search_form
- active_loop: job_search_form
- active_loop: null
- action: action_search_jobs
- intent: provide_job_preference  # User refines search
- action: action_search_jobs      # Bot updates search with new preferences
```

### Gender Bias Handling

Asha is designed to detect and address gender-biased questions by providing positive information about women in the workplace and sharing success stories.

### Contextual Conversations

Using Rasa's dialogue management capabilities, Asha maintains context throughout conversations to provide a seamless user experience.

## Usage Examples

- "I'm looking for a job in marketing"
- "Actually, I'm interested in data science roles"
- "Tell me about upcoming events"
- "How can I find a mentor?"
- "What resources do you have for women returning to work?"
- "What is JobsForHer?"

## Development Roadmap

- Integrate with external job databases for real-time job listings
- Add authentication for personalized job recommendations
- Implement multi-language support
- Create a mobile app interface
- Add analytics tracking for conversation insights

## Testing

The repository includes test scripts to verify key functionality:

```bash
# Run tests for FAQ handling
python tests/test_faq.py

# Run tests for conversation flows
python tests/test_conversations.py
```

## Contributors

- Jannet Akanksha Ekka
- JobsForHer Foundation Team

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Developed for the JobsForHer Foundation Hackathon, April 2025.