# Fungal microbiomes: strategies for improving taxonomy resolution of environmental sequences

Table of Contents
--------
* [**Authors**](#authors)
* [**Abstract**](#abstract)
* [**Study Purpose**](#study-purpose)
* [**Script Purpose**](#script-purpose)
* [**System Requirements**](#sys-req)


<a name="authors"></a>
Authors
--------
* "Kristi Gdanetz MacCready"
* "Natalie Vande Pol"
* "Gregory Bonito"
* "Gian Maria Niccolò Benucci"


<a name="abstract"></a>
Abstract
--------
One of the most crucial steps in high-throughput sequence based microbiome studies is the taxonomic assignment of sequences belonging to operational taxonomic units (OTUs). Without taxonomic classification, functional and biological information of microbial communities cannot be inferred or interpreted. The Internal Transcribed Spacer (ITS) region of the nuclear ribosomal DNA (rDNA) is the conventional marker region for fungal community studies. While bioinformatics pipelines that cluster reads into OTUs have received much attention in the literature, the taxonomic classification of these sequences, upon which biological inference is dependent, has been largely neglected. Here we compared how the most common fungal OTU taxonomic assignment approaches, UTAX, RDP standalone, and SINTAX, handle ITS1 and ITS2 fungal sequence data generated by Illumina MiSeq amplicon sequencing. The classification power (ability to assign taxonomy at a given taxonomic rank) varied among the classifiers. Our results demonstrate how taxonomy assignment tools can bias understanding of fungal communities, and distort the linkage between taxa and specific treatments or ecosystems. We conclude with general guidelines and best practices for assigning taxonomy in fungal microbiome studies.


<a name="study-purpose"></a>
Study Purpose
--------
We set out to test whether the most commonly used taxonomic classifiers generate similar profiles of the fungal community. To do so we used two published MiSeq ITS datasets and compared the standalone command line Ribosomal Database Project Classifier (not to be confused with the Ribosomal Database Project) (Wang et al. 2007; Cole et al. 2013),  UTAX (Edgar 2010; 2013), and SINTAX (Edgar 216).



<a name="script-purpose"></a>
Script Purpose
--------
The first script in this pipeline accepts database files in FASTA format and re-generates that database in formats compatible with the RDP, UTAX, and SINTAX classifiers. It also calls on two scripts to generate files for training the RDP classifier.

The second script accepts the classified OTU taxonomy outputs from each of the three classifiers, filters by confidence score, and reformats them to a standardized output. In addition, it compares the standardized classifications to generate a consensus taxonomy based on all three classifiers.

<a name="sys-req"></a>
System Requirements
--------
All three scripts in the first step must be in the same directory. The input and output files can be in any accessible directory as long as the path between the scripts and files is specified. Output files are generated in the same directory as the input file(s) and named based upon the input file unless otherwise specified.
