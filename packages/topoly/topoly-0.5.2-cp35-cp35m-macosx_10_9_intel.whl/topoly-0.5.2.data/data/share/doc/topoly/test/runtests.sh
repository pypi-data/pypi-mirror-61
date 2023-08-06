#!/usr/bin/env bash
# Resolve local directory of the script
SOURCE="${BASH_SOURCE[0]}"
while [ -h "$SOURCE" ]; do # resolve $SOURCE until the file is no longer a symlink
  DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE" # if $SOURCE was a relative symlink, we need to resolve it relative to the path where the symlink file was located
done
DIR="$( cd -P "$( dirname "$SOURCE" )" && pwd )"

BIN_DIR=${DIR}/../../../../bin
export LD_LIBRARY_PATH=${DIR}/../../../../lib:$LD_LIBRARY_PATH
TEST_DIR=/tmp/topopack

echo "---------------------------------------------------------------------"
echo -e "\tTopopack tests and examples\n"
echo -e "\tversion: $($BIN_DIR/knotnet --version)\n"
echo "---------------------------------------------------------------------"

mkdir -p $TEST_DIR
# run test knotnet
IN_FILE="$DIR/knotnet/2efv_A"
OUT_FILE="$TEST_DIR/knotnet_out.txt"
STDOUT_FILE="$TEST_DIR/knotnet_stdout.txt"

# knotnet_2efv_test
${BIN_DIR}/knotnet ${IN_FILE} -c 2 -t 2 --try 100 -o ${OUT_FILE}> ${STDOUT_FILE}
# compare results
bash ${DIR}/knotnet/compare_output.sh ${DIR}/knotnet/result/KNOTS_2efv_A ${OUT_FILE} && echo 'Knotnet - PASSED' || echo 'Knotnet - FAILED'


# Python wrapper for knotnet
PY_OUT_FILE="$TEST_DIR/knotnet_py_out.txt"
PY_STDOUT_FILE="$TEST_DIR/knotnet_py_stdout.txt"

bash ${DIR}/knotnet/test_py_knotnet.sh ${DIR}/../../../../lib ${IN_FILE} ${PY_OUT_FILE} > ${PY_STDOUT_FILE}
# compare results
bash ${DIR}/knotnet/compare_output.sh ${DIR}/knotnet/result/KNOTS_2efv_A ${PY_OUT_FILE} && echo 'Python wrapper for knotnet - PASSED' || echo 'Python wrapper for knotnet - FAILED'


# Python wrapper for preprocess
IN_FILE="$DIR/preprocess/t31_numbered_cut.xyz"
PY_OUT_FILE="$TEST_DIR/preprocess_py_out.txt"
PY_STDOUT_FILE="$TEST_DIR/preprocess_py_stdout.txt"

bash ${DIR}/preprocess/test_py_preprocess.sh ${DIR}/../../../../lib  ${IN_FILE} ${PY_OUT_FILE} > ${PY_STDOUT_FILE}
# compare results
#bash ${DIR}/knotnet/compare_output.sh ${DIR}/knotnet/result/KNOTS_2efv_A ${PY_OUT_FILE} && echo 'Python wrapper for knotnet - PASSED' || echo 'Python wrapper for knotnet - FAILED'

# Python wrapper for homfly - Yamada full
IN_DIR="$DIR/data"
PY_STDOUT_FILE="$TEST_DIR/yamada_py_stdout.txt"

bash ${DIR}/homfly/test_py_Yamada_full.sh ${DIR}/../../../../lib  ${IN_DIR} > ${PY_STDOUT_FILE}


# Surfaces (Lassos)
OUT_FILE="$TEST_DIR/lassos.out"

cd ${DIR}/surfaces
bash ${DIR}/surfaces/find_lassos.sh ${BIN_DIR}/surfacesmytraj ${OUT_FILE}
cmp -s ${DIR}/surfaces/good_lassos.out ${OUT_FILE} && echo 'Surfaces - PASSED' || echo 'Surfaces  - FAILED'

# Homfly
OUT_FILE="$TEST_DIR/knots.out"
STDOUT_FILE="$TEST_DIR/knots_stdout.txt"

cd ${DIR}/homfly
bash ${DIR}/homfly/calc_homfly.sh ${BIN_DIR}/homflylink ${BIN_DIR}/lmpoly ${BIN_DIR}/ncuclinks ${OUT_FILE} > ${STDOUT_FILE}
cmp -s ${DIR}/homfly/good_knots.out ${OUT_FILE} && echo 'Homflylink - PASSED' || echo 'Homflylink - FAILED'
