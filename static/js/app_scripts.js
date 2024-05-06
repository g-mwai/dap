function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      var cookies = document.cookie.split(';');
      for (var i = 0; i < cookies.length; i++) {
        var cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
  }
  
// Listen for the delete confirmation button click



$(".tab").click(function(){
    $(".tabs-bar").find(".tab-active").removeClass("tab-active");
    $(".content-container").children().hide();
    $(this).addClass("tab-active");
    $(".content-" + this.id).show();
})

$(".form-tab").click(function(){
    $(".form-tabs-bar").find(".form-tab-active").removeClass("form-tab-active");
    $(".form-content-container").children().hide();
    $(this).addClass("form-tab-active");
    $(".form-content-" + this.id).show();
})

$(".profile-tab").click(function(){
  $(".profile-tabs-bar").find(".profile-tab-active").removeClass("profile-tab-active");
  $(".profile-content-container").children().hide();
  $(this).addClass("profile-tab-active");
  $(".profile-content-" + this.id).show();
})

$('.file-input').on('change', function() {
    var fileName = $(this).val().split('\\').pop();
    $(this).next('.file-label').html('<span class="icon">📷</span> ' + fileName);
});

$('#id_image').change(function () {
    var fileInput = $(this)[0];
    if (fileInput.files && fileInput.files[0]) {
        var reader = new FileReader();
        reader.onload = function (e) {
            $('#thumbnail').attr('src', e.target.result);
            $('.thumbnail-container').show(); // Show the thumbnail container
        };
        reader.readAsDataURL(fileInput.files[0]);
    } else {
        $('.thumbnail-container').hide(); // Hide the thumbnail container
    }
});

$('.clear-image-button').click(function () {
    $('#id_image').val(null); // Clear the selected image
    $('.thumbnail-container').hide();
});


$('#id_sell_image').change(function () {
  
  var fileInput = $(this)[0];
  if (fileInput.files && fileInput.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        
          $('#sell_thumbnail').attr('src', e.target.result);
          $('.sell-thumbnail-container').show(); // Show the thumbnail container
      };
      reader.readAsDataURL(fileInput.files[0]);
  } else {
      $('.sell-thumbnail-container').hide(); // Hide the thumbnail container
  }
});

$('.clear-sell-image-button').click(function () {
  $('#id_sell_image').val(null); // Clear the selected image
  $('.sell-thumbnail-container').hide();
});

$('#id_project_image').change(function () {
  
  var fileInput = $(this)[0];
  if (fileInput.files && fileInput.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        
          $('#project_thumbnail').attr('src', e.target.result);
          $('.project-thumbnail-container').show(); // Show the thumbnail container
      };
      reader.readAsDataURL(fileInput.files[0]);
  } else {
      $('.project-thumbnail-container').hide(); // Hide the thumbnail container
  }
});

$('.clear-project-image-button').click(function () {
  $('#id_project_image').val(null); // Clear the selected image
  $('.project-thumbnail-container').hide();
});



$('#id_comment_image').change(function () {
  
  var fileInput = $(this)[0];
  if (fileInput.files && fileInput.files[0]) {
      var reader = new FileReader();
      reader.onload = function (e) {
        
          $('#comment_thumbnail').attr('src', e.target.result);
          $('.comment-thumbnail-container').show(); // Show the thumbnail container
      };
      reader.readAsDataURL(fileInput.files[0]);
  } else {
      $('.comment-thumbnail-container').hide(); // Hide the thumbnail container
  }
});

$('.clear-comment-image-button').click(function () {
  $('#id_comment_image').val(null); // Clear the selected image
  $('.comment-thumbnail-container').hide();
});




$('.show-more-link').click(function () {
    $(this).hide();
    $(this).siblings('.short-body').hide();
    $(this).siblings('.full-body').show();
    $(this).siblings('.show-less-link').show();

});

$('.show-less-link').click(function () {
    $(this).hide();
    $(this).siblings('.full-body').hide();
    $(this).siblings('.short-body').show();
    $(this).siblings('.show-more-link').show();
});

$('.category-button').click(function() {
  const category = $(this).data('category');
  window.location.href = `/category/${category}/`; // Redirect to the category URL
});

$('.copy-url-button').click(function () {
  const postURL = $(this).data('url');
  
  navigator.clipboard.writeText(postURL)
      .then(() => {
          // Show a notification or alert that URL is copied
          alert('URL copied to clipboard: ' + postURL);
      })
      .catch((error) => {
          console.error('Error copying URL:', error);
      });
});

$('#follow-button').click(function () {
  const username = $(this).data('username');
  const button = $(this);
  const csrfToken = $('input[name=csrfmiddlewaretoken]').val(); // Get the CSRF token value

  $.ajax({
    url: `/toggle_follow/${username}/`,
    type: 'POST',
    data: {},
    headers: {
      'X-CSRFToken': csrfToken, // Include the CSRF token in the request headers
    },
    success: function (data) {
      if (data.followed) {
        button.text('Unfollow');
      } else {
        button.text('Follow');
      }
    },
    error: function (error) {
      console.error('Error toggling follow status');
    }
  });
});

// Select all comment textareas
var commentTextareas = $('.comment-form textarea');

// Function to adjust textarea height
function adjustTextareaHeight(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}

// Attach input event listener to all comment textareas
commentTextareas.on('input', function () {
  adjustTextareaHeight(this);
});

// Initialize textarea heights
commentTextareas.each(function () {
  adjustTextareaHeight(this);
});


// Select all comment textareas
var DcommentTextareas = $('.detail-comment-form textarea');

// Function to adjust textarea height
function adjustDTextareaHeight(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}

// Attach input event listener to all comment textareas
DcommentTextareas.on('input', function () {
  adjustDTextareaHeight(this);
});

// Initialize textarea heights
DcommentTextareas.each(function () {
  adjustDTextareaHeight(this);
});

// Select all comment textareas
var RcommentTextareas = $('.reply-form textarea');

// Function to adjust textarea height
function adjustRTextareaHeight(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}

// Attach input event listener to all comment textareas
RcommentTextareas.on('input', function () {
  adjustRTextareaHeight(this);
});

// Initialize textarea heights
RcommentTextareas.each(function () {
  adjustRTextareaHeight(this);
});

// Select all comment textareas
var postTextareas = $('.post_form textarea');

// Function to adjust textarea height
function adjustTextareaHeight(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}

// Attach input event listener to all post textareas
postTextareas.on('input', function () {
  adjustTextareaHeight(this);
});

// Initialize textarea heights
postTextareas.each(function () {
  adjustTextareaHeight(this);
});


$('.set-bg').each(function () {
  var bg = $(this).data('setbg');
  $(this).css('background-image', 'url(' + bg + ')');
});

//Search Switch
$('.search-switch').on('click', function () {
  $('.search-model').fadeIn(400);
});

$('.search-close-switch').on('click', function () {
  $('.search-model').fadeOut(400, function () {
      $('#search-input').val('');
  });
});

//Canvas Menu
$(".canvas__open").on('click', function () {
  $(".offcanvas-menu-wrapper").addClass("active");
  $(".offcanvas-menu-overlay").addClass("active");
});

$(".offcanvas-menu-overlay, .offcanvas__close").on('click', function () {
  $(".offcanvas-menu-wrapper").removeClass("active");
  $(".offcanvas-menu-overlay").removeClass("active");
});