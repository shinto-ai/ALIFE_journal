// Experiment.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

function Experiment() {
  const [images, setImages] = useState([]);
  const [prompt, setPrompt] = useState('');
  const [generation, setGeneration] = useState(1);
  const [isLoading, setIsLoading] = useState(true);
  const history = useHistory();

  const fetchExperimentData = () => {
    axios
      .get('http://localhost:5000/experiment', { withCredentials: true })
      .then((response) => {
        console.log('Experiment data:', response.data); // デバッグ用ログ
        if (response.data.images && response.data.images.length > 0) {
          setImages(response.data.images);
          setPrompt(response.data.prompt || '質問が取得できませんでした。');
          setGeneration(response.data.generation || 1);
          setIsLoading(false);
        } else {
          console.error('画像が取得できませんでした。');
          setIsLoading(false);
        }
      })
      .catch((error) => {
        console.error('データの取得中にエラーが発生しました:', error);
        if (error.response && error.response.status === 401) {
          // 未認証の場合、ログインページにリダイレクト
          history.push('/login');
        } else {
          setIsLoading(false);
        }
      });
  };

  // 初期データの取得
  useEffect(() => {
    fetchExperimentData();
  }, []);

  // 画像クリック時の処理
  const handleImageClick = (choice) => {
    setIsLoading(true);
    axios
      .post(
        'http://localhost:5000/submit_choice',
        { choice },
        { withCredentials: true }
      )
      .then((response) => {
        console.log('Server response:', response.data);  // デバッグ用ログ
        if (response.data.finished) {
          // 実験終了時
          history.push('/result');
        } else if (response.data.new_generation) {
          // 新しい世代の開始時にデータを再取得
          fetchExperimentData();
        } else if (response.data.images && response.data.images.length > 0) {
          // 次の画像ペアをセット
          setImages(response.data.images);
          setPrompt(response.data.prompt || '質問が取得できませんでした。');
          setGeneration(response.data.generation || generation);
          setIsLoading(false);
        } else {
          console.error('次の画像が取得できませんでした。');
          setIsLoading(false);
        }
      })
      .catch((error) => {
        console.error('選択の送信中にエラーが発生しました:', error);
        setIsLoading(false);
      });
  };

  if (isLoading) {
    return (
      <div className="container">
        <h2>実験</h2>
        <p className="loading">データを読み込んでいます...</p>
      </div>
    );
  }

  if (images.length === 0) {
    return (
      <div className="container">
        <h2>実験</h2>
        <p>現在表示できる画像がありません。</p>
      </div>
    );
  }

  return (
    <div className="container experiment-container">
      <h2>実験</h2>
      <p className="prompt">{prompt}</p>
      <div className="image-container">
        <img
          src={`data:image/png;base64,${images[0]}`}
          alt="選択肢 1"
          className="image-choice"
          onClick={() => handleImageClick(1)}
        />
        <img
          src={`data:image/png;base64,${images[1]}`}
          alt="選択肢 2"
          className="image-choice"
          onClick={() => handleImageClick(2)}
        />
      </div>
      <p>現在の世代: {generation}</p>
    </div>
  );
}

export default Experiment;
