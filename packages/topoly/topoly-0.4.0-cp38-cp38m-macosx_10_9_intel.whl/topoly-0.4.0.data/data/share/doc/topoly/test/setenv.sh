#!/usr/bin/env bash
# Resolve local directory of the script
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

TOPOLY_DIR=$DIR/..

cp $TOPOLY_DIR/build/dist-packages/topoly/* $TOPOLY_DIR/topoly/
export PYTHONPATH=$TOPOLY_DIR
export LD_LIBRARY_PATH=$TOPOLY_DIR/build
export DYLD_LIBRARY_PATH=$TOPOLY_DIR/build
