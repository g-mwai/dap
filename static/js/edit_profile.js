    $('#editAccountForm').submit(function (e) {
        e.preventDefault();

        $.ajax({ 
            url: '/edit_profile/',  
            type: 'POST',
            data: $(this).serialize(),
            success: function (data) {
                if (data.success) {
                    $('#successModal').modal('show');
                    setTimeout(function() {
                        $('#successModal').modal('hide');
                      }, 2000);
                } else {
                    // Handle errors and display them in the modal
                    $('#errorModal').modal('show');
                    setTimeout(function() {
                        $('#errorModal').modal('hide');
                      }, 2000);
                    // You can append the errors to a specific element in the modal
                    // e.g., $('#errorModal .modal-body').html(data.errors);
                }
            },
            error: function (error) {
                console.error(error);
            }
        });
    });

