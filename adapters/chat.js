var form, user;

function refreshLog() {
    $.post("/log", {"user": user}, function(data) {
        var chatRecord = $("#chatRecord");
        for (var i = 0; i < data.length; i++) {
            chatRecord.append($('<div class="message">').text(data[i]));
        }
        if (data.length > 0) {
            chatRecord.scrollTop(chatRecord[0].scrollHeight);
        }
    }, "json");
}

$(function() {
    form = $("#inputLine > form");
    user = $('input[name="user"]', form).val();

    form.submit(function(e) {
        e.preventDefault();
        e.stopPropagation();

        var field = $('input[name="m"]', form);
        $.post("/", {"m": field.val(), "user": user}, function() {
            refreshLog();
        });
        field.val("");
    });
});

$(window).load(function() {
    var newUser = window.prompt("Pick a nickname:", user);
    if (newUser) {
        user = newUser;
    }
    $("#userName").text(user);
    $('input[type="submit"]').attr("disabled", "1");
    $.post("/", {"join": user}, function() {
        $('input[type="submit"]').removeAttr("disabled");
    });
    window.setInterval(refreshLog, 2000);
});
