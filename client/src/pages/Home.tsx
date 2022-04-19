import "./styles/Home.css";
import { useEffect } from 'react';
import { useQuantumKeyGen } from '../api/keygen';
import { useNavigate } from 'react-router-dom';
import * as forge from 'node-forge';

const Home = () => {
  const keygen = useQuantumKeyGen();
  let navigate = useNavigate();

  useEffect(() => {
    async function x() {
      console.log(await keygen());
    }
    x().catch(console.error);
  }, [])

  const onFormSubmit = (e: any) => {
    e.preventDefault();

    async function x() {
      let message: String = e.target["message-input"].value;
      const key = await keygen();
      console.log(message, key);
    }

    x().catch(console.error);
  }

  return (
    <div className="home">
      <div className="header">
        <p onClick={() => navigate("/", { replace: true })}>QuantumMessenger</p>
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
          <form className="message-form" onSubmit={onFormSubmit}>
            <input id="message-input" type="text" placeholder="Enter Message Here"/>
            <button type="submit">Send</button>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Home;
