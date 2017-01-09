#################################################################################
#	Written by Natalie Vande Pol						#
#	May 3, 2016								#
#										#
#	*  command line: python generaldb_to_UTAXdb.py [path/filename(s)]	#
#	*  accepts unlimited reference database files and converts them to a	#
#	   general format							#
#	*  filters out any taxonomic levels that are "unknown", "unidentified",	#
#	   or "Incertae_sedis" and any sequences whose kingdom is not "Fungi".	#
#	*  output files written to original file location, appended		#
#	   "__UTAX.fasta"							#
#################################################################################

import sys, os

for arg in sys.argv[1:]:
	gen = open(arg, "r")
	all_lines = gen.readlines()
	gen.close()

	fastatax = open(".".join(os.path.splitext(arg)[:-1])+"__UTAX.fasta","w")
	for i, line in enumerate(all_lines):
		if line[0]==">":
			temp0 = line[1:].split("|")
			utax_name = temp0[1]+"|"+temp0[2]
			utax_taxa = temp0[4][1:].strip().replace("__",":").replace(";",",")
			
			temp_line = ">"+utax_name+";tax=d"+utax_taxa+";\n"
			temp = temp_line.strip().split(",")
			if temp[0].endswith("Fungi"):
				temp2 = [x for x in temp if "unidentified" not in x]
				temp3 = [y for y in temp2 if "Incertae_sedis" not in y]
				temp4 = [z for z in temp3 if "unknown" not in z]
				utax_taxa = ",".join(temp4)
							
				seq = all_lines[i+1].upper()
				fastatax.write(utax_taxa+"\n"+seq)
	fastatax.close()
