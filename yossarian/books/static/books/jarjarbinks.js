function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function vote(voteButton) {
    var csrftoken = getCookie('csrftoken');

    var targetValues = $.parseJSON($(voteButton).attr("target-values"));

    if (targetValues.currentValue == 0) {
        var voteValue = 1;
    } else {
        var voteValue = 0;
    };

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    var postURL = '/arena_vote/' + targetValues.book + '/'

    $.post(postURL, { value: voteValue})
        .done(function(data) {
            console.log("missa happy!")
            targetValues.currentValue = voteValue
            if (voteValue == 1) {
                $(voteButton).text("Voted")
                $(voteButton).addClass("voted")
            } else {
                $(voteButton).text("Vote")
                $(voteButton).removeClass("voted")
            }
            $(voteButton).attr("target-values", JSON.stringify(targetValues))
        })
        .fail(function(data) {
            console.log("missa no care!")
        });
}