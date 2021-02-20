ace.require("ace/ext/language_tools");
let editor = ace.edit("editor");

editor.setOptions({
    enableBasicAutocompletion: true,
    enableSnippets: true,
    enableLiveAutocompletion: true,
});


editor.setTheme("ace/theme/nord_dark");
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
    
    $(".success").css({"display": "none"});
    $(".error").css({"display": "none"});
    
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
                $("#success_message").append(
                    "<tr><td>" + i + ". </td><td>" + data['verdict' + i] + ".</td><td> Time taken: " + data['time' + i] + "</td><td> Memory used: " + data['memory' + i] + "</td><td> Score: " + data['score' + i] + "</td></tr>"
                );
            }
            $("#success_message").append("<br>Total Score: " + data['totalscore'] + "/100<br><br>" );
            if(data['totalscore'] > 20){
                $("#success").css({"display": "block"});
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

function run_code(){
    var code = editor.getValue();
    var language = document.getElementById('lang').value;
    var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;
    var slug = document.getElementById('slug').innerHTML;
    
    $("#processing").css({"display": "block"});
    
    $(".success").css({"display": "none"});
    $(".error").css({"display": "none"});
    
    $("#success_message").empty();
    $("#error_message").empty();

    $.ajax({
        method: 'POST',
        url: '/dashboard/run/' + slug,
        data: {
            language: language,
            code: code,
            csrfmiddlewaretoken: csrf,
        }
    })
    .done(function (data, status) {
        $("#processing").css({"display": "none"});
        if (data.status === "success") {
            $("#success_message").append("<p class='messageText'>" + data['verdict'] + ". Time taken: " + data['time'] + ", Memory used: " + data['memory'] + "</p>");    
            $("#success").css({"display": "block"});
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
