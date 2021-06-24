#!/bin/bash

# /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_many_scripts_VVCPartDatabase.sh /home/cleonard/dev/TpgVvcPartDatabase/ /home/cleonard/dev/stage/results/scripts_results/Features/test_seed_200gen/ /home/cleonard/dev/stage/scripts/VVCPartDatabase/launch_1train_TPG.sh BIG_training TPGVVCPartDatabase_featuresEnv 1 5

# Finish all prob study
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_all-prob.sh AllProbProg 1 5

# echo ' '
# echo ' '
# echo ' '
# echo ' '
# echo ' '
# echo ' '

# Finish 10000 nbRoots study N°1 ...

# Finish 5000 7000 10000 nbRoots study
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_1.sh nbRoots 1 5

# echo ' '
# echo ' '
# echo ' '
# echo ' '
# echo ' '
# echo ' '

# Launch parallel study for nbRoot and ratioDeletedRoots
/home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_double_study.sh LotOfRoots 1 1

echo ' '
echo ' '
echo ' '
echo ' '
echo ' '
echo ' '

# Finish last training study 2 roots
# /home/cleonard/dev/stage/scripts/test.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/Roots2/ Roots 2

# echo ' '
# echo ' '
# echo ' '
# echo ' '
# echo ' '
# echo ' '

# Launch pMutateSwap study
# /home/cleonard/dev/stage/scripts/launch_many_scripts.sh /home/cleonard/dev/gegelati-apps/mnist/ /home/cleonard/dev/stage/results/scripts_results/params_study/onMNIST/ /home/cleonard/dev/stage/scripts/paramStudy/launch_MNIST_diff-Param_2.sh pMutateSwap 1 5

# echo ' '
# echo ' '
# echo ' '
# echo ' '
# echo ' '
# echo ' '
