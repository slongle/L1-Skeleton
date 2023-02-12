#!/bin/bash
set -e

if [ $# -ne 3 ]; then
  echo "Usage: $0 <ply_path> <skel_path> <json_config_path>"
  exit 1
fi


SCRIPTPATH="$( cd "$(dirname "$0")" ; pwd -P )"
# delete if exists
rm -rf $SCRIPTPATH/tmp
mkdir $SCRIPTPATH/tmp
# copy ply and json_config to tmp
cp $1 $SCRIPTPATH/tmp/pointcloud.ply
cp $3 $SCRIPTPATH/tmp/config.json

docker run --rm \
    -v $SCRIPTPATH/tmp/:/input/ \
    pointcloudl1:latest \
    /input/pointcloud.ply /input/skeleton.skel /input/config.json

cp $SCRIPTPATH/tmp/skeleton.skel $2
