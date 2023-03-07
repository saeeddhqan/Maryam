function addResults(pageWiseResults) {
    pageWiseResults.forEach(res => {
        let { a, c, d, t } = res;
        let result = ` <div class="result">
                        <a href=${c} target="_blank" rel="noopener noreferrer">
                            <div class="link">${c}</div>
                        </a>
                        <a href=${c} target="_blank" rel="noopener noreferrer">
                            <h2 class="result-heading">${t}</h2>
                        </a>
                        <div class="result-desc">${d}</div>
                    </div>`;
        $('#pagedResults').append(result);
    });
}

export function createResult(data) {
    $('#pagedResults').empty();
    window.scrollTo({ top: 0, behavior: 'smooth' });
    let results = data['output']['results'];
    let totalResults = results.length;

    let currPage = 1;
    let rangeStart = (currPage - 1) * 10;
    let rangeEnd = rangeStart + 10;
    let pageWiseResults = results.slice(rangeStart, rangeEnd);
    addResults(pageWiseResults);

    if (rangeEnd <= totalResults) {
        $('#moreResults').css("display", "block");;
    }

    $('#moreResults').click(() => {
        currPage = currPage + 1;
        rangeStart = (currPage - 1) * 10;
        rangeEnd = rangeStart + 10;
        pageWiseResults = results.slice(rangeStart, rangeEnd);
        let pageDivider = `<div class="flex">
                                <div class="number">${currPage}</div>
                                <hr></hr>
                            </div>`;
        $('#pagedResults').append(pageDivider);
        addResults(pageWiseResults);
    })

}