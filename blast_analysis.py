#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv

#./blast_analysis.py <query fasta> <blast_to_reference_outfmt6.txt> <percent identity to consider, as integer (like '98' for 98 %)>
pid_threshold=float(argv[3])
blastHandle=open("%s"%argv[2],"r")
queryHandle=open('%s'%argv[1],'r')
#diagnosticHandle=open('%s_%s.txt'%(argv[2],pid_threshold),'w')
subjectDict={}
queryDict={}
subject_running_total=0
subject_interval_sum=0
query_running_total=0
query_interval_sum=0
for line in blastHandle:#first, load dictionaries
	if line[:1]!='#':
		pid=float(line.split()[2])
        	if pid>=pid_threshold:
			contig=line.split()[1]
			qcontig=line.split()[0]
			start=int(line.split()[8])
			stop=int(line.split()[9])
			qstart=int(line.split()[6])
			qstop=int(line.split()[7])
			if start>stop:
				start=int(line.split()[9])
	        	        stop=int(line.split()[8])
			if qstart>qstop:
				qstart=int(line.split()[7])
				qstop=int(line.split()[6])
			tuple=[start,stop]
			qtuple=[qstart,qstop]
		#load the subject dict
			if subjectDict.has_key(contig):
				newlist=subjectDict[contig]
				newlist.append(tuple)
				subjectDict[contig]=newlist
			else:
				newlist=[]
				newlist.append(tuple)
				subjectDict[contig]=newlist
		#now do query dict too
			if queryDict.has_key(qcontig):
                                newlist=queryDict[qcontig]
                                newlist.append(qtuple)
                                queryDict[qcontig]=newlist
                        else:
                                newlist=[]
                                newlist.append(qtuple)
                                queryDict[qcontig]=newlist
#below is all for subject
contigs=subjectDict.keys()
m=0
n=0
for contig in contigs:
	intlist=subjectDict[contig]
	intlist.sort()
	firsttuple=intlist[0]
	marker=firsttuple[1]
	begin=firsttuple[0]
	x=0
	for interval in intlist:
		x+=1
		m+=1
		new_start=interval[0]
		new_stop=interval[1]
		subject_interval_sum+=new_stop-new_start
		if new_start<= marker:#new interval is overlapping
			if new_stop>marker:
				marker=new_stop #inching along
		elif new_start>marker:#new interval
			subject_running_total+=marker-begin#store previous interval
			n+=1
			begin=new_start
			marker=new_stop	
	subject_running_total+=marker-begin#store last interval
	n+=1

print '%s subject intervals found but compressed to %s nonredundant intervals'%(m,n)

#below is all for query
qcontigs=queryDict.keys()
j=0
k=0
for qcontig in qcontigs:
        intlist=queryDict[qcontig]
        intlist.sort()
	#print '%s	%s'%(qcontig,intlist)
        firsttuple=intlist[0]
        marker=firsttuple[1]
        begin=firsttuple[0]
        x=0
        for interval in intlist:
                x+=1
		j+=1
                new_start=interval[0]
                new_stop=interval[1]
                query_interval_sum+=new_stop-new_start
                if new_start<= marker:#new interval is overlapping
                        if new_stop>marker:
                                marker=new_stop #inching along
                elif new_start>marker:#new interval
                        query_running_total+=marker-begin#store previous interval
			#diagnosticHandle.write('%s	%s	%s\n'%(qcontig,begin,marker))
			k+=1
                        begin=new_start
                        marker=new_stop
        query_running_total+=marker-begin
	#diagnosticHandle.write('%s	%s	%s\n'%(qcontig,begin,marker))
	k+=1

print '%s query intervals found but %s nonredundant query intervals'%(j,k)
query_fasta_length=0
num=0
for seq_record in SeqIO.parse(queryHandle,'fasta'):
	query_fasta_length+=len(seq_record.seq)
	num+=1
print 'query FASTA length was %s bp from %s sequences'%(query_fasta_length,num)
print 'for matches at or equal %s percent identity threshold:'%pid_threshold
#print 'SUBJECT summed intervals was %s'%subject_interval_sum
#print 'SUBJECT non-redundant sum was %s'%subject_running_total
#print 'QUERY summed intervals was %s'%query_interval_sum
#print 'QUERY non-redundant sum was %s'%query_running_total

print 'query %s bp found in blast output, matching to %s total subject bp'%(query_running_total,subject_running_total)
print '%s percent of query was found in the blast output'%((float(query_running_total)/float(query_fasta_length))*100)
print 'matching query / subject was %s percent'%((float(query_running_total)/float(subject_running_total))*100)
print 'ratio of query length to reference length was %s'%((float(query_fasta_length)/float(subject_running_total)))
blastHandle.close()
queryHandle.close()
