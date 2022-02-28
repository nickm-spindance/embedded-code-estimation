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

function gitstats {
    git log --shortstat $1..$2 | \
    awk '/^ [0-9]/ { f += $1; i += $4; d += $6 } END \
        { printf("%d %d %d\n", f, i, d) }'
}

count_loc $FIRST_COMMIT
count_loc $LAST_COMMIT
stat_output=$(gitstats $FIRST_COMMIT $LAST_COMMIT)
FILES_CHANGED=$(echo $stat_output | cut -d' ' -f1)
LINES_ADDED=$(echo $stat_output | cut -d' ' -f2)
LINES_DELETED=$(echo $stat_output | cut -d' ' -f3)

# Feed data into python script
python $MY_DIR/estimate.py \
    $MY_DIR/report_$FIRST_COMMIT.json \
    $MY_DIR/report_$LAST_COMMIT.json \
    $LINES_ADDED \
    $LINES_DELETED \
    $OPENAIR_HOURS
