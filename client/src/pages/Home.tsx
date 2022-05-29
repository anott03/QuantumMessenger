import "./styles/Home.css";
import { useQuantumKeyGen } from '../api/keygen';
import { useNavigate } from 'react-router-dom';
import { useSendMessage } from "../api/send-message";
import { nanoid } from "@reduxjs/toolkit";
import { useFetchMessages } from "../api/fetch-messsages";
import { useEffect, useState } from "react";
import { useAppSelector, useAppDispatch } from '../redux/hooks';
import { selectUser, setUser } from '../redux/reducers/userSlice';
import { setMessages } from "../redux/reducers/userSlice";
import { signOut, getAuth } from 'firebase/auth';
import { useInteractingUsers } from "../api/interacting-users";

const Home = () => {
  const keygen = useQuantumKeyGen();
  let navigate = useNavigate();
  const sendMessage = useSendMessage();
  const fetchMessages = useFetchMessages();
  const interactingUsers = useInteractingUsers();
  const user = useAppSelector(selectUser);
  const dispatch = useAppDispatch()
  const [focusedUser, setFocusedUser] = useState("New Message")

  const onFormSubmit = (e: any) => {
    e.preventDefault();

    async function encryptAndSend(message: String, receiver: String) {
      // create ID for message and generate a key
      let messageId = nanoid();
      const key = await keygen(messageId);
      const keyStr = key.toString()
      // convert message to ASCII bytes
      let messageBytes = ""
      for (let i = 0; i < message.length; i++) {
        messageBytes += message.charCodeAt(i).toString(2).padStart(7, "0")
      }
      // XOR the message bytes with the key, repeating the key bits as necessary
      let xorBytes = ""
      let keyPointer = 0
      for (let i = 0; i < messageBytes.length; i++) {
        let messageBit = Number.parseInt(messageBytes[i])
        let keyBit = Number.parseInt(keyStr[keyPointer])
        xorBytes += messageBit === keyBit ? "0" : "1"
        keyPointer += 1
        keyPointer %= keyStr.length
      }
      // send the encrypted message
      sendMessage(messageId, xorBytes, receiver);
    }

    let _message: String = e.target['message-input'].value;
    if (focusedUser === "New Message") {
      let _receiver: String = e.target['receiver-input'].value;
      //@ts-ignore
      document.getElementById("message-input-form").reset();
      encryptAndSend(_message, _receiver).catch(console.error);
    } else {
      //@ts-ignore
      document.getElementById("message-input-form").reset();
      encryptAndSend(_message, focusedUser).catch(console.error);
    }
  }

  useEffect( () => {
    if (!user.email) {
      navigate("/")
    }
    console.log("USER", user);
    fetchMessages(user.email ?? "test2")
    console.log(user.messages);
  }, []);

  const logoutClicked = () => {
    const auth = getAuth();
    signOut(auth).then(function() {
      dispatch(setUser({
        displayName: undefined,
        email: undefined
      }))
    });
    navigate("/")
  }

  const filteredMessages = () => {
    return user.messages.filter(msg => msg.sender === focusedUser)
  }

  const refresh = () => {
    fetchMessages(user.email ?? "")
    interactingUsers(user.email ?? "")
  }

  return (
    <div className="home">
      <div className="header">
        <p onClick={() => navigate("/", { replace: true })}>QuantumMessenger</p>
        <div>
          <p>{user.email}</p>
          <button onClick={logoutClicked}>Logout</button>
        </div>
      </div>

      <div className="home__body">
        <div className="sidebar">
          <h2 className="sidebar-item">Messages</h2>
          <hr/><br/><br/>
          <div className={focusedUser === "New Message" ? "sidebar-item selected" : "sidebar-item"} onClick={() => setFocusedUser("New Message")}>
            <h3 >New Message</h3>
          </div>
          {
            user.interactingUsers.map((user: any) => <div key={nanoid()} className={user === focusedUser ? "sidebar-item selected" : "sidebar-item"} onClick={() => setFocusedUser(user)}>
              <h3>{user}</h3>
            </div>)
          }
        </div>

        <div className="messages">
          <form id="message-input-form" className="message-form" onSubmit={onFormSubmit}>
            { focusedUser === "New Message" && <input id="receiver-input" type="text" placeholder="Enter Recipient Here" style={{flexGrow: "1"}}/> }
            <input id="message-input" type="text" placeholder="Enter Message Here" style={{flexGrow: "5", marginLeft: "10px", marginRight: "10px"}}/>
            <button type="submit">Send</button>
          </form>
          <br/>
          <button onClick={() => refresh()} style={{width: "20%", alignSelf: "center"}}>Refresh</button>
          <br/>
          <hr style={{marginBottom: "10px"}}/>
          { filteredMessages().length !== 0 ? (
            filteredMessages().map((message: any) => <div key={nanoid()} className="message">
              <p><strong>{message.sender}</strong> at {message.timestamp}</p>
              <p>{message.content}</p>
            </div>)
            ) : (<h3 style={{textAlign: "center", marginTop: "2rem"}}>You haven't received any messages from this user yet.</h3>)
          }
        </div>
      </div>
    </div>
  );
}

export default Home;
