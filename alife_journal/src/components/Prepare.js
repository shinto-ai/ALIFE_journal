// Prepare.js

import React from 'react';
import { useHistory } from 'react-router-dom';

function Prepare() {
  const history = useHistory();

  const handleStart = () => {
    history.push('/experiment');
  };

  return (
    <div className="prepare-container">
      <div className="content-box">
        <h2>実験の注意事項</h2>
        <div className="content-section">
          <p>
            デモは以上になります。デモと本番では文章や画像が異なりますのでご注意ください。
          </p>
          <p>
            実験中は、ブラウザの「戻る」ボタンや「更新」ボタンを押さないでください。
            ログイン画面に戻る可能性があります。
          </p>
          <p>
            もし、ログイン画面に戻ってしまった場合は、再度ログインして実験を再開してください。
          </p>
        </div>

        <div className="content-section">
          <h2>実験の開始</h2>
          <p>
            それでは、これから実験を行います。所要時間の目安は30分～1時間程度です。
            準備が完了したら以下の実験開始ボタンを押して始めてください。
          </p>
          <p>
            なお、実験の参加辞退や不明点等があればお手数ですが shinto.ryoma@gmail.com までご連絡お願いします。
          </p>
        </div>

        <div className="button-container">
          <button onClick={handleStart} className="start-button">
            実験開始
          </button>
        </div>
      </div>
    </div>
  );
}

export default Prepare;