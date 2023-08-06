const dark = `<link id='darkcss' rel="stylesheet" href="/static/css/dark.css">`;
const light = `<link id='lightcss' rel="stylesheet" href="/static/css/light.css">`;

function addLight(){    
    $('#darkcss').remove();
}

function addDark(){
    $('head').append(dark);
}

export function themeHandler(type){
    type == 0 ? addLight() : addDark();
}