#!/usr/bin/python
from Bio import SeqIO
from scipy import stats
import numpy as np
import sys
from sys import argv
# ./get_protein_stats.py <*.all.maker.proteins.fasta> <output file prefix>
inHandle=open("%s"%argv[1], "r")
fastaHandle=open("%s"%argv[1], "r")
outHandle=open("%s_protein_stats.txt"%argv[2], "w")
outHandle.write("mean_evidence_prot_length\tmedian_evidence_prot_length\tstd_evidence_length\tmean_no_evidence_prot_length\tmedian_no_evidence_prot_length\tstd_no_evidence_length\tttest\n")
ElengthList=[]
NElengthList=[]
evidenceDict={}
noevidenceDict={}
#x is the total length of protein sequences with evidence
x=0
#w is number of proteins with evidence
w=0
#y is the total length of protein sequences without evidence
y=0
#z is number of proteins without evidence
z=0
for line in inHandle:
	if line.startswith('>'):
		proteinid=line.split()[0]
		protein=proteinid.split('>')[1]
		AED=line.split()[2]
		value=AED.split(':')[1]
		if value == "1.00":
			noevidenceDict[protein]=protein
		else:
			evidenceDict[protein]=protein

for seq_record in SeqIO.parse(fastaHandle, "fasta"):
	seqlength=len(seq_record.seq)
	proteinid='%s'%seq_record.id
	protein=proteinid.split()[0]
	if evidenceDict.has_key(protein):
		ElengthList.append(seqlength)
		x=x+seqlength
		w=w+1
	elif noevidenceDict.has_key(protein):
		NElengthList.append(seqlength)
		y=y+seqlength
		z=z+1

ElengthList.sort()
NElengthList.sort()
stdE=np.std(ElengthList, ddof=1)
stdNE=np.std(NElengthList, ddof=1)
ttest=stats.ttest_ind(NElengthList, ElengthList, equal_var=False)

outHandle.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\n"%(x/w, ElengthList[w/2], stdE, y/z, NElengthList[z/2], stdNE, ttest))

print "mean protein length with evidence"
print x/w
print "median protein length with evidence"
print ElengthList[w/2]
print "standard deviation with evidence" 
print stdE
print "mean protein length without evidence"
print y/z
print "median protein length without evidence"
print NElengthList[z/2]
print "standard deviation without evidence"
print stdNE
print "t-test"
print ttest

inHandle.close()
outHandle.close()
fastaHandle.close()
