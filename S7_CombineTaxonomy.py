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



import sys, os, itertools

################################################################################
def reformat_RDP(rdp_file):
	input = open(rdp_file, "U")
	all_lines = input.readlines()
	input.close()

	output_file = ".".join(os.path.splitext(rdp_file)[:-1])+"_rdp_final.txt"
	output = open(output_file,"w")
	output.write("OTU_ID\tOTU_Score\tKingdom\tK_score\tPhylum\tP_score\tClass\tC_score")
	output.write("\tOrder\tO_score\tFamily\tF_score\tGenus\tG_score\tSpecies\tS_score\n")

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
			if  "unidentified" in taxon[j] or float(confi[j])<confidence:
				del confi[j:]
				break
			else: new_taxon.append(taxon[j].capitalize())
			j+=1

		# remove "_sp" from species classificaitons
		if len(new_taxon)>0 and " sp" in new_taxon[-1]:
			del new_taxon[-1]
			del confi[-1]
		# remove meaningless terminal Incertae_sedis
		while len(new_taxon)>0 and "Incertae_sedis" in new_taxon[-1]:
			del new_taxon[-1]
			del confi[-1]


		if confi == []:
			score = "NA"
		else:
			score = confi[-1]

		iters = [iter(new_taxon), iter(confi)]
		tax_confi = list(str(it.next()) for it in itertools.cycle(iters))

		output.write(temp[0]+"\t"+score+"\t"+"\t".join(tax_confi)+"\n")

	output.close()
	return output_file

################################################################################
def reformat_UTAX(utax_file):
	input = open(utax_file, "U")
	all_lines = input.readlines()
	input.close()

	output_file = ".".join(os.path.splitext(utax_file)[:-1])+"_utax_final.txt"
	output = open(output_file,"w")
	output.write("OTU_ID\tOTU_Score\tKingdom\tK_score\tPhylum\tP_score\tClass\tC_score")
	output.write("\tOrder\tO_score\tFamily\tF_score\tGenus\tG_score\tSpecies\tS_score\n")
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
			if  "unidentified" in temp1[j] or float(confid[j-1]) < confidence:
				del confid[j-1:]
				break
			else:
				new_line.append(temp1[j])
			j+=1

		line2 = ",".join(new_line)

		temp2 = line2.split(",")
		# OTU_1328        d:Fungi, p:Ascomycota, c:Archaeorhizomycetes, o:Archaeorhizomycetales, f:Archaeorhizomycetaceae, g:Archaeorhizomyces, s:Archaeorhizomyces_sp
		temp3 = temp2[0].split()
		# OTU_1328, d:Fungi
		temp4 = []
		for item in temp2[1:]:
			temp4.append(item[2:].capitalize())
		# Ascomycota, Archaeorhizomycetes, Archaeorhizomycetales, Archaeorhizomycetaceae, Archaeorhizomyces, Archaeorhizomyces_sp

		# remove "_sp" from species classificaitons
		if len(temp4)>0 and temp4[-1].endswith("_sp"):
			del temp4[-1]
			del confid[-1]

		# remove meaningless terminal Incertae_sedis
		while len(temp4)>0 and temp4[-1]=="Incertae_sedis":
			del temp4[-1]
			del confid[-1]

		confid = [str(x) for x in confid]
		confid.insert(0, "NA")
		score = confid[-1]
		final_line = temp3[0]+"\t"+score+"\t"+temp3[1][2:].capitalize()+"\t"

		iters = [iter(confid), iter(temp4)]
		tax_confi = list(str(it.next()) for it in itertools.cycle(iters))

		output.write(final_line+"\t".join(tax_confi)+"\n")

	output.close()
	return output_file

################################################################################
def reformat_SINTAX(sintax_file):
	input = open (sintax_file, "U")
	all_lines = input.readlines()
	input.close()

	output_file = ".".join(os.path.splitext(sintax_file)[:-1])+"_sintax_final.txt"
	output = open(output_file, "w")
	output.write("OTU_ID\tOTU_Score\tKingdom\tK_score\tPhylum\tP_score\tClass\tC_score")
	output.write("\tOrder\tO_score\tFamily\tF_score\tGenus\tG_score\tSpecies\tS_score\n")
	for i, line in enumerate(all_lines):
		#remove unwanted third column and convert "(" and ")" to "*"
		temp = line.replace("(", "*").replace(")","*").split("\t")
		del temp[2:]
		#temp =>  'OTU_999'	'd:Fungi*1.0000*,p:Ascomycota*1.0000*,c:Leotiomycetes*1.0000*,o:Helotiales*1.0000*,s:Helotiales_sp*1.0000*'

		temp0 = temp[1].split("*")
		#temp0 =>  'd:Fungi,' '1.0000' ',p:Ascomycota' '1.0000' ',c:Leotiomycetes' '1.0000' ',o:Helotiales' '1.0000' ',s:Helotiales_sp' '1.0000'
		confid = temp0[1:][::2]
		#confid =>  '1.0000' '1.0000' '1.0000' '1.0000' '1.0000'
		temp_line = "".join(temp0[0:-2][::2])
		#temp_line =>  "d:Fungi,p:Ascomycota,c:Leotiomycetes,o:Helotiales,s:Helotiales_sp"

		# fix missing taxonomic levels
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
			elif confid[j]==9 and float(confid[j+1])<confidence:
				del confid[j:]
				break
			elif float(confid[j])<confidence:
				del confid[j:]
				break
			else:
				temp2.append(temp1[j].capitalize())
			j+=1

		# remove "_sp" from species classificaitons
		if len(temp2)>0 and temp2[-1].endswith("_sp"):
			del temp2[-1]
			del confid[-1]
		# remove meaningless terminal Incertae_sedis
		while len(temp2)>0 and "Incertae_sedis" in temp2[-1]:
			del temp2[-1]
			del confid[-1]

		confid = [str(x) if x!=9 else "NA" for x in confid]

		new_taxonomy = []
		for item in temp2:
			new_taxonomy.append(item[2:].capitalize())

		if confid == []:
			score = "NA"
		else:
			score = confid[-1]

		iters = [iter(new_taxonomy), iter(confid)]
		tax_confi = list(str(it.next()) for it in itertools.cycle(iters))

		output.write(temp[0]+"\t"+str(score)+"\t"+"\t".join(tax_confi)+"\n")


	output.close()
	return output_file

################################################################################
def build_dict(filename):
	file = open(filename, "r")
	all_lines = file.readlines()
	file.close()

	dict = {}
	for i, line in enumerate(all_lines[1:]):
		temp = line.replace(" ", "_").strip().split()
		dict[temp[0]] = []
		if len(temp)>2:
			dict[temp[0]]=temp[2:]
		if len(dict[temp[0]])<14:
			while len(dict[temp[0]])<14:
				dict[temp[0]].append("")
		# strip numbers from species identifications
		species = filter(lambda c: not c.isdigit(), dict[temp[0]][-2])
		dict[temp[0]][-2] = species.replace("_"," ")
	return dict

################################################################################
def vote(rdp, sin, uta):
	winner = ""
	taxa = [rdp[0], sin[0], uta[0]]
	scores = [rdp[1], sin[1], uta[1]]
	tally = ["0","0","0"]
	duplicates_notempty = [i for i, x in enumerate(taxa) if x!= "" and taxa.count(x) > 1]
	unique_2empty = [i for i, x in enumerate(taxa) if x!="" and taxa.count("") > 1]
	unique = [i for i, x in enumerate(taxa) if x!="" and taxa.count("") == 1]
	for j in range(0,3):
		if taxa[j]!="":
			if j in duplicates_notempty:
				winner = taxa[j]
				break
			elif j in unique_2empty:
				winner = taxa[j]
				break
			elif j in unique:
				scores = [float(x) if x!="NA" and x!="" else 0 for x in scores]
				winner = taxa[scores.index(max([scores[x] for x in unique]))]
		else:
			winner = taxa[j]
	return winner

################################################################################
def count_classifications(filenames):
	# rdp, utax, sintax, consensus
	file_num = 0
	unique_dict = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}, 6:{}}
	for i, file in enumerate(filenames):
		input = open(file, "r")
		all_lines = input.readlines()
		input.close()
		count_y = [0,0,0,0,0,0,0]
		count_n = [0,0,0,0,0,0,0]
		output1 = open(".".join(os.path.splitext(file)[:-1])+"_CountClassified.txt", "w")
		if i<3:	#first 3 files have scores
			start= 2
			freq = 2
		else: 	#consensus file does not have scores
			start= 1
			freq = 1
		for j, line in enumerate(all_lines[1:]):
			temp = line.strip().split("\t")
			taxonomy = temp[start::freq]
			if len(taxonomy)==7:
				# strip numbers from species identifications
				species = filter(lambda c: not c.isdigit(), taxonomy[-1])
				taxonomy[-1] = species.replace("_"," ")

			for k in range(0,7):
				if k<len(taxonomy):
					count_y[k]+=1
					if taxonomy[k] not in unique_dict[k]:
						unique_dict[k][taxonomy[k]] = [0,0,0,0]
						unique_dict[k][taxonomy[k]][file_num]+= 1
					else:
						unique_dict[k][taxonomy[k]][file_num]+= 1
				else:
					taxonomy.append("Unidentified")
					count_n[k]+=1
					if taxonomy[k] not in unique_dict[k]:
						unique_dict[k][taxonomy[k]] = [0,0,0,0]
						unique_dict[k][taxonomy[k]][file_num]+= 1
					else:
						unique_dict[k][taxonomy[k]][file_num]+= 1


		for l, level in enumerate(count_y):
			count_y[l] = str(level)
		for m, level in enumerate(count_n):
			count_n[m] = str(level)
		output1.write("\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")
		output1.write("Classified\t"+"\t".join(count_y)+"\n")
		output1.write("Unclassified\t"+"\t".join(count_n))
		output1.close()
		file_num+=1

	yes = set(['yes','y', 'ye'])
	no = set(['no','n'])
	choice_valid = 0
	print "Default classification summary file named 'Classification_Summary.txt'."
	while choice_valid != 1:
		choice = raw_input("Would you prefer to specify a different file name? y/n:	").lower()
		if choice in yes:
			choice_valid = 1
			summary_file = raw_input("Desired file name (include extension):	")
		elif choice in no:
			choice_valid = 1
			summary_file = "Classification_Summary.txt"
		else:
			sys.stdout.write("Please respond with 'y' or 'n'\n")

	output2 = open(summary_file, "w")
	output2.write("Classification\tRDP\tUTAX\tSINTAX\tConsensus\n")
	for l in range(0, 7):
		key_list = unique_dict[l].keys()
		key_list.sort()
		for key in key_list:
			output2.write(key+"\t"+"\t".join(str(x) for x in unique_dict[l][key])+"\n")
	output2.close()

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

print "Default confidence threshhold is 0.8"
yes = set(['yes','y', 'ye'])
no = set(['no','n'])
valid = 0
yes_no = raw_input("Do you want to specify an alternate value? (y/n)\t")
while valid != 1:
	if yes_no in yes:
		user_confid = raw_input("Please specify a number between 0 and 1:\t")
		if float(user_confid)>0 and float(user_confid)<1:
			confidence = float(user_confid)
			valid = 1
	elif yes_no in no:
		confidence = 0.8
		valid = 1
	else:
		yes_no = raw_input("Error, Please specify yes or no:\t")


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
print "Default consensus taxonomy file named 'consensus_taxonomy.txt'"
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

print "Generating combined taxonomy"
yes = set(['yes','y', 'ye'])
no = set(['no','n'])
choice_valid = 0
print "Default combined taxonomy file named 'combined_taxonomy.txt'"
while choice_valid != 1:
	choice = raw_input("Would you prefer to specify a different file name? y/n:	").lower()
	if choice in yes:
		choice_valid = 1
		combined_file = raw_input("Desired file name (include extension):	")
	elif choice in no:
		choice_valid = 1
		combined_file = "combined_taxonomy.txt"
	else:
		sys.stdout.write("Please respond with 'y' or 'n'\n")

consensus = open(consensus_file, "w")
consensus.write("OTU_ID\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")

combined = open(combined_file, "w")
combined.write("OTU_ID\tKingdom_RDP\tKingdom_SINTAX\tKingdom_UTAX\tKingdom_Consensus\tPhylum_RDP\tPhylum_SINTAX\tPhylum_UTAX")
combined.write("\tPhylum_Consensus\tClass_RDP\tClass_SINTAX\tClass_UTAX\tClass_Consensus\tOrder_RDP\tOrder_SINTAX\tOrder_UTAX")
combined.write("\tOrder_Consensus\tFamily_RDP\tFamily_SINTAX\tFamily_UTAX\tFamily_Consensus\tGenus_RDP\tGenus_SINTAX\tGenus_UTAX")
combined.write("\tGenus_Consensus\tSpecies_RDP\tSpecies_SINTAX\tSpecies_UTAX\tSpecies_Consensus\n")

for otu in rdp_dict.keys():
	consensus.write(otu+"\t")
	combined.write(otu)
	levels = []
	for m in range(0,14,2):
		level = vote(rdp_dict[otu][m:m+2], sin_dict[otu][m:m+2], uta_dict[otu][m:m+2])
		combined.write("\t"+rdp_dict[otu][m]+"\t"+sin_dict[otu][m]+"\t"+uta_dict[otu][m]+"\t")
		if level != "":
			levels.append(level)
		combined.write(level)
	consensus.write("\t".join(levels)+"\n")
	combined.write("\n")
print "Done\n"

consensus.close()
combined.close()

count_classifications([rdp_file, uta_file, sin_file, consensus_file])