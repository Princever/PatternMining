#coding=utf-8
__author__ = 'Prince'

from dataPrepare import *
from prefixSpan import *
import sys
# import util as u
from util import *
from coarsePatternMining import *
from splitPattern import *

if __name__ == "__main__":
    database,places,allPlaces = dataPrepare()
    # for each in database:
    # 	print each
    deltaT = 180
    min_supp = 0.03#0.03 perfect, 0.01 for more potential, 0.05 is consist but not serious
    varthreshold = 2
    bandwidth = 20
    dampeningfactor = 0.5

    count = 0
    for each in database:
        count += 1
    patterns = prefixSpan(SquencePattern([], sys.maxint), database, deltaT, min_supp * count)
    print_patterns(patterns)
    seqNums = []
    for each in patterns:
        seqNums.append(each.squence)
    maxSeqs = maxSeq(seqNums)
    # print maxSeqs
    # print("The sequential patterns :")
    # for i in maxSeqs:
    #     for sth in i:
    #         print "[",
    #         for ssth in sth:
    #             print ssth,
    #         print "]",
    #     print ""
    # print places
    maxSeqsBackUp = maxSeqs[:]
    # for each in database:
    # 	print each
    coarsePatterns = generateSnippets(maxSeqs, places, database, deltaT, allPlaces)
    # for eachp in coarsePatterns:
    # 	print eachp['pattern']
    # 	for eachs in eachp['snippets']:
    # 		print eachs
    fineGrainedPatterns = []
    for eachPattern in coarsePatterns:
        tmpResult = splitPattern(eachPattern['snippets'], min_supp * count, varthreshold, bandwidth, dampeningfactor)
        if tmpResult != []:
        	fineGrainedPatterns.append(tmpResult)
    for eachPattern in fineGrainedPatterns:
        print 'A Pattern:',eachPattern

    drawPatterns(fineGrainedPatterns)











