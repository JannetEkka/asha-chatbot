# Asha AI Chatbot Architecture

## Overview

Asha is an AI-powered chatbot designed for the JobsForHer Foundation. It assists women in their career journeys by providing information about job opportunities, community events, mentorship programs, and career resources. This document outlines the technical architecture of the Asha chatbot system.

## System Architecture

The Asha chatbot follows a modular architecture with several interconnected components:

![Asha Chatbot Architecture](https://i.imgur.com/nGF1K8f.jpg)

### Core Components

1. **User Interface (UI) Layer**
   - Web Chat Widget integrated with Herkey platform
   - Responsive design that works on both desktop and mobile interfaces
   - Clear visual cues for user interaction points

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

5. **Knowledge Base**
   - Structured data storage for job listings, events, and sessions
   - FAQ repository for common questions
   - Career resources and women empowerment content

## Technical Implementation

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

### Policies

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

### Integration with Herkey Platform

The chatbot integrates with the Herkey platform through:

1. Web-based chat widget embedded in the Herkey website
2. Socket.IO for real-time communication
3. Visual styling consistent with Herkey's brand identity

## Deployment Architecture

### Components

- **Rasa Server**: Processes user messages and manages conversations
- **Action Server**: Executes custom actions like job searches
- **Web Server**: Hosts the chat widget and static files
- **Database**: Stores conversation history and user information

### Infrastructure

The system can be deployed in the following ways:

1. **Cloud Deployment**
   - Rasa server and action server deployed on cloud infrastructure
   - Scalable to handle varying loads
   - High availability with redundancy

2. **On-premises Deployment**
   - Servers deployed within organization's infrastructure
   - Greater control over data and security
   - Suitable for specific compliance requirements

## Security Considerations

1. **Data Protection**
   - All sensitive user information is encrypted
   - Compliance with data protection regulations
   - Secure storage of conversation data

2. **Authentication & Authorization**
   - Token-based authentication for API access
   - Role-based access control for administrative functions
   - Secure communication using HTTPS

3. **Input Validation**
   - Sanitization of user inputs to prevent injection attacks
   - Rate limiting to prevent abuse
   - Content filtering to ensure appropriate interactions

## Scalability & Performance

1. **Horizontal Scaling**
   - Multiple instances of Rasa server for load balancing
   - Distributed processing for high message volumes
   - Cache mechanisms for frequent queries

2. **Performance Optimization**
   - Efficient NLU pipeline configuration
   - Optimized model size for faster response times
   - Database query optimization

## Monitoring & Maintenance

1. **Logging**
   - Comprehensive logging of conversations
   - Error tracking and reporting
   - Performance metrics collection

2. **Analytics**
   - User interaction analysis
   - Intent distribution tracking
   - Conversation success rate monitoring

3. **Continuous Improvement**
   - Regular model retraining with new conversation data
   - A/B testing of response variations
   - Iterative improvements based on user feedback

## Future Extensibility

The architecture supports future extensions including:

1. Multi-language support
2. Voice interface integration
3. Enhanced personalization based on user profile
4. Integration with additional third-party services
5. Advanced analytics capabilities