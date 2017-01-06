#################################################################
#	Written by Natalie Vande Pol, Sept 29, 2016		#
#	Edited 10-13-16 by KGM					#
#	Script converts RDP output taxonomy to standard output	#
#################################################################

import sys, os

input = open(sys.argv[1], "r")
all_lines = input.readlines()
input.close()

output = open(".".join(os.path.splitext(sys.argv[1])[:-1])+"__final.txt","w")
output.write("OTU_ID\tScore\tKingdom\tPhylum\tClass\tOrder\tFamily\tGenus\tSpecies\n")

for i, line in enumerate(all_lines):
	# capture confidence level at genus before changing line
	temp = line.strip().split("\t")
	confi = temp[7:-2][::3]
	confi.append(temp[-1])
	print temp
	print confi
	taxon = temp[5:][::3]

	# remove any taxonomic levels after first "unidentified"
	j=0
	new_taxon = []
	while j<len(taxon):
		if	taxon[j].endswith("Incertae_sedis"):
			taxon[j] = "Incertae_sedis"
		if  "unidentified" in taxon[j] or float(confi[j])<0.5:
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
