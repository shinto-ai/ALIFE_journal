import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Experiment() {
  const [candidate1, setCandidate1] = useState(null);
  const [candidate2, setCandidate2] = useState(null);
  const [prompt, setPrompt] = useState('');
  const [loading, setLoading] = useState(false);
  const [experimentFinished, setExperimentFinished] = useState(false);
  const [message, setMessage] = useState('');
  const [generation, setGeneration] = useState(0);

  useEffect(() => {
    startExperiment();
  }, []);

  const startExperiment = async () => {
    setLoading(true);
    try {
      const response = await axios.post(
        'http://localhost:5000/experiment/start',
        {},
        { withCredentials: true }
      );
      const data = response.data;
      setCandidate1(data.candidate1);
      setCandidate2(data.candidate2);
      setPrompt(data.prompt);
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
        'http://localhost:5000/experiment/choose',
        { selected_candidate_id: selectedCandidateId },
        { withCredentials: true }
      );
      const data = response.data;

      if (data.status === 'experiment_finished') {
        setExperimentFinished(true);
        setMessage(data.message);
      } else {
        setCandidate1(data.candidate1);
        setCandidate2(data.candidate2);
        setPrompt(data.prompt);
        setGeneration((prevGen) => prevGen + 1);
      }
      setLoading(false);
    } catch (error) {
      setLoading(false);
      console.error('Error choosing candidate:', error);
      setMessage('選択の送信中にエラーが発生しました。');
    }
  };

  if (experimentFinished) {
    return (
      <div>
        <h2>実験終了</h2>
        <p>{message}</p>
      </div>
    );
  }

  if (loading || !candidate1 || !candidate2) {
    return <div>読み込み中...</div>;
  }

  return (
    <div>
      <h2>実験</h2>
      <p>試行回数: {generation}</p>
      <p>{prompt}</p>
      <div style={{ display: 'flex', justifyContent: 'center' }}>
        <div onClick={() => chooseCandidate(candidate1.id)} style={{ margin: '0 20px' }}>
          <img
            src={`data:image/png;base64,${candidate1.image_base64}`}
            alt="Candidate 1"
            width="300"
            height="300"
          />
        </div>
        <div onClick={() => chooseCandidate(candidate2.id)} style={{ margin: '0 20px' }}>
          <img
            src={`data:image/png;base64,${candidate2.image_base64}`}
            alt="Candidate 2"
            width="300"
            height="300"
          />
        </div>
      </div>
      {message && <p>{message}</p>}
    </div>
  );
}

export default Experiment;
