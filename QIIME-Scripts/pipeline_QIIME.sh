### process raw reads to generate OTUs 
QC_OTU-picking.sh 

### format general fasta
python generaldb_to_QIIMEdb.py sh_general_release_31.01.2016.fasta
# outputs: 
sh_general_release_31.01.2016__QIIME.fasta
sh_general_release_31.01.2016__QIIME_taxonomy.txt

### assign taxonomy
parallel_assign_taxonomy_rdp.py -i /path_to_files/peay_otus_sampled.fasta -t /path_to_files/sh_general_release_31.01.2016__QIIME_taxonomy.txt -r /path_to_files/sh_general_release_31.01.2016__QIIME.fasta -O 6 -c 0.5 --rdp_max_memory 12000 -o peay_taxonomy_qiime

### post-assignment filtering
### standardize taxonomy table format
python filter_QIIME.py peay_taxonomy_qiime.txt peay_taxonomy_qiime__final.txt




