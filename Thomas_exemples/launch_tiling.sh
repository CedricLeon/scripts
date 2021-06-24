#!/bin/bash

nframes=$1
bt=$2
classif=$3
echo "num parameters "$#
if [ "$#" -ne 3 ]; then
echo "parametres: nframes unif tolerance"    
echo "Illegal number of parameters"
    exit
fi

cp cfg_templates/VTM62_RA_template.cfg cfg_templates/VTM_RA_template.cfg
rm cores
 
#unif=$2
#tol=$3

#unif=0
#tol=0
#numthr_list="1" 
#for numthr in $numthr_list; do
#	out_dir=results_VTM62_Tiling_dynamic_unif${unif}_tol${tol}_numthr${numthr}_Fr${nframes}
#  echo "./configure --disable-class="SDRB"  --dst-dir=${out_dir} --numThr=${numthr} --tolerance=${tol} --unif=${unif} --disable-configuration=AI --less=${nframes}"
#	./configure --disable-class="SDRB"  --dst-dir=${out_dir} --numThr=${numthr} --tolerance=${tol} --unif=${unif} --disable-configuration=AI --less=${nframes}
#	sleep 1 
#done
#
#for numthr in $numthr_list; do
#	out_dir=results_VTM62_Tiling_dynamic_unif${unif}_tol${tol}_numthr${numthr}_Fr${nframes}
#	echo "./launch.sh ${out_dir}"
#	./launch.sh ${out_dir} ${numthr}
#	sleep 1 
#done


#unif=1
#tol=0
#numthr_list="4 8 12" 
#for numthr in $numthr_list; do
#	out_dir=results_VTM62_Tiling_dynamic_unif${unif}_tol${tol}_numthr${numthr}_Fr${nframes}
#  echo "./configure --disable-class="SDRB"  --dst-dir=${out_dir} --numThr=${numthr} --tolerance=${tol} --unif=${unif} --disable-configuration=AI --less=${nframes}"
#	./configure --disable-class="SDRB"  --dst-dir=${out_dir} --numThr=${numthr} --tolerance=${tol} --unif=${unif} --disable-configuration=AI --less=${nframes}
#	sleep 1 
#done
#
#for numthr in $numthr_list; do
#	out_dir=results_VTM62_Tiling_dynamic_unif${unif}_tol${tol}_numthr${numthr}_Fr${nframes}
#	echo "./launch.sh ${out_dir}"
#	./launch.sh ${out_dir} ${numthr}
#	sleep 1 
#done
#


unif=0
numthr_list="4 8 12" 
for numthr in $numthr_list; do

	tolerances="10000"
	for tol in $tolerances; do
		out_dir=results_VTM62_Tiling_dynamic_unif${unif}_tol${tol}_numthr${numthr}_Fr${nframes}
		echo "./configure --disable-class="SDRB"  --dst-dir=${out_dir} --numThr=${numthr} --tolerance=${tol} --unif=${unif} --disable-configuration=AI --less=${nframes}"
		./configure --disable-class="SDRB" --dst-dir=${out_dir} --numThr=${numthr} --tolerance=${tol} --unif=${unif} --disable-configuration=AI --less=${nframes}
		sleep 1 
	done

	for tol in $tolerances; do
	#for numthr in $numthr_list; do
		out_dir=results_VTM62_Tiling_dynamic_unif${unif}_tol${tol}_numthr${numthr}_Fr${nframes}
		echo "./launch.sh ${out_dir}"
		./launch.sh ${out_dir} ${numthr}
		sleep 1 
	done
done

