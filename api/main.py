from fastapi import FastAPI
from pydantic import BaseModel
from qiskit import QuantumCircuit
from qiskit import Aer, assemble


class User(BaseModel):
    username: str


class Message(BaseModel):
    body: str
    sender: str
    receiver: str
    id: int


app = FastAPI()
registered_users = []
# active_users = []
# for the sake of simplicity we will only have one active user
active_user = None


@app.get("/")
def root():
    return {"message": "Hello World!"}


# USER STUFF
@app.post("/v1/create-user")
def create_user(user: User):
    registered_users.append(user.username)


@app.post("/v1/login")
def login(user: User):
    global active_user
    active_user = user.username


@app.post("/v1/logout")
def logout(user: User):
    global active_user
    if user.username in active_user:
        active_user = None


# QUANTUM KEY GENERATION THINGS
@app.post("/v1/qc/generate-key")
def generate_key(message: Message):
    pass


@app.post("/v1/qc/fetch-key")
def fetch_key(message: Message):
    pass
