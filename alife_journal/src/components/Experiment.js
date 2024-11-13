// Experiment.js

import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

function Experiment() {
  const history = useHistory();
  const [candidate1, setCandidate1] = useState(null);
  const [candidate2, setCandidate2] = useState(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState('');

  // プロンプトをフロントエンドで定義
  const promptText = `
    画像内の図形に注目し、左側の画像と右側の画像のどちらかに「ぬもる(numolu)」という名前を付けるならばどちらに名付けますか？
    「ぬもる(numolu)」と名付ける方をクリックしてください。
  `;

  useEffect(() => {
    startExperiment();
  }, []);

  const startExperiment = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/experiment/start`,
        {},
        { withCredentials: true }
      );
      const data = response.data;
      setCandidate1(data.candidate1);
      setCandidate2(data.candidate2);
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error('Error starting experiment:', error);
      setMessage('実験の開始中にエラーが発生しました。');
    }
  };

  const chooseCandidate = async (selectedCandidateId) => {
    setLoading(true);
    try {
      const response = await axios.post(
        `${process.env.REACT_APP_BACKEND_URL}/experiment/choose`,
        { selected_candidate_id: selectedCandidateId },
        { withCredentials: true }
      );
      const data = response.data;

      if (data.status === 'experiment_finished') {
        setLoading(false);
        history.push('/result');
      } else {
        setCandidate1(data.candidate1);
        setCandidate2(data.candidate2);
        setLoading(false);
      }
    } catch (error) {
      setLoading(false);
      console.error('Error choosing candidate:', error);
      setMessage('選択の送信中にエラーが発生しました。');
    }
  };

  return (
    <div className="container experiment-container">
      <h2>実験</h2>
      <p className="prompt">{promptText}</p>
      {loading || !candidate1 || !candidate2 ? (
        <div className="loading">読み込み中...</div>
      ) : (
        <div className="image-container">
          <div className="image-wrapper">
            <img
              src={`data:image/png;base64,${candidate1.image_base64}`}
              alt="Candidate 1"
              onClick={() => chooseCandidate(candidate1.id)}
              className="experiment-image"
            />
          </div>
          <div className="image-wrapper">
            <img
              src={`data:image/png;base64,${candidate2.image_base64}`}
              alt="Candidate 2"
              onClick={() => chooseCandidate(candidate2.id)}
              className="experiment-image"
            />
          </div>
        </div>
      )}
      {message && <p className="error-message">{message}</p>}
    </div>
  );
}

export default Experiment;