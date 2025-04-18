# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
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
        
        # Mock job search functionality
        # In a real implementation, this would query the job_listing_data.csv
        # For now, we'll use a simple mock response
        
        # Try to load the job listing data if available
        job_data = []
        try:
            # Path to the job listing data CSV
            data_path = os.path.join(os.getcwd(), "data", "job_listing_data.csv")
            
            if os.path.exists(data_path):
                # Read the data
                job_data = pd.read_csv(data_path)
                
                # Filter based on user preferences
                if job_role:
                    job_data = job_data[job_data['role'].str.contains(job_role, case=False, na=False)]
                
                if location:
                    job_data = job_data[job_data['location'].str.contains(location, case=False, na=False)]
                
                if experience:
                    # Assuming experience is stored as a range or number in the CSV
                    # This is a simplified filter
                    job_data = job_data[job_data['experience'].astype(str).str.contains(experience, case=False, na=False)]
                
                if job_type:
                    job_data = job_data[job_data['job_type'].str.contains(job_type, case=False, na=False)]
                
                if skill:
                    job_data = job_data[job_data['skills'].str.contains(skill, case=False, na=False)]
                
                # Format the results
                job_count = len(job_data)
                
                if job_count > 0:
                    # Take the top 5 jobs to show
                    top_jobs = job_data.head(5)
                    
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
                    # No jobs found
                    dispatcher.utter_message(template="utter_no_jobs_found")
            
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
                
                if events:
                    # Format the events
                    events_info = "Here are some upcoming events:\n\n"
                    for event in events[:5]:  # Show top 5 events
                        events_info += f"- {event.get('title')} on {event.get('date')} at {event.get('time')}\n"
                    
                    dispatcher.utter_message(text=events_info)
                else:
                    # No events found
                    dispatcher.utter_message(text="I don't have any upcoming events in my records at the moment. Please check back later or visit our website for the most up-to-date event information.")
            
            else:
                # If the data file doesn't exist, use mock data
                events_info = """Here are some upcoming events:

- Women in Tech Workshop on May 10, 2025 at 2:00 PM
- Resume Building Workshop on May 15, 2025 at 3:30 PM
- Career Transition Webinar on May 20, 2025 at 6:00 PM
- Networking Mixer on May 25, 2025 at 5:00 PM
- Leadership Skills Workshop on June 1, 2025 at 4:00 PM"""
                
                dispatcher.utter_message(text=events_info)
                
        except Exception as e:
            # If there's an error, use mock data
            events_info = """Here are some upcoming events:

- Women in Tech Workshop on May 10, 2025 at 2:00 PM
- Resume Building Workshop on May 15, 2025 at 3:30 PM
- Career Transition Webinar on May 20, 2025 at 6:00 PM
- Networking Mixer on May 25, 2025 at 5:00 PM
- Leadership Skills Workshop on June 1, 2025 at 4:00 PM"""
            
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
                    # Format the sessions
                    sessions_info = "Here are some upcoming sessions:\n\n"
                    for session in sessions[:5]:  # Show top 5 sessions
                        sessions_info += f"- {session.get('title')} on {session.get('date')} at {session.get('time')}\n"
                    
                    dispatcher.utter_message(text=sessions_info)
                else:
                    # No sessions found
                    dispatcher.utter_message(text="I don't have any upcoming sessions in my records at the moment. Please check back later or visit our website for the most up-to-date session information.")
            
            else:
                # If the data file doesn't exist, use mock data
                sessions_info = """Here are some upcoming sessions:

- Career Growth Strategies on May 12, 2025 at 2:00 PM
- Technical Skills Update on May 18, 2025 at 3:30 PM
- Work-Life Balance Session on May 22, 2025 at 6:00 PM
- Interviewing Skills Workshop on May 28, 2025 at 5:00 PM
- Negotiation Tactics Session on June 5, 2025 at 4:00 PM"""
                
                dispatcher.utter_message(text=sessions_info)
                
        except Exception as e:
            # If there's an error, use mock data
            sessions_info = """Here are some upcoming sessions:

- Career Growth Strategies on May 12, 2025 at 2:00 PM
- Technical Skills Update on May 18, 2025 at 3:30 PM
- Work-Life Balance Session on May 22, 2025 at 6:00 PM
- Interviewing Skills Workshop on May 28, 2025 at 5:00 PM
- Negotiation Tactics Session on June 5, 2025 at 4:00 PM"""
            
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
        
        mentorship_info = """At JobsForHer, we offer various mentorship programs to help women advance in their careers:

1. One-on-One Mentorship: Get paired with an experienced professional in your field for personalized guidance.

2. Group Mentorship Sessions: Join small groups of women with similar career interests for shared learning.

3. Industry-Specific Mentorship: Connect with leaders from specific industries like Tech, Finance, Marketing, etc.

4. Return to Work Mentorship: Special programs for women returning to the workforce after a career break.

Would you like to know more about any specific mentorship program?"""
        
        dispatcher.utter_message(text=mentorship_info)
        return []

class ActionHandleFAQ(Action):
    """Action to handle frequently asked questions."""

    def name(self) -> Text:
        return "action_handle_faq"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Provide answers to frequently asked questions."""
        
        # Get the latest user message
        user_message = tracker.latest_message.get('text', '').lower()
        
        # FAQ database - in a real implementation, this would be stored externally
        faq_db = {
            "what is jobsforher": "JobsForHer is a platform dedicated to accelerating women's careers by connecting them with job opportunities, mentorship, and resources for upskilling.",
            
            "how can jobsforher help me": "JobsForHer can help you find job opportunities tailored to your skills and preferences, connect you with mentors, provide access to networking events, and offer resources for professional development.",
            
            "is jobsforher only for women": "JobsForHer primarily focuses on women's career advancement, but anyone interested in diversity and inclusion can benefit from our resources and community.",
            
            "does jobsforher charge any fees": "Basic services on JobsForHer are free for job seekers. Premium services that provide enhanced visibility to employers and priority access to events may have a fee associated.",
            
            "how do i create an account": "You can create an account by visiting our website, clicking on 'Sign Up', and following the registration process. You'll need to provide basic information and create your profile.",
            
            "what resources does jobsforher provide": "JobsForHer provides job listings, mentorship programs, career resources, webinars, workshops, networking events, and a supportive community for women professionals.",
            
            "how can i post my resume": "After creating an account on JobsForHer, you can build your profile, which serves as your resume. Go to 'My Profile' and fill in your education, work experience, skills, and career preferences.",
            
            "how do employers use jobsforher": "Employers use JobsForHer to post job opportunities, search for qualified candidates, participate in virtual job fairs, and demonstrate their commitment to diversity and inclusion.",
            
            "does jobsforher offer career counseling": "Yes, JobsForHer offers career counseling through our mentorship programs, where experienced professionals provide guidance on career growth, transitions, and development.",
            
            "can men use jobsforher": "While JobsForHer's primary focus is on women's career advancement, men can use the platform to access resources on diversity and inclusion and to support women's professional growth.",
            
            "what makes jobsforher different from other job sites": "JobsForHer is specifically tailored to women's career needs, offering not just job listings but also mentorship, community support, and resources to help women overcome unique challenges in their professional journey.",
            
            "how successful is jobsforher": "JobsForHer has helped thousands of women find meaningful employment, advance in their careers, and return to the workforce after career breaks. We work with hundreds of companies committed to diversity and inclusion."
        }
        
        # Default response if no match is found
        answer = "I don't have specific information on that. Please check our website for more details or contact our support team."
        
        # Find the closest matching question
        for question, response in faq_db.items():
            if any(keyword in user_message for keyword in question.split()):
                answer = response
                break
        
        # Send the response
        dispatcher.utter_message(template="utter_faq", faq_answer=answer)
        return []

class ActionAddressGenderBias(Action):
    """Action to address gender-biased questions."""

    def name(self) -> Text:
        return "action_address_gender_bias"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        """Address gender-biased questions by providing positive information about women in the workplace."""
        
        # Gender bias patterns to detect
        gender_bias_patterns = [
            "women can't", "women are not", "women don't", "women should not",
            "women inferior", "women weaker", "women less", "women unable",
            "not suitable for women", "not appropriate for women",
            "men are better", "men do better", "better than women"
        ]
        
        # Success stories to counter gender bias
        success_stories = [
            "Did you know that companies with more women in leadership positions often outperform those with less gender diversity? Research shows diverse teams make better decisions.",
            
            "Women leaders like Indra Nooyi (former PepsiCo CEO), Mary Barra (GM CEO), and Kiran Mazumdar-Shaw (Biocon founder) have transformed their industries and proven that women excel in leadership roles.",
            
            "Research by McKinsey shows that companies in the top quartile for gender diversity are 25% more likely to have above-average profitability than companies in the bottom quartile.",
            
            "NASA's Katherine Johnson, Dorothy Vaughan, and Mary Jackson were essential to the success of U.S. space missions, proving women's capabilities in STEM fields.",
            
            "Women entrepreneurs start 40% of businesses in the US, generating $1.8 trillion in revenue annually according to American Express."
        ]
        
        # Get the latest user message
        user_message = tracker.latest_message.get('text', '').lower()
        
        # Check if the message contains gender bias
        contains_bias = any(pattern in user_message for pattern in gender_bias_patterns)
        
        if contains_bias:
            # Send the default response
            dispatcher.utter_message(template="utter_address_gender_bias")
            
            # Also send a success story
            import random
            dispatcher.utter_message(text=random.choice(success_stories))
        else:
            # If not clearly biased, still provide positive information
            dispatcher.utter_message(template="utter_women_empowerment")
        
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
        
        if slot_value and len(slot_value) > 2:
            # Valid job role
            return {"job_role": slot_value}
        else:
            # Invalid job role
            dispatcher.utter_message(text="Please provide a valid job role, such as 'Software Developer' or 'Marketing Manager'.")
            return {"job_role": None}

    def validate_location(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate location value."""
        
        if slot_value and len(slot_value) > 2:
            # Valid location
            return {"location": slot_value}
        else:
            # Invalid location
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
        
        # Experience can be a number or a range
        if slot_value:
            # Valid experience
            return {"experience": slot_value}
        else:
            # Invalid experience
            dispatcher.utter_message(text="Please provide your years of experience, such as '2 years' or 'entry level'.")
            return {"experience": None}