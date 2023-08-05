#!/usr/bin/env bash
# Resolve local directory of the script
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

###
BUILD_DIR=$1
INFILE=$2
# This is required since the knotnet library and the python extension are not installed on the system
export PYTHONPATH=$1:$PYTHONPATH
python3 $DIR/test_Yamada_full.py $2
