# test_faq.py
from actions import ActionHandleFAQ
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk import Tracker

class MockTracker(Tracker):
    def __init__(self, message):
        self.latest_message = {'text': message}
    
    def get_slot(self, slot_name):
        return None

def test_faq_action():
    action = ActionHandleFAQ()
    dispatcher = CollectingDispatcher()
    
    # Test cases - list of (input, expected_in_output)
    test_cases = [
        ("What is JobsForHer?", "platform dedicated to accelerating women's careers"),
        ("How can JobsForHer help me?", "find job opportunities tailored to your skills"),
        ("Is JobsForHer for men too?", "primary focus is on women's career advancement"),
        ("Something completely unrelated", "don't have specific information"),
    ]
    
    for test_input, expected_output in test_cases:
        tracker = MockTracker(test_input)
        action.run(dispatcher, tracker, {})
        
        # Check if expected_output is in the response
        response_text = dispatcher.messages[-1]['text'] if dispatcher.messages else ""
        assert expected_output.lower() in response_text.lower(), f"Failed on input: {test_input}\nExpected: {expected_output}\nGot: {response_text}"

if __name__ == "__main__":
    test_faq_action()
    print("All FAQ tests passed!")