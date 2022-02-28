#!/bin/bash

OPENAIR_HOURS=470
FIRST_COMMIT=882409b
LAST_COMMIT=5d173b5
REPO_PATH=$HOME/src/ego_firmware

./sd_multiplier.sh  \
    $REPO_PATH \
    $OPENAIR_HOURS \
    $FIRST_COMMIT \
    $LAST_COMMIT
