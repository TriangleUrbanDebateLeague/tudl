#!/bin/bash
git clone $(pwd) /tmp/tft

if test $1 = test; then
    (cd /tmp/tft
    git checkout testing
    rsync -rv --exclude .git site nfsn.sh fwilson42_tft-test@ssh.phx.nearlyfreespeech.net:/home/protected)
else
    if test $1 = prod; then
        (cd /tmp/tft
        git checkout master
        rsync -rv --exclude .git site nfsn.sh fwilson42_tft-production@ssh.phx.nearlyfreespeech.net:/home/protected)
    fi
fi

rm -rf /tmp/tft
