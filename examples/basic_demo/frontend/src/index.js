/**
 * index.js
 *
 * Entry point of the React application.
 * Renders the <App /> component into the DOM.
 *
 * Description:
 * - Follows recommended React 18 best practices
 *   by using StrictMode and createRoot.
 */

import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App';
import './index.css';

// Identify the root DOM node
const rootElement = document.getElementById('root');

// Create a React root
const root = createRoot(rootElement);

// Render the App component within StrictMode
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);