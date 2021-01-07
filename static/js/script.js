ace.require("ace/ext/language_tools");
let editor = ace.edit("editor");

editor.setOptions({
    enableBasicAutocompletion: true,
    enableSnippets: true,
    enableLiveAutocompletion: true,
});


editor.setTheme("ace/theme/tomorrow_night_blue");
editor.session.setMode("ace/mode/python");
editor.setFontSize(16);


editor.setOptions({
    enableBasicAutocompletion: true,
    enableSnippets: true,
    enableLiveAutocompletion: true,
});


function submit_code() {
    
    var code = editor.getValue();
    var language = document.getElementById('lang').value;
    var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var slug = document.getElementById('slug').innerHTML;
    $("#processing").css({"display": "block"});
    
    $("#success_message").empty();
    $("#error_message").empty();

    $.ajax({
        method: 'POST',
        url: '/dashboard/submit/' + slug,
        data: {
            language: language,
            code: code,
            csrfmiddlewaretoken: csrf,
        }
    })
    .done(function (data, status) {
        $("#processing").css({"display": "none"});
        if (data.status === "success") {
            for (let i = 1; i <= 5; i++) {
                $("#success_message").append(i + "." + data['verdict' + i] + " Time taken: " + data['time' + i] + " Memory used: " + data['memory' + i] + " Score: " + data['score' + i] + "<br>");
            }
            $("#success_message").append("Total Score: " + data['totalscore'] + "/100<br><br>" );
            if(data['totalscore'] > 20){
                $("#success").css({"display": "block"});
                $("#success_message").append("Pass");
            }else{
                $("#error").css({"display": "block"});
                $("#error_message").append("Wrong Answer!");
            }
        } else {
            $("#error").css({"display": "block"});
            $('#error_message').text(data['error']['message'] + "<br>");
            $('#error_message').append(data['error']['output']);
        }
    })
    .fail(function (data, status) {
        $('#error_message').text(data);
    });
}

window.goBack = function (e){
    let defaultLocation = "http://localhost:8000/dashboard/";
    let oldHash = window.location.hash;

    history.back();
    let newHash = window.location.hash;
    if(
        newHash === oldHash &&
        (typeof(document.referrer) !== "string" || document.referrer  === "")
    ){
        window.setTimeout(function(){
            window.location.href = defaultLocation;
        },1000);
    }
    if(e){
        if(e.preventDefault)
            e.preventDefault();
        if(e.preventPropagation)
            e.preventPropagation();
    }
    return false;
}
