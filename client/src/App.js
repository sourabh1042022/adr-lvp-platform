import React, { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [rules, setRules] = useState([]);
  const [selectedRule, setSelectedRule] = useState({ filename: null, content: '' });
  const [error, setError] = useState(null);

  useEffect(() => {
    fetch('/api/rules')
      .then(response => response.json())
      .then(data => setRules(data.rules))
      .catch(error => {
        console.error("Fetch Error:", error);
        setError("Failed to load rules. Is the backend server running?");
      });
  }, []);

  // NEW: Function to handle clicking on a rule
  const handleRuleClick = (filename) => {
    fetch(`/api/rules/${filename}`)
      .then(response => response.text()) // Get the raw text content
      .then(content => {
        setSelectedRule({ filename, content });
      })
      .catch(error => console.error("Error fetching rule content:", error));
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>ADR-LVP Rule Dashboard</h1>
        <div className="main-content">
          <div className="rule-list">
            <h2>Available Rules</h2>
            {error ? (
              <p className="error-message">{error}</p>
            ) : (
              <ul>
                {rules.map(rule => (
                  <li key={rule} onClick={() => handleRuleClick(rule)}>
                    {rule}
                  </li>
                ))}
              </ul>
            )}
          </div>
          <div className="rule-editor">
            <h2>Rule Content</h2>
            <textarea
              readOnly
              value={selectedRule.content}
              placeholder="Click on a rule to view its content..."
            />
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
