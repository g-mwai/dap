$(document).ready(function () {
    $('#yesno_form').submit(function (e) {
      e.preventDefault();
  
      $.ajax({
        type: 'POST',
        url: '/new_yesno',  
        data: $(this).serialize(),
        success: function (data) {
          if (data.success) {
            showModal('success', 'Post submitted successfully!');
          } else {
            // Display errors in the error modal
            $('#errorModal .modal-body').html(data.errors);
            showModal('error', 'Error submitting form. Please check your input.');
          }
        },
        error: function (error) {
          showModal('error', 'Server error. Please try again later.');
        },
      });
    });
  
    function showModal(type, message) {
      // Set the modal title and body based on type
      var modalTitle = $('#' + type + 'ModalLabel');
      var modalBody = $('#' + type + 'Modal .modal-body');
      modalTitle.text(type === 'success' ? 'Success' : 'Error');
      modalBody.text(message);
  
      // Display the modal
      $('#' + type + 'Modal').modal('show');
    }
  });
  