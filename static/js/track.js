
document.addEventListener( 'visibilitychange' , function() {
    let today = new Date();
    let dateTime = today.getFullYear()+'-'+(today.getMonth()+1)+'-'+today.getDate()+' '+ today.getHours() + ":" + today.getMinutes() + ":" + today.getSeconds();
    var log = JSON.parse(localStorage.getItem('activity')) || [];

    if (document.hidden) {
        log.push({
            'time': dateTime,
            'activity': 'User has left'
        });
    } else {
        
        log.push({
            'time': dateTime,
            'activity': 'User is back'
        });
    }
    localStorage.setItem('activity', JSON.stringify(log));
}, false );
