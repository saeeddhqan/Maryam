import { getInput } from "../js/controllers/takeInput.js";
import { settings } from "../js/controllers/settings.js";

export function home(params) {
    let home = `<header class="home-header">
    <div id="header_icons">
        <button>
            <img src="./../static/icons/circle-grid-3x3.svg" id='grid' alt="">
        </button>
        <button>
            <img src="./../static/icons/gear.svg" id='gear' alt="">
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
<div class='home-main'>
    <h1 style="text-align:center">
        Iris
    </h1>
    <form id="searchBar" style="justify-content: center;">
        <input id="searchInput" type="text" name="searchInput" placeholder="Search" value='' />
        <button id="searchBtn" type="submit" name="searchBtn">
            <svg style="width:24px;height:24px;" viewBox="0 0 24 24">
                <path fill=" #5c97ff"
                    d="M9.5,3A6.5,6.5 0 0,1 16,9.5C16,11.11 15.41,12.59 14.44,13.73L14.71,14H15.5L20.5,19L19,20.5L14,15.5V14.71L13.73,14.44C12.59,15.41 11.11,16 9.5,16A6.5,6.5 0 0,1 3,9.5A6.5,6.5 0 0,1 9.5,3M9.5,5C7,5 5,7 5,9.5C5,12 7,14 9.5,14C12,14 14,12 14,9.5C14,7 12,5 9.5,5Z" />
            </svg>
        </button>
    </form>

</div>
<footer>

</footer>`;
        $('#root').html(home);
        getInput();
        settings();
}