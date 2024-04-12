$(document).ready(function() {
    // Function to get CSRF token
    function getCSRFToken() {
        return $("input[name='csrfmiddlewaretoken']").val();
    }

    var clickedButtons = []; // Array to store clicked button IDs

    $('.comment-upvote-button').click(function(e) {
        e.preventDefault();
        var commentId = $(this).data('comment-id');
        var upvoteButton = $(this);

        $.ajax({
            url: '/comment/' + commentId + '/upvote/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()  // Include the CSRF token
            },
            success: function(response) {
                if (response.success) {
                    // Remove clicked-button class from other button
                    $('.comment-downvote-button').removeClass('clicked-button');

                    // Add clicked-button class to the clicked upvote button
                    upvoteButton.addClass('clicked-button');

                    // Update vote count
                    $('#vote-count-' + commentId).text(response.vote_count);

                    // Update clickedButtons array
                    if (!clickedButtons.includes(commentId)) {
                        clickedButtons.push(commentId);
                    }
                }
            }
        });
    });

    $('.comment-downvote-button').click(function(e) {
        e.preventDefault();
        var commentId = $(this).data('comment-id');
        var downvoteButton = $(this);

        $.ajax({
            url: '/comment/' + commentId + '/downvote/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()  // Include the CSRF token
            },
            success: function(response) {
                if (response.success) {
                    // Remove clicked-button class from other button
                    $('.comment-upvote-button').removeClass('clicked-button');

                    // Add clicked-button class to the clicked downvote button
                    downvoteButton.addClass('clicked-button');

                    // Update vote count
                    $('#vote-count-' + commentId).text(response.vote_count);

                    // Update clickedButtons array
                    if (!clickedButtons.includes(commentId)) {
                        clickedButtons.push(commentId);
                    }
                }
            }
        });
    });

    // Handle maintaining clicked state on page reload
    clickedButtons.forEach(function(commentId) {
        $('.comment-upvote-button[data-comment-id="' + commentId + '"]').addClass('clicked-button');
    });
});