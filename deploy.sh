#!/bin/bash
git clone $(pwd) /tmp/tft
(cd /tmp/tft
git checkout testing
rsync -rv --exclude .git site fwilson42_tft-test@ssh.phx.nearlyfreespeech.net:/home/protected)
rm -rf /tmp/tft
