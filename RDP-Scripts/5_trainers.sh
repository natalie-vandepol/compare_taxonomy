

### Train Classifiers

# UTAX
./usearch8.1.1831_i86linux64 -utax_train /mnt/home/gdanetzk/unite_ref_db/sh_general_release_31.01.2016__UTAX__filtered.fasta  -report /mnt/home/gdanetzk/unite_ref_db/utax_db_31.01.2016_report.txt -taxconfsout /mnt/home/gdanetzk/unite_ref_db/utax.31.01.2016.tc -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log /mnt/home/gdanetzk/unite_ref_db/utax_train.log -report /mnt/home/gdanetzk/unite_ref_db/utax_report.txt

./usearch8.1.1831_i86linux64 -makeudb_utax /mnt/home/gdanetzk/unite_ref_db/sh_general_release_31.01.2016__UTAX.plus_plant.fasta -taxconfsin /mnt/home/gdanetzk/unite_ref_db/utax.31.01.2016.tc -output /mnt/home/gdanetzk/unite_ref_db/utax_db_31.01.2016.plus_plant.db -log /mnt/home/gdanetzk/unite_ref_db/make_udb.log -report /mnt/home/gdanetzk/unite_ref_db/utax_report.txt


### RDP
java -Xmx5g -jar /mnt/research/rdp/public/RDPTools/classifier.jar train -o /mnt/home/gdanetzk/RDP-UTAX/RDP_trained/ -s /mnt/home/gdanetzk/RDP-UTAX/sh_general_release_31.01.2016__RDP_trained.fasta -t /mnt/home/gdanetzk/RDP-UTAX/sh_general_release_31.01.2016__RDP_taxonomy_trained.txt 

### QIIME

