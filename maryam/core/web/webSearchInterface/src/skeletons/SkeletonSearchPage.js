import Shimmer from "./Shimmer";
import SkeletonElement from "./SkeletonElement";

const SkeletonSearchPage = ({ theme }) =>{
    const themeClass= theme || 'light';

    return (
        <div className={`skeleton-wrapper ${themeClass}`}>
            <div className="skeleton-searchPage">
                <SkeletonElement type = "title"/>
                <SkeletonElement type = "text"/>
                <SkeletonElement type = "description"/>
            </div>
            <Shimmer />
        </div>
        )
}

export default SkeletonSearchPage;