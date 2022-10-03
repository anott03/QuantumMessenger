# QuantumMessenger

Pilot project for an instant messaging service that utilizes quantum key distribution for end-to-end encryption. A deployed version can be viewd [here](https://qm.twdl.us).

### Goals
+ Create a backend in Python using FastAPI and Qiskit
  + Implement quantum random number generation to produce initial keys
  + Implement the BB84 protocol for quantum key distribution to share a key between users
+ Create a front-end in TypeScript with React
  + Communicate between client and API to send messages
  + Implement a user authentication scheme

### Possible Additions (time permitting)
+ Create an eavesdropper interface where users can simulate intercepting a message
+ Implement multiple channels with user permissions
