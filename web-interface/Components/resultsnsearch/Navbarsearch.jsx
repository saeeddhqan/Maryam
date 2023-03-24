import axios from "axios";
export default function NavbarSearch({
  setResults,
  setLowerLimit,
  setUpperLimit,
  setCurrentPage,
  setLoading,
  setshowHome,
  setshowRes,
}) {
  return (
    <div className="Navbarsearch-parent">
      <div className="small-logo">
        <img
          onClick={() => {
            console.log("clicked");
            setshowHome(true);
            setshowRes(false);
          }}
          src="/owasp.png"
        ></img>
      </div>
      <div className="Navbarsearch">
        <form
          autoComplete="off"
          className="form-small"
          onSubmit={async function handleSubmit(e) {
            e.preventDefault();

            try {
              setLoading(true);
              const res = await axios.get(
                `http://localhost:1313/api/modules?_module=iris&query=${e.target[0].value}`
              );
              console.log(res);
              const SearchResults = res.data.output.results;
              setResults(SearchResults);
              setCurrentPage(0);
              setLowerLimit(0);
              setUpperLimit(10);
              setLoading(false);
            } catch (err) {
              console.log(err);
            }
          }}
          input
        >
          <input
            type="text"
            name="search"
            placeholder="iris search &#128373;&#65039;"
          />
          <button className="nav-button">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              viewBox="0 0 30 30"
              width="30px"
              height="30px"
            >
              <path d="M 13 3 C 7.4889971 3 3 7.4889971 3 13 C 3 18.511003 7.4889971 23 13 23 C 15.396508 23 17.597385 22.148986 19.322266 20.736328 L 25.292969 26.707031 A 1.0001 1.0001 0 1 0 26.707031 25.292969 L 20.736328 19.322266 C 22.148986 17.597385 23 15.396508 23 13 C 23 7.4889971 18.511003 3 13 3 z M 13 5 C 17.430123 5 21 8.5698774 21 13 C 21 17.430123 17.430123 21 13 21 C 8.5698774 21 5 17.430123 5 13 C 5 8.5698774 8.5698774 5 13 5 z" />
            </svg>
          </button>
        </form>
      </div>
    </div> // closing navbar search parent
  );
}
