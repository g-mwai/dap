$(document).ready(function() {
    // Function to get the CSRF token from the cookie
    function getCSRFToken() {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, 'csrftoken'.length + 1) === 'csrftoken=') {
                    cookieValue = decodeURIComponent(cookie.substring('csrftoken='.length));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Attach event listeners to the file input fields
    $('#cover-image-input').on('change', function () {
        var input = this;
        var userCover = $('#user-cover');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                // Hide the current cover image and display the selected cover image
                userCover.hide();
                userCover.attr('src', e.target.result).show();
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    
    $('#avatar-modal-input').on('change', function () {
        var input = this;
        var userAvatar = $('#user-avatar');

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                // Hide the current avatar image and display the selected avatar image
                userAvatar.hide();
                userAvatar.attr('src', e.target.result).show();
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

 


   

   $('#ProfileEditModal').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission

        // var formData = $(this).serialize();
        var formData = new FormData();

        // Log the serialized form data to the console for debugging
        console.log(formData);

        // Append other profile information
        formData.append('name', $('#id_name').val());
        formData.append('location', $('#id_location').val());
        formData.append('job_title', $('#id_job_title').val());

        formData.append('ext_link', $('#id_ext_link').val());
        formData.append('bio', $('#id_bio').val());

        // Get the CSRF token
        var csrfToken = getCSRFToken();

        if (csrfToken) {
            // Add the CSRF token as a header
            $.ajaxSetup({
                headers: {
                    'X-CSRFToken': csrfToken
                }
            });

            $.ajax({
                type: 'POST',
                url: '/update_profile/', // Replace with your actual URL for profile update
                data: formData,
                processData: false,
                contentType: false,
                success: function(data) {
                    // Handle the success response
                    displayMessage('Success', 'Profile updated successfully');
                    setTimeout(function() {
                        location.reload();
                    }, 2000); // Reload the page after 2 seconds
                },
                error: function(xhr, status, error) {
                    // Handle the error response
                    displayMessage('Error', 'Profile update failed. Please check the form.');
                }
            });
        }
    });

    function displayMessage(title, message) {
        // Set the title and message in the modal
        $('#messageModalLabel').text(title);
        $('#messageText').text(message);

        // Show the modal
        $('#messageModal').modal('show');

        // Automatically close the modal after 2 seconds
        setTimeout(function() {
            $('#messageModal').modal('hide');
        }, 2000);
    }

});
