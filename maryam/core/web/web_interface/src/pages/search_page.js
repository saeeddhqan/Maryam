import React, { useState, useEffect } from "react";
import "./search_page.css";
import { useStateValue } from "../state_provider";
import useWebApi from "./use_web_api";
import { Link } from "react-router-dom";
import Search from "./search";
import SkeletonSearchPage from "../skeletons/skeleton_search_page";
import logo_white from "./image/logo_white.png";


function SearchPage() {
  const [{ term }] = useStateValue();
  const { data, isLoading } = useWebApi(term);
  const [selectedOption, setSelectedOption] = useState("All");
  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      if (window.pageYOffset > 0) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };
    window.addEventListener("scroll", handleScroll);
    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);


  return (
    <div className={`searchPage ${scrolled ? "scrolled" : ""}`}>
      <div className="searchPage_header">
        <Link to="/" style={{ textDecoration: "none" }}>
          <div className={`title `}>
            <img src={logo_white} alt="Logo" />
          </div>
        </Link>
        <div className="searchPage_headerBody">
          <div className={`searchBox`}>
            <Search/>
          </div>
        </div>
        <div className={`searchPage_optionLeft`}>
          <div
            className={`searchPage_option ${selectedOption === "All" ? "selected" : ""}`}
            onClick={() => handleOptionSelect("All")}
          >
            <Link to="/search">Web</Link>
          </div>
          <div
            className={`searchPage_option ${selectedOption === "Image" ? "selected" : ""}`}
            onClick={() => handleOptionSelect("Image")}
          >
            <Link to="/search">Image</Link>
          </div>
        </div>
      </div>
      {term && (
        <div className="searchPage_results">
          {data &&
            !isLoading &&
            data.output.results.map((item) => (
              <div className="searchPage_result" key={item.id}>
                <a className="searchPage_resultLink" href={item.a} target="_blank" rel="noreferrer">
                  {item.c}
                </a>
                <a className="searchPage_resultTitle" href={item.a} target="_blank" rel="noreferrer">
                  <h2>{item.t}</h2>
                </a>
                <p className="searchPage_resultSnippet">{item.d}</p>
              </div>
            ))}
          {isLoading && [...Array(15)].map((_, index) => <SkeletonSearchPage key={index} theme="dark" />)}
        </div>
      )}

      <div className="footer">
        <div className="licensed">GPLv3 Licensed</div>
        <div> Maryam Project</div>
      </div>
        <div className="madewith">Made with ❤️ + ☕</div>
    </div>
  );
}

export default SearchPage;
