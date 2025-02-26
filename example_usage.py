from ws_client import CryptoWSClient
from payload.channel import *
import time

# Initialize the client
client = CryptoWSClient(env="uat.ro")

# Initial subscription request
# message1 = {
#     "id": 1,
#     "method": "unsubscribe",
#     "params": {
#         "channels": ["user.balance"]
#     }
# }
msg1 = unsubscribe_user_balance()

# Start the WebSocket
client.start()
time.sleep(5)
client.send_message(msg1)

# Wait a bit to ensure connection and authentication
time.sleep(5)

# Send a new message while the connection is open
msg2 = subscribe_user_balance()
client.send_message(msg2)

# Keep the program running
client.run()