// App.js

import React, { useState } from 'react';
import { BrowserRouter as Router, Switch, Route, Redirect } from 'react-router-dom';
import Login from './components/Login';
import Instructions from './components/Instructions';
import Demo from './components/Demo';
import Prepare from './components/Prepare';
import Experiment from './components/Experiment';
import Result from './components/Result';

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  return (
    <Router>
      <div className="container">
        <Switch>
          <Route exact path="/">
            {isLoggedIn ? <Redirect to="/instructions" /> : <Login setIsLoggedIn={setIsLoggedIn} />}
          </Route>
          <Route path="/instructions">
            {isLoggedIn ? <Instructions /> : <Redirect to="/" />}
          </Route>
          <Route path="/demo">
            {isLoggedIn ? <Demo /> : <Redirect to="/" />}
          </Route>
          <Route path="/prepare">
            {isLoggedIn ? <Prepare /> : <Redirect to="/" />}
          </Route>
          <Route path="/experiment">
            {isLoggedIn ? <Experiment /> : <Redirect to="/" />}
          </Route>
          <Route path="/result">
            {isLoggedIn ? <Result /> : <Redirect to="/" />}
          </Route>
        </Switch>
      </div>
    </Router>
  );
}

export default App;