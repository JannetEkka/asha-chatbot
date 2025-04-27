# Asha AI Chatbot - Technical Documentation

## System Overview

Asha is an AI-powered contextual chatbot designed for the JobsForHer Foundation (rebranded as Herkey) to assist women in their career journeys. This document provides detailed technical information about the chatbot's architecture, implementation, and deployment instructions.

## Architecture

### Component Architecture

Asha follows a modular architecture with several interconnected components:

1. **User Interface (UI) Layer**
   - Web Chat Widget integrated with Herkey platform
   - Responsive design for desktop and mobile interfaces
   - Built with HTML/CSS/JavaScript

2. **Natural Language Processing (NLP) Engine**
   - Rasa NLU pipeline for intent classification and entity extraction
   - Contextual understanding of user queries
   - Entity recognition for job roles, locations, skills, etc.

3. **Dialog Management System**
   - Rasa Core for managing conversation flow
   - Form-based slot filling for collecting structured information
   - Context tracking across conversation turns

4. **Integration Layer**
   - REST API endpoints for communication with external systems
   - Action server for custom business logic
   - Data connectors for job listings and session information
   - Optional: Google Gemini API for enhanced job search

5. **Knowledge Base**
   - Structured data storage for job listings, events, and sessions
   - FAQ repository for common questions
   - Career resources and women empowerment content

### NLU Pipeline

The NLU pipeline consists of the following components:

- WhitespaceTokenizer: Splits user messages into tokens based on whitespace
- RegexFeaturizer: Extracts features from user messages based on regular expressions
- LexicalSyntacticFeaturizer: Extracts lexical and syntactic features
- CountVectorsFeaturizer: Converts tokens to vectors using bag-of-words approach
- DIETClassifier: Performs intent classification and entity extraction
- EntitySynonymMapper: Maps entity synonyms to standardized values
- ResponseSelector: Selects appropriate responses for FAQs and chitchat
- FallbackClassifier: Handles messages with low classification confidence

### Dialogue Management Policies

The dialogue management system uses the following policies:

- MemoizationPolicy: Memorizes training conversations for exact matches
- TEDPolicy: Machine learning policy for generalizing to unseen conversation paths
- RulePolicy: Implements rule-based dialog behavior
- UnexpecTEDIntentPolicy: Identifies unexpected intents in conversation context

### Data Flow

1. User sends a message through the web interface
2. Message is processed by the NLU pipeline to extract intent and entities
3. Dialog management selects the next action based on the conversation context
4. If a custom action is needed, the action server is called
5. Response is sent back to the user interface

## Technical Implementation Details

### Core Features Implementation

#### 1. Job Search

The job search feature is implemented using a Rasa form (`job_search_form`) and a custom action (`action_search_jobs`):

```python
# Form definition in domain.yml
forms:
  job_search_form:
    required_slots:
      - job_role
      - location
      - experience

# Custom action for job search
class ActionSearchJobs(Action):
    def name(self) -> Text:
        return "action_search_jobs"

    def run(self, dispatcher, tracker, domain):
        # Get slot values
        job_role = tracker.get_slot("job_role")
        location = tracker.get_slot("location")
        experience = tracker.get_slot("experience")
        
        # Search for jobs (using Gemini API or local data)
        jobs = self.search_jobs(job_role, location, experience)
        
        # Format and return results
        # ...
```

The job search function has three implementations in order of preference:
- Google Gemini API integration (if configured)
- Local CSV data search
- Mock data generation as fallback

#### 2. Events and Sessions Information

Information about events and sessions is retrieved from a JSON data source:

```python
class ActionProvideEventsInfo(Action):
    def name(self) -> Text:
        return "action_provide_events_info"

    def run(self, dispatcher, tracker, domain):
        # Load session data from JSON
        with open("data/Session Details.json", 'r') as file:
            session_data = json.load(file)
        
        # Filter for events, format response
        events = [s for s in session_data if s.get('type') == 'event']
        # ...
```

#### 3. Gender Bias Management

The chatbot detects and addresses gender-biased statements using a dedicated intent and custom action:

```python
class ActionAddressGenderBias(Action):
    def name(self) -> Text:
        return "action_address_gender_bias"

    def run(self, dispatcher, tracker, domain):
        # Provide factual, positive information about women in the workplace
        # Different responses based on specific bias detected
        # ...
```

#### 4. Context Management with Pause/Resume

The chatbot implements a pause/resume feature to maintain conversation context:

```python
class ActionPauseConversation(Action):
    def name(self) -> Text:
        return "action_pause_conversation"

    def run(self, dispatcher, tracker, domain):
        # Store current conversation state
        current_state = {
            "active_form": tracker.active_form.get("name"),
            "slots": tracker.current_slot_values(),
            "latest_action": tracker.latest_action_name
        }
        
        return [SlotSet("paused_state", current_state)]
```

### Web Interface Implementation

The web interface is built using HTML, CSS, and JavaScript, with the following key components:

- Chat widget with responsive design
- WebSocket connection to Rasa server using Socket.IO
- Message handling and display
- Interactive buttons for quick responses
- Styling consistent with Herkey brand identity

#### HTML Structure

```html
<div class="chat-widget">
    <div class="chat-button" id="chat-toggle">
        <img src="avatar.png" alt="Asha">
    </div>
    <div class="chat-window" id="chat-window">
        <div class="chat-header">...</div>
        <div class="chat-messages" id="chat-messages">...</div>
        <div class="chat-input">
            <input type="text" id="message-input" placeholder="Type a message...">
            <button id="send-button">Send</button>
        </div>
    </div>
</div>
```

#### JavaScript for Communication

```javascript
function sendToRasa(message) {
    fetch('http://localhost:5005/webhooks/rest/webhook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            sender: 'user',
            message: message
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Process and display responses
        // ...
    });
}
```

## Setup Instructions

### Prerequisites

- Python 3.9 or higher
- Node.js and npm (for web interface development)
- Git

### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/JannetEkka/asha-chatbot.git
   cd asha-chatbot
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Optional: Set up Google Gemini API**
   
   To enable enhanced job search capabilities:
   ```bash
   # On Windows
   set GEMINI_API_KEY=your_api_key_here
   # On Linux/Mac
   export GEMINI_API_KEY=your_api_key_here
   ```

5. **Train the model**
   ```bash
   rasa train
   ```

6. **Run the chatbot**
   
   In separate terminal windows:
   ```bash
   # Terminal 1: Run Rasa server
   rasa run --enable-api --cors "*" --debug
   
   # Terminal 2: Run actions server
   rasa run actions
   ```

7. **Access the web interface**
   
   Open `index.html` in a web browser.

## Integration Guidelines

### Integrating with Herkey Platform

To integrate Asha with the Herkey platform:

1. **Embed the chat widget**
   
   Add the chat widget HTML, CSS, and JavaScript to the Herkey website template.

2. **Configure API endpoints**
   
   Update the API endpoint in the JavaScript code to point to the deployed Rasa server.

3. **Match styling**
   
   Adjust the widget styling to match Herkey's brand guidelines.

### API Documentation

The chatbot exposes the following REST API endpoints:

- **POST /webhooks/rest/webhook**
  - Request body: `{ "sender": "user_id", "message": "user message" }`
  - Response: Array of bot responses

- **GET /health**
  - Returns health status of the Rasa server

## Deployment Instructions

### Development Environment

For local development and testing:

1. Follow the installation steps above
2. Make changes to the code as needed
3. Retrain the model: `rasa train`
4. Test using the web interface or Rasa shell: `rasa shell`

### Production Deployment

For production deployment:

1. **Deploy Rasa server**
   
   Set up a server with the following components:
   - Rasa server
   - Rasa actions server
   - Web server (Nginx/Apache) for static files

2. **Configure HTTPS**
   
   Enable HTTPS to secure communication between the client and server.

3. **Set up environment variables**
   
   Configure necessary environment variables, including API keys.

4. **Enable logging**
   
   Set up logging for monitoring and debugging.

5. **Configure CORS**
   
   Set appropriate CORS headers to allow connections from the Herkey domain.

## Maintenance and Updates

### Updating the Model

To update the chatbot's model:

1. Modify training data in `data/` directory
2. Retrain the model: `rasa train`
3. Test the new model thoroughly
4. Deploy the updated model files

### Extending Functionality

To add new features:

1. **Add new intents and entities**
   
   Update `nlu.yml` with new training examples.

2. **Define new actions**
   
   Create new custom actions in `actions.py`.

3. **Update the domain**
   
   Add new intents, entities, and actions to `domain.yml`.

4. **Create new stories/rules**
   
   Define conversation flows in `stories.yml` or `rules.yml`.

### Monitoring and Analytics

Monitor the chatbot's performance using:

- Rasa X (optional enterprise tool)
- Custom logging implemented in actions
- Web analytics for user interaction

## Security Considerations

- **Data Protection**: User data is not stored beyond the session unless explicitly needed
- **Input Validation**: All user inputs are validated to prevent injection attacks
- **API Security**: API keys are stored securely as environment variables
- **CORS Configuration**: Proper CORS settings to prevent unauthorized access

## Troubleshooting

### Common Issues and Solutions

1. **NLU model not recognizing intents correctly**
   - Add more training examples in nlu.yml
   - Retrain the model with `rasa train --force`

2. **Actions server not responding**
   - Check if actions server is running
   - Verify that custom actions are properly registered

3. **Web interface not connecting to Rasa**
   - Check CORS settings on Rasa server
   - Verify API endpoint URL in JavaScript

4. **Slots not being properly filled**
   - Check form configuration in domain.yml
   - Verify entity extraction in NLU pipeline

## Conclusion

Asha AI Chatbot provides a comprehensive solution for enhancing user engagement on the Herkey platform. This technical documentation covers the architecture, implementation details, setup instructions, and deployment guidelines necessary for successfully implementing and maintaining the chatbot.

For any further assistance or questions, please contact the development team.