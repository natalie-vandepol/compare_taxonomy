#################################################################################
#	Written by Natalie Vande Pol						#
#	May 3, 2016								#
#										#
#	*  command line: python generaldb_to_UTAXdb.py [path/filename(s)]	#
#	*  accepts unlimited reference database files and splits them to fasta	#
#	   and taxonomy files in the QIIME format				#
#	*  output files written to original file location, the original		#
#	   filename appended "__UTAX.fasta" and "__UTAX_taxonomy.txt"		#
#################################################################################

import sys, os

for arg in sys.argv[1:]:
	gen = open(arg, "r")
	all_lines = gen.readlines()
	gen.close()

	fastatax = open(".".join(os.path.splitext(arg)[:-1])+"__UTAX.fasta","w")
	for i, line in enumerate(all_lines):
		if line[0]==">":
			temp = line[1:].split("|")
			utax_name = temp[1]+"|"+temp[2]
			utax_taxa = temp[4][1:].strip().replace("__",":").replace(";",",")
			
			temp2 = utax_taxa.strip().split(",")
			if temp2[0].startswith(">"):
				temp3 = [x for x in temp2 if "unidentified" not in x]
				temp4 = [y for y in temp3 if "Incertae_sedis" not in y]
				temp5 = [z for z in temp4 if "unknown" not in z]
				new_name = ",".join(temp5)
				
			fastatax.write(">"+utax_name+";tax=d"+utax_taxa+";\n")
		else:
			fastatax.write(line)
	fastatax.close()
