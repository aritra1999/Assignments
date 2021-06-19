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


// Prevent Right click 
document.addEventListener('contextmenu', event => event.preventDefault());

// Prevent external copy paste
document.body.addEventListener("keydown",function(e){
    e = e || window.event;
    let key = e.which || e.keyCode; // keyCode detection
    let ctrl = e.ctrlKey ? e.ctrlKey : ((key === 17) ? true : false); // ctrl detection

    if ( key == 86 && ctrl ) {
        e.preventDefault();
        let clipboard_text = localStorage.getItem("clipboard");
        editor.session.insert(editor.getCursorPosition(), clipboard_text);

    } else if ( key == 67 && ctrl ) {
        e.preventDefault();
        let selected = editor.getSession().doc.getTextRange(editor.selection.getRange());
        localStorage.setItem("clipboard", selected);
    } else if ( key == 88 && ctrl){
        e.preventDefault();
        let selected = editor.getSession().doc.getTextRange(editor.selection.getRange());
        editor.session.replace(editor.selection.getRange(), "");  
        localStorage.setItem("clipboard", selected);
    }
},false);
