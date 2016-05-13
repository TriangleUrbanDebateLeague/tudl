#!/bin/bash
git clone $(pwd) /tmp/tft
pushd /tmp/tft

if test $1 = test; then
    git checkout testing
    rsync -rv --exclude .git site nfsn.sh fwilson42_tft-test@ssh.phx.nearlyfreespeech.net:/home/protected
elif test $1 = prod; then
    git checkout master
    rsync -rv --exclude .git site nfsn.sh fwilson42_tft-production@ssh.phx.nearlyfreespeech.net:/home/protected
fi

popd
rm -rf /tmp/tft
