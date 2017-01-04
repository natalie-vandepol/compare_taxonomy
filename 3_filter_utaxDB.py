################################################################################
#	Written by Natalie Vande Pol											   #
#	May 9, 2016																   #
#																			   #
#	*   command line: python generaldb_to_UTAXdb.py [path/filename]		   #
#	*   accepts (1) UTAX database files and filters out any taxonomic levels   #
#		that are "unknown", "unidentified", or "Incertae_sedis" and any		   #
#		sequences whose kingdom is not "Fungi".								   #
#	*   output files written to original file locations, the initial filename  #
#		appended with "__filtered.fasta"									   #
################################################################################

import sys, os

input = open(sys.argv[1], "r")
all_lines = input.readlines()
input.close()

output = open(".".join(os.path.splitext(sys.argv[1])[:-1])+"__filtered.fasta","w")
for i, line in enumerate(all_lines):
	if line[0]==">":
		temp = line.strip().split(",")
		if temp[0].endswith("Fungi"):
			temp2 = [x for x in temp if "unidentified" not in x]
			temp3 = [y for y in temp2 if "Incertae_sedis" not in y]
			temp4 = [z for z in temp3 if "unknown" not in z]
			new_name = ",".join(temp4)
			print new_name
			seq = all_lines[i+1].upper()
			output.write(new_name+"\n"+seq)
output.close()