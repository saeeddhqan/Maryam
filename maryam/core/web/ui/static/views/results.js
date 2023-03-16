
export function results(params) {
    let query = params.get("q");
    let results = `<header class='results-header'>
            <a id="title" href="#">Iris</a>
            <form id="searchBar">
                <input id="searchInput" type="text" name="searchInput" placeholder="Search" value="${query}" />
                    <button id="searchBtn" type="submit" name="searchBtn">
                        <svg style="width:24px;height:24px;" viewBox="0 0 24 24">
                            <path fill=" #5c97ff"
                                d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
                        </svg>
                    </button>
            </form>

            <div id="header_icons">
                <button>
                    <img src="./../static/icons/circle-grid-3x3.svg" alt="">
                </button>
                <button>
                    <img src="./../static/icons/gear.svg" alt="" id="gear">
                </button>

            </div>
        </header>
        <div class="settings">
            <header>
                <span>Settings</span>
                <button>
                    <img src="./../static/icons/cross.svg" id='cross' alt="">
                </button>
            </header>
            <div class="theme-selector">
                <p>Theme</p>
                        <button>
                            <img src="./../static/icons/sun.svg" alt="" id="light">
                        </button>
                <button>
                    <img src="./../static/icons/moon.svg" alt="" id="dark">
                </button>
            </div>
        </div>
        <div id="main-wrapper">
            <div id="navbar">
                <!--creates the category on the basis of search results-->
            </div>

            <main>
                <div id="results">
                    <div id="pagedResults">

                    </div>
                    <button id="moreResults" class="rounded-btn flex" type='button'>
                        <svg width="20" height="20" viewBox="0 0 16 16" xmlns="http://www.w3.org/2000/svg"><g fill="none" fill-rule="evenodd"><path d="M0 0h16v16H0z"></path><path fill="currentColor" d="m8.7 10.8 3.5-3.6 1 1L8 13.2 2.8 8.1l1-.9 3.5 3.6V2.7h1.4z"></path></g></svg>
                        Display More Results
                    </button>
                </div>


            </main>
        </div>

        <footer>

        </footer>`;
    return results;
}