# Written by Natalie Vande Pol
# April 16, 2017
#
# Command line: python MasterScript2.py
# Script will prompt for taxonomy file from each classifier and validate file
# Creates a taxonomy file in standardized format for each input file and
# generates a consensus taxonomy file based on the three input files
# Reformatted taxonomy files are named and located based on the input file
# Consenus taxonomy file located in working directory under default name unless
# otherwise specified by user



import sys, os

def reformat_RDP(rdp_file):
	input = open(rdp_file, "r")
	all_lines = input.readlines()
	input.close()

	output_file = ".".join(os.path.splitext(rdp_file)[:-1])+"__final.txt"
	output = open(output_file,"w")
	output.write("OTU_ID\tScore\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")

	for i, line in enumerate(all_lines):
		# capture confidence level at genus before changing line
		temp = line.strip().split("\t")
		confi = temp[7:-2][::3]
		confi.append(temp[-1])
		taxon = temp[5:][::3]

		# remove any taxonomic levels after first "unidentified"
		j=0
		new_taxon = []
		while j<len(taxon):
			if	taxon[j].endswith("Incertae_sedis"):
				taxon[j] = "Incertae_sedis"
			if  "unidentified" in taxon[j] or float(confi[j])<0.8:
				del confi[j:]
				break
			else: new_taxon.append(taxon[j])
			j+=1

		if confi == []:
			score = "NA"
		else:
			score = confi[-1]

		final_line = temp[0]+"\t"+score+"\t"+"\t".join(new_taxon)+"\n"
		output.write(final_line)

	output.close()
	return output_file

################################################################################
def reformat_UTAX(utax_file):
	input = open(utax_file, "r")
	all_lines = input.readlines()
	input.close()

	output_file = ".".join(os.path.splitext(utax_file)[:-1])+"__final.txt"
	output = open(output_file,"w")
	output.write("OTU_ID\tScore\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")
	for i, line in enumerate(all_lines):
		#remove unwanted third column and convert "(" and ")" to "*"
		temp = line.replace("(", "*").replace(")","*").split()
		line = temp[0]+"\t"+temp[1]

		temp0 = line.split("*")
		confid = temp0[1:][::2]
		line2 = "".join(temp0[0:-2][::2])

		temp1 = line2.split(",")
		j=1
		new_line = [temp1[0]]
		while j<len(temp1):
			if  "unidentified" in temp1[j] or float(confid[j-1]) < 0.8:
				del confid[j-1:]
				break
			else:
				new_line.append(temp1[j])
			j+=1

		line2 = ",".join(new_line)

		temp2 = line2.split(",")
		temp3 = temp2[0].split()
		temp4 = []
		for item in temp2[1:]:
			temp4.append(item[2:])

		if confid == []:
			score = "NA"
		else:
			score = confid[-1]
		final_line = temp3[0]+"\t"+score+"\t"+temp3[1][2:]+"\t"+"\t".join(temp4)+"\n"
		output.write(final_line)

	output.close()
	return output_file

################################################################################
def reformat_SINTAX(sintax_file):
	input = open (sintax_file, "r")
	all_lines = input.readlines()
	input.close()

	output_file = ".".join(os.path.splitext(sintax_file)[:-1])+"_sintax_final.txt"
	output = open(output_file, "w")
	output.write("OTU_ID\tScore\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")
	for i, line in enumerate(all_lines):
		#remove unwanted third column and convert "(" and ")" to "*"
		temp = line.replace("(", "*").replace(")","*").split()
		del temp[2:]
		#temp =>  'OTU_999'	'd:Fungi*1.0000*,p:Ascomycota*1.0000*,c:Leotiomycetes*1.0000*,o:Helotiales*1.0000*,s:Helotiales_sp*1.0000*'

		temp0 = temp[1].split("*")
		#temp0 =>  'd:Fungi,' '1.0000' ',p:Ascomycota' '1.0000' ',c:Leotiomycetes' '1.0000' ',o:Helotiales' '1.0000' ',s:Helotiales_sp' '1.0000'
		confid = temp0[1:][::2]
		#confid =>  '1.0000' '1.0000' '1.0000' '1.0000' '1.0000'
		temp_line = "".join(temp0[0:-2][::2])
		#temp_line =>  "d:Fungi,p:Ascomycota,c:Leotiomycetes,o:Helotiales,s:Helotiales_sp"

		temp1 = temp_line.split(",")
		#temp1 =>  'd:Fungi' 'p:Ascomycota' 'c:Leotiomycetes' 'o:Helotiales' 's:Helotiales_sp'
		levels = ["d:", "p:", "c:", "o:", "f:", "g:", "s:"]
		if len(temp1)<len(levels):
			if "g:" in temp1[-2]:
				for k, level in enumerate(temp1):
					if levels[k] not in temp1[k]:
						temp1.insert(k, levels[k]+"Incertae_sedis")
						confid.insert(k, 9)
			else:
				for k, level in enumerate(temp1):
					if levels[k] not in temp1[k]:
						temp1.insert(k, levels[k]+"unidentified")
						confid.insert(k, 0)

		j=0
		temp2 = []
		while j<len(temp1):
			if  "unidentified" in temp1[j]:
				del confid[j:]
				break
			elif confid[j]==9 and float(confid[j+1])<0.5:
				del confid[j:]
				break
			elif float(confid[j])<0.5:
				del confid[j:]
				break
			else:
				temp2.append(temp1[j])
			j+=1

		new_taxonomy = []
		for item in temp2:
			new_taxonomy.append(item[2:])

		if confid == []:
			score = "NA"
		else:
			score = confid[-1]
		output.write(temp[0]+"\t"+str(score)+"\t"+"\t".join(new_taxonomy)+"\n")

	output.close()
	return output_file

################################################################################
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
		dict[temp[0]][-1] = species.replace("_"," ")
	return dict

################################################################################
def vote(file1, file2, file3):
	taxa = [file1, file2, file3]
	tally = ["0","0","0"]
	duplicates_notempty = [i for i, x in enumerate(taxa) if x!= "" and taxa.count(x) > 1]
	unique_2empty = [i for i, x in enumerate(taxa) if x!="" and taxa.count("") > 1]
	for j in range(0,3):
		if taxa[j]!="":
			if j in duplicates_notempty:
				break
			elif j in unique_2empty:
				break
	return taxa[j]

###############################################################################
# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
###############################################################################
#Example RDP input:
#OTU_2836	_	Root	rootrank	1.0	Fungi	Kingdom	0.98	Zygomycota	Phylum	0.05	Zygomycota_Incertae_sedis	Class	0.05	Mucorales	Order	0.04	Syncephalastraceae	Family	0.01	Fennellomyces	Genus	0.01	Fennellomyces linderi	Species	0.01
#Criteria: temp = line.split("\t"), temp[3]=="rootrank" len(temp)> 21

#Example UTAX input
#OTU_2545	d:Fungi,p:Basidiomycota(0.9941),c:Agaricomycetes(0.8548),o:Agaricales(0.8523),f:Mycenaceae(0.5664),g:Mycena(0.2776),s:Mycena_epipterygia(0.0882)	p:Basidiomycota,c:Agaricomycetes,o:Agaricales	-
#Criteria: "),c:" in line, temp = line.split("\t"), temp[1].startswith("d:")

#Example SINTAX input
#OTU_5443	d:Fungi(1.0000),p:Ascomycota(0.9700),c:Pezizomycetes(0.8000),o:Pezizales(0.7900),f:Sarcosomataceae(0.7700),g:Pseudoplectania(0.3700),s:Pseudoplectania_nigrella(0.3700)	+	d:Fungi,p:Ascomycota,c:Pezizomycetes
#Criteria: "),p:" in line, temp = line.split("\t"), temp[1].startswith("d:")


three_classifiers = ["RDP", "UTAX", "SINTAX"]

for classifier in three_classifiers:
	valid = 0
	while valid != 1:
		file_name = raw_input("Enter file path/name for "+classifier+" output:  ")
		try:
			open(file_name,"r")
			valid = 1
		except IOError:
			print "ERROR: file could not be opened."
			valid = 0
			continue
		input_file = open(file_name,"r")
		line = input_file.readline()
		temp0 = line.split("\t")
		if classifier == "RDP":
			if len(temp0)<21 or temp0[3]!="rootrank":
				valid = 0
				print "Input file not in RDP format. Please Reformat As Below:"
				print "OTU_###	_	Root	rootrank	1.0	Fungi	Kingdom	0.98	Zygomycota	Phylum	0.05	Zygomycota_Incertae_sedis	Class	0.05	Mucorales	Order	0.04	Syncephalastraceae	Family	0.01	Fennellomyces	Genus	0.01	Fennellomyces linderi	Species	0.01"
		elif classifier == "UTAX":
			if "),c:" not in temp0[1] or not temp0[1].startswith("d:"):
				valid = 0
				print "Input file not in UTAX format. Please Reformat As Below:"
				print "OTU_###	d:Fungi,p:Ascomycota(0.9700),c:Pezizomycetes(0.8000),o:Pezizales(0.7900),f:Sarcosomataceae(0.7700),g:Pseudoplectania(0.3700),s:Pseudoplectania_nigrella(0.3700)	+	d:Fungi,p:Ascomycota,c:Pezizomycetes"
		else:
			if "),p:" not in temp0[1] or not temp0[1].startswith("d:"):
				valid = 0
				print "Input file not in SINTAX format. Please Reformat As Below:"
				print "OTU_###	d:Fungi(1.0000),p:Ascomycota(0.9700),c:Pezizomycetes(0.8000),o:Pezizales(0.7900),f:Sarcosomataceae(0.7700),g:Pseudoplectania(0.3700),s:Pseudoplectania_nigrella(0.3700)	+	d:Fungi,p:Ascomycota,c:Pezizomycetes"

		input_file.close()

	print "Reformatting "+classifier+" file"
	if classifier == "RDP":
		rdp_file = reformat_RDP(file_name)
		rdp_dict = build_dict(rdp_file)
	elif classifier == "UTAX":
		uta_file = reformat_UTAX(file_name)
		uta_dict = build_dict(uta_file)
	else:
		sin_file = reformat_SINTAX(file_name)
		sin_dict = build_dict(sin_file)
	print classifier+" File reformatted\n"

print "Generating consensus taxonomy"
yes = set(['yes','y', 'ye'])
no = set(['no','n'])
choice_valid = 0
print "Default consensus taxonomy file named 'consensus_taxonomy.txt'."
while choice_valid != 1:
	choice = raw_input("Would you prefer to specify a different file name? y/n:	").lower()
	if choice in yes:
		choice_valid = 1
		consensus_file = raw_input("Desired file name (include extension):	")
	elif choice in no:
		choice_valid = 1
		consensus_file = "consensus_taxonomy.txt"
	else:
		sys.stdout.write("Please respond with 'y' or 'n'\n")

consensus = open(consensus_file, "w")
for otu in rdp_dict.keys():
	consensus.write(otu+"\t")
	levels = []
	for m in range(0,7):
		level = vote(rdp_dict[otu][m], sin_dict[otu][m], uta_dict[otu][m])
		if level != "":
			levels.append(level)
	consensus.write("\t".join(levels)+"\n")
print "Done\n"

consensus.close()