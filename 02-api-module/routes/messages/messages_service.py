from routes.messages.message import Message


def get_public_message():
    return Message(
        "The API doesn't require an access token to share this message."
    )

