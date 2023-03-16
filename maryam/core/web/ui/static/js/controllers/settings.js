import addURLParams from "./addURLParams.js"
import { themeHandler } from "./themeHandler.js";

export function settings(){
    $('#gear').click((e)=>{
        if($('.settings').hasClass('slideOut'))
            $('.settings').removeClass("slideOut");
        $('.settings').addClass('slideIn');
    })
    $("#dark").click((e)=>{
        addURLParams("theme","1");
        const params = new URLSearchParams(window.location.search);
        themeHandler(params);
    })

    $("#light").click((e)=>{
        addURLParams("theme","0");
        const params = new URLSearchParams(window.location.search);
        themeHandler(params);
    })

    $('#cross').click((e)=>{
        if($('.settings').hasClass('slideIn'))
            $('.settings').removeClass("slideIn");
        $('.settings').addClass('slideOut');
    })


}