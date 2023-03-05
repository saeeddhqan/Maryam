import React from "react";
import "./index.css";
import CloseRoundedIcon from "@mui/icons-material/CloseRounded";
import MicRoundedIcon from "@mui/icons-material/MicRounded";

const VoiceSearch = ({ closeVoiceSearch }) => {
  return (
    <div className="voiceModal">
      <div className="voiceSearch ">
        <div className="voiceSearchBox">
          <h3>Voice Search</h3>
          <CloseRoundedIcon onClick={() => closeVoiceSearch()} />
        </div>
        <div className="voiceModalMic">
          <MicRoundedIcon fontSize="large" />
        </div>
      </div>
    </div>
  );
};

export default VoiceSearch;
