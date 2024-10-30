import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

function Instructions() {
  const [instructions, setInstructions] = useState('');
  const history = useHistory();

  useEffect(() => {
    const fetchInstructions = async () => {
      try {
        const response = await axios.get('http://localhost:5000/instructions', { withCredentials: true });
        setInstructions(response.data.instructions);
      } catch (error) {
        console.error('Error fetching instructions:', error);
        // 必要に応じてエラーメッセージを表示
      }
    };
    fetchInstructions();
  }, []);

  const handleNext = () => {
    history.push('/demo');
  };

  return (
    <div>
      <h2>注意事項</h2>
      <p>{instructions}</p>
      <button onClick={handleNext}>次へ</button>
    </div>
  );
}

export default Instructions;
