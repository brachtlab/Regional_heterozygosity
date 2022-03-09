#!/usr/bin/env python
import sys
from sys import argv
from Bio import SeqIO
from decimal import Decimal
#./get_total_heterozygosity.py <vcf> 

vcfHandle=open('%s'%argv[1],'r')
univeralHandle=open('total_heterozygosity_results.txt','a')
snp_number=0
total_len=0
for line in vcfHandle:
	if line[:1]!='#':
		#print line
		snp_number+=1
	if line[:8]=='##contig':
		le=line.split('length=')[1]
		leng=int(le.rstrip('>\n'))
		total_len+=leng
het=float(snp_number)/float(total_len)
print '{:.3e}'.format(het)
heterozygosity='{:.3e}'.format(het)
print 'snps %s summed len %s total heterozygosity %s'%(snp_number,total_len,heterozygosity)
univeralHandle.write('%s\t%s\t%s\t%s\n'%(snp_number,total_len,heterozygosity,argv[1]))
univeralHandle.close()
vcfHandle.close()
