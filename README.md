# 'CONSTAX: a tool for improved taxonomic resolution of environmental fungal ITS sequences' 

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

One of the most crucial steps in high-throughput sequence-based microbiome studies is the taxonomic assignment of sequences belonging to operational taxonomic units. Without taxonomic classification, functional and biological information of microbial communities cannot be inferred or interpreted. The internal transcribed spacer (ITS) region of the ribosomal DNA is the conventional marker region for fungal community studies. While bioinformatics pipelines that cluster reads into operational taxonomic units (OTUs) have received much attention in the literature, less attention has been given to the taxonomic classification of these sequences, upon which biological inference is dependent. Here we compare how three common fungal OTU taxonomic assignment tools (RDP Classifier, UTAX, and SINTAX) handle ITS fungal sequence data. The classification power, defined as the proportion of assigned operational taxonomic units at a given taxonomic rank, varied among the classifiers. Classifiers were generally consistent (assignment of the same taxonomy to a given operational taxonomic unit) across datasets and ranks; a small number of operational taxonomic units were assigned unique classifications across programs. We developed CONSTAX (CONSensus TAXonomy), a Python tool that compares taxonomic classifications of the three programs and merges them into an improved consensus taxonomy. This tool also produces summary classification outputs that are useful for downstream analyses. Our results demonstrate that independent taxonomy assignment tools classify unique members of the fungal community, and greater classification power is realized by generating consensus taxonomy of available classifiers with CONSTAX.


<a name="study-purpose"></a>
Study Purpose
--------
We set out to test whether the most commonly used taxonomic classifiers generate similar profiles of the fungal community. To do so we used published MiSeq ITS datasets and compared the standalone command line [Ribosomal Database Project Classifier](http://rdp.cme.msu.edu/) (Wang et al. 2007; Cole et al. 2013),  [UTAX](http://www.drive5.com/usearch/manual/utax_algo.html) (Edgar 2010; 2013), and [SINTAX](http://biorxiv.org/content/early/2016/09/09/074161) (Edgar 2016) Classifiers.

<a name="pipeline"></a>
Pipeline
--------
#### The analysis requires four general steps to go from raw sequences to a consesus taxonomy: 
1. Sequence QC and OTU-picking 
2. Database formatting and training 
3. Taxonomy assignment 
4. Post-taxonomy-assignment processing, filtering, analyzing 

Steps 2 through 4 are automated through *constax.sh* and implemented in the CONSTAX tool.

<a name="sys-req"></a>
System Requirements
--------
* Python version 2.7
* [PEAR version 0.9.8](http://sco.h-its.org/exelixis/web/software/pear/) (Zhang et al. 2014)
* [USEARCH version 8](http://drive5.com/usearch/manual8.1/) (Edgar et al. 2011; Edgar 2013)
* [RDP version 11](https://github.com/rdpstaff/classifier) (Cole et al. 2013)
* [USEARCH version 9/10](http://drive5.com/usearch/manual/whatsnewv9.html) (Edgar 2016)

<a name="sys-req"></a>
Supplemental Files
--------
* Supplementary File 1. CONSTAX.zip - download and unzip to use CONSTAX
* Supplementary File 2. CONSTAX Tutorial
* Supplementary File 3. otu_processing.sh - Code for sequence QC and OTU-picking.

