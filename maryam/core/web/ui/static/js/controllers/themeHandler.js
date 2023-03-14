export function themeHandler(params){
    const dark = `<link rel="stylesheet" href="/static/css/dark.css">`;
    const light = `<link rel="stylesheet" href="/static/css/light.css">`;
    if(!params.has('theme') || params.get("theme")=="0"){
        // theme not specified or theme specified is white
        $('head').append(light);
    }
    else{
        // dark theme specified
        $('head').append(dark);
    }
    
}