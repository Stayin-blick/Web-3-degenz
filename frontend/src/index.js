import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import { BrowserRouter as Router } from 'react-router-dom';
import { CurrentUserProvider } from './contexts/CurrentUserContext';
import { ProfileDataProvider } from "./contexts/ProfileDataContext";
import { CommunityDataProvider } from './contexts/CommunityDataContext';

ReactDOM.render(
    <Router>
      <CurrentUserProvider>
        <ProfileDataProvider>
          <CommunityDataProvider>
            <App />
          </CommunityDataProvider>
        </ProfileDataProvider>
      </CurrentUserProvider>
    </Router>,
  document.getElementById('root')
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
