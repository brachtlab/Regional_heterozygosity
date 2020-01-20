#!/usr/bin/env python
import sys
from sys import argv
#./parse_genes.py <enriched_genes> <original_PatherScoreOutput> <total_genome_coordinate_file>
inHandle=open('%s'%argv[1],'r')
outHandle=open('%s_genomic_locations.txt'%argv[1],'w')
numberedgenes=[]
x=0
m=0
for line in inHandle:
	m+=1
	item=line.split()[1]
	print 'original: %s'%item
	if ',' in item:
		split=item.split(',')
		for j in split:
			x+=1
			numberedgenes.append(int(j))
			#print int(j)
	else:
		x+=1
		numberedgenes.append(int(item))
		#print item
print 'for %s lines found %s genes'%(m,x)
#print 'numberedgenes: %s'%numberedgenes
inHandle.close()
pantherHandle=open('%s'%argv[2],'r')
numberNameDict={}
x=0
for line in pantherHandle:
	x+=1
	name=line.split()[0]
	numberNameDict[x]=name

print '%s genes found in Panther assignment file'%x
#print numberNameDict	
pantherHandle.close()
genenames=[]
for num in numberedgenes:
	genenames.append(numberNameDict[num])

gffhandle=open('%s'%argv[3],'r')
coordDict={}
for line in gffhandle:
	start=int(line.split()[1])
	stop=int(line.split()[2])
	contig=line.split()[0]
	startstop=[contig,start,stop]
	name=line.split()[3]
	coordDict[name]=startstop
gffhandle.close()

for mRNA in genenames:
	l=coordDict[mRNA]
	start=l[1]
	stop=l[2]
	contig=l[0]
	outHandle.write('%s\t%s\t%s\t%s\n'%(contig,start,stop,mRNA))
outHandle.close()
