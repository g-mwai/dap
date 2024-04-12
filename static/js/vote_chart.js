$(document).ready(function() {
    $('.toggle-progress-button').on('click', function() {
        var postId = $(this).data('post-id');

        // Toggle the visibility of the progress container
        $(this).closest('.post_card').find('.progress-container').toggle();

        // Update progress bar with real-time data
        updateLikeData(postId);
    });

    // Function to get real-time like data
    function updateLikeData(postId) {
        // Replace the following with your actual data retrieval logic
        var likePercentage = getLikePercentage(postId);

        // Update progress bar width
        $('.like-progress').css('width', likePercentage + '%');
    }

    // Function to get like percentage from the server
    function getLikePercentage(postId) {
        // Assuming you have an API endpoint to get the like percentage for a post
        var apiUrl = '/api/get_like_percentage/' + postId; // Replace with your actual API endpoint

        // Make an AJAX request to get like percentage
        $.ajax({
            url: apiUrl,
            type: 'GET',
            success: function(data) {
                // Assuming the API returns the like percentage directly
                var likePercentage = data.like_percentage;

                // Log the like percentage to the console (you can remove this in production)
                console.log('Like Percentage for Post ' + postId + ': ' + likePercentage);

                // Update progress bar width
                $('.like-progress').css('width', likePercentage + '%');
            },
            error: function(xhr, status, error) {
                // Handle the error as needed
                console.error(xhr.responseText);
            }
        });
    }
});
