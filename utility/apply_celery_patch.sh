#!/bin/bash
# manual patching of celery beat module

# should be run with the virtualenv activated

# the specific file location is needed for python patch module
# the file should be placed into the venv directory.

PATCH_DIR="../requirements"

if [ -z $1 ]
then
    PATCH_APPLYING_DIR_RELATIVE_PATH="../../venv"
else
    PATCH_APPLYING_DIR_RELATIVE_PATH=$1
fi

cd $PATCH_DIR
cp celery_beat_tick.patch $PATCH_APPLYING_DIR_RELATIVE_PATH
cd $PATCH_APPLYING_DIR_RELATIVE_PATH
python -m patch -v --debug celery_beat_tick.patch
