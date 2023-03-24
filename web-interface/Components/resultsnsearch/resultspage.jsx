import { useState } from "react";
import NavbarSearch from "./Navbarsearch";
import Results from "./results";
import BottomElement from "./pageElements";
import Loader from "../loader";

export default function Resultspage({
  setResults,
  show,
  SearchResults,
  Loading,
  setLoading,
  setshowHome,
  setshowRes,
}) {
  //calculting number of pages
  const totalitems = SearchResults.length;
  console.log("Total items=", totalitems);
  const totalPages = Math.ceil(totalitems / 10);
  //settings limits
  const [UpperLimit, setUpperLimit] = useState(10);
  const [LowerLimit, setLowerLimit] = useState(0);
  const [Currentpage, setCurrentPage] = useState(0);

  console.log("Total pages=", totalPages);

  if (show == true) {
    return (
      <div className="result-page">
        <Loader Loading={Loading} />
        <NavbarSearch
          setResults={setResults}
          setLowerLimit={setLowerLimit}
          setUpperLimit={setUpperLimit}
          setCurrentPage={setCurrentPage}
          Loading={Loading}
          setLoading={setLoading}
          setshowHome={setshowHome}
          setshowRes={setshowRes}
        />
        <div className="result-container">
          <Results
            data={SearchResults}
            LowerLimit={LowerLimit}
            UpperLimit={UpperLimit}
          />
          <BottomElement
            setLowerLimit={setLowerLimit}
            setUpperLimit={setUpperLimit}
            setCurrentPage={setCurrentPage}
            totalPages={totalPages}
            LowerLimit={LowerLimit}
            UpperLimit={UpperLimit}
            Currentpage={Currentpage}
            totalitems={totalitems}
          />
        </div>
      </div>
    );
  } else {
    return "";
  }
}
