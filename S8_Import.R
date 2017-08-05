library(dplyr)
library(ggplot2)

### import files
data = read.table("~/path_to_files/combined_taxonomy.txt", header=TRUE, row.names=1, sep="\t")
### format data frame
data[data==''|data==' ']<-NA
sapply(data, function(x) sum(is.na(x))) -> unassigned_data

### get number of unidentified OTUs
data2 <- as.data.frame(unassigned_data)
### add new column to data frame
data2$Classifier <- c("RDP","SINTAX","UTAX","COMBINED","RDP","SINTAX","UTAX","COMBINED","RDP","SINTAX","UTAX","COMBINED","RDP","SINTAX","UTAX","COMBINED","RDP","SINTAX","UTAX","COMBINED","RDP","SINTAX","UTAX","COMBINED","RDP","SINTAX","UTAX","COMBINED")
### covert row names to proper column
data2$Rank <- row.names(data2)
### calculate the number of assigned OTUs from unidentified 
data2$Assigned <- sqrt((data2$unassigned_data -500)^2) #change 500 to number of OTUs
### convert levels to factor for plotting 
data2$Classifier <- factor(data2$Classifier, levels = c("RDP","UTAX","SINTAX","COMBINED"))

### generate plot, colored by classifier
ggplot(data2, aes(x = Rank, y = Assigned, fill= Classifier)) + 
  geom_bar(stat = "identity") +
  scale_x_discrete(limits=data2$Rank) +
  theme(axis.text.x = element_text(angle = 90, hjust = 1),
        panel.grid=element_blank(),
        panel.background=element_blank()) +
  ggtitle("Assigned and Unidentified OTUs in ITS Dataset") +
  labs(x="Taxonomic Ranks", y="Number of classified OTUs")