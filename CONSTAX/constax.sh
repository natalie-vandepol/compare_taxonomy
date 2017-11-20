#!/bin/bash

echo "################################################################"
echo "###############*** This is CONSTAX v.1 ***######################"
echo "#                                                              #"
echo "#                     MIT License                              #"
echo "#                 Copyright (C) 2017                           #"
echo "#         Natalie Vandepol, Kristi Gdanetz,                    #"
echo "#     Gian Maria Niccolo' Benucci, Gregory Bonito              #"
echo "#                                                              #"
echo "#      https://github.com/natalie-vandepol/compare_taxonomy    #"
echo "################################################################"


# Import all variables defined in config file
source /path-to-folder/CONSTAX/config

# Execute the python script, passing as the first argument the value of the variable ref_database declared in the config file
python scripts/FormatRefDB.py DB/$ref_database

base=${ref_database%.fasta}

mkdir taxonomy_assignments
mkdir training_files
mkdir outputs

echo "__________________________________________________________________________"
echo "Training UTAX Classifier"

./usearch8 -utax_train DB/${base}__UTAX.fasta -report training_files/utax_db_report.txt -taxconfsout training_files/utax.tc -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log training_files/utax_train.log -report training_files/utax_report.txt

./usearch8 -makeudb_utax DB/${base}__UTAX.fasta -taxconfsin training_files/utax.tc -output training_files/utax.db -log training_files/make_udb.log -report training_files/utax_report.txt

./usearch8 -utax otus/$otu_file -db training_files/utax.db -strand both -utaxout taxonomy_assignments/otu_taxonomy.utax -utax_cutoff $conf -threads 6

echo "__________________________________________________________________________"
echo "Training RDP Classifier"

# -Xmx set to memory GB you want to use

java -Xmx10g -jar /RDPTools/classifier.jar train -o training_files -s DB/${base}__RDP_trained.fasta -t DB/${base}__RDP_taxonomy_trained.txt

cp /RDPTools/mytrained/rRNAClassifier.properties training_files/.

java -Xmx10g -jar /RDPTools/classifier.jar classify --conf $conf --format allrank --train_propfile training_files/rRNAClassifier.properties -o taxonomy_assignments/otu_taxonomy.rdp otus/$otu_file

echo "__________________________________________________________________________"
echo "Training SINTAX Classifier"

./usearch10 -makeudb_sintax DB/${base}__UTAX.fasta -output training_files/sintax.db

./usearch10 -sintax otus/$otu_file -db training_files/sintax.db -tabbedout taxonomy_assignments/otu_taxonomy.sintax -strand both -sintax_cutoff $conf

echo "__________________________________________________________________________"
echo "Creating Consensus Taxonomy"

python scripts/CombineTaxonomy.py $conf

# plot graphs in R
Rscript R/ComparisonBars.R








