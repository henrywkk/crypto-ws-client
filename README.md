# Crypto.com Exchange WebSocket Client

A Python WebSocket client for interacting with the Crypto.com Exchange v1 WebSocket API. This client supports switching between UAT Sandbox and Production environments, authenticates using API key and secret, and allows subscription to various WebSocket channels (e.g., `user.balance`, order creation).

## Features
- Switch between UAT Sandbox and Production environments.
- Authenticate using user-provided API key and secret.
- Supports all WebSocket API methods (e.g., `user.balance`, order creation, etc.).
- Template-based user input for WebSocket requests.

## Prerequisites
- Python 3.6+
- Install dependencies: `pip install -r requirements.txt`

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/henrywkk/crypto-ws-client.git
   cd crypto-ws-client
   ```

2. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create an `.env` file by copying the example:
   ```bash
   cp .env.example .env
   ```
4. Edit `.env` with your API key, secret, and environment:
   ```
   API_KEY=your_api_key
   API_SECRET=your_api_secret
   ENVIRONMENT=production  # or UAT
   ```


## Usage
1. Import and initialize the client in your script:
    ```python
    from ws_client import CryptoWSClient

    # Initialize with API key, secret, and environment
    client = CryptoWSClient(
        api_key="your_api_key",
        api_secret="your_api_secret",
        environment="production"  # or "sandbox"
    )
    ```

2. Start the client and send a subscription request:
    ```python
    # Example subscription to user.balance
    request = {
        "id": 1,
        "method": "subscribe",
        "params": {
            "channels": ["user.balance"]
        }
    }
    client.start(request)
    ```

3. See `example_usage.py` for a full example.


## Request Template
The client accepts JSON requests following this structure:
```json
{
  "id": 1,
  "method": "subscribe",
  "params": {
    "channels": ["user.balance"]
  }
}
```

Supported methods include subscribe, unsubscribe, and others as per the [Crypto.com Exchange v1 WebSocket API documentation](https://exchange-docs.crypto.com/exchange/v1/rest-ws/index.html).


## Environment Configuration
- Loaded from `.env` file:
  - `ENVIRONMENT=UAT`: UAT Sandbox (`wss://uat-stream.3ona.co/v1/user`).
  - `ENVIRONMENT=production`: Production (`wss://stream.crypto.com/v1/user`).

## Dependencies
Listed in `requirements.txt`:
- `websocket-client`: For WebSocket communication.
- `python-dotenv`: For loading environment variables from `.env`.
- `hmac`, `hashlib`: For authentication signature generation (built-in).

## Example
Run the example script:
```bash
python example_usage.py
```


## Notes
- Ensure your API key and secret have appropriate permissions set in the Crypto.com Exchange User Center.
- Keep your `.env` file secure and do not commit it to version control (it’s ignored by `.gitignore` if added).
- Responses from the WebSocket are printed to the console; modify the `on_message` handler in `ws_client.py` for custom processing.

## License
MIT License