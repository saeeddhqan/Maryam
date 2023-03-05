import { useEffect } from "react";
import { useState } from "react";
import "./App.css";
import { Homesearch } from "../Components/Homesearch";
import Resultspage from "../Components/resultsnsearch/resultspage";

function App() {
  const [showHome, setshowHome] = useState(true); //home screen with big owasp logo and search
  const [showRes, setshowRes] = useState(false); // screen with search results
  const [SearchResults, setResults] = useState([]);
  const [Loading, setLoading] = useState(false);
  useEffect(() => {
    console.log(showHome);
  }, [SearchResults]);

  return (
    <div className="App">
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
      />
    </div>
  );
}

export default App;
