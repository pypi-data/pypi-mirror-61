#!/usr/bin/env Rscript
###################################################################
#Script Name    :heatmap.R
#Description    :Plot heatmap of kmer mapping.
#Args           :<summary> <output dir>
#Dependecies    :conda env -n heatmap r r-pheatmap r-gplots
#                conda activate map_kmers
#Author         :Lennard Epping; Felix Hartkopf
#Email          :eppingl@rki.de; hartkopff@rki.de
###################################################################



args = commandArgs(trailingOnly=TRUE)

# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("Please specify the path to the summary.", call.=FALSE)
}

path = args[1]
output = args[2]

# Write everything into log file
log <- file.path(output,"RKP.log")
sink(log, type=c("output", "message"), append = TRUE)


# Import
library(gplots, warn.conflicts = FALSE)
library(pheatmap, warn.conflicts = FALSE)

##read in results and set NA to 0##
mapping_result <- read.csv(path, row.names=1,  dec=",",header = TRUE)

# Make ID to rownames
rownames(mapping_result) <- mapping_result[,1]
mapping_result[,1] <- NULL

# Make data a numeric matrix
mapping_result <- as.matrix(mapping_result)
class(mapping_result) <- "numeric"

# Shorten colnames
colnames(mapping_result)=sub('\\_coverage_non_zero_genes_sorted_locus$', '', colnames(mapping_result))

##filter all columns if all values in row < 0.2##
mapping_result_filtered <- data.frame(mapping_result[apply(mapping_result, 1, function(x) !all(x < 0.2)),])

##Plot results
pheatmap(mapping_result_filtered,show_rownames=T, cex = 1,   fontsize = 10,border_color=NA,cellheight = 10, filename=sub('\\.csv$', '.pdf', path))

##write raw and filterd tables##
write.csv(mapping_result, file = sub('\\.csv$', '_Genes_raw.csv', path))
write.csv(mapping_result_filtered, file = sub('\\.csv$', '_Genes_cutoff_20.csv', path))

##count occurrence of genes based on min. coverage##
mapping_result_count<-as.matrix(mapping_result)
for (i in c(0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9)){ 
  mapping_result_count <- cbind(mapping_result_count, rowSums(mapping_result > i))
}
colnames(mapping_result_count)[4:12] <- c("> 0.1", "> 0.2", "> 0.3", "> 0.4", "> 0.5", "> 0.6", "> 0.7", "> 0.8", "> 0.9")

##write occurrence table##
write.csv(mapping_result_count, file = sub('\\.csv$', '_Genes_count.csv', path))

sink()