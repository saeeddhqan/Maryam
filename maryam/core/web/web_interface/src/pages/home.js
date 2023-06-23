import React from "react";
import "./home.css";
import SettingsOutlinedIcon from "@mui/icons-material/SettingsOutlined";
import AppsOutlinedIcon from "@mui/icons-material/AppsOutlined";
import Search from "./search";
import { Tooltip } from "@mui/material";
import logo_white from "./image/logo_white.png";

function Home() {
  return (
    <div className="home">
      <div className="home_header">
        <div className="homeSetting">
          <Tooltip title="Setting">
            <SettingsOutlinedIcon fontSize="large" style={{ color: "white" }} />
          </Tooltip>
        </div>
        <div className="homeApps">
          <Tooltip title="Apps">
            <AppsOutlinedIcon fontSize="large" style={{ color: "white" }} />
          </Tooltip>
        </div>
      </div>

      <div className="home_body">
        <div className="webName">
          <img src={logo_white} alt="Logo" />
        </div>
        <div className="home_inputContainer">
          {/* Search */}
          <Search hideShortCut />
        </div>
      </div>
    </div>
  );
}

export default Home;

