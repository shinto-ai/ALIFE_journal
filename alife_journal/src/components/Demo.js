// Demo.js

import React, { useState } from 'react';
import { useHistory } from 'react-router-dom';
import demoImage1 from '../assets/demo_image1.png';
import demoImage2 from '../assets/demo_image2.png';
import demoImage3 from '../assets/demo_image3.png';
import demoImage4 from '../assets/demo_image4.png';
import demoImage5 from '../assets/demo_image5.png';
import demoImage6 from '../assets/demo_image6.png';
import demoImage7 from '../assets/demo_image7.png';
import demoImage8 from '../assets/demo_image8.png';
import demoImage9 from '../assets/demo_image9.png';
import demoImage10 from '../assets/demo_image10.png';

function Demo() {
  const history = useHistory();
  const [step, setStep] = useState(0);

  const images = [
    [demoImage1, demoImage2],
    [demoImage3, demoImage4],
    [demoImage5, demoImage6],
    [demoImage7, demoImage8],
    [demoImage9, demoImage10],
  ];

  const prompt = 'どちらが「kiki」ですか？';

  const handleImageClick = () => {
    if (step < images.length - 1) {
      setStep(step + 1);
    } else {
      history.push('/prepare'); // 遷移先を '/prepare' に変更
    }
  };

  return (
    <div className="container">
      <h2>デモ</h2>
      <p className="prompt">{prompt}</p>
      <div className="image-container">
        <img
          src={images[step][0]}
          alt="Option 1"
          onClick={handleImageClick}
        />
        <img
          src={images[step][1]}
          alt="Option 2"
          onClick={handleImageClick}
        />
      </div>
    </div>
  );
}

export default Demo;
