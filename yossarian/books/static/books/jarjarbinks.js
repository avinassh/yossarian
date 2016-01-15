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
                $(voteButton).removeClass("not-voted").addClass("voted")
            } else {
                $(voteButton).text("Vote")
                $(voteButton).removeClass("voted").addClass("not-voted")
            }
            $(voteButton).attr("target-values", JSON.stringify(targetValues))
        })
        .fail(function(data) {
            console.log("missa no care!")
        });
}


var replyBoxForm = '<div class="reply-box">' +
                  '<form class="ui reply form" action="/comments/" method="post" >' +
                   '<div class="field"><textarea></textarea></div>' +
                   '<button class="ui blue labeled submit icon button">' +
                   '<i class="icon edit"></i>Add Reply</button></form></div>'


function displayCommentBox(replyDiv) {
    var commentDiv = $(replyDiv).closest(".comment");
    var replyBox = $(commentDiv).children(".reply-box");

    if (replyBox.length) {
        $(replyBox).toggle();
    } else {
        var contentDiv = $(commentDiv).children(".content");
        $(contentDiv).after(replyBoxForm);
    };
    return false;
}

function postComment(replyBoxEvent, formContainer) {
    replyBoxEvent.preventDefault();
    var csrftoken = getCookie('csrftoken');
    raw_comment = formContainer.find('textarea').val()
    var commentDiv = formContainer.closest('.comment')
    var targetValues = $.parseJSON(commentDiv.attr("target-values"));
    console.log(targetValues)

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });

    $.post('/comments/', {raw_comment: raw_comment, book: targetValues.book_id,
                    parent: targetValues.comment_id}
        ).done(function(data) {
            console.log("missa happy!")
        })
        .fail(function(data) {
            console.log("missa no care!")
        });

}