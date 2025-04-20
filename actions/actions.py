"""
Custom actions for the Asha chatbot.
"""
import os
import json
import csv
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, AllSlotsReset
from difflib import get_close_matches

class ActionSearchJobs(Action):
    """Action to search for jobs based on user preferences."""

    def name(self) -> Text:
        return "action_search_jobs"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Search for jobs matching user criteria and return results."""
        
        # Get slot values
        job_role = tracker.get_slot("job_role")
        location = tracker.get_slot("location")
        experience = tracker.get_slot("experience")
        job_type = tracker.get_slot("job_type")
        skill = tracker.get_slot("skill")
        
        # Check latest message to update job_role if needed
        latest_message = tracker.latest_message.get('text', '').lower()
        if 'data science' in latest_message or 'scientist' in latest_message:
            job_role = 'data science'
        elif 'software' in latest_message and ('engineer' in latest_message or 'engineering' in latest_message or 'developer' in latest_message):
            job_role = 'software developer'
        
        # Log the search criteria for debugging
        print(f"Searching for jobs with criteria: role={job_role}, location={location}, experience={experience}")
        
        # Try to load the job listing data if available
        job_data = []
        try:
            # Path to the job listing data CSV
            data_path = os.path.join(os.getcwd(), "data", "job_listing_data.csv")
            
            if os.path.exists(data_path):
                # Read the data
                import pandas as pd
                job_data = pd.read_csv(data_path)
                
                # Debug: Print first few rows to see the structure
                print(f"CSV loaded. Found {len(job_data)} jobs. Sample: {job_data.head(2)}")
                
                # Make all string columns lowercase for case-insensitive comparison
                for col in job_data.columns:
                    if job_data[col].dtype == 'object':
                        job_data[col] = job_data[col].str.lower()
                
                # Convert search terms to lowercase
                if job_role:
                    job_role = job_role.lower()
                if location:
                    location = location.lower()
                if job_type:
                    job_type = job_type.lower()
                if skill:
                    skill = skill.lower()
                
                # Use more flexible filtering with partial matches
                filtered_data = job_data.copy()
                
                if job_role:
                    filtered_data = filtered_data[
                        filtered_data['role'].str.contains(job_role, case=False, na=False) | 
                        filtered_data['title'].str.contains(job_role, case=False, na=False)
                    ]
                
                if location:
                    filtered_data = filtered_data[filtered_data['location'].str.contains(location, case=False, na=False)]
                
                if experience:
                    # Handle experience as string that might contain numbers
                    # This is a more flexible approach than exact matching
                    exp_str = str(experience).lower()
                    exp_digits = ''.join(c for c in exp_str if c.isdigit())
                    if exp_digits:
                        # If we extracted digits, filter by those
                        filtered_data = filtered_data[filtered_data['experience'].astype(str).str.contains(exp_digits, na=False)]
                
                if job_type:
                    filtered_data = filtered_data[filtered_data['job_type'].str.contains(job_type, case=False, na=False)]
                
                if skill:
                    filtered_data = filtered_data[filtered_data['skills'].str.contains(skill, case=False, na=False)]
                
                # Format the results
                job_count = len(filtered_data)
                
                if job_count > 0:
                    # Take the top 5 jobs to show
                    top_jobs = filtered_data.head(5)
                    
                    job_results = ""
                    for index, job in top_jobs.iterrows():
                        job_results += f"- {job['title']} at {job['company']} ({job['location']})\n"
                    
                    # Respond with the results
                    dispatcher.utter_message(
                        template="utter_job_results", 
                        count=job_count, 
                        job_results=job_results
                    )
                else:
                    # No jobs found - save the new role for future searches
                    if job_role and job_role != tracker.get_slot("job_role"):
                        update_slots = [SlotSet("job_role", job_role)]
                    else:
                        update_slots = []
                        
                    # No jobs found - suggest alternatives
                    alternative_message = "I couldn't find exact matches for your criteria. "
                    
                    if job_role and location:
                        # Check if there are jobs with this role regardless of location
                        role_matches = job_data[job_data['role'].str.contains(job_role, case=False, na=False) | 
                                              job_data['title'].str.contains(job_role, case=False, na=False)]
                        
                        if len(role_matches) > 0:
                            # There are jobs with this role in other locations
                            alternative_message += f"I found {len(role_matches)} {job_role} positions in other locations. "
                            alternative_message += "Would you like to search without location restrictions?"
                        else:
                            # No jobs with this role at all
                            alternative_message += f"I don't have any current listings for {job_role} roles. "
                            alternative_message += "Would you like to try a different role or broaden your search criteria?"
                    else:
                        alternative_message += "Would you like to broaden your search criteria or try a different role?"
                    
                    dispatcher.utter_message(text=alternative_message)
                    
                    return update_slots
            
            else:
                # If the data file doesn't exist, use mock data
                dispatcher.utter_message(
                    template="utter_job_results",
                    count="several",
                    job_results="""- Software Developer at TechCorp (Bangalore)
- Marketing Manager at BrandX (Delhi)
- Data Analyst at DataInsights (Remote)
- Product Manager at InnovateTech (Mumbai)
- HR Specialist at PeopleFirst (Hyderabad)"""
                )
                
        except Exception as e:
            # Log the exception
            print(f"Error in job search: {str(e)}")
            
            # If there's an error, use mock data
            dispatcher.utter_message(
                template="utter_job_results",
                count="several",
                job_results="""- Software Developer at TechCorp (Bangalore)
- Marketing Manager at BrandX (Delhi)
- Data Analyst at DataInsights (Remote)
- Product Manager at InnovateTech (Mumbai)
- HR Specialist at PeopleFirst (Hyderabad)"""
            )
            
        # Return empty list as we're not setting any slots
        return []

class ActionProvideEventsInfo(Action):
    """Action to provide information about events."""

    def name(self) -> Text:
        return "action_provide_events_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Provide information about upcoming events."""
        
        # Try to load the session details JSON if available
        try:
            # Path to the session details JSON
            data_path = os.path.join(os.getcwd(), "data", "Session Details.json")
            
            if os.path.exists(data_path):
                # Read the data
                with open(data_path, 'r') as file:
                    session_data = json.load(file)
                
                # Filter for events
                events = [s for s in session_data if s.get('type') == 'event']
                
                # Check for event type in entities
                event_types = [e["value"] for e in tracker.latest_message.get("entities", []) 
                              if e["entity"] == "event_type"]
                
                # If specific event type requested, filter for it
                if event_types:
                    filtered_events = []
                    for event_type in event_types:
                        filtered_events.extend([e for e in events if event_type.lower() in e.get('title', '').lower()])
                    
                    # If we found specific events, use those; otherwise, fall back to all events
                    if filtered_events:
                        events = filtered_events
                
                if events:
                    # Sort events by date
                    from datetime import datetime
                    
                    # Convert date strings to datetime objects for sorting
                    for event in events:
                        try:
                            event['date_obj'] = datetime.strptime(event.get('date', ''), '%B %d, %Y')
                        except:
                            # If date can't be parsed, use a far future date
                            event['date_obj'] = datetime(2099, 12, 31)
                    
                    # Sort by date
                    events.sort(key=lambda x: x['date_obj'])
                    
                    # Remove the datetime objects after sorting
                    for event in events:
                        del event['date_obj']
                    
                    # Format the events
                    events_info = "Here are some upcoming events:\n\n"
                    for event in events[:5]:  # Show top 5 events
                        events_info += f"- {event.get('title')} on {event.get('date')} at {event.get('time')}\n"
                        events_info += f"  {event.get('description')}\n\n"
                    
                    events_info += "Would you like more details about any of these events or information about other types of events? You can also browse all events in the 'Events' section of Herkey."
                    
                    dispatcher.utter_message(text=events_info)
                else:
                    # No events found
                    dispatcher.utter_message(text="I don't have any upcoming events that match your criteria in my records at the moment. You can check the 'Events' section on Herkey to see all current listings. Would you like to know about our general event categories instead?")
            
            else:
                # If the data file doesn't exist, use mock data
                events_info = """Here are some upcoming events:

- Women in Tech Workshop on May 10, 2025 at 2:00 PM
  Learn about the latest technologies and how women are shaping the tech industry.

- Resume Building Workshop on May 15, 2025 at 3:30 PM
  Learn how to create a resume that stands out and showcases your skills effectively.

- Career Transition Webinar on May 20, 2025 at 6:00 PM
  Expert advice on how to successfully navigate career transitions and changes.

- Networking Mixer on May 25, 2025 at 5:00 PM
  Connect with professionals from various industries and expand your network.

- Leadership Skills Workshop on June 1, 2025 at 4:00 PM
  Develop essential leadership skills that will help you advance in your career.

Would you like more details about any of these events or information about other types of events? You can view all events in the 'Events' section of Herkey."""
                
                dispatcher.utter_message(text=events_info)
                
        except Exception as e:
            # Log the error
            print(f"Error in providing events info: {str(e)}")
            
            # If there's an error, use mock data
            events_info = """Here are some upcoming events:

- Women in Tech Workshop on May 10, 2025 at 2:00 PM
  Learn about the latest technologies and how women are shaping the tech industry.

- Resume Building Workshop on May 15, 2025 at 3:30 PM
  Learn how to create a resume that stands out and showcases your skills effectively.

- Career Transition Webinar on May 20, 2025 at 6:00 PM
  Expert advice on how to successfully navigate career transitions and changes.

- Networking Mixer on May 25, 2025 at 5:00 PM
  Connect with professionals from various industries and expand your network.

- Leadership Skills Workshop on June 1, 2025 at 4:00 PM
  Develop essential leadership skills that will help you advance in your career.

Would you like more details about any of these events or information about other types of events? You can view all events in the 'Events' section of Herkey."""
            
            dispatcher.utter_message(text=events_info)
            
        return []

class ActionProvideSessionsInfo(Action):
    """Action to provide information about sessions."""

    def name(self) -> Text:
        return "action_provide_sessions_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Provide information about available sessions."""
        
        # Try to load the session details JSON if available
        try:
            # Path to the session details JSON
            data_path = os.path.join(os.getcwd(), "data", "Session Details.json")
            
            if os.path.exists(data_path):
                # Read the data
                with open(data_path, 'r') as file:
                    session_data = json.load(file)
                
                # Filter for sessions
                sessions = [s for s in session_data if s.get('type') == 'session']
                
                if sessions:
                    # Sort sessions by date
                    from datetime import datetime
                    
                    # Convert date strings to datetime objects for sorting
                    for session in sessions:
                        try:
                            session['date_obj'] = datetime.strptime(session.get('date', ''), '%B %d, %Y')
                        except:
                            # If date can't be parsed, use a far future date
                            session['date_obj'] = datetime(2099, 12, 31)
                    
                    # Sort by date
                    sessions.sort(key=lambda x: x['date_obj'])
                    
                    # Remove the datetime objects after sorting
                    for session in sessions:
                        del session['date_obj']
                    
                    # Format the sessions
                    sessions_info = "Here are some upcoming learning sessions:\n\n"
                    for session in sessions[:5]:  # Show top 5 sessions
                        sessions_info += f"- {session.get('title')} on {session.get('date')} at {session.get('time')}\n"
                        sessions_info += f"  {session.get('description')}\n\n"
                    
                    sessions_info += "These sessions are designed to help you develop various skills relevant to your career. You can check the 'Sessions' section on Herkey to register for these or explore more available sessions."
                    
                    dispatcher.utter_message(text=sessions_info)
                else:
                    # No sessions found
                    dispatcher.utter_message(text="I don't have any upcoming sessions in my records at the moment. You can check the 'Sessions' section on Herkey to see all current offerings. Our sessions typically cover topics like career growth, technical skills, work-life balance, interviewing, and negotiation.")
            
            else:
                # If the data file doesn't exist, use mock data
                sessions_info = """Here are some upcoming learning sessions:

- Career Growth Strategies on May 12, 2025 at 2:00 PM
  Learn effective strategies to accelerate your career growth and advancement.

- Technical Skills Update on May 18, 2025 at 3:30 PM
  Stay updated with the latest technical skills in demand in the job market.

- Work-Life Balance Session on May 22, 2025 at 6:00 PM
  Tips and strategies for maintaining a healthy work-life balance.

- Interviewing Skills Workshop on May 28, 2025 at 5:00 PM
  Master the art of interviewing with practical tips and mock interview sessions.

- Negotiation Tactics Session on June 5, 2025 at 4:00 PM
  Learn effective negotiation strategies for salary discussions and career advancement.

These sessions are designed to help you develop various skills relevant to your career. You can browse and register for these sessions in the 'Sessions' section on Herkey."""
                
                dispatcher.utter_message(text=sessions_info)
                
        except Exception as e:
            # Log the error
            print(f"Error in providing sessions info: {str(e)}")
            
            # If there's an error, use mock data
            sessions_info = """Here are some upcoming learning sessions:

- Career Growth Strategies on May 12, 2025 at 2:00 PM
  Learn effective strategies to accelerate your career growth and advancement.

- Technical Skills Update on May 18, 2025 at 3:30 PM
  Stay updated with the latest technical skills in demand in the job market.

- Work-Life Balance Session on May 22, 2025 at 6:00 PM
  Tips and strategies for maintaining a healthy work-life balance.

- Interviewing Skills Workshop on May 28, 2025 at 5:00 PM
  Master the art of interviewing with practical tips and mock interview sessions.

- Negotiation Tactics Session on June 5, 2025 at 4:00 PM
  Learn effective negotiation strategies for salary discussions and career advancement.

These sessions are designed to help you develop various skills relevant to your career. You can browse and register for these sessions in the 'Sessions' section on Herkey."""
            
            dispatcher.utter_message(text=sessions_info)
            
        return []

class ActionProvideMentorshipInfo(Action):
    """Action to provide information about mentorship programs."""

    def name(self) -> Text:
        return "action_provide_mentorship_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Provide information about mentorship programs."""
        
        # Get the latest user message to check for specific questions
        latest_message = tracker.latest_message.get('text', '').lower()
        
        # Check if the query is about finding a mentor
        if 'find' in latest_message and 'mentor' in latest_message:
            mentorship_info = """Although Herkey doesn't have a dedicated "Mentorship" section, you can connect with potential mentors through these platform features:

1. **Network Section**: Browse and connect with professionals in your field. Look for experienced people who might be willing to provide guidance.

2. **Groups**: Join industry or skill-specific groups to meet peers and senior professionals who share your interests.

3. **Sessions & Events**: Participate in sessions and networking events where you can meet potential mentors face-to-face.

4. **Discussions**: Engage in discussions where you can demonstrate your interests and connect with knowledgeable professionals.

When reaching out to potential mentors:
- Be specific about your goals and what you hope to learn
- Respect their time by being prepared for conversations
- Start with a simple coffee chat request before asking for formal mentorship

Would you like tips on how to effectively approach potential mentors?"""
        
        # Check if the query is about benefits of mentorship
        elif 'benefit' in latest_message and 'mentor' in latest_message:
            mentorship_info = """The benefits of having a mentor include:

1. Personalized guidance from professionals who have successfully navigated similar career paths

2. Insider knowledge about industry trends and opportunities

3. Feedback on your skills, resume, and interview techniques

4. Expanded professional network through your mentor's connections

5. Support for career transitions, whether you're changing fields or returning after a break

6. Increased confidence in your professional abilities and decisions

7. Accountability for your career goals and development

Research shows that professionals with mentors are more likely to receive promotions and report higher job satisfaction. 

You can connect with potential mentors through Herkey's Network, Groups, and by participating actively in Sessions and Discussions."""
        
        # Check if the query is about types of mentorship
        elif 'type' in latest_message and 'mentor' in latest_message:
            mentorship_info = """There are several types of mentoring relationships you can develop through Herkey's platform:

1. **Peer Mentoring**: Connect with colleagues at similar career stages to share experiences and advice.

2. **Industry Mentoring**: Find leaders in specific industries by participating in industry-focused groups and events.

3. **Skill-Based Mentoring**: Connect with experts in particular skills you want to develop.

4. **Career Transition Mentoring**: Find guidance from professionals who have successfully changed careers or returned to work after breaks.

5. **Leadership Mentoring**: Learn from experienced leaders by engaging with them in sessions and groups focused on leadership.

You can identify potential mentors by actively participating in Herkey's events, joining relevant groups, and making meaningful connections through the Network section.

Which type of mentoring relationship are you most interested in developing?"""
        
        # Default response with general mentorship information
        else:
            mentorship_info = """Herkey supports your professional growth through various networking and learning opportunities that can lead to meaningful mentoring relationships.

While Herkey doesn't have a dedicated "Mentorship" section, you can connect with potential mentors through:

1. **Network Section**: Connect with experienced professionals in your field who might provide guidance.

2. **Groups**: Join communities of professionals with similar interests where you can meet potential mentors.

3. **Sessions & Events**: Participate in learning sessions and networking events to meet industry experts.

4. **Discussions**: Engage in conversations where you can learn from and connect with knowledgeable professionals.

Professional relationships often develop naturally through regular interaction and engagement on the platform. Would you like to know more about how to effectively approach potential mentors or specific ways to utilize Herkey's features for professional growth?"""
        
        dispatcher.utter_message(text=mentorship_info)
        return []

class ActionHandleFAQ(Action):
    """Enhanced action to handle frequently asked questions using the structured FAQ data."""

    def __init__(self):
        # Load the FAQ database
        try:
            faq_path = os.path.join(os.getcwd(), "data", "faqs.json")
            if os.path.exists(faq_path):
                with open(faq_path, 'r') as f:
                    faq_data = json.load(f)
                    
                # Create lookup structures for efficient question matching
                self.all_questions = []
                self.question_to_answer = {}
                self.question_to_category = {}
                
                for category in faq_data.get("faq", []):
                    category_name = category.get("category", "General")
                    for q_item in category.get("questions", []):
                        question = q_item.get("question", "").lower()
                        # Replace JobsForHer with Herkey in the questions
                        question = question.replace("jobsforher", "herkey")
                        
                        answer = q_item.get("answer", "")
                        # Replace JobsForHer with Herkey in the answers
                        answer = answer.replace("JobsForHer", "Herkey")
                        answer = answer.replace("jobsforher", "herkey")
                        
                        if question and answer:
                            self.all_questions.append(question)
                            self.question_to_answer[question] = answer
                            self.question_to_category[question] = category_name
            else:
                self.all_questions = []
                self.question_to_answer = {}
                self.question_to_category = {}
                print(f"FAQ file not found at {faq_path}")
        except Exception as e:
            self.all_questions = []
            self.question_to_answer = {}
            self.question_to_category = {}
            print(f"Error loading FAQ data: {e}")

    def name(self) -> Text:
        return "action_handle_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Provide answers to frequently asked questions."""
        
        # Get the latest user message
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Replace JobsForHer with Herkey in the user message
        user_message = user_message.replace("jobsforher", "herkey")
        
        # Try to find the closest matching question
        matches = get_close_matches(user_message, self.all_questions, n=1, cutoff=0.6)
        
        if matches:
            matched_question = matches[0]
            answer = self.question_to_answer[matched_question]
            category = self.question_to_category[matched_question]
            
            # Add a more empathetic intro based on category
            if "technical" in category.lower():
                intro = "I understand technical issues can be frustrating. "
            elif "career" in category.lower():
                intro = "Great question about career development! "
            elif "job search" in category.lower():
                intro = "I'm happy to help with your job search journey. "
            elif "mentorship" in category.lower():
                intro = "Mentorship is key to career growth. "
            else:
                intro = "Here's what I found for you: "
            
            # Send the response
            dispatcher.utter_message(text=f"{intro}{answer}")
        else:
            # Default response if no match is found
            dispatcher.utter_message(text="I don't have specific information on that. Please try rewording your question, or ask about job opportunities, career advice, or Herkey's services.")
        
        return []

class ActionAddressGenderBias(Action):
    """Action to address gender-biased questions."""

    def name(self) -> Text:
        return "action_address_gender_bias"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Address gender-biased questions by providing positive information about women in the workplace."""
        
        # Get the latest user message
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Custom responses based on specific biases in the message
        if "technical" in user_message or "tech" in user_message:
            response = """That's a misconception I'd like to address! Women have consistently proven their excellence in technical roles across the industry. 

Research from McKinsey shows that companies with gender-diverse technical teams are 21% more likely to experience above-average profitability. Women like Ada Lovelace (the first computer programmer), Grace Hopper (pioneer of COBOL), and Radia Perlman (inventor of STP) revolutionized computing.

Today, leaders like Fei-Fei Li (AI pioneer), Marian Croak (VoIP inventor with 200+ patents), and Reshma Saujani (Girls Who Code founder) continue to drive innovation in tech.

Would you like to hear about specific programs on Herkey that help women build technical skills?"""
            
        elif "leadership" in user_message or "lead" in user_message:
            response = """I'd like to challenge that perspective! Women have repeatedly demonstrated exceptional leadership capabilities across industries.

Research by Peterson Institute shows companies with 30%+ women in leadership have 15% higher profitability. Leaders like Indra Nooyi (former PepsiCo CEO), Mary Barra (GM CEO), and Kiran Mazumdar-Shaw (Biocon founder) have transformed their industries.

Studies from Harvard Business Review found women leaders score higher in most leadership skills including taking initiative, resilience, and driving results.

Herkey offers resources specifically designed to help women develop leadership skills through sessions and networking opportunities. Would you like me to share some upcoming leadership events?"""
            
        else:
            # General response if no specific bias is detected
            response = """I'd like to offer a different perspective! Research consistently shows that gender diversity improves organizational performance across all roles and industries.

A comprehensive study by McKinsey found that companies in the top quartile for gender diversity are 25% more likely to achieve above-average profitability. Women have proven to excel in every field when given equal opportunities and support.

Herkey is dedicated to empowering women in all career paths by providing resources, networking opportunities, and showcasing success stories that break stereotypes and biases.

Would you like to learn about specific success stories of women in your field of interest?"""
            
        dispatcher.utter_message(text=response)
        return []

class ValidateJobSearchForm(FormValidationAction):
    """Validation for job search form."""

    def name(self) -> Text:
        return "validate_job_search_form"

    def validate_job_role(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate job role value."""
        
        if not slot_value:
            # Check if we can extract job role from the message
            latest_message = tracker.latest_message.get('text', '').lower()
            
            # Try to extract common job roles
            if 'data science' in latest_message or 'data scientist' in latest_message:
                return {"job_role": "data science"}
            elif 'software' in latest_message and ('engineer' in latest_message or 'developer' in latest_message):
                return {"job_role": "software developer"}
            elif 'product manager' in latest_message:
                return {"job_role": "product manager"}
            elif 'marketing' in latest_message:
                return {"job_role": "marketing"}
            elif 'designer' in latest_message or 'design' in latest_message:
                return {"job_role": "designer"}
            
            # No job role detected
            dispatcher.utter_message(text="Please provide a valid job role, such as 'Software Developer', 'Data Scientist', or 'Marketing Manager'.")
            return {"job_role": None}
        
        # We have a slot value
        if len(slot_value) > 2:
            # Valid job role
            return {"job_role": slot_value}
        else:
            # Invalid job role (too short)
            dispatcher.utter_message(text="Please provide a more specific job role, such as 'Software Developer' or 'Marketing Manager'.")
            return {"job_role": None}

    def validate_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate location value."""
        
        if not slot_value:
            # Check if we can extract location from the message
            latest_message = tracker.latest_message.get('text', '').lower()
            
            # Try to extract common locations
            if 'bangalore' in latest_message:
                return {"location": "Bangalore"}
            elif 'mumbai' in latest_message:
                return {"location": "Mumbai"}
            elif 'delhi' in latest_message:
                return {"location": "Delhi"}
            elif 'hyderabad' in latest_message:
                return {"location": "Hyderabad"}
            elif 'remote' in latest_message or 'work from home' in latest_message:
                return {"location": "Remote"}
            
            # No location detected
            dispatcher.utter_message(text="Please provide a valid location, such as 'Bangalore', 'Mumbai', or 'Remote'.")
            return {"location": None}
        
        # We have a slot value
        if len(slot_value) > 2:
            # Valid location
            # Check for common location spelling variations
            slot_value_lower = slot_value.lower()
            if 'bangalore' in slot_value_lower:
                return {"location": "Bangalore"}
            elif 'mumbai' in slot_value_lower:
                return {"location": "Mumbai"}
            elif 'delhi' in slot_value_lower:
                return {"location": "Delhi"}
            elif 'hyderabad' in slot_value_lower:
                return {"location": "Hyderabad"}
            elif 'remote' in slot_value_lower or 'work from home' in slot_value_lower:
                return {"location": "Remote"}
            
            # Other location
            return {"location": slot_value}
        else:
            # Invalid location (too short)
            dispatcher.utter_message(text="Please provide a valid location, such as 'Bangalore' or 'Remote'.")
            return {"location": None}

    def validate_experience(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate experience value."""
        
        if not slot_value:
            # Check if we can extract experience from the message
            latest_message = tracker.latest_message.get('text', '').lower()
            
            # Try to extract years of experience
            import re
            years_match = re.search(r'(\d+)\s*(?:years?|yrs?)', latest_message)
            if years_match:
                years = years_match.group(1)
                return {"experience": f"{years} years"}
            
            # Check for experience levels
            if 'entry' in latest_message or 'junior' in latest_message or 'fresher' in latest_message:
                return {"experience": "entry level"}
            elif 'mid' in latest_message:
                return {"experience": "mid level"}
            elif 'senior' in latest_message or 'experienced' in latest_message:
                return {"experience": "senior level"}
            
            # No experience detected
            dispatcher.utter_message(text="Please provide your years of experience, such as '3 years' or specify if you're at entry, mid, or senior level.")
            return {"experience": None}
        
        # We have a slot value
        # Experience can be a number, a range, or a level
        if slot_value:
            # Valid experience
            return {"experience": slot_value}
        else:
            # Invalid experience
            dispatcher.utter_message(text="Please provide your years of experience, such as '3 years' or specify if you're at entry, mid, or senior level.")
            return {"experience": None}
        
class ActionPauseConversation(Action):
    """Pauses the current conversation and stores the state."""

    def name(self) -> Text:
        return "action_pause_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get current conversation state
        current_state = {
            "active_form": tracker.active_form.get("name"),
            "slots": tracker.current_slot_values(),
            "latest_action": tracker.latest_action_name
        }
        
        # Store state in a slot for later retrieval
        dispatcher.utter_message(text="I've paused our conversation. What additional details would you like to add?")
        
        return [SlotSet("paused_state", current_state)]

class ActionResumeConversation(Action):
    """Resumes conversation from paused state."""

    def name(self) -> Text:
        return "action_resume_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        paused_state = tracker.get_slot("paused_state")
        if not paused_state:
            dispatcher.utter_message(text="I couldn't find a paused conversation to resume.")
            return []
        
        # Resume the previous state
        dispatcher.utter_message(text="I'm continuing our previous conversation with the new information you've provided.")
        
        # Clear the paused state
        return [SlotSet("paused_state", None)]