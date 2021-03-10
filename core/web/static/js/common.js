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
