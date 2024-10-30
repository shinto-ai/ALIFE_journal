// Login.js

import React, { useState } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

function Login({ setIsLoggedIn }) {
  const [userId, setUserId] = useState('');
  const [password, setPassword] = useState('');
  const [errorMessage, setErrorMessage] = useState('');
  const history = useHistory();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMessage('');

    try {
      const response = await axios.post(
        'http://localhost:5000/login',
        {
          user_id: userId,
          password: password,
        },
        { withCredentials: true }
      );

      if (response.data.status === 'success') {
        console.log('Login successful, redirecting...');
        setIsLoggedIn(true);
        history.push('/instructions');
      } else {
        setErrorMessage(response.data.message || 'ログインに失敗しました。');
      }
    } catch (error) {
      console.error('Error during login:', error);
      setErrorMessage('サーバーに接続できません。しばらくしてから再度お試しください。');
    }
  };

  return (
    <div className="container">
      <h2>ログイン</h2>
      {errorMessage && <p className="error-message">{errorMessage}</p>}
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="ユーザーID"
          value={userId}
          onChange={(e) => setUserId(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="パスワード"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">ログイン</button>
      </form>
    </div>
  );
}

export default Login;
