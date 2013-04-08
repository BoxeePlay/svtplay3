function hasEnded() {
    return browser.execute("svtplayer.SVTPlayer._instances.player.videoState;") == "end";
};

function hasEndedPoll() {
    if (hasEnded()) {
        boxee.notifyPlaybackEnded();
    } else {
        setTimeout(hasEndedPoll, 500);
    }
};

function play() {
    browser.execute("svtplayer.SVTPlayer._instances.player.play();");
    hasEndedPoll();
};

function pause() {
    browser.execute("svtplayer.SVTPlayer._instances.player.pause();");
};

function seekTo(i) {
    browser.execute("svtplayer.SVTPlayer._instances.player.seek(" + i.toString() + ",1,0);");
};

function isPlaying() {
    return browser.execute("svtplayer.SVTPlayer._instances.player.video.isPlayingState;") == "true";
};

function isPaused() {
    return !isPlaying();
};

function time() {
    return parseFloat(browser.execute("svtplayer.SVTPlayer._instances.player.video.getCurrentTime();"));
};

function duration() {
    return parseFloat(browser.execute("svtplayer.SVTPlayer._instances.player.video._settings.video.materialLength;"));
};

function updateState() {
    playerState.canSeek = true
    playerState.canSeekTo = true;
    playerState.canPause = true;
    playerState.isPaused = isPaused();
    playerState.canSetFullScreen = false;
    playerState.time = time();
    playerState.duration = duration();
};

function getDebugText() {
    return browser.execute("svtplayer.SVTPlayer._instances.player.video.getDebugText();");
}

function isFullScreen() {
    return /displayState: fullScreen/.test(getDebugText());
};

function setFullScreen() {
    for (var w1 in boxee.getWidgets()) {
        var widg = boxee.getWidgets()[w1];
        if (/svtplayer/.test(widg.getAttribute("id"))) {
            widg.click(920, 520);
            break;
        }
    }
    if (!isFullScreen()) {
        setTimeout(setFullScreen, 100);
    }
};

boxee.onDocumentLoaded = function () {
    boxee.realFullScreen = true;
    boxee.setMode(boxee.PLAYER_MODE);
    play();
    setTimeout(setFullScreen, 1000);
};

boxee.onPlay = play;

boxee.onPause = pause;

boxee.onSeekTo = function (millis) {
    seekTo(millis / 1000);
};

boxee.onSkip = function () {
    seekTo(time() + 10);
};

boxee.onBigSkip = function () {
    seekTo(time() + 30);
};

boxee.onBack = function () {
    seekTo(time() - 10);
};

boxee.onBigBack = function () {
    seekTo(time() - 30);
};

boxee.onUpdateState = updateState;

