#!/bin/bash

OPENAIR_HOURS=470
FIRST_COMMIT=0184fc9dd123433f56837b87a378cfe5ee1c6507
LAST_COMMIT=70eb3d9f3a5b1e0141b53b6c6785b8f339ab83ab
REPO_PATH=$HOME/src/uvangel_air
IGNORE_DIR="(build|data|third-party|html|node_modules|proto-c|wasm_runner\/examples|emsdk|docs\/assets)"
IGNORE_FILE="(package-lock.json)"

./sd_multiplier.sh  \
    $REPO_PATH \
    $OPENAIR_HOURS \
    $FIRST_COMMIT \
    $LAST_COMMIT \
    $IGNORE_DIR \
    $IGNORE_FILE
