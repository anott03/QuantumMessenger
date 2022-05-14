import "./styles/Home.css";
import { useQuantumKeyGen } from '../api/keygen';
import { useNavigate } from 'react-router-dom';
import {useSendMessage} from "../api/send-message";
import { nanoid } from "@reduxjs/toolkit";
import {useFetchMessages} from "../api/fetch-messsages";
import {useFetchKey} from "../api/fetch-key";
import { useEffect, useState } from "react";
import { useAppSelector, useAppDispatch } from '../redux/hooks';
import { selectUser, setUser } from '../redux/reducers/userSlice';
import { setMessages } from "../redux/reducers/userSlice";

const Home = () => {
  const keygen = useQuantumKeyGen();
  let navigate = useNavigate();
  const sendMessage = useSendMessage();
  const fetchMessages = useFetchMessages();
  // TODO: actual decryption of messages; right now this just renders fetched data
  // without a considering the encryption
  const fetchKey = useFetchKey();
  const user = useAppSelector(selectUser);
  const dispatch = useAppDispatch()

  const onFormSubmit = (e: any) => {
    e.preventDefault();

    async function x(message: String, receiver: String) {
      let messageId = nanoid();
      const key = await keygen(messageId);
      const keyStr = key.toString()  // temp, for testing
      let messageBytes = ""
      for (let i = 0; i < message.length; i++) {
        messageBytes += message.charCodeAt(i).toString(2).padStart(7, "0")
      }
      let xorBytes = ""
      let keyPointer = 0
      for (let i = 0; i < messageBytes.length; i++) {
        let messageBit = Number.parseInt(messageBytes[i])
        let keyBit = Number.parseInt(keyStr[keyPointer])
        xorBytes += messageBit === keyBit ? "0" : "1"
        keyPointer += 1
        keyPointer %= keyStr.length
      }
      // xorBytes now contains an encrypted message
      sendMessage(messageId, xorBytes, receiver);
      console.log(message, key);

    }

    let _message: String = e.target['message-input'].value;
    let _receiver: String = e.target['receiver-input'].value;
    //@ts-ignore
    document.getElementById("message-input-form").reset();

    x(_message, _receiver).catch(console.error);
  }

  useEffect( () => {
    if (!user.username) {
      navigate("/login")
    }
    console.log("USER", user);
    fetchMessages(user.username ?? "test2")
    console.log(user.messages);
  }, []);

  const logoutClicked = () => {
    dispatch(setUser({username: undefined}))
    navigate("/")
  }

  return (
    <div className="home">
      <div className="header">
        <p onClick={() => navigate("/", { replace: true })}>QuantumMessenger</p>
        <button onClick={logoutClicked}>Logout</button>
      </div>

      <div className="home__body">
        <div className="sidebar">
          <div className="sidebar-item selected">
            <h3>Messages</h3>
          </div>
        </div>

        <div className="messages">
          <form id="message-input-form" className="message-form" onSubmit={onFormSubmit}>
            <input id="receiver-input" type="text" placeholder="Enter Recipient Here" style={{flexGrow: "1"}}/>
            <input id="message-input" type="text" placeholder="Enter Message Here" style={{flexGrow: "5", marginLeft: "10px", marginRight: "10px"}}/>
            <button type="submit">Send</button>
          </form>
          <br/>
          <button onClick={() => fetchMessages(user.username ?? "test")} style={{width: "20%", alignSelf: "center"}}>Refresh</button>
          <br/>
          <hr style={{marginBottom: "10px"}}/>
          {
            user.messages.map((message: any) => <div key={nanoid()} className="message">
              <p><strong>{message.sender}</strong> at {message.timestamp}</p>
              <p>{message.content}</p>
            </div>)
          }
        </div>
      </div>
    </div>
  );
}

export default Home;
