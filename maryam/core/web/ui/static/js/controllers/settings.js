import addURLParams from "./addURLParams.js"
import { themeHandler } from "./themeHandler.js";

export function settings(){
    $('#gear').click((e)=>{
        // slide in
        $(".settings").toggleClass("hidden");
        $(".settings").toggleClass("show");
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
        //slide out 
        $(".settings").toggleClass("hidden");
        $(".settings").toggleClass("show");
    })
}