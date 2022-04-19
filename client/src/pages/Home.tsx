import "./styles/Home.css";
import React, { useEffect } from 'react';
import { useQuantumKeyGen } from '../api/keygen';

const Home = () => {
  const keygen = useQuantumKeyGen();

  useEffect(() => {
    async function x() {
      console.log(await keygen());
    }
    x().catch(console.error);
  }, [])

  return (
    <div className="home">
      <div className="header">
        <p>QuantumMessenger</p>
        <button>Profile</button>
      </div>


      <div className="home__body">
        <div className="sidebar">
          <div className="contact selected">
            <h3>New Message</h3>
            <p>some text...</p>
          </div>

          <div className="contact">
            <h3>Rohan Malik</h3>
            <p>some text...</p>
          </div>

          <div className="contact">
            <h3>Paco Martin</h3>
            <p>some text...</p>
          </div>
        </div>

        <div className="messages">
          <form className="message-form">
            <input type="text" placeholder="Enter Message Here"/>
            <button type="submit">Send</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Home;
