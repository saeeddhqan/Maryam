import { navbarItems } from "../components/navbarItems.js";
import { results } from "../../views/results.js";
import { getInput } from '../controllers/takeInput.js'
import { settings } from "./settings.js";


function addResults(pageWiseResults) {
    pageWiseResults.forEach(res => {
        let { a, c, d, t } = res;
        let result = ` <div class="result">
                        <a href=${a} target="_blank" rel="noopener noreferrer">
                            <div class="breadcrumb">${c}</div>
                        </a>
                        <a href=${a} target="_blank" rel="noopener noreferrer">
                            <div class="result-heading">${t}</div>
                        </a>
                        <div class="result-desc">${d}</div>
                    </div>`;
        $('#pagedResults').append(result);
    });
}

export function createResult(params, data) {
    $('#root').html(results(params));
    navbarItems();
    getInput();
    settings();

    $('#pagedResults').empty();
    window.scrollTo({ top: 0, behavior: 'smooth' });
    let res = data['output']['results'];
    let totalResults = res.length;

    let currPage = 1;
    let rangeStart = (currPage - 1) * 10;
    let rangeEnd = rangeStart + 10;
    let pageWiseResults = res.slice(rangeStart, rangeEnd);
    addResults(pageWiseResults);

    if (rangeEnd <= totalResults) {
        $('#moreResults').css("display", "block");;
    }

    $('#moreResults').click(() => {
        currPage = currPage + 1;
        rangeStart = (currPage - 1) * 10;
        rangeEnd = rangeStart + 10;
        pageWiseResults = res.slice(rangeStart, rangeEnd);
        let pageDivider = `<div class="flex">
                                <div class="number">${currPage}</div>
                                <hr class='divider'></hr>
                            </div>`;
        $('#pagedResults').append(pageDivider);
        addResults(pageWiseResults);
    })

}