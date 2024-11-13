// Login.js

import React, { useState } from 'react';
import axios from 'axios';

function Login({ setIsLoggedIn }) {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [message, setMessage] = useState('');

  const handleUserIdChange = (event) => {
    setUserId(event.target.value);
  };

  const handlePasswordChange = (event) => {
    setPassword(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    setMessage('');

    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/login`,
        {
          user_id: userId,
          password: password,
        },
        { withCredentials: true }
      );

      if (response.data.status === 'success') {
        setIsLoggedIn(true);
      } else {
        setMessage(response.data.message);
      }
    } catch (error) {
      console.error('Error during login:', error);
      setMessage('ログイン中にエラーが発生しました。');
    }
  };

  return (
    <div className="login-container">
      <h2>ログイン</h2>
      <form onSubmit={handleSubmit}>
        <div>
          <label>ユーザーID：</label>
          <input 
            type="text" 
            value={userId} 
            onChange={handleUserIdChange} 
            required 
          />
        </div>
        <div>
          <label>パスワード：</label>
          <input 
            type="password" 
            value={password} 
            onChange={handlePasswordChange} 
            required 
          />
        </div>
        <button type="submit">ログイン</button>
      </form>
      {message && <p className="error-message">{message}</p>}
    </div>
  );
}

export default Login;