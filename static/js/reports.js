$(document).ready(function() {
    $('.delete-btn, .keep-btn').click(function() {
        // Find the nearest parent element with the class 'comment__counter'
        var commentCounter = $(this).closest('.comment__counter');
        
        // Get the post ID from the hidden input field within the parent element
        var postId = commentCounter.find('.post-id').val();
        
        // Log the post ID to the console to verify it
        console.log('Post ID:', postId);
        
        // Determine the action based on the data-action attribute of the button
        var action = $(this).data('action');
        
        // Make AJAX request based on the action
        $.ajax({
            url: '/dashboard/reported_post/' + action + '_reported_post/' + postId + '/',
            type: 'POST',
            success: function(data) {
                if (action === 'delete') {
                    alert('The reported post has been deleted.');
                } else {
                    alert('The reported post has been kept.');
                }
            },
            error: function(xhr, status, error) {
                console.error('Error:', error);
            }
        });
    });
});
