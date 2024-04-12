$(document).ready(function () {
    // Get CSRF token from cookies
    const csrftoken = getCookie('csrftoken');

    $('.repost-button').click(function () {
        const postID = $(this).data('post-id');
        const button = $(this);

        $.ajax({
            url: `/posts/${postID}/toggle_repost/`,
            method: 'POST',
            data: {},
            headers: { "X-CSRFToken": csrftoken },  // Include CSRF token in headers
            success: function (data) {
                if (data.is_reposted) {
                    button.find('i').addClass('fa-solid fa-retweet-active').removeClass('fa-solid fa-retweet');
                } else {
                    button.find('i').addClass('fa-solid fa-retweet').removeClass('fa-solid fa-retweet-active');
                }
            },
            error: function () {
                console.error('Error toggling repost');
            }
        });
    });

    // Function to get CSRF token from cookies
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
});
