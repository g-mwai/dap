$(document).ready(function () {
    $('.comment-button').click(function () {
      const postID = $(this).data('post-id');
      const commentForm = $(`.comment-form[data-post-id="${postID}"]`);
      commentForm.toggle();
    });
  
    $('.toggle-replies-link').click(function (e) {
      e.preventDefault();
      const commentID = $(this).data('target');
      const replies = $(`#${commentID}`);
  
      // Toggle replies visibility
      replies.toggle();
  
      // Toggle link text
      if (replies.is(':visible')) {
        $(this).text('Hide Replies');
      } else {
        $(this).text('Show Replies');
      }
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
  
 $('.comment-form').submit(function (e) {
      e.preventDefault();
      const form = $(this);
      const postID = form.data('post-id');
      const comment = form.find('[name="comment"]').val();
      const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // Extract CSRF token
  
      
      $.ajax({
          url: `/posts/${postID}/add_comment/`, // Replace with the actual URL
          method: 'POST',
          headers: { "X-CSRFToken": csrftoken }, // Include CSRF token in headers
          data: { comment: comment },
          success: function (data) {
              console.log('Comment posted successfully');
              // Display a success message and reload the page
              displayMessage('Comment posted successfully');
              window.location.reload();
          },
          error: function (error) {
              console.error('Error posting comment');
              // Display an error message
              displayMessage('Error posting comment', true);
          }
      });
  });



  
  $('.detail-comment-form').submit(function (e) {
      e.preventDefault();
      const form = $(this);
      const postID = form.data('post-id');
      const comment = form.find('[name="comment"]').val();
      const csrftoken = $('[name=csrfmiddlewaretoken]').val(); // Extract CSRF token
      const formData = new FormData();

      formData.append('comment', comment);
      formData.append('post_id', postID); 
    
      const imageInput = $('#id_comment_image')[0]; // Replace 'id_post_image' with the actual ID of the image input

    // Check if an image was selected
    if (imageInput.files.length > 0) {
        // Append the selected file to formData
        formData.append('comment_image', imageInput.files[0]);
    }
      $.ajax({
        url: `/posts/${postID}/add_comment/`, // Replace with the actual URL
        method: 'POST',
        headers: { "X-CSRFToken": csrftoken }, // Include CSRF token in headers
        data: formData,
        processData: false,
        contentType: false,
          success: function (data) {
              console.log('Comment posted successfully');
              // Display a success message and reload the page
              displayMessage('Comment posted successfully');
              window.location.reload();
          },
          error: function (error) {
              console.error('Error posting comment');
              // Display an error message
              displayMessage('Error posting comment', true);
          }
      });
  });
  

  });

  // Function to update comment count using AJAX
function updateCommentCount(postID) {
  $.ajax({
      url: `/posts/${postID}/get_comment_count/`, // Update the URL to your view
      method: 'GET',
      success: function (data) {
          const commentCountElement = $(`#comment-count-${postID}`);
          commentCountElement.text(data.comment_count);
      },
      error: function (error) {
          console.error('Error getting comment count');
      }
  });
}
  

