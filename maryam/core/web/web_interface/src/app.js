import React from "react";
import Home from "./pages/home";
import { MemoryRouter, Routes, Route } from "react-router-dom";
import SearchPage from "./pages/search_page";

function App() {
  return (
    <div className="App">
      <MemoryRouter>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/search" element={<SearchPage />} />
          <Route path="*" element={<Home />} />
        </Routes>
      </MemoryRouter>
    </div>
  );
}

export default App;
