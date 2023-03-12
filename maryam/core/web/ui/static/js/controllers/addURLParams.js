export default function addURLParams(key,value){
    const searchParams = new URLSearchParams(window.location.search);
    searchParams.set(key,value);
    const newRelativePathQuery = window.location.pathname + '?' + searchParams.toString();
    // update in history
    history.pushState({key : value}, null, newRelativePathQuery);
}