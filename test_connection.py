import requests
import json

def test_rasa_server():
    """Test if the Rasa server is responding correctly"""
    url = "http://localhost:5005/webhooks/rest/webhook"
    payload = {
        "sender": "test_user",
        "message": "Hello"
    }
    
    print("Sending test message to Rasa server...")
    try:
        response = requests.post(url, json=payload)
        print(f"Status code: {response.status_code}")
        
        if response.status_code == 200:
            print("Response content:")
            print(json.dumps(response.json(), indent=2))
            return True
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
            return False
    except Exception as e:
        print(f"Error connecting to Rasa server: {e}")
        return False

def test_socketio_endpoint():
    """Test if the SocketIO endpoint is available"""
    url = "http://localhost:5005/socket.io/"
    
    print("\nChecking SocketIO endpoint...")
    try:
        response = requests.get(url)
        print(f"Status code: {response.status_code}")
        print(f"Response: {response.text[:100]}...")  # Show just the start of the response
        return response.status_code == 200
    except Exception as e:
        print(f"Error connecting to SocketIO endpoint: {e}")
        return False

if __name__ == "__main__":
    print("= Asha Chatbot Connection Test =")
    print("Testing REST webhook...")
    rest_success = test_rasa_server()
    
    socketio_success = test_socketio_endpoint()
    
    print("\n= Test Results =")
    print(f"REST API: {'✓ Working' if rest_success else '✗ Not working'}")
    print(f"SocketIO: {'✓ Working' if socketio_success else '✗ Not working'}")
    
    if not rest_success or not socketio_success:
        print("\nTroubleshooting tips:")
        print("1. Make sure Rasa server is running with: rasa run --enable-api --cors \"*\"")
        print("2. Make sure action server is running with: rasa run actions")
        print("3. Check if there are any firewall issues blocking the connections")
        print("4. Try restarting both servers")
    else:
        print("\nAll connections are working correctly! If you're still having issues with the")
        print("chat widget, try using the updated index.html file.")