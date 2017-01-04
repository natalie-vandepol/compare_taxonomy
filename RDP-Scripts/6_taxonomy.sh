## Taxonomy Assignments

## Assign taxonomy using UTAX
./usearch8.1.1831_i86linux64 -utax /path_to_files/peay_otus_sampled.fasta -db /path_to_files/unite_ref_db/utax_db_31.01.2016.db -strand both -utaxout /path_to_files/assigned_taxonomy.peay.utax -otutabout /path_to_files/taxonomy.otu_tab.peay.utax -rdpout /path_to_files/rdpoutfile.peay.utax.txt -utax_cutoff 0.8 -strand plus -threads 6

## Assign taxonomy using RDP stand alone
java -Xmx5g -jar /mnt/research/rdp/public/RDPTools/classifier.jar classify --conf 0.5 --format allrank --train_propfile /path_to_files/mytrained/rRNAClassifier.properties --hier_outfile /path_to_files/peay.rdp_out_tab.txt -o /path_to_files/rdp_peay_assigned.taxonomy.txt /path_to_files/peay_otus_sampled.fasta

## Assign taxonomy using RDP inside Qiime 1.9
parallel_assign_taxonomy_rdp.py -i /path_to_files/peay_otus_sampled.fasta -t /path_to_files/sh_general_release_31.01.2016__QIIME_taxonomy.txt -r /path_to_files/sh_general_release_31.01.2016__QIIME.fasta -O 4 --rdp_max_memory 16000 -c 0.5 -o /path_to_files/taxonomy_assigned_qiime/
