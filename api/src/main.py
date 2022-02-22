from fastapi import FastAPI
from pydantic import BaseModel
import uuid
from BB84 import BB84


"""
--- API Flow ---
- Client requests key generation for a specific user and message
- Portion of quantum computer allocated to that user runs BB84 protocol
    - Quantum teleportation to send qubits to the portion allocated to the
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


class UserRequest(BaseModel):
    username: str
    keys: {}
    messages: {}


class MessageRequest(BaseModel):
    username: str
    user_id: str
    receiver_id: str
    message_body: str
    message_id: int


app = FastAPI()
registered_users = {}  # keys: user ID; values: UserData object
# active_users = []
# for the sake of simplicity we will only have one active user
# we would ultimately need to make instances of the API for every active user
# which would entail bundling all functionality into a class and creating
# an instance of that class for each user so that an API endpoint looks
# something like:
# @app.get("/")
# def root(user: UserRequest):
#   active_user[username].api.root()
active_user = None
bb84 = BB84()


def generate_id() -> str:
    return str(uuid.uuid4())


@app.get("/")
def root():
    return {"message": "Hello World!"}


# USER STUFF
@app.post("/v1/create-user")
def create_user(user: UserRequest):
    registered_users[generate_id()] = UserData(user.username)


@app.post("/v1/login")
def login(user: UserRequest):
    global active_user
    active_user = user.username


@app.post("/v1/logout")
def logout(user: UserRequest):
    global active_user
    if user.username in active_user:
        active_user = None


# QUANTUM KEY GENERATION THINGS
@app.post("/v1/qc/generate-key")
def generate_key(message: MessageRequest):
    pass


@app.post("/v1/fetch-key")
def fetch_key(message_req: MessageRequest):
    user = registered_users[message_req.user_id]
    return user.keys[message_req.message_id]
