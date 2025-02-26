from ws_client import CryptoWSClient
import time

# Initialize the client
client = CryptoWSClient()

# Initial subscription request
message1 = {
    "id": 1,
    "method": "unsubscribe",
    "params": {
        "channels": ["user.balance"]
    }
}

# Start the WebSocket
client.start()
time.sleep(5)
client.send_message(message1)

# Wait a bit to ensure connection and authentication
time.sleep(5)

# Send a new message while the connection is open
new_message = {
    "method": "subscribe",
    "params": {
        "channels": ["user.balance"]
    }
}
client.send_message(new_message)

# Keep the program running
client.run()