$(document).ready(function() {
    var audioPlaying = false;
    var audioElement = new Audio();

    $('#playPauseBtn').click(function() {
        var articleId = $(this).data('article-id');
        var buttonText = audioPlaying ? 'Play' : 'Pause';

        if (!audioPlaying) {
            audioElement.src = baseAudioURL.replace('0', articleId);
            console.log("Audio URL:", audioElement.src);
            audioElement.play();
            audioPlaying = true;
        } else {
            audioElement.pause();
            audioPlaying = false;
        }

        $(this).text(buttonText);
    });

    console.log("Initial Audio URL:", audioElement.src);
});
