import { searchInIris } from "./apicalls.js";

export function getInput() {
    $('#searchBar').submit((e)=>{
        e.preventDefault();
        let query = $('#searchInput').val();
        searchInIris(query);
    })
}

