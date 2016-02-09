#coding=utf-8
__author__ = 'Prince'

import csv
import numpy as np
import random

def read(filename):    #read and sort the places
    places = {}
    allPlaces = {}

    csvfilein = file(filename,'rb')
    reader = csv.reader(csvfilein)
    for parameters in reader:
        location = { 'x': parameters[1], 'y':parameters[2] } 
        newplace = { 'name': parameters[0], 'loc': location, 'category': parameters[3]}
        places.setdefault(newplace.get('category'),[])
        places[newplace.get('category')].append(newplace)
        allPlaces.setdefault(parameters[0], {'loc':location, 'category':parameters[3]})
    return places,allPlaces

def dataPrepare():	#genete datas
    filename = 'datas/places.csv'
    size = 10000
    ratio = 0.3
    minTimeConsistencyRatio = 2
    csvfileout = file('datas/trajectory.csv', 'wb')
    writer = csv.writer(csvfileout)
    places,allPlaces = read(filename)
    database = []
    setTrajectory = [['office','restaurant','gym'],['office','shop','restaurant','bar'],['office','gym','restaurant','shop','bar','office'],['shop','restaurant','gym']]
    for trajectory in setTrajectory:	#Generating pattern data
        for i in range(0,size):
        	timeInDay = 0
        	newtrajectory = []
        	for placeCategory in trajectory:
        		actionRecord = {'place': places[placeCategory][random.randint(0, len(places[placeCategory])-1)], 'time': timeInDay}
        		newtrajectory.append(actionRecord)
        		timeConsistencyRatio = random.randint(0,9)
        		if timeConsistencyRatio >= minTimeConsistencyRatio:
        			gap = random.randint(20,180)
        		else:
        			gap = random.randint(181,600)
        		timeInDay += gap
        	database.append(newtrajectory)

    for i in range(0, int(ratio * size * len(setTrajectory))):	#Generating noise data
    	newtrajectory = []
    	placeCategory = places.keys()
    	timeInDay = 0
    	for j in range(0, random.randint(2,7)):
    		randomPlaceCategory = placeCategory[random.randint(0, len(places)-1)]
    		actionRecord = {'place': places[randomPlaceCategory][random.randint(0, len(places[randomPlaceCategory])-1)], 'time': timeInDay}
    		newtrajectory.append(actionRecord)
    		timeConsistencyRatio = random.randint(0,9)
        	if timeConsistencyRatio >= minTimeConsistencyRatio:
        		gap = random.randint(20,180)
       		else:
       			gap = random.randint(181,600)
       		timeInDay += gap
    	database.append(newtrajectory)

    for eachTrajectory in database:	#output data for a view
    	data = []
    	for eachActionRecord in eachTrajectory:
    		data.append([eachActionRecord['place']['name'],eachActionRecord['time']])
    	writer.writerow(data)

    finaldatabase = []

    count = 0
    for eachTrajectory in database:
    	trajectoryWithID = {'id':count, 'data':eachTrajectory}
    	finaldatabase.append(trajectoryWithID)
    	count += 1

    return finaldatabase,allPlaces
