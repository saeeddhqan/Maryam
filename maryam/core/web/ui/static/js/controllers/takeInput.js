import { searchInIris } from "./apicalls.js";

function highlightSearch(){
    $('#searchInput').on('change',()=>{
        let value = $('#searchInput').val();
        if(value!==''){
        }
    })
}

export function getInput() {
    highlightSearch();
    $('#searchBar').submit((e)=>{
        e.preventDefault();
        let query = $('#searchInput').val();
        searchInIris(query);
    })
}

