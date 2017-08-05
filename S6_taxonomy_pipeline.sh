############################################################
#  Taxonomy Assignment 
#  Pipeline for Gdanetz, VandePol, Bonito, Benucci
#  Updated May 8, 2017
############################################################

## Assign taxonomy using UTAX
cd /path_to_files/RDP_installation/

usearch8 /path_to_files/unite_ref_db/sh_general_release_31.01.2016__UTAX__filtered.fa  -report /path_to_files/unite_ref_db/utax_db_31.01.2016_report.txt -taxconfsout /path_to_files/unite_ref_db/utax.31.01.2016.tc -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log /path_to_files/unite_ref_db/utax_train.log -report /path_to_files/unite_ref_db/utax_report.txt

usearch8 /path_to_files/unite_ref_db/sh_general_release_31.01.2016__UTAX.fa -taxconfsin /path_to_files/unite_ref_db/utax.31.01.2016.tc -output /path_to_files/unite_ref_db/utax_db_31.01.2016.db -log /path_to_files/unite_ref_db/make_udb.log -report /path_to_files/unite_ref_db/utax_report.txt

usearch8 -utax /path_to_files/RDP-UTAX/OTU_500.fa -db /path_to_files/unite_ref_db/utax_db_31.01.2016.db -strand both -utaxout /path_to_files/RDP-UTAX/OTU_500.utax -utax_cutoff 0.8 -threads 6

## Assign taxonomy using RDP stand alone
java -Xmx5g -jar /mnt/research/rdp/public/RDPTools/classifier.jar classify --conf 0.8 --format allrank --train_propfile /path_to_files/RDP-UTAX/mytrained/rRNAClassifier.properties -o /path_to_files/OTU_500.rdp /path_to_files/OTU_500.fa

## Assign taxonomy with SINTAX
cd /path_to_files/usearch9.2/
usearch9 -sintax /path_to_files/OTU_500.fa -db sintax.31.01.2016.udb -tabbedout /path_to_files/OTU_500.sintax -strand both -sintax_cutoff 0.8