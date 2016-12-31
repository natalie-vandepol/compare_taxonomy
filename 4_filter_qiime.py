####
#	Written by Natalie Vande Pol, Sept 29, 2016
#	Modified Oct 4, 2016. KGM
#	Script converts QIIME output taxonomy to standard output
####

import sys, os

#input = open ("jump_taxonomy_QIIME.txt", "r")
input = open(sys.argv[1], "r")
all_lines = input.readlines()
input.close()

#output = open("jump_qiime_to_same.txt", "w")
output = open(".".join(os.path.splitext(sys.argv[1])[:-1])+"__final.txt","w")
output.write("OTU_ID\tScore\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")

for i, line in enumerate(all_lines):
	# capture confidence level at genus before changing line
	temp = line.split()
	confi = temp[-1]

	# remove any taxonomic levels after first "unidentified"
	temp1 = temp[1].split("__")
	j=1
	taxon = []
	while j<len(temp1):
		if  "unidentified" in temp1[j]:
			break
		elif ";" in temp1[j]:
			taxon.append(temp1[j][:-2])
		else: taxon.append(temp1[j])
		j+=1

	final_line = temp[0]+"\t"+confi+"\t"+"\t".join(taxon)+"\n"
	output.write(final_line)

output.close()