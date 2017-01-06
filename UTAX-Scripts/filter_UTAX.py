#################################################################
#	Written by Natalie Vande Pol, Sept 26, 2016		#
#	Edited 10-10-2016 KGM					#
#	Script converts UTAX output taxonomy to standard output	#
#################################################################

import sys, os

#input = open ("jump_taxonomy_utax.txt", "r")
input = open(sys.argv[1], "r")
all_lines = input.readlines()
input.close()

#output = open("jump_utax_to_same.txt", "w")
output = open(".".join(os.path.splitext(sys.argv[1])[:-1])+"__final.txt","w")
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
		if  "unidentified" in temp1[j] or float(confid[j-1]) < 0.5:
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
