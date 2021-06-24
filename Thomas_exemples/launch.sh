#!/bin/bash

if [ "$#" -ne 2 ]; then
echo "parametres: dossier_res numThr"
echo "Illegal number of parameters"
    exit
fi

jobs=`ls $1/job`
numthr=$2
numcores=0
fichier_cores=cores
#rm $fichier_cores
touch $fichier_cores

maFonction()
{

sh $1/job/$job

numcores=`cat $fichier_cores`
numcores=`expr $numcores - $numthr`
echo $numcores > $fichier_cores
echo "end $job $numcores"
}

for job in $jobs; do
	numcores=`cat $fichier_cores`
	while [[ "$numcores" -gt "17" ]]; do
		sleep 1
		numcores=`cat $fichier_cores`
		#echo $numcores
	done

	echo "Cores Launched "$numcores
	numcores=`expr $numcores + $numthr`
	echo $numcores > $fichier_cores

 	maFonction $1 &

done
