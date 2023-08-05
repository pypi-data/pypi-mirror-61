#!/usr/bin/env bash
SURF_EXE=$1
OUT_FILE=$2
i=0
echo "" > $OUT_FILE

for file in ../data/lasso_*.xyz
do
	echo 't 0' | cat - $file > tmp.txt
	#$SURF_EXE tmp.txt 1 30 -o 0 -n -traj 1  #nowa wersja testu, jesli bedzie uzywany nowy program surfaces
        $SURF_EXE tmp.txt 1 30 -o   0 -n --traj -p 1
	sed -e "s/^/$i /" traj_tmp_1_30.txt >> $OUT_FILE
        i=$((i+1))
done
rm tmp.txt traj_tmp_1_30.txt
