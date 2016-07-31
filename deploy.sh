#!/bin/bash
rm -rf /tmp/tft
git clone $(pwd) /tmp/tft
pushd /tmp/tft

environment=$1
commitish=$2
if test -z $2; then
    case $1 in
        test) commitish=testing;;
        production) commitish=master;;
        *) echo "Couldn't figure out what to deploy."; exit 1;;
    esac
fi

echo "About to deploy $2 to environment $1."
echo -n "OK? "
read go

case $go in
    y|Y)
        git checkout $commitish
        rsync -rv --exclude .git site nfsn.sh fwilson42_tft-${environment}@ssh.phx.nearlyfreespeech.net:/home/protected
    ;;
    *)
        echo "Aborting deployment."
        exit 0;
    ;;
esac

popd
rm -rf /tmp/tft
