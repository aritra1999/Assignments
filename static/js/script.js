ace.require("ace/ext/language_tools");
var editor = ace.edit("editor");

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
    console.log(code)

    

    // $("#processing").css({"display": "block"});
    // $("#verdict").empty();
    // $.ajax({
    //     method: 'POST',
    //     url: '/dashboard/submit/{{ question.slug }}',
    //     data: {
    //         language: language,
    //         code: code,
    //         csrfmiddlewaretoken: csrf,
    //     }
    // })
    // .done(function (data, status) {
    //     $("#processing").css({"display": "none"});

    //     if (data.status === "success") {
    //         for (let i = 1; i <= 5; i++) {
    //             $("#verdict").append(i + "." + data['verdict' + i] + " Time taken: " + data['time' + i] + " Memory used: " + data['memory' + i] + " Score: " + data['score' + i] + "<br>");
    //         }
    //         $("#verdict").append("Total Score: " + data['totalscore'] + "/100<br><br>" );
    //         if(data['totalscore'] > 20){
    //             $("#verdict").append("Pass");
    //         }else{
    //             $("#verdict").append("Fail");
    //         }

    //     } else {
    //         $('#verdict').text(data['error']['message'] + "<br>");
    //         $('#verdict').append(data['error']['output']);
    //     }
    // })
    // .fail(function (data, status) {
    //     $('#verdict').text(data);
    // });
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
