#!/usr/bin/env python
from Bio import SeqIO
import sys
from sys import argv
inHandle=open('%s'%argv[1],'r')
tDict={}
oldQuery='initial'
f=0#fragmented counts
d=0#duplicate counts
m=0#match counts
resultsDict={}
assemblies_list=['p1','p3','p5','p7','p10','p15','p20','p30','s23','s47','s63','ref']
for assembly in assemblies_list:
	resultsDict[assembly]={}
for line in inHandle:
	target=line.split()[1]
	query=line.split()[0]
	start=int(line.split()[6])
	stop=int(line.split()[7])
	if int(start)>int(stop):
		print 'reversed found: %s'%line
	t='%s_%s_%s'%(target,start,stop)
	if query == oldQuery:
		if tDict.has_key(t):
			print 'duplicate found, query %s oldquery %s dict query %s target %s'%(query,oldQuery,tDict[t],t)
		tDict[t]=query			
	else: #new query 
		discount=0
		keys=tDict.keys()
		#print 'for %s, tDict was:'%oldQuery
		#print tDict
		tqDict={}
		refmatch=0
		for item in keys:
			name=item.split('_')[0]
			if 'ref|' in name:
				if name != oldQuery:#indicates paralogy only if ref contig is not the self-self match.
					discount =1 #note that self-self matches still get through.
			#print 'discount is %s'%discount
			assembly=name.split('|')[0]
			if assembly=='ref':
				if discount ==0:#chieck for paralogy
					refmatch=1
			tstart=int(item.split('_')[1])
			tstop=int(item.split('_')[2])
			interval=[tstart,tstop]
			if tqDict.has_key(assembly):
				tqDict[assembly].append(interval)
			else:
				tqDict[assembly]=[interval]
		if refmatch==0 and discount==0:
			print 'an example case without self-self match'
			for item in keys:
				print '%s	%s'%(item,tDict[item])
			print '----end---'
		if discount==0:#now just go through ordered tq matches and look for non-overlapping.		
			k = tqDict.keys()
			for assembly in k:
				intervals=tqDict[assembly]
				intervals.sort()
				#print 'intervals are %s'%intervals
				local_d=0
				local_f=0
				local_m=0
				if len(intervals)>1:
					last_end=0
					for i in intervals:#now just checking if last end is greater than next start, overlap!
						end=i[1]
						start=i[0]
						if last_end<=start and last_end !=0:#gap, so is fragmented
							local_f+=1
							#print 'start is %s and last end is %s so is fragmented'%(start,last_end)
						else: #overlap, so is duplicated
							local_d+=1
							#print 'start is %s and last end is %s so is duplicated'%(start,last_end)
						last_end=end
					local_m=1
					local_d=local_d-1#correct for one being 'right'
				else:
					#print 'single interval for assembly so is a match.'
					local_m=1
				#print 'for assembly %s'%assembly
				#print 'intervals are %s'%intervals
				#print 'local_m is %s'%local_m
				#print 'local_d is %s'%local_d
				#print 'local_f is %s'%local_f
				if resultsDict.has_key(assembly):
					if resultsDict[assembly].has_key('d'):
						resultsDict[assembly]['d']+=local_d
					else:
						resultsDict[assembly]['d']=local_d
					if resultsDict[assembly].has_key('m'):
                                                resultsDict[assembly]['m']+=local_m
                                        else:
                                                resultsDict[assembly]['m']=local_m
					if resultsDict[assembly].has_key('f'):
                                                resultsDict[assembly]['f']+=local_f
                                        else:
                                                resultsDict[assembly]['f']=local_f
				else:
					resultsDict[assembly]['d']=local_d #add it
					resultsDict[assembly]['m']=local_m
					resultsDict[assembly]['f']=local_f

				d=d+local_d
				f=f+local_f
				m=m+local_m					
		tDict={}
		tDict[t]=oldQuery
	oldQuery=query

#now, rescue the last set of matches when you fall off the end.
discount=0
keys=tDict.keys()
tqDict={}
for item in keys:
	name=item.split('_')[0]
        if 'ref|' in name:
        	if name != oldQuery:#indicates paralogy only if ref contig is not the self-self match.
                	discount =1
	assembly=name.split('|')[0]
	tstart=int(item.split('_')[1])
        tstop=int(item.split('_')[2])
        interval=[tstart,tstop]
        if tqDict.has_key(assembly):
        	tqDict[assembly].append(interval)
        else:
                tqDict[assembly]=[interval]

        if discount==0:#now just go through ordered tq matches and look for non-overlapping.
        	k = tqDict.keys()
                for assembly in k:
                	intervals=tqDict[assembly]
                        intervals.sort()
                        local_d=0
                        local_f=0
                        local_m=0
			if len(intervals)>1:
                        	last_end=0
				for i in intervals:#now just checking if last end is greater than next start, overlap!
                                	end=i[1]
                                        start=i[0]
                                        if last_end<=start and last_end !=0:#gap, so is fragmented
                                        	local_f+=1
					else: #overlap, so is duplicated
                                        	local_d+=1
                                        last_end=end
				local_m=1
                                local_d=local_d-1#correct for one being 'right'

			else:
				local_m=1
			if resultsDict.has_key(assembly):
                        	if resultsDict[assembly].has_key('d'):
                                	resultsDict[assembly]['d']+=local_d
				else:
					resultsDict[assembly]['d']=local_d
                                if resultsDict[assembly].has_key('m'):
                                        resultsDict[assembly]['m']+=local_m
                                else:
                                        resultsDict[assembly]['m']=local_m
                                if resultsDict[assembly].has_key('f'):
                                        resultsDict[assembly]['f']+=local_f
                                else:
					resultsDict[assembly]['f']=local_f
			else:
				resultsDict[assembly]['d']=local_d #add it
                                resultsDict[assembly]['m']=local_m
                                resultsDict[assembly]['f']=local_f

			d=d+local_d
                        f=f+local_f
                        m=m+local_m

print 'total blast matches counted: %s'%(d+f+m)
print 'total duplicated: %s'%d
print 'total fragmented: %s'%f
print 'total correctly matching: %s'%m
print resultsDict
a=resultsDict.keys()
outHandle=open('%s_mdf_analysis.txt'%argv[1],'w')
outHandle.write('assembly\tmatching\tduplicated\tfragmented\n')
for assembly in a:
	if resultsDict[assembly]:
		outHandle.write('%s\t%s\t%s\t%s\n'%(assembly,resultsDict[assembly]['m'],resultsDict[assembly]['d'],resultsDict[assembly]['f']))
outHandle.close()  

inHandle.close()
