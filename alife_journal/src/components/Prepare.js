// Prepare.js

import React from 'react';
import { useHistory } from 'react-router-dom';

function Prepare() {
  const history = useHistory();

  const handleStart = () => {
    history.push('/experiment');
  };

  return (
    <div className="container">
      <h2>実験の準備</h2>
      <p>
        それでは、これから実験を行います。所要時間は30分～1時間程度です。準備が完了したら以下の開始ボタンを押して始めてください。なお、不明点があれば、○○までご連絡お願いします。
      </p>
      <button onClick={handleStart}>開始</button>
    </div>
  );
}

export default Prepare;
