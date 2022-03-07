import React from 'react';
import { Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import Landing from './pages/Landing';
import Login from './pages/Login';

function Router() {
  return (<Routes>
    <Route path="/" element={<Landing />}/>
    <Route path="/home" element={<Home />}/>
    <Route path="/login" element={<Login />}/>
  </Routes>);
}

export default Router;
