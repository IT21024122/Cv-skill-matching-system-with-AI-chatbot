import logo from './logo.svg';
import './index.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import ProfilePage from './components/profile';
import LoginPage from './components/login';
import Register from './components/register';
import MainPage from './components/main_page';

function App() {
  return (
    <Router>
    <div>
      <Routes>
        <Route path="/" element={<Register />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<Register />} />
        <Route path='/mainpage/:username' element={<MainPage />} />
      </Routes>
    </div>
  </Router>
  );
}

export default App;
