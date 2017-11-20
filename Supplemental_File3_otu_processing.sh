############################################################
#  OTU-picking 
#  Pipeline for Gdanetz, Benucci, VandePol, Bonito
#  Updated May 5, 2017
############################################################

## get quality statistics
fastqc ./*_R1_001.fastq
fastqc ./*_R2_001.fastq

## merge forward and reverse, change labels
usearch8 -fastq_mergepairs *_R1.fq -relabel @ -tabbedout merged_tabbed.txt -report merged_summary.txt -fastqout merged.fastq

## subsample reads
#download from https://github.com/lh3/seqtk
seqtk sample -s100 merged.fastq 500000 > sub.merged.fastq

## quality filter
usearch8 -fastq_eestats2 sub.merged.fastq -output merged.pre_filtered.eestats2.txt -length_cutoffs 100,400,10
usearch8 -fastq_filter sub.merged.fastq -fastq_minlen 150 -fastq_maxee 0.5 -fastaout merged.filtered.fa -fastaout_discarded merged.no_filter.fa -fastqout merged.filtered.fastq
usearch8 -fastq_eestats2 merged.filtered.fastq -output merged.post_filtered.eestats2.txt -length_cutoffs 150,400,10

## trim cleaned reads 
usearch8 -fastx_truncate merged.filtered.fastq -padlen 250 -trunclen 250 -fastaout cleaned.fa

## find unique/representative sequences
usearch8 -derep_fulllength cleaned.fa -sizeout -fastaout derep.fa -threads 4

## cluster OTUs, remove singletons, de novo chimera check
usearch8 -cluster_otus derep.fa -minsize 2 -sizein -sizeout -relabel OTU_ -otus derep.otus.fa -uparseout reads.derep.otus.txt

## reference-based chimera check
#use for ITS1 region: uchime_sh_refs_dynamic_develop_985_01.01.2016.ITS1.fasta
#use for ITS2 region: uchime_sh_refs_dynamic_develop_985_01.01.2016.ITS2.fasta
#wget https://unite.ut.ee/sh_files/uchime_reference_dataset_01.01.2016.zip
usearch8 -uchime_ref derep.otus.fa -db /path_to_files/UNITE_db/uchime_sh_refs_dynamic_develop_985_01.01.2016.ITS2.fasta -nonchimeras otus.no_chimera.fa -uchimeout reads.derep.otus.no_chimera.uchime -strand plus -sizein -sizeout

## map reads back to OTUs and create the otu_tab.txt for phyloseq
usearch8 -usearch_global merged.filtered.fa -db otus.no_chimera.fa -strand plus -id 0.97 -top_hit_only -otutabout otu_table.txt -sizein -sizeout

## subsample OTUs to 500
seqtk sample -s100 otus.no_chimera.fa 500 > OTU_500.fa
