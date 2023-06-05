import Shimmer from "./Shimmer";
import SkeletonElement from "./SkeletonElement";

const SkeletonSearchPage = ({ theme, isScrolled}) =>{
    const themeClass= theme || 'light';

    return (
        <div className={`skeleton-wrapper ${themeClass}`}>
            <div className={`skeleton-searchPage ${isScrolled ? "headerOffset" : ""}`}>
                <SkeletonElement type = "title"/>
                <SkeletonElement type = "text"/>
                <SkeletonElement type = "description"/>
            </div>
            <Shimmer />
        </div>
        )
}

export default SkeletonSearchPage;