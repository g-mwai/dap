$(document).ready(function() {
    // Function to get CSRF token
    function getCSRFToken() {
        return $("input[name='csrfmiddlewaretoken']").val();
    }

    var clickedButtons = []; // Array to store clicked button IDs

    $('.upvote-button').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var upvoteButton = $(this);

        $.ajax({
            url: '/post/' + postId + '/upvote/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()  // Include the CSRF token
            },
            success: function(response) {
                if (response.success) {
                    // Remove clicked-button class from other button
                    $('.downvote-button').removeClass('clicked-button');

                    // Add clicked-button class to the clicked upvote button
                    upvoteButton.addClass('clicked-button');

                    // Update vote count
                    $('#vote-count-' + postId).text(response.vote_count);

                    // Update clickedButtons array
                    if (!clickedButtons.includes(postId)) {
                        clickedButtons.push(postId);
                    }
                }
            }
        });
    });

    $('.downvote-button').click(function(e) {
        e.preventDefault();
        var postId = $(this).data('post-id');
        var downvoteButton = $(this);

        $.ajax({
            url: '/post/' + postId + '/downvote/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()  // Include the CSRF token
            },
            success: function(response) {
                if (response.success) {
                    // Remove clicked-button class from other button
                    $('.upvote-button').removeClass('clicked-button');

                    // Add clicked-button class to the clicked downvote button
                    downvoteButton.addClass('clicked-button');

                    // Update vote count
                    $('#vote-count-' + postId).text(response.vote_count);

                    // Update clickedButtons array
                    if (!clickedButtons.includes(postId)) {
                        clickedButtons.push(postId);
                    }
                }
            }
        });
    });

    // Handle maintaining clicked state on page reload
    clickedButtons.forEach(function(postId) {
        $('.upvote-button[data-post-id="' + postId + '"]').addClass('clicked-button');
    });
});