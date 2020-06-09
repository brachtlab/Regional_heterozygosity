#!/usr/bin/python
from Bio import SeqIO
import sys
from sys import argv
#getRef.py <outfmt 6> 
outHandle=open("Ref_only_%s.txt"%argv[1],'w')
genome_handle=open("%s"%argv[1],"r")
for line in genome_handle:
	ident=line.split()[0]
	if 'ref|' in ident:
		outHandle.write(line)
		
genome_handle.close()
outHandle.close()
