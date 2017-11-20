#################################################################
###############*** This is CONSTAX v.1 ***#######################
#								
#                     MIT License                               
#								
#     Copyright (c) 2017 Natalie Vandepol, Kristi Gdanetz,      
#     Gian Maria Niccolo' Benucci, Gregory Bonito               
#								
#     https://github.com/natalie-vandepol/compare_taxonomy            
#################################################################
#################################################################

# Before running CONSTAX, please complete all the instructions below.
# See GitHub page for more detailed instructions.

# Install all the following dependancies:
1) USEARCH8 which implements the UTAX algorhitm 
2) USEARCH9 or USEARCH10 which implements the SINTAX algorithm
2) Standalone RDP classifier 
4) R 
5) Python version 2.7

####################################
# INSTALL USEARCH 
####################################

# Download both USEARCH versions and put them in the CONSTAX folder
# Make sure to download the correct build for your operating system (macOS vs. linux)

# Change permissions for USEARCH binaries
chmod +x usearch10.0.240_i86osx32
chmod +x usearch8.1.1861_i86osx32

# Create symbolic links by specifying the full paths of the executables
ln -sf /path-to-folder/CONSTAX/usearch10.0.240_i86osx32 usearch10
ln -sf /path-to-folder/CONSTAX/usearch8.1.1861_i86osx32 usearch8

####################################
# INSTALL RDP Classifier
####################################

# First, install Apache Ant.
## For Linux
sudo wget http://apache.mirrors.pair.com//ant/binaries/apache-ant-1.10.1-bin.zip

## For Mac
sudo curl http://apache.mirrors.pair.com//ant/binaries/apache-ant-1.10.1-bin.zip -o apache-ant-1.10.1-bin.zip
sudo unzip apache-ant-1.10.1-bin.zip

# Add the Apache Ant path to the .bash_profile or .bashrc
# If you do not have a bash profile file, create one. $ nano .bash_profile
cd

# Open the .bash_profile
nano .bash_profile

# Add the following line, save, and close.
export PATH=/path-to/apache-ant-1.10.1/bin:$PATH 

# Reload bash profile to enact the changes.
source .bashrc

# Next, download and install the RDP Classifier.
# Make sure you are in your home directory. For Mac it is usually “/“ and for Linux it is “/home”
sudo git clone https://github.com/rdpstaff/RDPTools
cd RDPTools
sudo git submodule init
sudo git submodule update
sudo make

# After successful installtion the following will be printed out in the terminal:
BUILD SUCCESSFUL
Total time: 2 seconds
(cp Framebot/dist/FrameBot.jar Clustering/dist/Clustering.jar SequenceMatch/dist/SequenceMatch.jar classifier/dist/classifier.jar AbundanceStats/dist/AbundanceStats.jar ReadSeq/dist/ReadSeq.jar SeqFilters/dist/SeqFilters.jar ProbeMatch/dist/ProbeMatch.jar KmerFilter/dist/KmerFilter.jar Xander-HMMgs/dist/hmmgs.jar AlignmentTools/dist/AlignmentTools.jar ./; cp -r */dist/lib/* lib/; rm -r classifier/dist/)


#######################################################
# RUN CONSTAX v.1
#######################################################

# Download the CONSTAX.zip file form Github and place it in your home directory.
### All the scripts are set-up assuming the directory is named CONSTAX
sudo git clone https://github.com/natalie-vandepol/compare_taxonomy/CONSTAX.zip  
unzip CONSTAX.zip 
cd CONSTAX

# Set parameters in the “config” file and save
nano config

# Download the UNITE (or other) reference database and place in /path-to-folder/CONSTAX/DB/
# Place a copy your data (otus.fasta) inside /path-to-folder/CONSTAX/otus/

# Run the CONSTAX tool
sh constax.sh


#######################################################
# INSTALL BLAST for MacQIIME
#######################################################

# constax.sh is not set up to inlcude blast output as part of the consensus taxonomy
# Blast formatting scripts are inluded to allow researchers to compare blast output with the output from the other classifier programs

# Download the proper BLAST version for QIIME here
http://qiime.org/install/alternative.html#installing-qiime-natively-with-a-full-install
unzip blast-2.2.22-universal-macosx.tar.gz

# Add the blast PATH to your .bash_profile by adding the line
export PATH=/Users/BonitoLab/blast-2.2.22/bin:$PATH
source .bashrc
