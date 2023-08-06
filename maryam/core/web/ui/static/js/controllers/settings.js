import { themeHandler } from "./themeHandler.js";

export function settings(params){
    $('#gear').click((e)=>{
        if($('.settings').hasClass('slideOut'))
            $('.settings').removeClass("slideOut");
        $('.settings').addClass('slideIn');
    })
    $("#dark").click((e)=>{
        themeHandler(1);
    })

    $("#light").click((e)=>{
        themeHandler(0);
    })

    $('#cross').click((e)=>{
        if($('.settings').hasClass('slideIn'))
            $('.settings').removeClass("slideIn");
        $('.settings').addClass('slideOut');
    })


}