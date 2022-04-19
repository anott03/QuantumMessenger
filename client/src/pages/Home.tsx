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
        hello
      </div>
    </div>
  );
}

export default Home;
