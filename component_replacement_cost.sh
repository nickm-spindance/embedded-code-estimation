#!/bin/bash

set -u

function cleanup {
    echo "checking out: $start_branch"
    git checkout $start_branch
}

MY_DIR=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )
REPO_PATH=$HOME/src/esp32-aws-starter
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
    cd $REPO_PATH
    cloc \
        --fullpath \
        --json \
        --by-file \
        --report-file=$MY_DIR/report_$1.json \
        --not-match-d="(build|data|third-party|html|node_modules|proto-c|wasm_runner\/examples|emsdk|docs\/assets)" \
        --not-match-f="(package-lock.json|espcoredump.py)" \
        code/components code/projects tools
}

function gitstats {
    git log --shortstat | \
    awk '/^ [0-9]/ { f += $1; i += $4; d += $6 } END \
        { printf("%d %d %d\n", f, i, d) }'
}

BRANCH=master

# Multiplier for COCOMO model, computed from prior customer projects
# (see, for example, ego_sd_multiplier.sh)
COCOMO_SD_MULTIPLIER=0.31693

count_loc $BRANCH

# NOTE (Nick)
#
# We can't really use this data right now. It's useful for Brian Tol's model,
# but that model depends on having total openair hours, which we don't
# have for the starter kit as a whole. I'll leave this snippet here in
# case we find a way to use it in the future.
stat_output=$(gitstats)
FILES_CHANGED=$(echo $stat_output | cut -d' ' -f1)
LINES_ADDED=$(echo $stat_output | cut -d' ' -f2)
LINES_DELETED=$(echo $stat_output | cut -d' ' -f3)

# Python script will compute the estimated replacement cost for each reusable component.
# For now, it only uses the COCOMO model. In the future, we might also compute
# using Brian Tol's model, if we can resolve the "total hours" problem mentioned
# in the comment above this one.
python $MY_DIR/component_replacement_cost.py \
    $MY_DIR/report_$BRANCH.json \
    $COCOMO_SD_MULTIPLIER
