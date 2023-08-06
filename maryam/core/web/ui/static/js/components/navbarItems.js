export function navbarItems(){

    let categories = ['All', 'Images', 'News', 'Shopping', 'Videos', 'Maps'];
    

    categories.forEach(cat => {
        let item = "<a class='nav-item'>"+cat+"</a>";    
        $('#navbar').append(item);
    });

    

}