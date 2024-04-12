$(document).ready(function () {
    $('.reply-button').click(function () {
      const commentID = $(this).data('comment-id'); // Use data-comment-id here
      const replyForm = $(`.reply-form[data-comment-id="${commentID}"]`); // Use data-comment-id here
      replyForm.toggle();
    });


  
    function displayMessage(message, isError = false) {
      // Display a modal with the provided message
      const modal = $('#messageModal');
      const modalContent = $('#messageText');
      
      // Set the modal content and style
      modalContent.text(message);
      if (isError) {
          modalContent.addClass('text-danger');
      } else {
          modalContent.removeClass('text-danger');
      }
  
      modal.modal('show');
  
      // Hide the modal after 2 seconds
      setTimeout(function () {
          modal.modal('hide');
      }, 2000);
  }
  
  $('.reply-form').submit(function (e) {
      e.preventDefault();
      const form = $(this);
      const csrftoken = $('[name=csrfmiddlewaretoken]').val();
      const commentID = form.data('comment-id');
      const reply = form.find('[name="reply"]').val();
      
      $.ajax({
          url: `/comments/${commentID}/add_reply/`,
          method: 'POST',
          headers: { "X-CSRFToken": csrftoken },
          data: { reply: reply },
          success: function (data) {
              console.log('Reply posted successfully');
              // Display a success message and reload the page
              displayMessage('Reply posted successfully');
              window.location.reload();
          },
          error: function (error) {
              console.error('Error posting reply');
              // Display an error message
              displayMessage('Error posting reply', true);
          }
      });
  });
  
  
    $('.cancel-reply').click(function () {
      const form = $(this).closest('.reply-form');
      form.removeClass('active');
      form.find('[name="reply"]').val('');
    });
  });
  
  // Function to update reply count using AJAX
function updateReplyCount(commentID) {
    $.ajax({
      url: `/comments/${commentID}/get_reply_count/`,
      method: 'GET',
      success: function (data) {
        const replyCountElement = $(`#reply-count-${commentID}`);
        replyCountElement.text(data.reply_count);
      },
      error: function (error) {
        console.error('Error getting reply count');
      }
    });
  }


  