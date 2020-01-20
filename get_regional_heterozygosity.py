#!/usr/bin/env python
import sys
from sys import argv
from decimal import Decimal
#./get_regional_heterozygosity.py <genome_coordinates_file> <vcf>

coordHandle=open('%s'%argv[1],'r')
outHandle=open('%s_heterozygosity.txt'%argv[1],'w')
univeralHandle=open('combined_heterozygosity_results.txt','a')
coordDict={}
snp_number=0
summed_regional_len=0
for line in coordHandle:
	contig=line.split()[0]
	start=int(line.split()[1])
	stop=int(line.split()[2])
	summed_regional_len+=stop-start
	vcfHandle=open('%s'%argv[2],'r')
	vcfHandle.next()#skip header
	for line in vcfHandle:
		if line[:1]!='#':
			vcontig=line.split()[0]
			vposition=int(line.split()[1])
			if vcontig==contig:
				if vposition > stop:#we're past it
        	                        break
				else:	
					if start <= vposition <= stop:
						snp_number+=1
	vcfHandle.close()			
het=float(snp_number)/float(summed_regional_len)
print '{:.3e}'.format(het)
heterozygosity='{:.3e}'.format(het)


print 'snps %s summed len %s regional heterozygosity %s'%(snp_number,summed_regional_len,heterozygosity)
outHandle.write('%s\t%s\t%s\n'%(snp_number,summed_regional_len,heterozygosity))
univeralHandle.write('%s\t%s\t%s\t%s\n'%(snp_number,summed_regional_len,heterozygosity,argv[1]))
coordHandle.close()
outHandle.close()
