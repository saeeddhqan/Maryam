import PacmanLoader from "react-spinners/PacmanLoader";

export default function Loader({ Loading }) {
  if (Loading == true) {
    return (
      <div className="loader-container">
        <PacmanLoader color="#36d7b7" loading={true} size={40} />
        <div className="loading-text-container">
          <h3 className="loading-text">Loading...</h3>
        </div>
      </div>
    );
  } else {
    return "";
  }
}
