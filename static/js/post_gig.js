$(document).ready(function() {
    $('#gig-form').submit(function(event) {
        event.preventDefault();

        var formData = new FormData(this);
        var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

        var modal = $('#GigModal'); // Assuming your modal ID is 'gigModal'

        $.ajaxSetup({
            headers: {
                'X-CSRFToken': csrfToken
            }
        });

        $.ajax({
            url: '{% url "upload_gig" %}',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                if (response.success) {
                    modal.modal('hide');
                    $('#gig-form')[0].reset();
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

    // Other JavaScript code for gig_form
});
