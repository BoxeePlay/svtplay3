boxee.setMode(boxee.PLAYER_MODE);
boxee.realFullScreen = true;

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

function isLive() {
    return browser.execute("svtplayer.SVTPlayer._instances.player.isLiveBroadcast;") == "true";
}

function seekTo(i) {
    browser.execute("svtplayer.SVTPlayer._instances.player.seek(" + i.toString() + ",1,0);");
};

function isPlaying() {
    return browser.execute("svtplayer.SVTPlayer._instances.player.video.isReady;") == "true" &&
        browser.execute("svtplayer.SVTPlayer._instances.player.video.isPlayingState;") == "true";
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
    playerState.canSeek = !isLive();
    playerState.canSeekTo = !isLive();
    playerState.canPause = true;
    playerState.isPaused = isLive() || isPaused();
    playerState.canSetFullScreen = true;
    playerState.time = isLive() ? 0 : time();
    playerState.duration = isLive() ? 0 : duration();
    playerState.progress = time() / duration() * 100;
};

function getDebugText() {
    return browser.execute("svtplayer.SVTPlayer._instances.player.video.getDebugText();");
}

function isFullScreen() {
    return /displayState: fullScreen/.test(getDebugText());
};

function setFullScreen() {
    if (!isFullScreen()) {
        setTimeout(setFullScreen, 500);
    }
    for (var w1 in boxee.getWidgets()) {
        var widg = boxee.getWidgets()[w1];
        if (/svtplayer/.test(widg.getAttribute("id"))) {
            widg.setActive();
        }
    }
};

boxee.onDocumentLoading = function () {
    setTimeout(setFullScreen, 1000);
    hasEndedPoll();
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

boxee.onSetFullScreen = setFullScreen;

boxee.onUpdateState = updateState;

