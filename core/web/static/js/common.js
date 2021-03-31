document.addEventListener("DOMContentLoaded", function(){
  window.addEventListener('scroll', function() {
      if (window.scrollY>-1) {
        document.getElementById('navbar_top').classList.add('fixed-top');
        // add padding top to show content behind navbar
        navbar_height = document.querySelector('.navbar').offsetHeight;
        document.body.style.paddingTop = navbar_height + 'px';
      } else {
        document.getElementById('navbar_top').classList.remove('fixed-top');
         // remove padding top from body
        document.body.style.paddingTop = '0';
      } 
  });
});

//Notification
(async () => {
    // create and show the notification
    const showNotification = () => {
        // create a new notification
        const notification = new Notification('Instruction', {
            body: 'To save outputs of modules use --output after command',
        });

        // close the notification after 5 seconds
        setTimeout(() => {
            notification.close();
        }, 5 * 1000);
    }
    let granted = false;

	if (Notification.permission === 'granted') {
	    granted = true;
	} else if (Notification.permission !== 'denied') {
	    let permission = await Notification.requestPermission();
	    granted = permission === 'granted' ? true : false;
	}

	// show notification or the error message 
	granted ? showNotification() : showError();

})();



function changeSection(section){
      var head = document.getElementsByTagName('head')[0];
      var script = document.createElement('script');
      script.type = 'text/javascript';
      script.src = `/js/${section}.js`;
      head.appendChild(script);
      console.log(1);
}