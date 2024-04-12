function replyDelete(replyId) {
    // Display the Delete Modal if needed
    $('#DeleteModal').modal('show');

    // Handle the deletion when the user confirms
    $('#deleteConfirmButton').click(function() {
        $.ajax({
            url: `/delete_reply/${replyId}/`,  // Construct the URL with the postId
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function(response) {
                // Close the delete confirmation modal
                $('#DeleteModal').modal('hide');

                // Display a success message in another modal
                $('#postDeletedModal').modal('show');

                // Optionally, remove the deleted post from the page
                $('#reply-' + replyId).remove();

                // Hide the 'postDeletedModal' after 2 seconds
                setTimeout(function() {
                    $('#postDeletedModal').modal('hide');
                    // Reload the page after hiding the modal
                    location.reload();
                }, 3000);
            },
            error: function(error) {
                console.error('Error deleting post');
            }
        });
    });
}
