import websocket
import json
import time
import hmac
import hashlib
from threading import Thread
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

class CryptoWSClient:
    def __init__(self):
        """Initialize the WebSocket client with values from .env."""
        self.api_key = os.getenv("API_KEY")
        self.api_secret = os.getenv("API_SECRET")
        self.environment = os.getenv("ENVIRONMENT", "production").lower()

        if not self.api_key or not self.api_secret:
            raise ValueError("API_KEY and API_SECRET must be set in the .env file.")

        self.ws_url = (
            "wss://uat-stream.3ona.co/v1/user" if self.environment == "UAT"
            else "wss://stream.crypto.com/v1/user"
        )
        self.ws = None
        self.authenticated = False

    def _generate_signature(self, params):
        """Generate HMAC-SHA256 signature for authentication."""
        param_str = "".join([f"{k}{v}" for k, v in sorted(params.items())])
        sign_str = f"{param_str}{self.api_secret}"
        return hmac.new(
            self.api_secret.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

    def _authenticate(self):
        """Prepare and return authentication request."""
        nonce = str(int(time.time() * 1000))
        params = {
            "api_key": self.api_key,
            "nonce": nonce
        }
        sig = self._generate_signature(params)
        auth_request = {
            "id": 0,
            "method": "public/auth",
            "params": {
                "api_key": self.api_key,
                "nonce": nonce,
                "sig": sig
            }
        }
        return json.dumps(auth_request)

    def _respond_heartbeat(self):
        """Prepare and return heartbeat response."""
        heartbeat_response = {
            "id": -1,
            "method": "public/respond-heartbeat"
        }
        return json.dumps(heartbeat_response)

    def on_open(self, ws):
        """Handle WebSocket connection opening."""
        print("WebSocket connection opened.")
        # Send authentication request
        ws.send(self._authenticate())

    def on_message(self, ws, message):
        """Handle incoming WebSocket messages."""
        data = json.loads(message)
        print("Received:", json.dumps(data, indent=2))

        # Check for successful authentication
        if data.get("method") == "public/auth" and data.get("code") == 0:
            self.authenticated = True
            print("Authentication successful.")

        # Respond to heartbeat messages
        if data.get("method") == "public/heartbeat":
            ws.send(self._respond_heartbeat())
            print("Sent heartbeat response.")

    def on_error(self, ws, error):
        """Handle WebSocket errors."""
        print(f"Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket closure."""
        print("WebSocket connection closed.")

    def start(self, request):
        """Start the WebSocket client and send the initial request."""
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        # Run WebSocket in a separate thread
        ws_thread = Thread(target=self.ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()

        # Wait for connection and authentication
        while not self.ws.sock or not self.authenticated:
            time.sleep(1)

        # Send the user request
        self.ws.send(json.dumps(request))

        # Keep the main thread alive
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.ws.close()
            print("Client stopped.")