#!/usr/bin/env bash
###################################################################
#Script Name	:create_kmers.sh
#Description	:Uses KMC 3 to create kmers of genomes and maps
#                them afterwards using map_kmers.sh. A and C are
#		 		 original species and B is a hybrid of A and C.
#Args           :<genome dir acceptor> <genome dir hybrid> 
#				 <genome dir donor> <kmerlength> <tresholdAcceptor> 
#				 <tresholdDonor> <acceptor reference fasta>
#		 		 <acceptor reference gff> <output> <threads>
#Dependecies    :conda env -n  kmc kmc seqkit bowtie2 bedtools  
#                seqkit bedops blast samtools
#                conda activate kmc
#Author       	:Lennard Epping; Felix Hartkopf
#Email         	:eppingl@rki.de; hartkopff@rki.de
###################################################################

# Arguments
dirAcceptor=$1
dirHybrid=$2
dirDonor=$3
kmerlength=$4
tresholdAcceptor=$5
tresholdDonor=$6
mapAcceptorFasta=$7
mapAcceptorGff=$8
output=$9
threads=${10}

baseAcceptor=$output/$(basename $dirAcceptor)/
baseHybrid=$output/$(basename $dirHybrid)/
baseDonor=$output/$(basename $dirDonor)/

mkdir $baseAcceptor
mkdir $baseHybrid
mkdir $baseDonor

# Define samplesdir
find $dirAcceptor -mindepth 1 -maxdepth 1 -printf '%Ts %p\n' | sort -n | cut -d ' ' -f2- | grep ".fna$\|.fna.gz$\|.fasta$\|.fasta.gz$\|.fa.gz$\|.fa$"  > ${baseAcceptor}inputset.txt
find $dirHybrid -mindepth 1 -maxdepth 1 -printf '%Ts %p\n' | sort -n | cut -d ' ' -f2- | grep ".fna$\|.fna.gz$\|.fasta$\|.fasta.gz$\|.fa.gz$\|.fa$"  > ${baseHybrid}inputset.txt
find $dirDonor -mindepth 1 -maxdepth 1 -printf '%Ts %p\n' | sort -n | cut -d ' ' -f2- | grep ".fna$\|.fna.gz$\|.fasta$\|.fasta.gz$\|.fa.gz$\|.fa$"  > ${baseDonor}inputset.txt

echo "INFO - acceptor genomes: "$(cat  ${baseAcceptor}inputset.txt | tr '\n' ' ')  | tee -a $output"/RKP.log" 
echo "INFO - hybrid genomes: "$(cat  ${baseHybrid}inputset.txt | tr '\n' ' ')  | tee -a $output"/RKP.log" 
echo "INFO - donor genomes: "$(cat  ${baseDonor}inputset.txt | tr '\n' ' ')  | tee -a $output"/RKP.log" 

## Build kmc databases##
# 5% cutoff
thresholdAcceptorRel=$(wc -l < ${baseAcceptor}"inputset.txt")
thresholdDonorRel=$(wc -l < ${baseDonor}"inputset.txt")
thresholdAcceptorRel=$(python -c "print($thresholdAcceptorRel*$tresholdAcceptor)")
thresholdDonorRel=$(python -c "print($thresholdDonorRel*$tresholdDonor)")


echo "K-mer threshold for acceptor genomes is calculated: "$thresholdAcceptorRel
echo "K-mer hreshold for donor genomes is calculated: "$thresholdDonorRel

echo "INFO - KMC version: " $(kmc -v | head -n 1 ) >> $output"/RKP.log" 
echo "INFO - KMC path: " $(which kmc)  >> $output"/RKP.log" 

echo "INFO - Calculate k-mers for acceptor genomes with cutoff at "$tresholdAcceptor" -> "$thresholdAcceptorRel" genomes" | tee -a $output"/RKP.log" 
kmc -k$kmerlength -t$threads -ci$thresholdAcceptorRel -fm @${baseAcceptor}inputset.txt ${baseAcceptor}kmer_db ${baseAcceptor} >> $output"/RKP.log" 2>&1
#95% cutoff
echo "INFO - Calculate k-mers for donor genomes with cutoff at "$tresholdDonor" -> "$thresholdDonorRel" genomes" | tee -a $output"/RKP.log" 
kmc -k$kmerlength -t$threads -ci$thresholdDonorRel -fm @${baseDonor}inputset.txt ${baseDonor}kmer_db ${baseDonor} >> $output"/RKP.log" 2>&1

# Calulate intersection between donor and hybrids and subtract acceptor k-mers. After that dump sequences to text file
echo "Calculate k-mer intersections for hybrid, donor and acceptor genomes"
res=$(cat ${baseHybrid}inputset.txt | wc -l)
echo "Found $res hybrid genomes to process"
i=1
IFS=$'\n'; for f in $(cat ${baseHybrid}inputset.txt); do
	# Processbar
	echo -n "["
    for ((j=0; j<i; j++)) ; do echo -n ' '; done
    	echo -n '=>'
    for ((j=i; j<$res; j++)) ; do echo -n ' '; done
    	echo -n "] $i / $res $file" $'\r'
    ((i++))

	fout=${f%.*}
	echo "INFO - Calculate k-mers for hybrid genome "$fout >> $output"/RKP.log" 
	kmc -k$kmerlength -ci1 -fm ${f} ${baseHybrid}${fout##*/}_kmers ${baseHybrid}  -t$threads >> $output"/RKP.log" 2>&1
	echo "Intersection of hybrid and donor "$fout >> $output"/RKP.log" 
	kmc_tools simple ${baseHybrid}${fout##*/}_kmers ${baseDonor}kmer_db intersect ${baseHybrid}${fout##*/}_intersectDonor  >> $output"/RKP.log" 2>&1
	echo "Substract acceptor k-mers of intersection of hybrid and donor "$fout >> $output"/RKP.log" 
    kmc_tools simple ${baseHybrid}${fout##*/}_intersectDonor ${baseAcceptor}kmer_db kmers_subtract ${baseHybrid}${fout##*/}_subtractAcceptor >> $output"/RKP.log" 2>&1
    echo "Dump results to text file "$fout >> $output"/RKP.log" 
	kmc_tools transform ${baseHybrid}${fout##*/}_subtractAcceptor dump ${baseHybrid}${fout##*/}_final.txt >> $output"/RKP.log" 2>&1
done

##map kmers##
codepath=$(dirname $0)
echo "Map k-mers to acceptor reference genome"
res=$(find ${baseHybrid}*final.txt | wc -l)
echo "Found $res hybrid genomes to process"
i=1
for f in ${baseHybrid}*final.txt ; do
	# Processbar
	echo -n "["
    for ((j=0; j<i; j++)) ; do echo -n ' '; done
    echo -n '=>'
    for ((j=i; j<$res; j++)) ; do echo -n ' '; done
    echo -n "] $i / $res $file" $'\r'
    ((i++))

	# Run map_kmers.sh
	awk '{printf("%.0f %s\n", NR, $0)}' $f | awk '{print ">kmer_" $1 ";counts:" $3 "\n" $2}' > $(echo "$f" | sed -e 's/\.[^.]*$//')".fasta"
	genomeHybrid=$dirHybrid/$(basename "$f" _final.txt)
	bash $codepath/map_kmers.sh $mapAcceptorFasta $mapAcceptorGff $(echo "$f" | sed -e 's/\.[^.]*$//')".fasta" $(basename $f _final.txt) $genomeHybrid $output $threads
done


