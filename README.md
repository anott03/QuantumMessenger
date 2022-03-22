# QuantumMessenger

Pilot project for an instant messaging service that utilizes quantum key distribution for end-to-end encryption.

### Goals
The core components of this project.
+ Create a backend in Python using FastAPI and Qiskit
  + Implement quantum random number generation to produce initial keys
  + Implement the BB84 protocol for quantum key distribution to share a key between users
+ Create a front-end in TypeScript with React
  + Communicate between client and API to send messages
  + Implement a user authentication scheme

### Structure and Workflow
This project has two components, the client and the api, each of which are contained within a docker container and connected using docker-compose. Thus, the entrypoint to the system is `docker-compose up`.

#### API
+ Build with python, using Qiskit for our quantum algoritms and FastAPI to run the API

#### Client
+ Build using Typescript and ReactJS

### Possible Additions (time permitting)
Features we would like to add if possible.
+ Create an eavesdropper interface where users can simulate intercepting a message
+ Implement multiple channels with user permissions
