## get quality statistics
fastqc ./*_R1_001.fastq
fastqc ./*_R2_001.fastq

## merge forward and reverse, change labels
usearch -fastq_mergepairs *_R1.fq -relabel @ -tabbedout merged_tabbed.txt -report merged_summary.txt -fastqout merged.fastq

## subsample reads
#download from https://github.com/lh3/seqtk
seqtk sample -s100 merged.fastq 500000 > sub.merged.fastq

## quality filter
usearch -fastq_eestats2 sub.merged.fastq -output merged.filtered.eestats2.txt -length_cutoffs 100,400,10
usearch -fastq_filter sub.merged.fastq -fastq_minlen 150 -fastq_maxee 0.5 -fastaout merged.filtered.fasta -fastaout_discarded merged.no_filter.fasta -fastqout merged.filtered.fastq
usearch -fastq_eestats2 merged.filtered.fastq -output merged.filtered.eestats2.txt -length_cutoffs 150,400,10

## trim cleaned reads - ITS1 length = ?, Toju ITS2 length = 380
#usearch -fastq_filter merged.filtered.fastq -fastaout sub.filter.fasta -fastq_truncqual 10 -fastq_minlen 180
usearch -fastx_truncate merged.filtered.fastq -padlen 250 -trunclen 250 -fastaout cleaned.fasta

## find unique/representative sequences
usearch -derep_fulllength cleaned.fasta -sizeout -fastaout derep.fa -threads 4

## cluster OTUs, remove singletons, de novo chimera check
usearch -cluster_otus derep.fa -minsize 2 -sizein -sizeout -relabel OTU_ -otus derep.otus.fa -uparseout reads.derep.otus.txt

## reference-based chimera check
#use this version uchime_sh_refs_dynamic_develop_985_01.01.2016.ITS2.fasta
#use this version uchime_sh_refs_dynamic_develop_985_01.01.2016.ITS1.fasta
usearch -uchime_ref derep.otus.fa -db /media/Data/UNITE_db/uchime_sh_refs_dynamic_develop_985_01.01.2016.ITS2.fasta -nonchimeras otus.no_chimera.fasta -uchimeout reads.derep.otus.no_chimera.uchime -strand plus -sizein -sizeout

## map reads back to OTUs and create the otu_tab.txt for phyloseq
usearch -usearch_global merged.filtered.fasta -db otus.no_chimera.fasta -strand plus -id 0.97 -top_hit_only -otutabout otu_table.txt -sizein -sizeout

## TAXONOMY ASSIGNMENT ##

## Assign taxonomy using UTAX
cd /mnt/research/rdp/public/thirdParty

./usearch8.1.1831_i86linux64 -utax_train /mnt/home/gdanetzk/unite_ref_db/sh_general_release_31.01.2016__UTAX__filtered.fasta  -report /mnt/home/gdanetzk/unite_ref_db/utax_db_31.01.2016_report.txt -taxconfsout /mnt/home/gdanetzk/unite_ref_db/utax.31.01.2016.tc -utax_splitlevels NVpcofgs -utax_trainlevels kpcofgs -log /mnt/home/gdanetzk/unite_ref_db/utax_train.log -report /mnt/home/gdanetzk/unite_ref_db/utax_report.txt

./usearch8.1.1831_i86linux64 -makeudb_utax /mnt/home/gdanetzk/unite_ref_db/sh_general_release_31.01.2016__UTAX.plus_plant.fasta -taxconfsin /mnt/home/gdanetzk/unite_ref_db/utax.31.01.2016.tc -output /mnt/home/gdanetzk/unite_ref_db/utax_db_31.01.2016.plus_plant.db -log /mnt/home/gdanetzk/unite_ref_db/make_udb.log -report /mnt/home/gdanetzk/unite_ref_db/utax_report.txt

./usearch8.1.1831_i86linux64 -utax /mnt/home/gdanetzk/RDP-UTAX/peay_otus_sampled.fasta -db /mnt/home/gdanetzk/unite_ref_db/utax_db_31.01.2016.db -strand both -utaxout /mnt/home/gdanetzk/RDP-UTAX/assigned_taxonomy.peay.utax -otutabout /mnt/home/gdanetzk/RDP-UTAX/taxonomy.otu_tab.peay.utax -rdpout /mnt/home/gdanetzk/RDP-UTAX/rdpoutfile.peay.utax.txt -utax_cutoff 0.8 -strand plus -threads 6

## Assign taxonomy using RDP stand alone
java -Xmx5g -jar /mnt/research/rdp/public/RDPTools/classifier.jar classify --conf 0.5 --format allrank --train_propfile /mnt/home/gdanetzk/RDP-UTAX/mytrained/rRNAClassifier.properties --hier_outfile /mnt/home/gdanetzk/RDP-UTAX/peay.rdp_out_tab.txt -o /mnt/home/gdanetzk/RDP-UTAX/rdp_peay_assigned.taxonomy.txt /mnt/home/gdanetzk/RDP-UTAX/peay_otus_sampled.fasta

## Assign taxonomy using RDP inside Qiime 1.9
parallel_assign_taxonomy_rdp.py -i ITS_otus_numbered.fna -t “/home/mycolab/Databases/taxonomy_UNITE_SH_qiime_release_30.12.2014/sh_taxonomy_qiime_ver6_dynamic_30.12.2014.txt” -r “/home/mycolab/Databases/taxonomy_UNITE_SH_qiime_release_30.12.2014/sh_refs_qiime_ver6_dynamic_30.12.2014.fasta” -O 4 --rdp_max_memory 16000 -o taxonomy_assigned_RDP



# cat /mnt/home/gdanetzk/all_crops/host_plants.fasta /mnt/home/gdanetzk/unite_ref_db/sh_general_release_31.01.2016__UTAX__filtered.fasta > /mnt/home/gdanetzk/unite_ref_db/sh_general_release_31.01.2016__UTAX__filtered.plus_plant.fasta
