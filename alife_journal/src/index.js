// index.js

import React from 'react';
import ReactDOM from 'react-dom/client'; // '/client' を追加
import App from './App';

// ReactDOM.render(<App />, document.getElementById('root')); // 古い書き方

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
