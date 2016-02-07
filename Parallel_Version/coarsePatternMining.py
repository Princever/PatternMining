#coding=utf-8
__author__ = 'Prince'


import numpy as np
import copy
import time
from util import *

# def groupCategory(database):
# 	""" --- no necessary --- """
# 	return

# def generateCombination(currentCombination, currentPattern, places):
#     resultSet = []
#     pattern = currentPattern[:]
#     if currentPattern == []:
#         return [currentCombination]
#     else:
#         nextPlace = pattern.pop(0)
#         for eachCertainPlace in places[nextPlace[0]]:
#             lenthPlueOneCombination = currentCombination[:]
#             lenthPlueOneCombination.append([eachCertainPlace['name']])
#             generated = generateCombination(lenthPlueOneCombination, pattern, places)
#             resultSet.extend(generated)
#         return resultSet

# def generateCombinationWithTime(currentCombination, currentPattern, places):
#     resultSet = []
#     pattern = currentPattern[:]
#     # print 'currentPattern:',currentPattern,' Type:',type(currentPattern)
#     if currentPattern == []:
#         # print currentCombination
#         return [currentCombination]
#     else:
#         nextPlace = pattern.pop(0)
#         # print places
#         for eachCertainPlace in places[nextPlace[0]]:
#             lenthPlueOneCombination = currentCombination[:]
#             # if lenthPlueOneCombination == []:
#             # print 'place:',eachCertainPlace
#             if lenthPlueOneCombination == [] or lenthPlueOneCombination[-1]['time'] < eachCertainPlace['time']:
#                 lenthPlueOneCombination.append(eachCertainPlace)
#                 generated = generateCombinationWithTime(lenthPlueOneCombination, pattern, places)
#             else:
#                 generated = None
#             if generated is not None:
#                 resultSet.extend(generated)
#         if resultSet == []:
#             return None
#         else:
#             return resultSet

# def compactInfo(record):
#     info = []
#     for each in record['data']:
#         compactInfo = {'place':each['place']['name'], 'time':each['time']}
#         info.append(compactInfo)
#     return info

# def cutByDeltaT(record, deltaT):
#     # print record
#     result = []
#     tmp = []
#     ptime = 0
#     for eachPlace in record['data']:
#         ntime = eachPlace['time']
#         if ntime - ptime > deltaT:
#             result.append(tmp)
#             tmp = []
#         tmp.append([eachPlace['place']['name']])
#         ptime = ntime
#     result.append(tmp)
#     return result

# def isInSeqWithTime(nseq,tseq,deltaT):
#     # print nseq
#     fixedRecords = cutByDeltaT(tseq, deltaT)

#     for anySeq in fixedRecords:
#         if isContained(nseq, anySeq):
#             # print 'yes',nseq,anySeq
#             return True
#     # print 'no'
    # return False

    # allPossibleSeq = []
    # record = compactInfo(tseq)
    # places = {}
    # for eachItem in nseq:
    #     places.setdefault(eachItem[0], [])
    #     for each in record:
    #         if each['place'] == eachItem[0]:
    #             places[eachItem[0]].append(each)
    # allPossibleSeq = generateCombinationWithTime([], nseq, places)

    # # print allPossibleSeq
    # if allPossibleSeq == None:
    #     return False

    # maxTimeGaps = []

    # for eachCandidate in allPossibleSeq:
    #     maxTimeGap = 0
    #     count = 0
    #     for each in eachCandidate:
    #         count += 1
    #     timeGaps = []
    #     for i in range(0, count-1):
    #         timeGaps += [eachCandidate[i+1]['time'] - eachCandidate[i]['time']]
    #     maxTimeGap = max(timeGaps)

    #     maxTimeGaps += [maxTimeGap]

    # minMaxTimeGap = min(maxTimeGaps)

    # if minMaxTimeGap < deltaT:
    #         return True
    # else:
    #         return False

def converToPoint(record, allPlaces):
	matrix = []
	for eachPlace in record:
		# print allPlaces
		coordinates = [float(allPlaces[eachPlace[0]]['loc']['x']),float(allPlaces[eachPlace[0]]['loc']['y'])]
		matrix.append(coordinates)
	return np.array(matrix)

def generateSnippets(allPatterns, allPlaces):
    coarsePattern = []


    for eachPattern in allPatterns:
        pattern = {'pattern':eachPattern.squence, 'snippets':[]}
        for eachSnippet in eachPattern.snippets:
            snippet = {'snippet':eachSnippet['snippet'], 'mat':converToPoint(eachSnippet['snippet'], allPlaces), 'weight':eachSnippet['weight']}
            pattern['snippets'].append(snippet)
        coarsePattern.append(pattern)

    return coarsePattern














