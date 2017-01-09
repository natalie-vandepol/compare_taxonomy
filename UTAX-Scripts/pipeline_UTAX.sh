### process raw reads to generate OTUs 
QC_OTU-picking.sh 

### format general fasta & create UTAX-DB training files
python generaldb_to_UTAXdb.py sh_general_release_31.01.2016.fasta
# outputs:
sh_general_release_31.01.2016__UTAX.fasta

### train the classifier
usearch8 -utax_train /path_to_files/unite_ref_db/sh_general_release_31.01.2016__UTAX__filtered.fasta  -report /path_to_files/unite_ref_db/utax_db_31.01.2016_report.txt -taxconfsout /path_to_files/unite_ref_db/utax.31.01.2016.tc -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log /path_to_files/unite_ref_db/utax_train.log -report /path_to_files/unite_ref_db/utax_report.txt

usearch8 -makeudb_utax /path_to_files/unite_ref_db/sh_general_release_31.01.2016__UTAX.fasta -taxconfsin /path_to_files/unite_ref_db/utax.31.01.2016.tc -output /path_to_files/unite_ref_db/utax_db_31.01.2016.plus_plant.db -log /path_to_files/unite_ref_db/make_udb.log -report /path_to_files/unite_ref_db/utax_report.txt

### assign taxonomy
usearch8 -utax /path_to_files/peay_otus_sampled.fasta -db /path_to_files/unite_ref_db/utax_db_31.01.2016.db -strand both -utaxout /path_to_files/peay_taxonomy_utax.txt -otutabout /path_to_files/peay_otu_utax.txt -rdpout /path_to_files/peay.rdpoutfile.utax.txt -utax_cutoff 0.8 -strand plus -threads 6

### post-assignment filtering
### standardize taxonomy table format
python filter_UTAX.py peay_taxonomy_utax.txt peay_taxonomy_utax__final.txt

