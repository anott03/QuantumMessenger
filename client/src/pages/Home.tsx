import "./styles/Home.css";
import { useQuantumKeyGen } from '../api/keygen';
import { useNavigate } from 'react-router-dom';
import { useSendMessage } from "../api/send-message";
import { nanoid } from "@reduxjs/toolkit";
import { useFetchMessages } from "../api/fetch-messsages";
import { useEffect, useState } from "react";
import { useAppSelector, useAppDispatch } from '../redux/hooks';
import { selectUser, setUser } from '../redux/reducers/userSlice';
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
  const [focusedUser, setFocusedUser] = useState<string>("New Message")
  const [recipient, setRecipient] = useState<string>("");
  const [message, setMessage] = useState<string>("");

  const sendMessageClicked = (e: any) => {
    e.preventDefault();

    async function encryptAndSend(message: string, receiver: string) {
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

    let _message: string = message;
    if (focusedUser === "New Message") {
      let _receiver: string = recipient.toLowerCase();
      //@ts-ignore
      setMessage("");
      setRecipient("");
      encryptAndSend(_message, _receiver).catch(console.error);
    } else {
      //@ts-ignore
      setMessage("");
      setRecipient("");
      encryptAndSend(_message, focusedUser).catch(console.error);
    }
  }

  useEffect(() => {
    if (!user.email) {
      navigate("/")
    }
    fetchMessages(user.email ?? "test2")
    interactingUsers(user.email ?? "")
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
    <div className="home p-3">
      <div className="header flex flex-row justify-between items-center">
        <p className="font-sans text-2xl cursor-pointer" onClick={() => navigate("/", { replace: true })}>QuantumMessenger</p>
        <div className="flex flex-row jusitfy-between items-center">
          <p className="mr-2">{user.email} | </p>
          <button className="text-red-400" onClick={logoutClicked}>Logout</button>
        </div>
      </div>

      <div className="home__body flex flex-row mt-1 h-full">
        <div className="sidebar flex-0.2 mr-1">
          <div className="buttons mb-1 flex flex-row space-between">
            <button className="bg-violet-400 px-3 py-2 rounded-lg text-slate-900" onClick={() => setFocusedUser("New Message")}>New Message</button>
            <button className="bg-violet-400 px-3 py-2 rounded-lg text-slate-900" onClick={() => refresh()}>Refresh</button>
          </div>
          {
            user.interactingUsers.map((user: any) => <div key={nanoid()} className={user === focusedUser ? "sidebar-item selected" : "sidebar-item"} onClick={() => setFocusedUser(user)}>
              <h3>{user}</h3>
            </div>)
          }
        </div>

        <div className="messages flex-0.8 ml-1 flex flex-col p-2 pt-0 w-full">
          { focusedUser == "New Message" ?
            <div className="w-full flex flex-col">
              <input    className="rounded-lg px-3 py-2 flex-1 m-1 border-solid border-[1px] border-blue-400 bg-inherit focus:border-0" id="receiver-input" type="email" placeholder="Enter Recipient Here" value={recipient} onChange={(e: any) => setRecipient(e.target.value)}/>
              <textarea className="rounded-lg px-3 py-2 flex-1 m-1 border-solid border-[1px] border-blue-400 bg-inherit focus:border-0" id="message-input" placeholder="Enter Message Here" value={message} onChange={(e: any) => setMessage(e.target.value)}/>
              <button onClick={sendMessageClicked}>Send</button>
            </div>
          : filteredMessages().length !== 0 ? (
            <> <button className="" onClick={() => { setRecipient(focusedUser); setFocusedUser("New Message"); }}/>
              { filteredMessages().map((message: any) =>
              <div key={nanoid()} className="message mr-0">
                <p><strong>{message.sender}</strong> at {message.timestamp}</p>
                <p>{message.content}</p>
              </div>) } </>
            ) : (<h3 style={{textAlign: "center", marginTop: "2rem"}}>You have not yet received any messages from this user. Messages that you sent will not appear.</h3>)
          }
        </div>
      </div>
    </div>
  );
}

export default Home;
