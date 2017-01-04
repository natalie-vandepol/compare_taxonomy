### process raw reads to generate OTUs 
1_QC_OTU-picking.sh 

### format general fasta
python 2_generaldb_to_RDP.py /peay/unite_ref_db/sh_general_release_31.01.2016.fasta
# outputs:
sh_general_release_31.01.2016__RDP_taxonomy.txt
sh_general_release_31.01.2016__RDP.fasta

### create RDP-Classifier training files
# train taxonomy
python 3_lineage2taxonomyTrain.py sh_general_release_31.01.2016__RDP_taxonomy.txt > sh_general_release_31.01.2016__RDP_taxonomy_trained.txt
# train fasta 
python 4_fasta_addFullLineage.py sh_general_release_31.01.2016__RDP_taxonomy.txt  sh_general_release_31.01.2016__RDP.fasta > sh_general_release_31.01.2016__RDP_trained.fasta

### train the Classifier
java -Xmx8g -jar /mnt/research/rdp/public/RDPTools/classifier.jar train -o /peay/RDP_trained/ -s /peay/sh_general_release_31.01.2016__RDP_trained.fasta -t /peay/sh_general_release_31.01.2016__RDP_taxonomy_trained.txt 
# download sample files from RDP GitHub page
cp samplefiles/rRNAClassifier.properties RDP_trained/

### assign taxonomy
java -Xmx8g -jar /mnt/research/rdp/public/RDPTools/classifier.jar classify --conf 0.5 --format allrank --train_propfile /peay/RDP_trained/rRNAClassifier.properties --hier_outfile /peay/peay_otu_rdp.txt -o /peay/peay_taxonomy_rdp.txt /peay/peay_otus_sampled.fasta

### post-assignment filtering
### standardize taxonomy table format
python 7_filter_rdp.py peay_taxonomy_rdp.txt peay_taxonomy_rdp__final.txt

### merge all three taxonomy files
python compare_taxonomies_012.py peay_taxonomy_rdp__final.txt peay_taxonomy_qiime__final.txt peay_taxonomy_utax__final.txt


