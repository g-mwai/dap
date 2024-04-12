$(document).ready(function() {
    // Function to get CSRF token
    function getCSRFToken() {
        return $("input[name='csrfmiddlewaretoken']").val();
    }

    var clickedButtons = []; // Array to store clicked button IDs

    // Function to update vote count
    function updateVoteCount(replyId, newVoteCount) {
        $('#reply-vote-count-' + replyId).text(newVoteCount);
    }

    $('.reply-upvote-button').click(function(e) {
        e.preventDefault();
        var replyId = $(this).data('reply-post-id');
        var upvoteButton = $(this);

        $.ajax({
            url: '/reply/' + replyId + '/upvote/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function(response) {
                if (response.success) {
                    // Remove clicked-button class from other button
                    $('.reply-downvote-button').removeClass('clicked-button');

                    // Add clicked-button class to the clicked upvote button
                    upvoteButton.addClass('clicked-button');

                    // Update vote count
                    updateVoteCount(replyId, response.vote_count);

                    // Update clickedButtons array
                    if (!clickedButtons.includes(replyId)) {
                        clickedButtons.push(replyId);
                    }
                }
            }
        });
    });

    $('.reply-downvote-button').click(function(e) {
        e.preventDefault();
        var replyId = $(this).data('reply-post-id');
        var downvoteButton = $(this);

        $.ajax({
            url: '/reply/' + replyId + '/downvote/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function(response) {
                if (response.success) {
                    // Remove clicked-button class from other button
                    $('.reply-upvote-button').removeClass('clicked-button');

                    // Add clicked-button class to the clicked downvote button
                    downvoteButton.addClass('clicked-button');

                    // Update vote count
                    updateVoteCount(replyId, response.vote_count);

                    // Update clickedButtons array
                    if (!clickedButtons.includes(replyId)) {
                        clickedButtons.push(replyId);
                    }
                }
            }
        });
    });

    // Handle maintaining clicked state on page reload
    clickedButtons.forEach(function(replyId) {
        $('.reply-upvote-button[reply-post-id="' + replyId + '"]').addClass('clicked-button');
    });
});
