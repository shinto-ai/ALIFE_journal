// Result.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Result() {
  const [resultData, setResultData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [feedback, setFeedback] = useState('');

  // 結果データの取得
  useEffect(() => {
    axios
      .get('http://localhost:5000/result', { withCredentials: true })
      .then((response) => {
        setResultData(response.data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('結果データの取得中にエラーが発生しました:', error);
        setIsLoading(false);
      });
  }, []);

  // フィードバックの送信
  const handleSubmit = (e) => {
    e.preventDefault();
    axios
      .post(
        'http://localhost:5000/submit_feedback',
        { feedback },
        { withCredentials: true }
      )
      .then((response) => {
        alert('フィードバックを送信しました。ご協力ありがとうございます。');
        setFeedback('');
      })
      .catch((error) => {
        console.error('フィードバックの送信中にエラーが発生しました:', error);
      });
  };

  if (isLoading) {
    return (
      <div className="container">
        <h2>結果</h2>
        <p className="loading">結果を読み込んでいます...</p>
      </div>
    );
  }

  return (
    <div className="container result-container">
      <h2>実験終了</h2>
      <p>ご協力ありがとうございました。</p>
      {resultData && (
        <>
          <p>{resultData.message}</p>
          {/* 必要に応じて結果データを表示 */}
        </>
      )}
      <form onSubmit={handleSubmit}>
        <label htmlFor="feedback">ご感想やご意見があればご記入ください：</label>
        <textarea
          id="feedback"
          value={feedback}
          onChange={(e) => setFeedback(e.target.value)}
          rows="5"
          style={{ width: '100%', marginTop: '10px' }}
        ></textarea>
        <button type="submit">送信</button>
      </form>
    </div>
  );
}

export default Result;
