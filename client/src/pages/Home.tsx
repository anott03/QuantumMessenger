import "./styles/Home.css";
import { useQuantumKeyGen } from '../api/keygen';
import { useNavigate } from 'react-router-dom';
import {useSendMessage} from "../api/send-message";
import { nanoid } from "@reduxjs/toolkit";
import {useFetchMessages} from "../api/fetch-messsages";
import {useFetchKey} from "../api/fetch-key";
import { useEffect, useState } from "react";
import { useAppSelector } from '../redux/hooks';
import { selectUser } from '../redux/reducers/userSlice';

const Home = () => {
  const keygen = useQuantumKeyGen();
  let navigate = useNavigate();
  const sendMessage = useSendMessage();
  const fetchMessages = useFetchMessages();
  // TODO: actual decryption of messages; right now this just renders fetched data
  // without a considering the encryption
  const fetchKey = useFetchKey();
  const user = useAppSelector(selectUser);

  // const messageList = async () => {
    // let messages = await fetchMessages(user.username ?? "test")
    // let reconstructeds = []
    // for (const message in messages) {

      // // @ts-ignore
      // let keyStr = fetchKey(message["message_id"]).toString()

      // // @ts-ignore
      // let content = message["content"]
      // let decryptedBytes = ""
      // let keyPointer = 0
      // for (let i = 0; i < content.length; i++) {
        // let messageBit = Number.parseInt(content[i])
        // let keyBit = Number.parseInt(keyStr[keyPointer])
        // decryptedBytes += messageBit === keyBit ? "0" : "1"
        // keyPointer += 1
        // keyPointer %= keyStr.length
      // }
      // let reconstructed = ""
      // for (let i = 0; i < decryptedBytes.length; i+=7) {
        // let chunk = decryptedBytes.slice(i, i+7)
        // reconstructed += String.fromCharCode(Number.parseInt(chunk, 2))
      // }
      // reconstructeds.push(reconstructed)
    // }
    // return reconstructeds
  // }

  const onFormSubmit = (e: any) => {
    e.preventDefault();

    async function x() {
      let message: String = e.target["message-input"].value;
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
      sendMessage(messageId, xorBytes);
      console.log(message, key);
    }

    x().catch(console.error);
  }

  useEffect( () => {
    console.log("USER", user);
    fetchMessages(user.username ?? "test");
    console.log(user.messages);
  }, []);

  return (
    <div className="home">
      <div className="header">
        <p onClick={() => navigate("/", { replace: true })}>QuantumMessenger</p>
        <button>Profile</button>
      </div>

      <div className="home__body">
        <div className="sidebar">
          <div className="sidebar-item selected">
            <h3>Messages</h3>
          </div>
        </div>

        <div className="messages">
          <form className="message-form" onSubmit={onFormSubmit}>
            <input id="message-input" type="text" placeholder="Enter Message Here"/>
            <button type="submit">Send</button>
          </form>
          {
            user.messages.map((message: any) => <div key={nanoid()} className="message">
              <p><strong>{message.sender}</strong></p>
              <p>{message.content}</p>
            </div>)
          }
        </div>
      </div>
    </div>
  );
}

export default Home;
