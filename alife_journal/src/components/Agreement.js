// Agreement.js

import React from 'react';
import { useHistory } from 'react-router-dom';

function Agreement() {
  const history = useHistory();

  const handleAgree = () => {
    history.push('/instructions');
  };

  return (
    <div className="agreement-container">
      <h2>実験同意書</h2>
      <p>
        この度は，ご協力いただきありがとうございます．
        以下の説明を全て読み，ご理解いただいたうえで本実験への参加に同意する方は，次のページに進んでください．
      </p>
      <h3>実験について：</h3>
      <p>
        本実験では、特定の単語を含む文章と2枚の画像が繰り返し表示されます。
        「より単語の印象を表現する画像」を選択し続けることで、言語と画像の対応関係を明らかにします．
      </p>
      <p>
        この調査に参加することは自由意思によるものです．
        本実験は何ら健康を害するものではありませんが，もし体調や気分が悪くなった場合には，いつでも調査を中止してください．
      </p>
      <p>
        調査では，参加者の選択した画像が記録されます．
        調査への同意と説明・実験デモに約10分，画像選択調査に50分程度かかり、1回の調査は合計1時間ほどです．
      </p>
      <p>
        調査により得られた画像から個人が特定されることはありません．学会，論文，書籍等で発表されますが，いかなる場合においても，個人が特定できる形で公表されることはありません．
      </p>
      <p>
        調査の対価として謝金をお支払いいたします．最終コードを入力すると、クラウドワークスから支払われます。
      </p>
      <h3>倫理審査の承認</h3>
      <p>
        本研究は，○○センターの倫理審査委員会の承認を得ています（承認番号　R6-21）．
      </p>
      <h3>★実験に関するお問い合わせ先</h3>
      <p>
        北海道大学，人間知・脳・AI研究教育センター，実験責任者：飯塚　博幸
        〒060-0812　北海道札幌市北区北12条西7丁目
        北海道大学中央キャンパス総合研究棟2号館3階
        電話番号: 011-706-3803／電子メール: iizuka@chain.hokudai.ac.jp
      </p>
      <button onClick={handleAgree}>同意して次へ進む</button>
    </div>
  );
}

export default Agreement;