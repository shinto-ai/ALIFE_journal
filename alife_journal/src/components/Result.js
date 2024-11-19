// Result.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';

function Result() {
  const [resultData, setResultData] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    axios
      .get(`${process.env.REACT_APP_BACKEND_URL}/result`, { withCredentials: true })
      .then((response) => {
        setResultData(response.data);
        setIsLoading(false);
      })
      .catch((error) => {
        console.error('結果データの取得中にエラーが発生しました:', error);
        setIsLoading(false);
      });
  }, []);

  if (isLoading) {
    return (
      <div className="container result-container">
        <h2>結果</h2>
        <p className="loading">結果を読み込んでいます...</p>
      </div>
    );
  }

  if (!resultData || resultData.status !== 'success') {
    return (
      <div className="container result-container">
        <h2>エラー</h2>
        <p className="error-message">結果を取得できませんでした。</p>
      </div>
    );
  }

  return (
    <div className="container result-container">
      <h2>実験終了</h2>
      <div className="content-section">
        <p className="result-message">{resultData.message}</p>
        <p className="instruction">次のコードを Cloud Works で入力してください。</p>
      <h2>112233</h2> 
        <p className="instruction">入力完了後,ブラウザを閉じてください。</p>
        <p className="contact-info">
          実験に関してご意見がございましたら、shinto.ryoma@gmail.com までご連絡お願いします。
        </p>
      </div>
    </div>
  );
}

export default Result;