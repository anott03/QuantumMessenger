import React, { useEffect } from 'react';
import { useQuantumKeyGen } from '../api/keygen';
import { SodiumPlus } from 'sodium-plus';

const Home = () => {
  const keygen = useQuantumKeyGen();

  useEffect(() => {
    async function x() {
      let sodium = await SodiumPlus.auto();
      console.log(await keygen());

      let key = await sodium.crypto_secretbox_keygen();
      let nonce = await sodium.randombytes_buf(24);
      let message = 'This is just a test message';
      // Message can be a string, buffer, array, etc.

      let ciphertext = await sodium.crypto_secretbox(message, nonce, key);
      console.log(ciphertext);
      let decrypted = await sodium.crypto_secretbox_open(ciphertext, nonce, key);
      console.log(decrypted.toString('utf-8'));
    }
    x().catch(console.error);
  }, [])

  return (
    <div></div>
  );
}

export default Home;
