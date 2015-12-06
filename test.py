#coding=utf-8
__author__ = 'Prince'

from dataPrepare import *
# from util import *
import numpy as np
import pylab as pl

# def getAllIndex(s,element):
#     indices = []
#     count = 0
#     for each in s:
#         if each == element:
#             indices += [count]
#         count += 1
#     return indices

# def generateCombination(currentCombination, currentPattern, places):
#     resultSet = []
#     pattern = currentPattern[:]
#     # print 'currentPattern:',currentPattern,' Type:',type(currentPattern)
#     if currentPattern == []:
#     	# print currentCombination
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
#     	# print currentCombination
#         return [currentCombination]
#     else:
#         nextPlace = pattern.pop(0)
#         # print places
#         for eachCertainPlace in places[nextPlace[0]]:
#             lenthPlueOneCombination = currentCombination[:]
#             # if lenthPlueOneCombination == []:
#             # print lenthPlueOneCombination[-1]
#             if lenthPlueOneCombination == [] or lenthPlueOneCombination[-1]['time'] < eachCertainPlace['time']:
#             	lenthPlueOneCombination.append(eachCertainPlace)
#             	generated = generateCombinationWithTime(lenthPlueOneCombination, pattern, places)
#             else:
#                 generated = None
#             if generated is not None:
#                 resultSet.extend(generated)
#         if resultSet == []:
#         	return None
#         else:
#         	return resultSet

# def compactInfo(record):
# 	info = []
# 	for each in record['data']:
# 		compactInfo = {'place':each['place']['name'], 'time':each['time']}
# 		info.append(compactInfo)
# 	return info

# def isInSeqWithTime(nseq,tseq,deltaT):
# 	allPossibleSeq = []
# 	record = compactInfo(tseq)
# 	places = {}
# 	for eachItem in nseq:
# 		places.setdefault(eachItem[0], [])
# 		for each in record:
# 			if each['place'] == eachItem[0]:
# 				places[eachItem[0]].append(each)
# 	allPossibleSeq = generateCombinationWithTime([], nseq, places)

# 	print allPossibleSeq

# 	maxTimeGaps = []

# 	for eachCandidate in allPossibleSeq:
# 		maxTimeGap = 0
# 		count = 0
# 		for each in eachCandidate:
# 			count += 1
# 		timeGaps = []
# 		for i in range(0, count-1):
# 			timeGaps += [eachCandidate[i+1]['time'] - eachCandidate[i]['time']]
# 		maxTimeGap = max(timeGaps)

# 		maxTimeGaps += [maxTimeGap]

# 	minMaxTimeGap = min(maxTimeGaps)

# 	if minMaxTimeGap < deltaT:
# 			return True
# 	else:
# 			return False

def converToPoint(snippet):
	matrix = []
	for eachPlace in snippet['objects'][0]['data']:
		coordinates = [int(eachPlace['place']['loc']['x']),int(eachPlace['place']['loc']['y'])]
		matrix.append(coordinates)
	return np.array(matrix)

def distance(point1, point2):
	tmp = point1 - point2
	distance = np.linalg.norm(tmp,ord=None)
	return distance


if __name__ == "__main__":

    gammaS = [{'points': [{'snippet': [['b'], ['s'], ['t']], 'mat': [[ 1, 14],[12, 12],[14, 30]], 'weight': 1}], 'center': [[ 1, 14],[12, 12],[14, 30]]}]
    eachSi = {'points': [{'snippet': [['b'], ['s'], ['t']], 'mat': [[ 1, 14],[12, 12],[14, 30]], 'weight': 1}], 'center': [[ 1, 14],[12, 12],[14, 30]]}
    # print gammaS
    # print eachSi

    # gammaS.remove(eachSi)
    # print gammaS

    amat = [[1, 14],[12, 12],[14, 30]]

    mat = np.array(amat)

    l = [x[0] for x in mat]

    color = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

    pl.plot([x[0] for x in mat], [x[1] for x in mat], color[3])# use pylab to plot x and y
    pl.plot([x[0] for x in mat], [x[1] for x in mat], color[3]+'o')    
    pl.show()

    print l

    print 7%7







