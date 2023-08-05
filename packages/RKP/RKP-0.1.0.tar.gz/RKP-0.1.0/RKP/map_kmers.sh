#!/usr/bin/env bash
###################################################################
#Script Name	:map_kmers.sh
#Description	:Maps hybrid k-mers to a reference genome and 
#                calculates coverage of genes. Uses esearch to get 
#                locus_tag and returns bed file with genes.
#Args           :<acceptor genome fasta file> <acceptor file> <list of kmers>
#                <name> <hybrid genome> <output> <threads>
#Dependecies    :conda env -n  map_kmers bowtie2 bedtools entrez-direct 
#                seqkit bedops blast samtools
#                conda activate map_kmers 
#Author       	:Felix Hartkopf
#Email         	:hartkopff@rki.de
###################################################################

# Arguments
genomeAcceptorRef=$1
gffAcceptorRef=$2
kmers=$3
name=$4
genomeHybrid=$5
output=$6
threads=${7}

echo "INFO - Reference acceptor genome $genomeAcceptorRef" >> $output"/RKP.log" 
echo "INFO - Reference acceptor gff $gffAcceptorRef" >> $output"/RKP.log" 

kmerlength=$(grep -v ">" $kmers | head -1 | wc -c)
kmerlength=$(python -c "print($kmerlength-1)")
echo "INFO - Detected kmerlength: "$kmerlength >> $output"/RKP.log" 

dir=$(dirname "${kmers}")

# Map kmers to genome
echo "INFO - Bowtie2 version: " $(bowtie2 --version | tr -d '\0' ) >> $output"/RKP.log" 
bowtie2-build --threads $threads $genomeAcceptorRef $genomeAcceptorRef >> $output"/RKP.log" 2>&1
bowtie2 --threads $threads -x $genomeAcceptorRef -f $kmers  -L $kmerlength -N 0 -R 3 -D 2 -S "$dir/${name}.sam" >> $output"/RKP.log" 2>&1

echo "INFO - $dir/${name}.sam" >> $output"/RKP.log" 
echo "INFO - $dir/${name}.bam" >> $output"/RKP.log" 

echo "INFO - Bowtie2 version: $(bowtie2 --version | tr -d '\0' )" >> $output"/RKP.log" 
# Only consider exact unique matches
echo "INFO - Samtools version: " $(samtools --version | tr -d '\0' ) >> $output"/RKP.log" 
samtools view -bS -q 42 "$dir/${name}.sam" > "$dir/${name}.bam" 

# Sort bam
samtools sort "$dir/${name}.bam" -o "$dir/${name}_sorted.bam" 

# Index bam
samtools index "$dir/${name}_sorted.bam" 

# Convert gff to bed
echo "INFO - gff2bed " $(gff2bed --version | grep version: | tr -d '\0' ) >> $output"/RKP.log" 
gff2bed < "$gffAcceptorRef" > "$dir/$name.bed"

# Calculate per base coverage
echo "INFO - bedtools version: " $(bedtools --version | tr -d '\0' ) >> $output"/RKP.log" 
bedtools coverage -a "$dir/$name.bed" -b "$dir/${name}_sorted.bam" > "$dir/${name}_coverage.bed"

# Get mapped features
awk  -F "\t" '{ if ($11 != 0) { print } }' "$dir/${name}_coverage.bed" > "$dir/${name}_coverage_non_zero.bed"

# Only genes
awk  -F "\t" '{ if ($8 == "gene") { print } }' "$dir/${name}_coverage_non_zero.bed" > "$dir/${name}_coverage_non_zero_genes.bed"

# Sort by coverage
sort -t$'\t' -k14 -nr "$dir/${name}_coverage_non_zero_genes.bed" > "$dir/${name}_coverage_non_zero_genes_sorted.bed"

# Grep locus tag
grep -oP  '(?<=locus_tag=).\S*(?=\t)' "$dir/${name}_coverage_non_zero_genes_sorted.bed" > "$dir/${name}_locus_tags.txt"

# Insert locus tag
IFS=$'\n'; for p in $(cat "$dir/${name}_locus_tags.txt"); do
   grep $p "$dir/${name}_coverage_non_zero_genes_sorted.bed" | perl -ne 'print "'"$p"'\t$_"' >> "$dir/${name}_coverage_non_zero_genes_sorted_locus_tmp.bed"
done

# Get sequences of reference
awk -v OFS="\t" -F"\t" '{print $2,$3,$4,$1,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15}' "$dir/${name}_coverage_non_zero_genes_sorted_locus_tmp.bed" > "$dir/${name}_coverage_non_zero_genes_sorted_locus.bed"
rm "$dir/${name}_coverage_non_zero_genes_sorted_locus_tmp.bed"
bedtools getfasta  -fi $genomeAcceptorRef -bed "$dir/${name}_coverage_non_zero_genes_sorted_locus.bed" -name -fo $dir/${name}_seq_ref.fasta

# Create blast db for second genome
echo "INFO - Blastn version: " $(blastn -version | head -n 1 | tr -d '\0' ) >> $output"/RKP.log" 
makeblastdb -in $genomeHybrid*.ffn -out $dir/${name}.db -dbtype 'nucl' -hash_index >> $output"/RKP.log" 2>&1

# Run blast
echo "INFO - "$name >> $output"/RKP.log" 
blastn -query $dir/${name}_seq_ref.fasta -task blastn -db $dir/${name}.db -out $dir/${name}_blast_filtered.tsv -num_threads $threads -qcov_hsp_perc 70 -outfmt 6 -evalue 0.01 >> $output"/RKP.log" 2>&1

# Only keep best blast hit
sort -k1,1 -k12,12nr -k11,11n  $dir/${name}_blast_filtered.tsv | sort -u -k1,1 --merge > $dir/${name}_blast_filtered_best.tsv

# Extract blast sequences and write them in fasta file
for f in $(cut -d$'\t' -f2 $dir/${name}_blast_filtered_best.tsv); do awk -v seq=${f} -v RS='>' '$1 == seq {print RS $0}' $genomeHybrid*.ffn; done  > $dir/${name}_iso_seq.fasta

# Extract key to value table
awk -v OFS="\t" -F"\t" '{print $2, $1}' $dir/${name}_blast_filtered_best.tsv > $dir/${name}_locus_ids.txt

# Add reference loci to header of fasta
seqkit replace -p "^(\w+) " -r '{kv}|${1} ' -k $dir/${name}_locus_ids.txt ${dir}/${name}_iso_seq.fasta --keep-key --threads $threads --out-file ${dir}/${name}_iso_seq_seqkit.fasta >> $output"/RKP.log" 2>&1
rm -f ${dir}/${name}_iso_seq.fasta
mv ${dir}/${name}_iso_seq_seqkit.fasta  ${dir}/${name}_iso_seq.fasta