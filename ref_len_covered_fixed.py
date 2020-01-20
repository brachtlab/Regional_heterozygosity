#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv

#./ref_len_covered_fixed.py <query.fasta> <blast_to_reference_outfmt6.txt>

blastHandle=open("%s"%argv[2],"r")
outHandle=open("fixed_OMEGA-nonredundant-blast-lengths_covered.txt","a")
fastaHandle=open('%s'%argv[1],'r')

queryLength=0
for seq_record in SeqIO.parse(fastaHandle,'fasta'):
	queryLength+=len(seq_record.seq)#store lengths

contigDict={}
running_total=0
interval_sum=0
for line in blastHandle:
	if line[:1]!='#':
		pid=float(line.split()[2])
        	if pid>=98:
			contig=line.split()[1]
			start=int(line.split()[8])
			stop=int(line.split()[9])
			if start>stop:
				start=int(line.split()[9])
	        	        stop=int(line.split()[8])
			tuple=[start,stop]
			if contigDict.has_key(contig):
				newlist=contigDict[contig]
				newlist.append(tuple)
				contigDict[contig]=newlist
			else:
				newlist=[]
				newlist.append(tuple)
				contigDict[contig]=newlist
contigs=contigDict.keys()
for contig in contigs:
	intlist=contigDict[contig]
	intlist.sort()
	firsttuple=intlist[0]
	marker=firsttuple[1]
	begin=firsttuple[0]
	x=0
	for interval in intlist:
		x+=1
		new_start=interval[0]
		new_stop=interval[1]
		interval_sum+=new_stop-new_start
		if new_start<= marker:#new interval is overlapping
			if new_stop>marker:
				marker=new_stop #inching along
		elif new_start>marker:#new interval
			running_total+=marker-begin#store previous interval
			begin=new_start
			marker=new_stop	
	running_total+=marker-begin#store last interval
ratio=float(queryLength)/float(running_total)
print 'ratio of lengths is %s'%ratio
outHandle.write("%s\t%s\t%s\t%s\t%s\n"%(argv[1],argv[2],ratio,queryLength,running_total))
blastHandle.close()
fastaHandle.close()
outHandle.close()
