import React, { useEffect, useState } from "react";
import "./search_page.css";
import { useStateValue } from "../state_provider";
import useWebApi from "./use_web_api";
import { Link } from "react-router-dom";
import Search from "./search";
import { Tooltip } from "@mui/material";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import AppsOutlinedIcon from "@mui/icons-material/AppsOutlined";
import SkeletonSearchPage from "../skeletons/skeleton_search_page";
import logo_white from "./image/logo_white.png";
import SearchIcon from "@mui/icons-material/Search";
import InsertPhotoOutlinedIcon from "@mui/icons-material/InsertPhotoOutlined";

function SearchPage() {
  const [{ term }] = useStateValue();
  const { data, isLoading } = useWebApi(term);
  const [isScrolled, setIsScrolled] = useState(false);
  const [selectedOption, setSelectedOption] = useState("All");

  useEffect(() => {
    function handleScroll() {
      setIsScrolled(window.scrollY > 0);
    }

    window.addEventListener("scroll", handleScroll);

    return () => {
      window.removeEventListener("scroll", handleScroll);
    };
  }, []);

  const handleOptionSelect = (option) => {
    setSelectedOption(option);
  };

  return (
    <div className={`searchPage ${isScrolled ? "scrolled" : ""}`}>
      <div className={`searchPage_header ${isScrolled ? "scrolled" : ""}`}>
        <Link to="/" style={{ textDecoration: "none" }}>
          <div className={`title ${isScrolled ? "scrolled" : ""}`}>
            <img src={logo_white} alt="Logo" />
          </div>
        </Link>
        <div className="searchPage_headerBody">
          <div className={`searchBox ${isScrolled ? "scrolled" : ""}`}>
            <Search hideShortCut />
          </div>
          <div className={`searchPage_optionRight ${isScrolled ? "scrolled" : ""}`}>
            <div className="searchPage_optionRightSetting">
              <Link to="#">
                <Tooltip title="Setting">
                  <SettingsOutlinedIcon style={{ color: "white" }} fontSize="large" />
                </Tooltip>
              </Link>
            </div>
            <div className="searchPage_optionRightApps">
              <Link to="#">
                <Tooltip title="Apps">
                  <AppsOutlinedIcon style={{ color: "white" }} fontSize="large" />
                </Tooltip>
              </Link>
            </div>
          </div>
        </div>
        <div className={`searchPage_optionLeft ${isScrolled ? "hidden" : ""}`}>
          <div
            className={`searchPage_option ${selectedOption === "All" ? "selected" : ""}`}
            onClick={() => handleOptionSelect("All")}
          >
            <SearchIcon />
            <Link to="/search">All</Link>
          </div>
          <div
            className={`searchPage_option ${selectedOption === "Image" ? "selected" : ""}`}
            onClick={() => handleOptionSelect("Image")}
          >
            <InsertPhotoOutlinedIcon />
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
        <div className="footerServices">Services</div>
        <div className="footerAbout">About Webpage</div>
      </div>
    </div>
  );
}

export default SearchPage;
