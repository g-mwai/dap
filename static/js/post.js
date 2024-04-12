$(document).ready(function() {

   
    $('#post-form').submit(function(event) {
    event.preventDefault();

    var formData = new FormData(this);
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    var modal = $('#StoryModal'); // Assuming your modal ID is 'postModal'
    
    var imageInput = $('#id_image')[0]; // Replace 'id_post_image' with the actual ID of the image input

    // Check if an image was selected
    if (imageInput.files.length > 0) {
        // Append the selected file to formData
        formData.append('post_image', imageInput.files[0]);
    }

    var successModal = $('#successModal'); // Your success modal ID
    $.ajaxSetup({
        headers: {
            'X-CSRFToken': csrfToken
        }
    });
    $.ajax({
        url: '{% url "upload_post" %}',
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.success) {
                modal.modal('hide');
                $('#post-form')[0].reset();
                // Show the success modal
                successModal.modal('show');
                // Update the success message in the modal
                $('#successMessage').text(response.message);
                // Close the success modal after a certain delay (e.g., 3 seconds)
                setTimeout(function() {
                    successModal.modal('hide');
                }, 3000); // 3000 milliseconds (3 seconds)
            } else {
                alert(response.message);
            }
        },
        error: function() {
            alert('An error occurred while submitting the form.');
        }
    });
});
    
    

    $('.follow-button').click(function(e) {
        e.preventDefault();
        var profileUsername = $(this).data('profile-username');
        var button = $(this);

        $.ajax({
            url: '/follow/' + profileUsername + '/',
            type: 'post',
            dataType: 'json',
            data: {
                csrfmiddlewaretoken: getCSRFToken()  // Include the CSRF token
            },
            success: function(response) {
                if (response.success) {
                    if (response.action === 'follow') {
                        button.text('Unfollow');
                    } else if (response.action === 'unfollow') {
                        button.text('Follow');
                    }
                }
            }
        });
    });

    var maxWords = 144;

        $('#post-form-body').on('input', function() {
            var words = $(this).val().trim().split(/\s+/).length;
            var progress = (words / maxWords) * 100;
            $('.progress-bar').css('width', progress + '%').attr('aria-valuenow', progress);
            $('.word-count').text(words + '/' + maxWords + ' words');

            if (words > maxWords) {
                $(this).val($(this).val().split(/\s+/).slice(0, maxWords).join(' '));
            }
        });
    
        
});