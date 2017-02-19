#!/bin/bash

PATCH_DIR="../requirements"
PATCH_APPLYING_DIR_RELATIVE_PATH="../../"

cd $PATCH_DIR
cp celery_beat_tick.patch $PATCH_APPLYING_DIR_RELATIVE_PATH
cd $PATCH_APPLYING_DIR_RELATIVE_PATH
python -m patch -v --debug celery_beat_tick.patch
