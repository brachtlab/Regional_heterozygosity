#!/usr/bin/env python
import sys
from sys import argv
from decimal import Decimal
#./get_regional_depth.py <genome_coordinates_file> <depthfile.txt>

coordHandle=open('%s'%argv[1],'r')
#outHandle=open('%s_regional_depth2.txt'%argv[1],'w')
univeralHandle=open('combined_depth_results2.txt','a')
coordDict={}
summed_depth=0
summed_regional_len=0
c=0
d=0
for line in coordHandle:
	c+=1
	contig=line.split()[0]
	start=int(line.split()[1])
	stop=int(line.split()[2])
	tuple=[start,stop]
	if coordDict.has_key(contig):
		l=coordDict[contig]
		l.append(tuple)
		coordDict[contig]=l
	else:
		newlist=[]
		newlist.append(tuple)
		coordDict[contig]=newlist

print coordDict
depthHandle=open('%s'%argv[2],'r')
for line in depthHandle:
	d+=1
	if line[:1]!='#':
		dcontig=line.split()[0]
		dposition=int(line.split()[1])
		basedepth=int(line.split()[2])
		if coordDict.has_key(dcontig):
			coordslist=coordDict[dcontig]
			for t in coordslist:
				cstart=t[0]
				cstop=t[1]
				if cstart <= dposition <= cstop:
					print '%s	%s	%s	%s'%(dcontig,dposition,cstart,cstop)
					summed_regional_len+=1
					summed_depth+=basedepth
depthHandle.close()

regional_depth=float(summed_depth)/float(summed_regional_len)
print '{:.3e}'.format(regional_depth)
formatted_regional_depth='{:.3e}'.format(regional_depth)


print 'summed coverage %s summed len %s regional regional_depth %s'%(summed_depth,summed_regional_len,formatted_regional_depth)
#outHandle.write('%s\t%s\t%s\n'%(summed_depth,summed_regional_len,formatted_regional_depth))
univeralHandle.write('%s\t%s\t%s\t%s\n'%(summed_depth,summed_regional_len,formatted_regional_depth,argv[1]))
coordHandle.close()
#outHandle.close()
