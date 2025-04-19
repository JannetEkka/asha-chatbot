# test_conversations.py
import requests
import json
import time

def send_message(sender_id, message_text):
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": sender_id,
        "message": message_text
    }
    response = requests.post(url, json=payload)
    return response.json()

def run_test_conversation():
    sender = f"test_user_{int(time.time())}"
    
    # Test basic greetings
    print("Testing greeting...")
    responses = send_message(sender, "Hello")
    print(f"Bot: {responses[0]['text'] if responses else 'No response'}")
    
    # Test job search
    print("\nTesting job search...")
    responses = send_message(sender, "I'm looking for a job")
    print(f"Bot: {responses[0]['text'] if responses else 'No response'}")
    
    # Provide job role
    responses = send_message(sender, "Software developer")
    print(f"Bot: {responses[0]['text'] if responses else 'No response'}")
    
    # Provide location
    responses = send_message(sender, "Bangalore")
    print(f"Bot: {responses[0]['text'] if responses else 'No response'}")
    
    # Provide experience
    responses = send_message(sender, "3 years")
    print(f"Bot: {responses[0]['text'] if responses else 'No response'}")
    
    # Check job results
    print("\nExpecting job results...")
    if responses and len(responses) > 0:
        print(f"Bot: {responses[0]['text']}")
    else:
        print("No job results returned")
    
    # Test events query
    print("\nTesting events query...")
    responses = send_message(sender, "Tell me about upcoming events")
    print(f"Bot: {responses[0]['text'] if responses else 'No response'}")
    
    # Test FAQ
    print("\nTesting FAQ...")
    responses = send_message(sender, "What is JobsForHer?")
    print(f"Bot: {responses[0]['text'] if responses else 'No response'}")

if __name__ == "__main__":
    run_test_conversation()