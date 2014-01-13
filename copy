#!/bin/bash

cd "$(dirname "$0")"

REPO=tv.boxeeplay.svtplay3
if [[ `uname -s` == Darwin* ]]
then
    TARGET=$HOME/Library/Application\ Support/BOXEE/UserData/apps
    echo "Copying $REPO to $TARGET"

    rm -rf "$TARGET/$REPO"
    cp -r "$REPO" "$TARGET"
else
    echo "Your platform is currently not supported."
fi
