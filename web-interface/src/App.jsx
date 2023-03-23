import { useEffect, useState, createContext, useContext } from "react";
import "./App.css";
import { Homesearch } from "../Components/Homesearch";
import Resultspage from "../Components/resultsnsearch/resultspage";

 export const themeContext = createContext(null);


function App() {
  const [showHome, setshowHome] = useState(true); //home screen with big owasp logo and search
  const [showRes, setshowRes] = useState(false); // screen with search results
  const [SearchResults, setResults] = useState([]); //setter for the search results
  const [Loading, setLoading] = useState(false); //loader
  const [Theme,setTheme] = useState("dark");//theme better
  const toggleTheme = () => {
    setTheme((curr)=>(curr === "light" ? "dark" : "light"))
  }
  useEffect(() => {
    console.log(showHome);
  }, [SearchResults]);

  return (
      <themeContext.Provider value={Theme}>
    <div className="App" id={Theme} >
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
    </themeContext.Provider>
  );
}

export default App;
