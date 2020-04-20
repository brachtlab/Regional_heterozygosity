#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
x=0
lenlist=[]
genome_handle=open('%s'%argv[1], 'r')
for seq_record in SeqIO.parse(genome_handle, 'fasta'):
        x= x+len(seq_record.seq)
        lenlist.append(len(seq_record.seq))
genome_handle.close()
lenlist.sort()
print "shortest contig is"
print lenlist[0]
lenlist.sort(reverse=True)
print "longest contig is"
print lenlist[0]
print "total genome length is"
print sum(lenlist)
print "The number of scaffolds in the assembly"
print len(lenlist)

total_genome_length=sum(lenlist)
running_length=0
for item in lenlist:
        running_length=running_length+item
        if running_length >= (total_genome_length/2):
                print "N50 is"
                print item
                break

