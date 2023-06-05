import React, { useEffect, useState } from "react";
import "./Image.css";
import { useStateValue } from "../StateProvider";
import useWebApi from "./useWebApi";
import { Link } from "react-router-dom";
import Search from "./Search";
import { Tooltip } from "@mui/material";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import AppsOutlinedIcon from "@mui/icons-material/AppsOutlined";
import SkeletonSearchPage from "../skeletons/SkeletonSearchPage";
import logo_white from "./image/logo_white.png";

function Image() {
    const [{ term }, dispatch] = useStateValue();
    const { data, isLoading } = useWebApi(term);
    const [isScrolled, setIsScrolled] = useState(false);

    useEffect(() => {
        function handleScroll() {
            setIsScrolled(window.scrollY > 0);
        }

        window.addEventListener("scroll", handleScroll);

        return () => {
            window.removeEventListener("scroll", handleScroll);
        };
    }, []);

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
                            <Link to="/setting">
                                <Tooltip title="Setting">
                                    <SettingsOutlinedIcon style={{ color: "white" }} fontSize="large" />
                                </Tooltip>
                            </Link>
                        </div>
                        <div className="searchPage_optionRightApps">
                            <Link to="/apps">
                                <Tooltip title="Apps">
                                    <AppsOutlinedIcon style={{ color: "white" }} fontSize="large" />
                                </Tooltip>
                            </Link>
                        </div>
                    </div>
                </div>
            </div>

            {term && (
                <div className="searchPage_results">
                    {data &&
                        !isLoading &&
                        data.output.results.map((item) => (
                            <div className="searchPage_result" key={item.id}>
                                <a className="searchPage_resultLink" href={item.a}>
                                    {item.c}
                                </a>
                                <a className="searchPage_resultTitle" href={item.a}>
                                    <h2>{item.t}</h2>
                                </a>
                                <p className="searchPage_resultSnippet">{item.d}</p>
                            </div>
                        ))}
                    {isLoading &&
                        [...Array(5)].map((_, index) => <SkeletonSearchPage key={index} theme="dark" />)}
                </div>
            )}

            <div className="footer">
                <div className="footerServices">Services</div>
                <div className="footerAbout">About Webpage</div>
            </div>
        </div>
    );
}

export default Image;
