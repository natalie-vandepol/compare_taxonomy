#################################################################################
#	Written by Natalie Vande Pol						#
#	October 18, 2016							#
#	Requires 3 taxonomy files, in this tab-delimited format, with header:	#
#	 OTU\tConfidence\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies	#
#	Prompts for each input file						#
#	For each taxonomic level, this script determines the most "popular"	#
#	classification and produces an output file in the following format	#
#		OTU	FILE_1	FILE_2	FILE_3					#	
#	where each file is given a '2' if it has the most popular value, a '1'	#
#	for unique classifications, or a '0' if the level was empty		#
#################################################################################

def build_dict(filename):
	file = open(filename, "r")
	all_lines = file.readlines()
	file.close()

	dict = {}
	for i, line in enumerate(all_lines[1:]):
		temp = line.replace(" ", "_").strip().split("\t")
		dict[temp[0]] = []
		if len(temp)>2:
			dict[temp[0]]=temp[2:]
		if len(dict[temp[0]])<7:
			while len(dict[temp[0]])<7:
				dict[temp[0]].append("")
		# strip numbers from species identifications
		species = filter(lambda c: not c.isdigit(), dict[temp[0]][-1])
		dict[temp[0]][-1] = species
	return dict

def vote(file1, file2, file3):
	taxa = [file1, file2, file3]
	tally = ["0","0","0"]
	duplicates_notempty = [i for i, x in enumerate(taxa) if x!= "" and taxa.count(x) > 1]
	for j in range(0,3):
		if taxa[j]!="":
			if j in duplicates_notempty:
				tally[j] = "2"
			else:
				tally[j] = "1"
	return tally

rqu = ["RDP", "QIIME", "UTAX"]
for i, file in enumerate(rqu):
	valid = 0
	while valid != 1:
		rqu[i] = raw_input("Enter file path/name for standardized "+str(file)+" taxonomy:  ")
		try:
			open(rqu[i],"r")
			valid = 1
		except IOError:
			print "ERROR: file could not be opened."
			valid = 0

rdp_dict = build_dict(rqu[0])
qii_dict = build_dict(rqu[1])
uta_dict = build_dict(rqu[2])

taxon_levels = ["Kingdom","Phylum","Class","Order","Family","Genus","Species"]
for i, level in enumerate(taxon_levels):
	output = open(level+"_012.txt", "w")
	output.write("OTU\tRDP\tQIIME\tUTAX\n")

	for otu in rdp_dict.keys():
		output.write(otu+"\t")
		total = vote(rdp_dict[otu][i], qii_dict[otu][i], uta_dict[otu][i])
		output.write("\t".join(total)+"\n")
	output.close()
