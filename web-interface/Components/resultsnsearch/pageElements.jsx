export default function BottomElement({
  setLowerLimit,
  setUpperLimit,
  setCurrentPage,
  totalPages,
  LowerLimit,
  UpperLimit,
  Currentpage,
  totalitems,
}) {
  function ScrollToTop() {
    //  scroll to top on page load
    window.scrollTo({ top: 0, left: 0, behavior: "smooth" });
  }
  function shiftPageUp() {
    if (LowerLimit > totalitems) {
      return;
    }
    setUpperLimit(UpperLimit + 10);
    setLowerLimit(LowerLimit + 10);
    setCurrentPage(Currentpage + 1);
    console.log(UpperLimit, LowerLimit);
    ScrollToTop();
  }
  function shiftPageDown() {
    if (LowerLimit == 0) {
      return;
    }
    setUpperLimit(UpperLimit - 10);
    setLowerLimit(LowerLimit - 10);
    setCurrentPage(Currentpage - 1);
    console.log(UpperLimit, LowerLimit);
    ScrollToTop();
  }

  return (
    <div className="bottom-element">
      <p className="page-number-text">
        Page {Currentpage + 1} of {totalPages + 1}
      </p>
      <button className="back-button" onClick={shiftPageDown}>
        <svg viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg">
          <title />
          <path d="M39.3756,48.0022l30.47-25.39a6.0035,6.0035,0,0,0-7.6878-9.223L26.1563,43.3906a6.0092,6.0092,0,0,0,0,9.2231L62.1578,82.615a6.0035,6.0035,0,0,0,7.6878-9.2231Z" />
        </svg>
      </button>
      <button className="next-button" onClick={shiftPageUp}>
        <svg viewBox="0 0 96 96" xmlns="http://www.w3.org/2000/svg">
          <title />
          <path d="M69.8437,43.3876,33.8422,13.3863a6.0035,6.0035,0,0,0-7.6878,9.223l30.47,25.39-30.47,25.39a6.0035,6.0035,0,0,0,7.6878,9.2231L69.8437,52.6106a6.0091,6.0091,0,0,0,0-9.223Z" />
        </svg>
      </button>
    </div>
  );
}
