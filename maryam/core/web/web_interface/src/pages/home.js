import React from "react";
import "./home.css";
import Search from "./search";
import logo from "./image/logo.png";

function Home() {
  return (
    <div className="home">
      <div className="home_body">
        <div className="webName">
          <img src={logo} alt="Logo" />
        </div>
        <div className="home_inputContainer">
          {/* Search */}
          <Search/>
        </div>
      </div>
    </div>
  );
}

export default Home;

