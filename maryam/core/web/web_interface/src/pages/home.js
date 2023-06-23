import React from "react";
import "./home.css";
import Search from "./search";
import logo_white from "./image/logo_white.png";

function Home() {
  return (
    <div className="home">
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

