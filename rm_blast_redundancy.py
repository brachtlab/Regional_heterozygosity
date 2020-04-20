#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv

inHandle=open("%s"%argv[1],"r")
outHandle=open("%s_removeRedundant.txt"%argv[1],"w")
Dict={}
x=0
for line in inHandle:
	ident='%s_%s'%(line.split()[0],line.split()[1])
	if Dict.has_key(ident):
		pass
	else:
		x+=1
		outHandle.write(line)
		Dict[ident]=1
print "%s non-redundant entries."%x
inHandle.close()
outHandle.close()
