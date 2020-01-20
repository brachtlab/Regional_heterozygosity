#!/usr/bin/env python
import sys
from sys import argv
from decimal import Decimal
from Bio import SeqIO
genomeHandle=open('%s'%argv[1],'r')
regionHandle=open('%s'%argv[2],'r')
outHandle=open('%s_genomic_sequence.fasta'%argv[2],'w')
genomeDict={}
for seq_record in SeqIO.parse(genomeHandle,'fasta'):
	genomeDict[seq_record.id]=seq_record.seq

for line in regionHandle:
	contig=line.split()[0]
	start=int(line.split()[1])
	stop=int(line.split()[2])
	outHandle.write('>%s_%s-%s\n%s\n'%(contig,start,stop,genomeDict[contig][start:stop]))

genomeHandle.close()
regionHandle.close()
outHandle.close()
