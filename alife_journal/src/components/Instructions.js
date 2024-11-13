// Instructions.js

import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

function Instructions() {
  const [instructions, setInstructions] = useState('');
  const history = useHistory();

  useEffect(() => {
    const fetchInstructions = async () => {
      try {
        const response = await axios.get(`${process.env.REACT_APP_BACKEND_URL}/instructions`, { withCredentials: true });
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
    <div className="instructions-container">
      <h2>実験概要</h2>
      <p>{instructions}</p>
      <p>
        本実験は、言語と画像の対応関係を明らかにするためのものです。
        2枚の画像と特定の単語を含む文章が繰り返し表示されます。
      </p>
      <p>
        表示される2枚の画像のうち、より単語の印象を表現すると思う画像を1つ選択してください。
        悩まず、直感的に選択してください。(目安: 1~2秒以内)
      </p>
      <p>
        実験を進める中で、似た画像や同じ画像が表示されたり、図形の無い単色画像が表示されることがありますが、
        直感に従ってどちらか一方を選択し続けてください。
        総選択回数は約1000回です。
      </p>
      <h3>デモ</h3>
      <p>
        次のページでデモを行います。
        表示される文章を読み、その文章に対応する画像を5回選択してください。
      </p>
      <p>
        なお、実験を通して文章は変化しないので、選択時に毎回読む必要はありません。
        ただし、デモの文章と実験の文章は異なりますので、注意してください。
      </p>
      <button onClick={handleNext}>デモへ進む</button>
    </div>
  );
}

export default Instructions;