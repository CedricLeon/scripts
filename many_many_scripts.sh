#!/bin/bash

# TPGVVCPartDatabase every trainings for every databases + inference and data storage
echo "Start BIG Training on 50%_dtb"
cd /home/cleonard/dev/TpgVvcPartDatabase2/build
source /home/cleonard/dev/stage/scripts/python/envVirDTB/bin/activate
python3.6 /home/cleonard/dev/stage/scripts/TpgVVCPartDatabase/launch_all_trainings.py > /home/cleonard/dev/stage/logs_all_trainings_BIG.logs

echo "  Compute inference scores"
cd /home/cleonard/dev/TpgVvcPartDatabase/build
python3.6 /home/cleonard/dev/stage/scripts/TpgVVCPartDatabase/evaluate_all_inference.py /home/cleonard/dev/stage/results/scripts_results/BinaryFeatures/cascade-full/TaillesDif/ult-script2_BIG/ > /home/cleonard/dev/stage/logs_all_inference_BIG.logs

echo "Change params.json"
cp /home/cleonard/dev/TpgVvcPartDatabase2/params.json ../BIG_params_TpgVvcPartDatabase2.json
rm /home/cleonard/dev/TpgVvcPartDatabase2/params.json
cp /home/cleonard/dev/TpgVVCPartDatabase_params.json /home/cleonard/dev/TpgVvcPartDatabase2/params.json

echo "Start Training on Balanced_dtb"
cd /home/cleonard/dev/TpgVvcPartDatabase2/build
python3.6 /home/cleonard/dev/stage/scripts/python/test.py > /home/cleonard/dev/stage/logs_all_trainings_Balanced.logs

echo "  Compute inference scores"
cd /home/cleonard/dev/TpgVvcPartDatabase/build
python3.6 /home/cleonard/dev/stage/scripts/TpgVVCPartDatabase/evaluate_all_inference.py /home/cleonard/dev/stage/results/scripts_results/BinaryFeatures/cascade-full/TaillesDif/ult-script3_BalancedDTB/ > /home/cleonard/dev/stage/logs_all_inference_Balanced.logs


# echo "Launch AllProbProg with \"forceProgramBehaviorChangeOnMutation\": false 1 5"
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/mnist2/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_all-prob.sh AllProbProgUnforce 1 5

# echo ' '
# echo ' '

# echo "Launch double study Roots 4k roots 3 3 "
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/mnist2/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/launch_MNIST_diff-Param_double_study.sh 4kRoots 3 3

# echo ' '
# echo ' '

# # Launch parallel study for nbRoot and ratioDeletedRoots
# /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_double_study.sh /home/cleonard/dev/mnist2/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/10kRoots1/ 4kRoots 3

# echo ' '
# echo ' '

# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/test.sh LotOfRootsFollowing 2 3

# echo ' '
# echo ' '

# /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_NP-Train_diff-Actions_personnalized.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/BinaryFeatures/test5_HORI-VERT_bal-binary_sink_32x32_BIG/ TPGVVCPartDatabase_binaryFeaturesEnv

# echo ' '
# echo ' '

# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/mnist2/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/test2.sh 360Roots 1 3

# echo ' '
# echo ' '

# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_double_study.sh 10kRoots 2 3

# echo ' '
# echo ' '

# /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_many_scripts_VVCPartDatabase.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/Features/test_seed_200gen/ /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_1train_TPG.sh BIG_training TPGVVCPartDatabase_featuresEnv 1 5

# Finish all prob study
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_all-prob.sh AllProbProg 1 5

# echo ' '
# echo ' '

# Finish 5000 7000 10000 nbRoots study
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_1.sh nbRoots 1 5

# echo ' '
# echo ' '

# Launch parallel study for nbRoot and ratioDeletedRoots
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_double_study.sh LotOfRoots 1 1

# echo ' '
# echo ' '

# Finish last training study 2 roots
# /home/cleonard/dev/stage/scripts/test.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots2/ Roots 2

# echo ' '
# echo ' '

# Launch pMutateSwap study
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_2.sh pMutateSwap 1 5

# echo ' '
# echo ' '
