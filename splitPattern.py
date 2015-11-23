#coding=utf-8
__author__ = 'Prince'

import numpy as np
import math
import copy

def distance(point1, point2):
	tmp = point1 - point2
	distance = np.linalg.norm(tmp,ord=None)
	return distance

# def converToPoint(snippet):
# 	matrix = []
# 	for eachPlace in snippet['objects'][0]['data']:
# 		coordinates = [int(eachPlace['place']['loc']['x']),int(eachPlace['place']['loc']['y'])]
# 		matrix.append(coordinates)
# 	return np.array(matrix)

def findPointsInRange(snippets, center, bandwidth, dampeningfactor):
	pointsInRange = []
	for eachSnippet in snippets:
		if distance(eachSnippet['mat'], center) <= max(bandwidth, math.sqrt(2) * dampeningfactor * bandwidth):
			pointsInRange.append(eachSnippet)
	return pointsInRange

def findNewCenter(pointSet):
	tmpMat = 0
	theSum = 0
	for eachPoint in pointSet:
		theSum += eachPoint['weight']
		tmpMat += eachPoint['weight'] * eachPoint['mat']
	tmpMat /= float(theSum)
	return tmpMat

def findInS(newCenter, gammaS):
	alreadyIn = False
	for cluster in gammaS:
		if distance(cluster['center'], newCenter) == 0:
			alreadyIn = True
			break
	return alreadyIn

def weightedSnippetShift(snippets, bandwidth, dampeningfactor):
	# epsilon = 0
	gammaS = []
	for eachSnippet in snippets:
		center = []
		k = 0
		# print eachSnippet
		center.append(eachSnippet['mat'])
		while True:
			pointSet = findPointsInRange(snippets, center[k], bandwidth, dampeningfactor)
			newCenter = findNewCenter(pointSet)
			center.append(newCenter)
			if distance(center[k + 1], center[k]) == 0:
				alreadyIn = findInS(newCenter, gammaS)
				if not alreadyIn :
					aCluster = {'center':center[k + 1], 'points':pointSet}
					gammaS.append(aCluster)
				break
			k = k + 1
	return gammaS

def supOf(cluster):
	sup = 0
	# print cluster
	for eachSnippet in cluster['points']:
		sup += eachSnippet['weight']
	return sup

def varOf(cluster):
	sumX2 = 0
	sumX = 0
	count += 0
	for eachSnippet in cluster['points']:
		sumX += eachSnippet['mat']
		sumX2 += np.dot(eachSnippet['mat'].T, eachSnippet['mat'])
		count += 1
	var = sumX2/float(count) - np.dot(sumX/float(count).T, sumX/float(count))

# def	gammaCommunities(gammaS, gamma):


def splitPattern(snippets, supthreshold, varthreshold, bandwidth, dampeningfactor):
	fineGrainedPatterns = []
	gammaS = weightedSnippetShift(snippets, bandwidth, dampeningfactor)
	for eachSi in gammaS:
		# if supOf(eachSi) >= supthreshold and varOf(eachSi) <= varthreshold:
		if True:
			fineGrainedPatterns.append(eachSi)
			gammaS.remove(eachSi)          

	# gamma = math.sqrt(2) * dampeningfactor * bandwidth
	gammaC = copy.deepcopy(gammaS)

	for eachCi in gammaC:
		if supOf(eachSi) >= supthreshold:
			result = splitPattern(eachCi, supthreshold, varthreshold, dampeningfactor * bandwidth, dampeningfactor)
			if result != []:
				fineGrainedPatterns.append(result)

	return fineGrainedPatterns