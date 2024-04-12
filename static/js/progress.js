var maxCharacters = 360;

// Function to update the character count and progress bar
function updateCharacterCountAndProgressBar(input, progressBarSelector, characterCountSelector) {
    var characters = input.val().trim().length;
    var progress = (characters / maxCharacters) * 100;
    $(progressBarSelector).css('width', progress + '%').attr('aria-valuenow', progress);
    $(characterCountSelector).text(characters + '/' + maxCharacters );

    if (characters > maxCharacters) {
        input.val(input.val().substring(0, maxCharacters));
    }
}

// Attach an event listener to the comment and reply inputs
$('.comment-input, .reply-input, .profile-input, .post-input',).on('input', function() {
    updateCharacterCountAndProgressBar($(this), '.progress-bar', '.character-count');
});


