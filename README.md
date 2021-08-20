# Scripts

## What's in there ?

This git repository as only one goal: backup every different scripts I have made so far.

Majority of those scripts have been made during my internship in the **VAADER** team of **IETR** for my research on **Tangled Program Graphs** and **Versatile Video Coding**, so they are very very (very) specific.

All these scripts are in bash or in python which make them easily usable and pretty useful if your interest meets mine. Still if you are already a great script author don't stay here too much, your eyes will bleed. 

#### Usage

The great majority of those scrips have a *usage* section at the beginning specifying how to use them. Whatever, since it's a lot of copy-paste this section may not be up-to-date.

## Scripts Families

#### paramStudy directory

Up-to-date this directory contains scripts I used to launch trainings on the **MNIST** application of the [GEGELATI-apps](https://github.com/gegelati/gegelati-apps) repository.

**/!\ CARE**, you can't run these scripts with the original code of the repository, I have made a bunch of  small modifications on my own [fork](https://github.com/CedricLeon/gegelati-apps). You should also check the code since it may be ugly with absolute paths ... ¯\_(ツ)_/¯

There is 4 different scripts very similar, please read their usage section to fully understand what you can do with them.

#### python directory

This directory mainly contains scripts used to balance databases, launch trainings, print data about my [TPGVVCPartDatabase](https://github.com/CedricLeon/TpgVvcPartDatabase) project.

About the very useful scripts I could cite:

- `full_DTB_management.py` which unzip, count, balance and create personalized datasets for A. Tissier CNN data
- `plot_3D-curve_fromCSV.py` which plot nice 2D and 3D curves (you can use the data stored in the *python/printData/3D-curve_example directory*) 
- `print_TPGAcesses.py` which plot a matrix with colorscale in function of TPG information found in the out_best_stats.md of GEGELATI

#### TpgVVCPartDatabase directory

This folder contains scripts I used to launch the different TPGVVCPartDatabase application executables.

About the very useful scripts I could cite:

- `launch_all_trainings.py` which ... launch all trainings for every size database (**CARE** only tested with the TPGVVCPartDatabase_binaryFeaturesEnv executable)
- `evaluate_all_inference.py` which should be paired with `launch_all_trainings.py` (**CARE** only works with the TPGVVCPartDatabase_binaryFeaturesEnv executable, could easily be generalized but whatever you will have to personalize your inference TPGs structure inside the TPGVVCPartDatabase code)

#### test files

Test files are pretty much garbage but I often used them to store different versions of the same script without duplicate it and then launching them all with `launch_many_scripts.sh`.

#### `many_scripts` files

These bash scripts were like my TODO_List scripts especially `many_many_scripts.sh`. If you exactly know what you are doing don't check them but if you want some interesting example of scripts usage in bash you will find them in there.





## Python Setup (for noobs like me)

A whole directory is full of python scripts, if you need to run them you may find interesting commands in this section.


#### Launch

````bash
python3.6 name_of_the_script.py
````

#### Install package

````bash
python -m pip install name_of_the_package
````


### Virtualenv usage

I recommend to create a virtual environment in order to use these python scripts :
To create a virtual python environment (install modules, etc.)

[Tuto](https://openclassrooms.com/fr/courses/4425111-perfectionnez-vous-en-python/4463278-travaillez-dans-un-environnement-virtuel)

#### Install

````bash
sudo apt-get install virtualenv
````

#### Create

````bash
virtualenv -p python3 envVirDTB
````

#### Activate

````bash
source envVirDTB/bin/activate
````

#### Desactivate

````bash
deactivate
````

#### Delete

````bash
rm -rf enVirDTB
````







