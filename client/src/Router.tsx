import { useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Landing from './pages/Landing';
import Login from './pages/Login';
import { initializeApp } from 'firebase/app';

function Router() {
  // initialize firebase
  useEffect(() => {
    const firebaseConfig = {
      apiKey: "AIzaSyAa7uMqRSWTab7DskA5CNRrXifugl6dqWI",
      authDomain: "quantummessenger-3d04a.firebaseapp.com",
      projectId: "quantummessenger-3d04a",
      storageBucket: "quantummessenger-3d04a.appspot.com",
      messagingSenderId: "169274790805",
      appId: "1:169274790805:web:a4a762858d3c22e16e5c9c"
    }
    initializeApp(firebaseConfig);
  }, []);

  return (<Routes>
    <Route path="/" element={<Landing />}/>
    <Route path="/home" element={<Home />}/>
    <Route path="/login" element={<Login />}/>
  </Routes>);
}

export default Router;
