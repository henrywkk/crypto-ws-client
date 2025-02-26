
def subscribe_user_balance():
    body = {
        "method": "subscribe",
        "params": {
            "channels": ["user.balance"]
        }
    }
    return body

def unsubscribe_user_balance():
    body = {
        "method": "unsubscribe",
        "params": {
            "channels": ["user.balance"]
        }
    }
    return body