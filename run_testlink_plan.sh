#!/bin/bash

function check_exit()
{
    if [[ $1 != 0 ]]; then
        exit 1
    fi
}

source params.env
check_exit $?
find . -name "*.json" -exec rm {} \;

python3 get-testplan-info.py
check_exit $?
python3 lava-job-builder.py --user="$JENKINS_USER" --token="$JENKINS_TOKEN" --nfsrootfs="$ROOTFS" --kernel="$KERNEL" --ramdisk="$RAMDISK" --output="output"
check_exit $?
cat output/104* | python3 lava-job-submitter.py --user="$JENKINS_USER" --host="validation.deepin.io" --token="$JENKINS_TOKEN"
check_exit $?
python3 upload-result.py
check_exit $?
