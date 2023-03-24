import { useEffect, useState, createContext, useContext } from "react";
import "./App.css";
import { Homesearch } from "../Components/Homesearch";
import Resultspage from "../Components/resultsnsearch/resultspage";
import Themetoggle from "../Components/themetoggle";
export const ThemeContext = createContext("light");
function App() {
  const [showHome, setshowHome] = useState(true); //home screen with big owasp logo and search
  const [showRes, setshowRes] = useState(false); // screen with search results
  const [SearchResults, setResults] = useState([]); //setter for the search results
  const [Loading, setLoading] = useState(false); //loader
  const [Theme, setTheme] = useState("light"); //theme better

  useEffect(() => {
    console.log(showHome);
  }, [SearchResults]);

  return (
    <ThemeContext.Provider value={Theme}>
      <div className="App" id={Theme}>
        <Themetoggle theme={Theme} setTheme={setTheme} />
        <Homesearch
          setResults={setResults}
          show={showHome}
          setshowHome={setshowHome}
          setshowRes={setshowRes}
          setLoading={setLoading}
          Loading={Loading}
        />
        <Resultspage
          setResults={setResults}
          show={showRes}
          SearchResults={SearchResults}
          Loading={Loading}
          setLoading={setLoading}
          setshowHome={setshowHome}
          setshowRes={setshowRes}
        />
      </div>
    </ThemeContext.Provider>
  );
}

export default App;
