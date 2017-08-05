# Written by Natalie Vande Pol
# April 13, 2017
#
# Command line: python MasterScript1.py
# Script will prompt for database file, validate file, and check for additional input
# Requires subscript_lineage2taxonomyTrain.py and subscript_fasta_addFullLineage.py
# be in the same directory
# Creates the following for each input file:
#	a combined taxonomy and fasta database file compatible with the UTAX classifier
#	fasta and taxonomy database files compatible with the RDP classifer
#	training files for the RDP classifier
# Output files are named and located based on the input file



# -*- coding: utf-8 -*-
import sys, os, unicodedata
import subscript_lineage2taxonomyTrain, subscript_fasta_addFullLineage

valid = 0
done = 0
all_filenames = []
while valid != 1 or done != 1:
		file_name = raw_input("Enter file path/name for database:  ")
		try:
			open(file_name,"r")
			valid = 1
		except IOError:
			print "ERROR: file could not be opened."
			valid = 0
			continue
		input_file = open(file_name,"r")
		line = input_file.readline()
		temp0 = line.split("|")
		if line[0]!=">" or len(temp0)!= 5 or "k__" not in temp0[-1]:
			valid = 0
			print "Header Format Incompatible. Please Reformat As Below:"
			print ">Peziza_sp|JN102365|SH189857.07FU|reps|k__Fungi;p__Ascomycota;c__Pezizomycetes;o__Pezizales;f__Pezizaceae;g__Peziza;s__Peziza_sp"
		if valid == 1:
			if file_name not in all_filenames:
				all_filenames.append(file_name)
			else:
				print "Database already specified"
			yes = set(['yes','y', 'ye'])
			no = set(['no','n'])
			choice_valid = 0
			while choice_valid != 1:
				choice = raw_input("Input additional databases? y/n	").lower()
				if choice in yes:
					done = 0
					choice_valid = 1
				elif choice in no:
					done = 1
					choice_valid = 1
				else:
					sys.stdout.write("Please respond with 'yes' or 'no'")
input_file.close()


for filename in all_filenames:
	filename_base = ".".join(os.path.splitext(filename)[:-1])
	#UTAX output file
	fastatax = open(filename_base+"__UTAX.fasta","w")

	#RDP output files
	fasta = open(filename_base+"__RDP.fasta","w")
	taxon = open(filename_base+"__RDP_taxonomy.txt","w")
	taxon.write("Seq_ID\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")

	num = 0
	with open(filename) as database:
		for line in database:
			if line[0]==">":
				#correct umlauts or special letters
				unico_line = unicode(line, '1252')
				ascii_line = unicodedata.normalize('NFKD', unico_line).encode('ASCII', 'ignore')
				temp = ascii_line[1:].split("|")

				#UTAX file
				utax_name = temp[1]+"|"+temp[2]
				utax_taxa = temp[4][1:].strip().replace("__",":").replace(";",",")
				temp_utax = utax_taxa.strip().split(",")
				if temp_utax[0].endswith("Fungi"):
					temp_utax2 = [x for x in temp_utax if "unidentified" not in x]
					temp_utax3 = [y for y in temp_utax2 if "Incertae_sedis" not in y]
					temp_utax4 = [z for z in temp_utax3 if "unknown" not in z]
					new_utax_taxa = ",".join(temp_utax4)
					fastatax.write(">"+utax_name+";tax=d"+new_utax_taxa+";\n")

				#RDP files
				name = str(temp[1])
				temp2 = temp[4].strip().split("__")
				to_genus = [ item[:-2] for item in temp2[1:-1] ]

				if "Incertae_sedis" in to_genus:
					indices = [i for i,x in enumerate(to_genus) if x == "Incertae_sedis"]
					for j in indices:
						if "Incertae_sedis" not in to_genus[j-1]:
							to_genus[j] = str(to_genus[j-1])+"_Incertae_sedis"
						else:
							to_genus[j] = str(to_genus[j-1])
				if "unidentified" in to_genus:
					indices = [i for i,x in enumerate(to_genus) if x == "unidentified"]
					for j in indices:
						to_genus[j] = "-"

				if to_genus[0] != "-":
					species = str(temp2[-1])
					if "Incertae" in species:
						species = "unidentified_sp"
					elif to_genus[-1] not in species:
						temp=species.split("_")
						species = temp[0]+"_unidentified_"+temp[1]
					if species.endswith("sp"):
						species+= "_"+str(num)
						num += 1

					taxonomy = name+"\t"+"\t".join(to_genus)+"\t"+species+"\n"
					fasta.write(">"+name+"\n")
					taxon.write(taxonomy)
					seq = next(database)
					fastatax.write(seq)
					fasta.write(seq)

		fasta.close()
		taxon.close()
		fastatax.close()

		subscript_lineage2taxonomyTrain.lin2tax(filename_base)
		subscript_fasta_addFullLineage.addFullLineage(filename_base)