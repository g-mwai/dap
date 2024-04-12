$(document).ready(function () {


    // Handle the click event for the "Update Avatar" button
    $('#updateAvatarButton').click(function () {
      const form = $('#updateAvatarForm')[0];
      const formData = new FormData(form);

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


  
      $.ajax({
        url: '/upload_avatar/', // Replace with the actual URL for updating avatar
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
          // Close the update avatar modal
          $('#updateAvatarModal').modal('hide');
  
          // Display a success message in a message modal
          displayMessage('Avatar updated successfully');
          
          // Reload the page after 2 seconds to reflect the changes
          setTimeout(function () {
            window.location.reload();
          }, 2000);
        },
        error: function (error) {
          console.error('Error updating avatar');
          // Display an error message in a message modal
          displayMessage('Error updating avatar', true);
        },
      });

  

    });

    $('#deleteAvatarButton').click(function () {
        // Send an AJAX request to delete the avatar
        $.ajax({
            url: '/delete_avatar/', // Replace with the URL to your delete avatar view
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
                // Close the update avatar modal
                $('#updateAvatarModal').modal('hide');
                
                // Display a success message in another modal (optional)
                $('#imageDeletedModal').modal('show');

                // Reload the page to reflect the changes
                setTimeout(function () {
                    window.location.reload();
                  }, 2000);
            },
            error: function (error) {
                console.error('Error deleting avatar');
            }
        });
    });
  
    // Function to display success or error message in a message modal
    function displayMessage(message, isError = false) {
      const messageModal = $('#messageModal');
      const messageText = $('#messageText');
  
      messageText.text(message);
  
      if (isError) {
        messageText.addClass('text-warning');
      } else {
        messageText.removeClass('text-warning');
      }
  
      messageModal.modal('show');
  
      // Hide the message modal after 2 seconds
      setTimeout(function () {
        messageModal.modal('hide');
      }, 2000);
    }
  });
  