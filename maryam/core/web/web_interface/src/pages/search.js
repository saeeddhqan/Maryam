import React, { useState, useEffect } from "react";
import "./search.css";
import SearchIcon from "@mui/icons-material/Search";
import { useNavigate } from "react-router-dom";
import { useStateValue } from "../state_provider";
import { actionTypes } from "../reducer";
import CloseIcon from '@mui/icons-material/Close';


function Search() {
  const [, dispatch] = useStateValue();
  const [input, setInput] = useState("");
  const navigate = useNavigate();

  useEffect(() => {
    const storedSearchQuery = localStorage.getItem("searchQuery");
    if (storedSearchQuery) {
      setInput(storedSearchQuery);
    }
  }, []);

  const handleKeyDown = (e) => {
    if (e.key === "Enter" || e.type === "click") {
      e.preventDefault();
      if (input === "") {
        // Handle empty search term
        return;
      }
      dispatch({
        type: actionTypes.SET_SEARCH_TERM,
        term: input,
      });
      navigate("/search");
    }
  };

  const clearInput = () => {
    setInput("");
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  };

  useEffect(() => {
    localStorage.setItem("searchQuery", input);
  }, [input]);

  return (
    <form className="search">
      <div className="search_input">
        < input
          value={input}
          onChange={handleInputChange}
          onKeyDown={handleKeyDown}
          placeholder="Search anything"
        />
        <div className="search_icon">
          {input && <CloseIcon className="clear_icon" onClick={clearInput} />}
          <SearchIcon onClick={handleKeyDown} />
        </div>
      </div>
    </form>
  );
}

export default Search;
