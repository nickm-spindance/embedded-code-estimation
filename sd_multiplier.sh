#!/bin/bash

set -u

function cleanup {
    echo "checking out: $start_branch"
    git checkout $start_branch
}

MY_DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
REPO_PATH=$1
OPENAIR_HOURS=$2
FIRST_COMMIT=$3
LAST_COMMIT=$4

cd $REPO_PATH

# Make sure there are no local changes in the repo
git diff --quiet --exit-code
(( $? != 0 )) && { echo "Error: there are local changes in $REPO_PATH"; exit 1; }

# Capture the current branch
start_branch=$(git branch | grep '^*' | sed 's/* //')
echo "starting branch: $start_branch"
trap cleanup EXIT

function count_loc {
    echo "checking out: $1"
    git checkout $1
    cd $REPO_PATH/code
    cloc \
        --fullpath \
        --json \
        --by-file \
        --report-file=$MY_DIR/report_$1.json \
        --not-match-d="(build|data|third-party|html|node_modules|proto-c|wasm_runner\/examples|emsdk|docs\/assets)" \
        --not-match-f="(package-lock.json)" \
        components projects
}

count_loc $FIRST_COMMIT
count_loc $LAST_COMMIT

# Feed data into python script
python $MY_DIR/sd_multiplier.py \
    $MY_DIR/report_$FIRST_COMMIT.json \
    $MY_DIR/report_$LAST_COMMIT.json \
    $OPENAIR_HOURS

