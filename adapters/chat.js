(function() {
    var form = $("#inputLine > form");
    var user = $('input[name="user"]', form).val();

    function refreshLog() {
        $.getJSON("/log?" + $.param({"user": user}), function(data) {
            var chatRecord = $("#chatRecord");
            for (var i = 0; i < data.length; i++) {
                chatRecord.append($('<div class="message">').text(data[i]));
            }
            if (data.length > 0) {
                chatRecord.scrollTop(chatRecord[0].scrollHeight);
            }
        });
    }

    form.submit(function(e) {
        e.preventDefault();
        e.stopPropagation();

        var field = $('input[name="m"]', form);
        $.post("/", {"m": field.val(), "user": user}, function() {
            refreshLog();
        });
        field.val("");
    });

    user = window.prompt("Pick a nickname:", user);
    $("#userName").text(user);
    $('input[type="submit"]').attr("disabled", "1");
    $.post("/", {"join": user}, function() {
        $('input[type="submit"]').removeAttr("disabled");
    });
    window.setInterval(refreshLog, 2000);
})();
