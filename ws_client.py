import websocket
import json
import time
import hmac
import hashlib
from threading import Thread
from dotenv import load_dotenv
import os

# Enable WebSocket tracing for debugging (optional, comment out if not needed)
# websocket.enableTrace(True)

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

        # Use updated URLs from documentation
        self.ws_url = os.getenv("WS_URL") or (
            "wss://uat-stream.3ona.co/exchange/v1/user" if self.environment == "sandbox"
            else "wss://stream.crypto.com/exchange/v1/user"
        )
        self.ws = None
        self.authenticated = False

    def _generate_signature(self, method, id, nonce):
        """Generate HMAC-SHA256 signature for authentication."""
        param_str = ""
        sign_str = f"{method}{str(id)}{self.api_key}{param_str}{str(nonce)}"
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            sign_str.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        print(f"Generated signature: {signature} for string: {sign_str}")
        return signature

    def _authenticate(self):
        """Prepare and return authentication request."""
        id = 1
        method = "public/auth"
        nonce = int(time.time() * 1000)
        sig = self._generate_signature(method, id, nonce)
        auth_request = {
            "id": id,
            "method": method,
            "api_key": self.api_key,
            "sig": sig,
            "nonce": nonce
        }
        print("Sending authentication request:", json.dumps(auth_request, indent=2))
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
        print(f"WebSocket connection opened to {self.ws_url}")
        ws.send(self._authenticate())

    def on_message(self, ws, message):
        """Handle incoming WebSocket messages."""
        data = json.loads(message)
        print("Received:", json.dumps(data, indent=2))

        if data.get("method") == "public/auth":
            if data.get("code") == 0:
                self.authenticated = True
                print("Authentication successful.")
            else:
                print(f"Authentication failed with code {data.get('code')}: {data.get('message')}")

        if data.get("method") == "public/heartbeat":
            ws.send(self._respond_heartbeat())
            print("Sent heartbeat response.")

    def on_error(self, ws, error):
        """Handle WebSocket errors."""
        print(f"WebSocket Error: {error}")

    def on_close(self, ws, close_status_code, close_msg):
        """Handle WebSocket closure."""
        print(f"WebSocket connection closed: {close_status_code} - {close_msg}")

    def start(self, request):
        """Start the WebSocket client and send the initial request."""
        print(f"Attempting connection to {self.ws_url}")
        self.ws = websocket.WebSocketApp(
            self.ws_url,
            on_open=self.on_open,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )

        ws_thread = Thread(target=self.ws.run_forever)
        ws_thread.daemon = True
        ws_thread.start()

        while not self.ws.sock or not self.authenticated:
            time.sleep(1)

        print("Sending request:", json.dumps(request, indent=2))
        self.ws.send(json.dumps(request))

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.ws.close()
            print("Client stopped.")