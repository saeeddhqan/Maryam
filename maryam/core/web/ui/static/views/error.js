import { themeHandler } from "../js/controllers/themeHandler.js";

export function error(params){
    themeHandler(params);
    let error =
    `<h1>Error - 404</h1>`;
    $('#root').html(error());
}