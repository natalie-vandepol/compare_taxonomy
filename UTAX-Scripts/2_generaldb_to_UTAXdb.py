#################################################################################
#	Written by Natalie Vande Pol												#
#	May 3, 2016																	#
#																				#
#	*  command line: python generaldb_to_QIIMEdb.py [path/filename(s)]			#
#	*  accepts unlimited reference database files and splits them to fasta		#
#	   and taxonomy files in the QIIME format									#
#	*  output files written to original file location, the original filename	#
#		appended "__QIIME.fasta" and "__QIIME_taxonomy.txt"						#
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
			fastatax.write(">"+utax_name+";tax=d"+utax_taxa+";\n")
		else:
			fastatax.write(line)
	fastatax.close()
