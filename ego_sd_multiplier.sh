#!/bin/bash

OPENAIR_HOURS=470
FIRST_COMMIT=882409b
LAST_COMMIT=5d173b5
REPO_PATH=$HOME/src/ego_firmware
IGNORE_DIR="(build|data|third-party|html|node_modules|proto-c|wasm_runner\/examples|emsdk|docs\/assets)"
IGNORE_FILE="(package-lock.json)"

./sd_multiplier.sh  \
    $REPO_PATH \
    $OPENAIR_HOURS \
    $FIRST_COMMIT \
    $LAST_COMMIT \
    $IGNORE_DIR \
    $IGNORE_FILE
