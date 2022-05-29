from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from BB84 import ParallelBB84
from collections import defaultdict
from datetime import datetime, timezone
import pytz

"""
--- QuantumMessenger API ---
Backend for QuantumMessenger that handles all of the following:
-> User management: registration, login, and logout
-> Quantum key generation: creating and fetching keys tied to messages
-> Messaging: sending messages and fetching a user's inbox
"""

# === APP SETUP AND GLOBAL STATE ===
metadata_tags = [
    {
        "name": "create-user",
        "description": "Creates and registers a user on the app."
    },
    {
        "name": "login",
        "description": "Signs the user into the app, allowing them to send and receive messages."
    },
    {
        "name": "logout",
        "description": "Signs the user out of the app."
    },
    {
        "name": "generate-key",
        "description": "Creates a shared encryption key for a sender and receiver using the BB84 quantum protocol."
    },
    {
        "name": "fetch-key",
        "description": "Fetches the shared key associated with a given message ID."
    },
    {
        "name": "send-message",
        "description": "Sends a message to a recipient, end-to-end encrypted with a quantum generated key."
    },
    {
        "name": "fetch-messages",
        "description": "Fetches all messages sent to a user, encrypted with their respective keys."
    },
    {
        "name": "interacting-users",
        "description": "Returns a list of all users who have interacted (sent or received messages) with the given user."
    }
]

app = FastAPI()
registered_users = {}  # keys: user IDs; values: UserData objects
origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

active_user = None
bb84 = ParallelBB84(5)
qc_state = {}  # keys: message IDs; values: statevector objects
pending_messages = defaultdict(list)  # keys: receiver IDs; values: [pending messages]


def generate_id() -> str:
    return str(uuid.uuid4())


@app.get("/")
def root():
    return {"message": "Hello World!"}


# USER STUFF
@app.post("/v1/create-user", tags=["create-user"])
def create_user(user: UserRequest):
    userID = generate_id()
    registered_users[userID] = UserData(user.username)
    return {"id": userID}

@app.post("/v1/login", tags=["login"])
def login(user: UserRequest):
    global active_user
    active_user = user.username


@app.post("/v1/logout", tags=["logout"])
def logout(user: UserRequest):
    global active_user
    if user.username in active_user:
        active_user = None


# QUANTUM KEY GENERATION AND MESSAGING STUFF
# @app.post("/v1/qc/send-message")
# def send_message(message: MessageSendRequest):
#     if active_user != message.username:
#         # user not logged in
#         return {"err": "Error: user cannot send a message unless they are logged in"}
#     qc_state[message.message_id] = bb84.sender_protocol()
#     # create a pending message entry so the receiver knows that they have to complete the key exchange
#     # when they try to retrieve the message
#     pending_messages[message.receiver_id].append(PendingMessage(message.user_id, message.message_id, message.message_body))
#
#
# @app.post("/v1/fetch-message")
# def fetch_messages(fetch_req: MessageFetchRequest):
#     if active_user != fetch_req.username:
#         # user not logged in
#         return {"err": "Error: user cannot send a message unless they are logged in"}
#     messages = []
#     for pending_message in pending_messages[fetch_req.user_id]:
#         key = bb84.receiver_protocol(qc_state[pending_message.message_id])
#         messages.append({"key": key, "messageContent": pending_message.message_content})
#     return messages


# ---- Revised API Structure and Function ----

class Message:
    def __init__(self, sender, receiver, message_id, content, timestamp):
        self.sender = sender
        self.receiver = receiver
        self.message_id = message_id
        self.content = content
        self.timestamp = timestamp


def sort_timestamps(messages):
    return list(sorted(messages, key=lambda x: int(x.timestamp), reverse=True))

def formatted_time(ts):
    formatted = datetime.fromtimestamp(int(ts)/1000, pytz.timezone("US/Eastern")).strftime(f"%-I:%M %p on %b %-d, %Y")
    print(formatted)
    return formatted


keys = {}  # maps message IDs to associated keys
inboxes = defaultdict(list)

class KeyGenRequest(BaseModel):
    message_id: str

class KeyFetchRequest(BaseModel):
    message_id: str

class SendMessageRequest(BaseModel):
    sender_id: str
    receiver_id: str
    message_id: str
    message_content: str
    timestamp: str

class FetchMessageRequest(BaseModel):
    receiver_id: str

class InteractingUserRequest(BaseModel):
    username: str

@app.post("/v1/generate-key", tags=["generate-key"])
def generate_key(key_gen_req: KeyGenRequest):
    qc_state[key_gen_req.message_id] = bb84.sender_protocol()
    key = bb84.receiver_protocol(qc_state[key_gen_req.message_id])
    keys[key_gen_req.message_id] = key
    return {"key": key}


@app.post("/v1/fetch-key", tags=["fetch-key"])
def fetch_key(key_fetch_req: KeyFetchRequest):
    return {"key": keys[key_fetch_req.message_id]}


@app.post("/v1/send-message", tags=["send-message"])
def send_message(send_req: SendMessageRequest):
    inboxes[send_req.receiver_id].append(Message(
        send_req.sender_id, send_req.receiver_id, send_req.message_id, send_req.message_content, send_req.timestamp
    ))


@app.post("/v1/fetch-messages", tags=["fetch-message"])
def fetch_messages(fetch_req: FetchMessageRequest):
    target_messages = sort_timestamps(inboxes[fetch_req.receiver_id])
    return [{"message_id": message.message_id,
             "key": keys[message.message_id],
             "sender": message.sender,
             "content": message.content,
             "timestamp": formatted_time(message.timestamp)} for message in target_messages]
    # return [{"message_id": "test id",
    #          "sender": "test sender",
    #          "content": "test content"} for i in range(10)]

@app.post("/v1/interacting-users", tags=["interacting-users"])
def interacting_users(user_req: InteractingUserRequest):
    all_msgs = []  # each item is [msg object, sender, receiver]
    for user, inbox in inboxes.items():
        for msg in inbox:
            all_msgs.append([msg, msg.sender, user])
    interacting_msgs = []  # each item is [msg object, other user]
    for info in all_msgs:
        if info[1] == user_req.username:
            interacting_msgs.append([info[0], info[2]])
        elif info[2] == user_req.username:
            interacting_msgs.append([info[0], info[1]])
    interacting_msgs = list(sorted(interacting_msgs, key=lambda x: int(x[0].timestamp), reverse=True))
    return {"users": [item[0] for item in interacting_msgs]}
