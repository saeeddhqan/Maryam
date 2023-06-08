import React, { useState } from "react";
import "./Search.css";
import SearchIcon from "@mui/icons-material/Search";
import MicIcon from "@mui/icons-material/Mic";
import imageIcon from "./image/image_icon.png";
import newsIcon from "./image/news_icon.png";
import socialIcon from "./image/social_icon.png";
import videoIcon from "./image/video_icon.png";
import { useNavigate } from "react-router-dom";
import { useStateValue } from "../StateProvider";
import { actionTypes } from "../reducer";
import VoiceSearch from "./VoiceSearch/index";
import { recognition } from "./VoiceSearch/VoiceRecognition";
import { Tooltip } from "@mui/material";
import CloseIcon from '@mui/icons-material/Close';


function Search({ hideShortCut = false }) {
  const [, dispatch] = useStateValue();
  const [voiceSearch, setVoiceSearch] = useState(false);
  const [input, setInput] = useState("");
  const navigate = useNavigate();
  const handleKeyDown = (e) => {
    if (e.key === "Enter" && e.target.value === "") {
      e.preventDefault();
    } else if (e.key === "Enter") {
      e.preventDefault();
      dispatch({
        type: actionTypes.SET_SEARCH_TERM,
        term: input,
      });

      navigate("/search");
    }
  };

  const openVoiceSearch = () => {
    setVoiceSearch(true);
    recognition.start();
    recognition.onresult = (event) => {
      const { transcript } = event.results[0][0];
      if (transcript !== null || transcript !== "" || transcript !== " ") {
        setVoiceSearch(false);
        setInput(transcript);
        console.log(transcript);
      } else {
        setVoiceSearch(false);
      }
    };
  };
  const closeVoiceSearch = () => {
    setVoiceSearch(false);
    recognition.stop();
  };

  const clearInput = () => {
    setInput("");
  };

  return (
    <form className="search">
      {voiceSearch ? <VoiceSearch closeVoiceSearch={closeVoiceSearch} /> : null}
      <div className="search_input">
        <SearchIcon />
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search anything"
        />
        {input && <CloseIcon onClick={clearInput} />}
        <Tooltip title="Search by voice">
          <MicIcon onClick={() => openVoiceSearch()} />
        </Tooltip>

      </div>

      {!hideShortCut ? (
        <div className="shortCut">
          <a href="/#">
            <img src={imageIcon} alt="Images" />
            <span>Images</span>
          </a>
          <a href="/#">
            <img src={newsIcon} alt="News" />
            <span>News</span>
          </a>
          <a href="/#">
            <img src={socialIcon} alt="Social" />
            <span>Social</span>
          </a>
          <a href="/#">
            <img src={videoIcon} alt="Shopping" />
            <span>Video</span>
          </a>
        </div>
      ) : (
        <div className="shortCut">
          <div className="shortCut_hidden">
            <a href="/#">
              <img src={imageIcon} alt="Images" />
              <span>Images</span>
            </a>
            <a href="/#">
              <img src={newsIcon} alt="News" />
              <span>News</span>
            </a>
            <a href="/#">
              <img src={socialIcon} alt="Social" />
              <span>Social</span>
            </a>
            <a href="/#">
              <img src={videoIcon} alt="Shopping" />
              <span>Video</span>
            </a>
          </div>
        </div>
      )}
    </form>
  );
}

export default Search;
