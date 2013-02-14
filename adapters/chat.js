(function() {
    function refreshLog() {
        // TODO(ross): make username dynamic
        $.getJSON("/log?user=user", function(data) {
            var chatRecord = $("#chatRecord");
            for (var i = 0; i < data.length; i++) {
                chatRecord.append($('<div class="message">').text(data[i]));
            }
        });
    }

    var form = $("#inputLine > form");
    form.submit(function(e) {
        e.preventDefault();
        e.stopPropagation();

        var field = $('input[name="m"]', form);
        $.post("/", {"m": field.val()}, function() {
            refreshLog();
        });
        field.val("");
    });

    window.setInterval(refreshLog, 5000);
})();
