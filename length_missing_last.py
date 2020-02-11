#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
refHandle=open("%s"%argv[1],"r")
lastHandle=open("%s"%argv[2],"r")
outHandle=open("%s_missing_lengths_fixed.txt"%argv[2],"w")
outHandle.write("contig\toriginal length\tlength missing\n")
lengthDict={}
subDict={}
contigDict={}
total_ref_length=0
for seq_record in SeqIO.parse(refHandle, "fasta"):
	seqlength=len(seq_record.seq)
	contig="%s"%seq_record.id
	lengthDict[contig]=seqlength
	total_ref_length+=seqlength
	subDict[contig]=seqlength
for line in lastHandle:
	if line[:1]!='#':
		contig=line.split()[1]
		start=int(line.split()[8])
		stop=int(line.split()[9])
		tuple=[start,stop]
		if contigDict.has_key(contig):
			newlist=contigDict[contig]
			newlist.append(tuple)
			contigDict[contig]=newlist
		else:
			newlist=[]
			newlist.append(tuple)
			contigDict[contig]=newlist
running_missing=0
Lkeys=lengthDict.keys()
keys=contigDict.keys()
for k in keys:
	intlist=contigDict[k]
	intlist.sort()
	firsttuple=intlist[0]
	old_stop=firsttuple[1]
	old_start=firsttuple[0]
	for interval in intlist:
		new_start=interval[0]
		new_stop=interval[1]
		if new_start-old_stop > 50:
			#interval subtraction
			interval_length=old_stop-old_start
			subDict[k]=subDict[k]-interval_length
			old_start=new_start
			old_stop=new_stop
		elif new_stop > old_stop:
			old_stop=new_stop
	interval_length=old_stop-old_start
	subDict[k]=subDict[k]-interval_length
	outHandle.write("%s\t%s\t%s\n"%(k, lengthDict[k], subDict[k]))
	running_missing=running_missing+subDict[k]
for l in Lkeys:
	if contigDict.has_key(l):
		pass
	else:
		running_missing=running_missing+lengthDict[l]
		#outHandle.write("%s\t%s\t%s\n"%(k, lengthDict[l], lengthDict[l]))
print "total missing"
print running_missing
print "total ref length"
print total_ref_length
outHandle.write("total missing\t-\t%s\n"%running_missing)
refHandle.close()
lastHandle.close()
outHandle.close()
