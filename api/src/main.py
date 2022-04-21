from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
from BB84 import ParallelBB84
from collections import defaultdict


"""
--- API Flow ---
- Client requests key generation for a specific user and message
- Portion of quantum computer allocated to that user runs BB84 protocol Quantum teleportation to send qubits to the portion allocated to the
      receiver
- Keys are stored classically in a user-specific dictionary after the protocol
  is run & measured
- Client can retrieve keys for a specific message id after they are generated
    - Encryption happens classically on the client side
"""


class UserData:
    def __init__(self, username):
        self.name = username
        self.keys = {}  # {message ID: key}
        self.messages = {}  # {message ID: content}


class PendingMessage:
    def __init__(self, sender, message_id, message_content):
        self.sender = sender
        self.message_id = message_id
        self.message_content = message_content


class UserRequest(BaseModel):
    username: str


class MessageSendRequest(BaseModel):
    username: str
    user_id: str
    receiver_id: str
    message_body: str
    message_id: int


class MessageFetchRequest(BaseModel):
    username: str
    user_id: str


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
pending_messages = defaultdict(list[PendingMessage])  # keys: receiver IDs; values: [pending messages]


def generate_id() -> str:
    return str(uuid.uuid4())


@app.get("/")
def root():
    return {"message": "Hello World!"}


# USER STUFF
@app.post("/v1/create-user")
def create_user(user: UserRequest):
    userID = generate_id()
    registered_users[userID] = UserData(user.username)
    return {"id": userID}

@app.post("/v1/login")
def login(user: UserRequest):
    global active_user
    active_user = user.username


@app.post("/v1/logout")
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
    # TODO implement this based on time scheme from client
    return messages


keys = {}  # maps message IDs to associated keys
inboxes = defaultdict(list[Message])

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

@app.post("/v1/generate-key")
def generate_key(key_gen_req: KeyGenRequest):
    qc_state[key_gen_req.message_id] = bb84.sender_protocol()
    key = bb84.receiver_protocol(qc_state[key_gen_req.message_id])
    keys[key_gen_req.message_id] = key
    return {"key": key}


@app.post("/v1/fetch-key")
def fetch_key(key_fetch_req: KeyFetchRequest):
    return {"key": keys[key_fetch_req.message_id]}


@app.post("/v1/send-message")
def send_message(send_req: SendMessageRequest):
    inboxes[send_req.receiver_id].append(Message(
        send_req.sender_id, send_req.receiver_id, send_req.message_id, send_req.message_content, send_req.timestamp
    ))


@app.post("/v1/fetch-messages")
def fetch_messages(fetch_req: FetchMessageRequest):
    target_messages = sort_timestamps([fetch_req.receiver_id])
    return [{"message_id": message.message_id,
             "sender": message.sender,
             "content": message.content} for message in target_messages]
