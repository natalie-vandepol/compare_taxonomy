# Fungal microbiomes: a strategy for improved taxonomic resolution of environmental ITS sequences 

Table of Contents
--------
* [**Authors**](#authors)
* [**Abstract**](#abstract)
* [**Study Purpose**](#study-purpose)
* [**Pipeline**](#pipeline)
* [**System Requirements**](#sys-req)
* [**Supplemental Files**](#sys-req)


<a name="authors"></a>
Authors
--------
* [Kristi Gdanetz MacCready](https://github.com/gdanetzk)
* [Gian Maria Niccolò Benucci](https://github.com/Gian77)
* [Natalie Vande Pol](https://github.com/natalie-vandepol)
* [Gregory Bonito](https://www.researchgate.net/profile/Gregory_Bonito)


<a name="abstract"></a>
Abstract
--------
One of the most crucial steps in high-throughput sequence based microbiome studies is the taxonomic assignment of sequences belonging to operational taxonomic units (OTUs). Without taxonomic classification, functional and biological information of microbial communities cannot be inferred or interpreted. The internal transcribed spacer (ITS) region of the ribosomal DNA (rDNA) is the conventional marker region for fungal community studies. While bioinformatics pipelines that cluster reads into OTUs have received much attention in the literature, the taxonomic classification of these sequences, upon which biological inference is dependent, has been largely neglected. Here we compared how the three most common fungal OTU taxonomic assignment tools (RDP Classifier, UTAX, and SINTAX) handle ITS fungal sequence data. The classification power (proportion of assigned OTUs at a given taxonomic rank) varied among the classifiers. Classifiers were generally consistent (assign the same taxonomy to a given OTU) across datasets and ranks; a small number of OTUs were assigned unique classifications across programs. We developed a tool in Python that compares the taxonomic classification of three classifier programs and merges them in an improved consensus taxonomy. The tool also produces summary classification outputs that are useful for downstream analyses. Our results demonstrate that independent taxonomy assignment tools classify different amounts of the fungal community, which may distort the linkage between taxa and specific treatments or ecosystems.

<a name="study-purpose"></a>
Study Purpose
--------
We set out to test whether the most commonly used taxonomic classifiers generate similar profiles of the fungal community. To do so we used published MiSeq ITS datasets and compared the standalone command line [Ribosomal Database Project Classifier](http://rdp.cme.msu.edu/) (Wang et al. 2007; Cole et al. 2013),  [UTAX](http://www.drive5.com/usearch/manual/utax_algo.html) (Edgar 2010; 2013), and [SINTAX](http://biorxiv.org/content/early/2016/09/09/074161) (Edgar 2016) Classifiers.

<a name="pipeline"></a>
Pipeline
--------
The analysis requires four general steps: 
(1) Sequence QC and OTU-picking 
(2) Database formatting and training
(3) Taxonomy assignment
(4) Post-taxonomy-assignment processing, filtering, analyzing

<a name="sys-req"></a>
System Requirements
--------
* Python version 2.6
* [PEAR version 0.9.8](http://sco.h-its.org/exelixis/web/software/pear/) (Zhang et al. 2014)
* [USEARCH version 8](http://drive5.com/usearch/manual8.1/) (Edgar et al. 2011; Edgar 2013)
* [RDP version 11](https://github.com/rdpstaff/classifier) (Cole et al. 2013)
* [USEARCH version 9](http://drive5.com/usearch/manual/whatsnewv9.html) (Edgar 2016)

<a name="sys-req"></a>
Supplemental Files
--------
* Supplementary File 1. Detailed workflow - implementation of code and scripts for sequence QC and OTU-picking, database formatting and trimming, taxonomy assignment, and post-taxonomy assignment filtering.
* Supplementary File 2. otu_processing.sh - Code for sequence QC and OTU-picking.
* Supplementary File 3. subscript_fasta_addFullLineage.py - First script required for training of RDP classifier.
* Supplementary File 4. subscript_lineage2taxonomyTrain.py - Second script required for training of RDP classifier.
* Supplementary File 5. FormatRefDB.py - Required for training of all classifiers and formatting of reference database.
* Supplementary File 6. taxonomy_pipeline.sh - Code for taxonomy assignment.
* Supplementary File 7. CombineTaxonomy.py - Python tool to improve taxonomy assignment of OTUs.
* Supplementary File 8. Import.R - Code used to generate barplots.
* Supplementary File 9. Fasta file with 500 OTUs as an example dataset to test the python tool.
