// Function to update bookmark button icon class based on initial bookmark status
function updateBookmarkButton(button, isBookmarked) {
  const icon = button.find('i');
  if (isBookmarked) {
      icon.removeClass('fa-regular').addClass('fa-solid text-primary');
  } else {
      icon.removeClass('fa-solid').addClass('fa-regular');
  }
}

// Attach click event handler to bookmark buttons
$('.bookmark-button').click(function () {
  const postID = $(this).data('post-id');
  const button = $(this);

  $.ajax({
      url: `/posts/${postID}/toggle_bookmark/`,
      type: 'POST',
      headers: { 'X-CSRFToken': getCookie('csrftoken') },
      data: {},
      success: function () {
          // Toggle bookmark button icon class after successful bookmark toggle
          const icon = button.find('i');
          icon.toggleClass('fa-solid orange').toggleClass('fa-regular');
      },
      error: function (error) {
          console.error('Error toggling bookmark');
      }
  });
});

// Fetch initial bookmark status for each bookmark button on page load
$('.bookmark-button').each(function () {
  const button = $(this);
  const postID = button.data('post-id');

  // Fetch bookmark status from the server
  $.ajax({
      url: `/posts/${postID}/bookmark_status/`,
      type: 'GET',
      success: function (response) {
          // Update bookmark button icon class based on initial bookmark status
          updateBookmarkButton(button, response.is_bookmarked);
      },
      error: function (error) {
          console.error('Error fetching bookmark status');
      }
  });
});



// Function to update bookmark button icon class based on initial bookmark status
function updateCommentBookmarkButton(button, isBookmarked) {
    const icon = button.find('i');
    if (isBookmarked) {
        icon.removeClass('fa-regular').addClass('fa-solid orange');
    } else {
        icon.removeClass('fa-solid').addClass('fa-regular');
    }
  }
  
  // Attach click event handler to bookmark buttons
  $('.comment-bookmark-button').click(function () {
    const commentID = $(this).data('comment-id');
    const button = $(this);
  
    $.ajax({
        url: `/posts/${commentID}/toggle_comment_bookmark/`,
        type: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken') },
        data: {},
        success: function () {
            // Toggle bookmark button icon class after successful bookmark toggle
            const icon = button.find('i');
            icon.toggleClass('fa-solid orange').toggleClass('fa-regular');
        },
        error: function (error) {
            console.error('Error toggling bookmark');
        }
    });
  });
  
  // Fetch initial bookmark status for each bookmark button on page load
  $('.comment-bookmark-button').each(function () {
    const button = $(this);
    const commentID = button.data('comment-id');
  
    // Fetch bookmark status from the server
    $.ajax({
        url: `/posts/${commentID}/comment_bookmark_status/`,
        type: 'GET',
        success: function (response) {
            // Update bookmark button icon class based on initial bookmark status
            updateCommentBookmarkButton(button, response.is_bookmarked);
        },
        error: function (error) {
            console.error('Error fetching bookmark status');
        }
    });
  });
  
