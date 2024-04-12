$(document).ready(function () {


    // Handle the click event for the "Update Cover" button
    $('#updateCoverButton').click(function () {
      const form = $('#updateCoverForm')[0];
      const formData = new FormData(form);




  
      $.ajax({
        url: '/upload_cover/', // Replace with the actual URL for updating cover
        type: 'POST',
        data: formData,
        processData: false,
        contentType: false,
        success: function (data) {
          // Close the update cover modal
          $('#updateCoverModal').modal('hide');
  
          // Display a success message in a message modal
          displayMessage('Cover image updated successfully');
          
          // Reload the page after 2 seconds to reflect the changes
          setTimeout(function () {
            window.location.reload();
          }, 2000);
        },
        error: function (error) {
          console.error('Error updating cover');
          // Display an error message in a message modal
          displayMessage('Error updating cover', true);
        },
      });

  

    });

    $('#deleteCoverButton').click(function () {
        // Send an AJAX request to delete the Cover
        $.ajax({
            url: '/delete_cover/', // Replace with the URL to your delete cover view
            type: 'POST',
            data: {
                csrfmiddlewaretoken: $('input[name=csrfmiddlewaretoken]').val(),
            },
            success: function (response) {
                // Close the update Cover modal
                $('#updateCoverModal').modal('hide');
                
                // Display a success message in another modal (optional)
                $('#imageDeletedModal').modal('show');

                // Reload the page to reflect the changes
                setTimeout(function () {
                    window.location.reload();
                  }, 2000);
            },
            error: function (error) {
                console.error('Error deleting cover image');
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
  