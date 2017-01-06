### process raw reads to generate OTUs 
QC_OTU-picking.sh 

### format general fasta
python generaldb_to_RDP.py /file_to_path/sh_general_release_31.01.2016.fasta
# outputs:
sh_general_release_31.01.2016__RDP_taxonomy.txt
sh_general_release_31.01.2016__RDP.fasta

### create RDP-Classifier training files
# train taxonomy
python lineage2taxonomyTrain.py sh_general_release_31.01.2016__RDP_taxonomy.txt > sh_general_release_31.01.2016__RDP_taxonomy_trained.txt
# train fasta 
python fasta_addFullLineage.py sh_general_release_31.01.2016__RDP_taxonomy.txt  sh_general_release_31.01.2016__RDP.fasta > sh_general_release_31.01.2016__RDP_trained.fasta

### train the Classifier
java -Xmx8g -jar /mnt/research/rdp/public/RDPTools/classifier.jar train -o /file_to_path/RDP_trained/ -s /file_to_path/sh_general_release_31.01.2016__RDP_trained.fasta -t /file_to_path/sh_general_release_31.01.2016__RDP_taxonomy_trained.txt 

# download sample files from RDP GitHub page
# https://github.com/rdpstaff/classifier
cp samplefiles/rRNAClassifier.properties /file_to_path/RDP_trained/

### assign taxonomy
java -Xmx8g -jar /mnt/research/rdp/public/RDPTools/classifier.jar classify --conf 0.5 --format allrank --train_propfile /file_to_path/RDP_trained/rRNAClassifier.properties --hier_outfile /file_to_path/peay_otu_rdp.txt -o /file_to_path/peay_taxonomy_rdp.txt /file_to_path/peay_otus_sampled.fasta

### post-assignment filtering
### standardize taxonomy table format
python filter_RDP.py peay_taxonomy_rdp.txt peay_taxonomy_rdp__final.txt



