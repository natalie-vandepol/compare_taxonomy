

### Train Classifiers

# UTAX
cd /mnt/research/rdp/public/thirdParty

./usearch8.1.1831_i86linux64 -utax_train /mnt/home/gdanetzk/unite_ref_db/sh_general_release_31.01.2016__UTAX__filtered.fasta -taxconfsout /mnt/home/gdanetzk/unite_ref_db/utax.31.01.2016.tc_2 -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log /mnt/home/gdanetzk/unite_ref_db/utax_train.log_2 -report /mnt/home/gdanetzk/unite_ref_db/utax_report.txt_2

./usearch8.1.1831_i86linux64 -makeudb_utax /mnt/home/gdanetzk/unite_ref_db/sh_general_release_31.01.2016__UTAX.fasta -taxconfsin /mnt/home/gdanetzk/unite_ref_db/utax.31.01.2016.tc -output /mnt/home/gdanetzk/unite_ref_db/utax_db_31.01.2016.db -log /mnt/home/gdanetzk/unite_ref_db/make_udb.log -report /mnt/home/gdanetzk/unite_ref_db/utax_report.txt


### RDP
java -Xmx5g -jar /mnt/research/rdp/public/RDPTools/classifier.jar train -o /mnt/home/gdanetzk/RDP-UTAX/mytrained -s /mnt/home/gdanetzk/RDP-UTAX/train.fasta -t /mnt/home/gdanetzk/RDP-UTAX/train.txt 

### QIIME

