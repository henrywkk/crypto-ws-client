from ws_client import CryptoWSClient

# Initialize the client (loads API_KEY, API_SECRET, ENVIRONMENT from .env)
client = CryptoWSClient()

# Example request to subscribe to user.balance
request = {
    "id": 1,
    "method": "subscribe",
    "params": {
        "channels": ["user.balance"]
    }
}

# Start the client with the request
client.start(request)