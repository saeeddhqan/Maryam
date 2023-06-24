import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import { useStateValue } from "../state_provider";
import useWebApi from "./use_web_api";
import Search from "./search";
import SkeletonSearchPage from "../skeletons/skeleton_search_page";
import logo_white from "./image/logo.png";
import "./search_page.css";

function SearchPage() {
  const [{ term }] = useStateValue();
  const { data, isLoading } = useWebApi(term);
  const [selectedOption, setSelectedOption] = useState("All");

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };


  return (
    <div className="searchPage">
      <div className="searchPage_header">
        <Link to="/" style={{ textDecoration: "none" }}>
          <div className="title">
            <img src={logo_white} alt="Logo" />
          </div>
        </Link>
        <div className="searchPage_headerBody">
          <div className="searchBox">
            <Search />
          </div>
        </div>
        <div className="searchPage_optionLeft">
          <Link to="/search" className={`searchPage_option_all ${selectedOption === "All" ? "selected" : ""}`} onClick={() => handleOptionSelect("All")}>
            Web
          </Link>
          <Link to="/search" className={`searchPage_option_image ${selectedOption === "Image" ? "selected" : ""}`} onClick={() => handleOptionSelect("Image")}>
            Images
          </Link>
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
          {isLoading &&
            [...Array(15)].map((_, index) => <SkeletonSearchPage key={index} theme="dark" />)}
        </div>
      )}

      <div className="footer">
        <div className="licensed">GPLv3 Licensed</div>
        <div>Maryam Project</div>
      </div>
      <div className="madewith">Made with <span className="heart">❤️</span>  + ☕</div>
    </div>
  );
}

export default SearchPage;
