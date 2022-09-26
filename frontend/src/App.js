import logo from './logo.svg';
import './App.css';
import React, { useEffect, useState } from 'react';
import axios from 'axios'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'

import Login from './components/Login'
import Question from './components/Question'
import Header from './components/Header'
import useToken from './components/useToken'
import Register from "./components/Register";
import MyNavbar from "./components/Navbar"
import Home from './components/Home';

function App() {
  const { token, removeToken, setToken } = useToken();

  return (
    <Router>
      <div>
        <MyNavbar />
        <Routes>
          <Route exact path='/' element={<Home />} />
          <Route exact path='/home' element={<Home />} />
          <Route exact path='/register' element={<Register />} />
          <Route exact path='/login' element={<Login setToken={setToken} />} />
          <Route exact path='/question' element={<Question token={token} />} />
        </Routes>
      </div>
    </Router>
  );
}
export default App;