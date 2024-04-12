$(document).ready(function() {
    $('#editUsernameForm').submit(function(e) {
        e.preventDefault();
        $.ajax({
            url: '/edit_username/',  // Replace with your URL
            type: 'POST',
            data: $(this).serialize(),
            success: function(data) {
                // Set the modal message
                $('#usernameEditMessage').text(data.message);
                // Show the modal
                $('#usernameEditModal').modal('show');
                // Hide the modal after 2 seconds
                setTimeout(function() {
                    $('#usernameEditModal').modal('hide');
                    // Reload the page after hiding the modal
                    location.reload();
                }, 2000);
            },
            error: function(error) {
                // Set the modal message for error
                $('#usernameEditMessage').text('Error updating username');
                // Show the modal
                $('#usernameEditModal').modal('show');
            }
        });
    });
});
