(function() {
    var form = $("#inputLine > form");

    function getUser() {
        return $('input[name="user"]', form).val();
    }

    function refreshLog() {
        $.getJSON("/log?" + $.param({"user": getUser()}), function(data) {
            var chatRecord = $("#chatRecord");
            for (var i = 0; i < data.length; i++) {
                chatRecord.append($('<div class="message">').text(data[i]));
            }
        });
    }

    form.submit(function(e) {
        e.preventDefault();
        e.stopPropagation();

        var field = $('input[name="m"]', form);
        $.post("/", {"m": field.val(), "user": getUser()}, function() {
            refreshLog();
        });
        field.val("");
    });

    window.setInterval(refreshLog, 2000);
})();
