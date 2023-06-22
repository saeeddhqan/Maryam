import { useState } from 'react';

function Settings() {
  const [fontSize, setFontSize] = useState(localStorage.getItem('fontSize') || 16);
  const [colorTheme, setColorTheme] = useState(localStorage.getItem('colorTheme') || 'light');

  function toggleSettings() {
    const settingsModal = document.getElementById('settingsModal');
    if (settingsModal.style.display === 'block') {
      settingsModal.style.display = 'none';
    } else {
      settingsModal.style.display = 'block';
    }
  }

  function saveSettings() {
    localStorage.setItem('fontSize', fontSize);
    localStorage.setItem('colorTheme', colorTheme);
    toggleSettings();
  }

  return (
    <div className="settings-container">
      <button className="settings-button" onClick={toggleSettings}>Settings</button>
      <div className="settings-modal" id="settingsModal">
        <h2>Settings</h2>
        <label htmlFor="font-size">Font Size:</label>
        <input type="range" id="font-size" name="font-size" min="10" max="30" step="1" value={fontSize} onChange={(e) => setFontSize(e.target.value)} />
        <br />
        <label htmlFor="color-theme">Color Theme:</label>
        <select id="color-theme" name="color-theme" value={colorTheme} onChange={(e) => setColorTheme(e.target.value)}>
          <option value="light">Light</option>
          <option value="dark">Dark</option>
        </select>
        <br />
        <button onClick={saveSettings}>Save</button>
      </div>
      <style>{`
        .settings-container {
          position: relative;
        }
        
        .settings-button {
          padding: 10px;
          background-color: #fff;
          border: 1px solid #ccc;
          border-radius: 5px;
          cursor: pointer;
        }
        
        .settings-modal {
          position: absolute;
          top: 50px;
          right: 0;
          background-color: #fff;
          border: 1px solid #ccc;
          padding: 20px;
          display: none;
        }
      `}</style>
    </div>
  );
}

export default Settings;
