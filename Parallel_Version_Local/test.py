#coding=utf-8
# from __future__ import print_function
__author__ = 'Prince'


import sys
from random import random
from operator import add
import findspark
findspark.init()
from pyspark import SparkContext

def sample(_):
    sc.parallelize([1,2],2).map(a).reduce(lambda x,y: x + y)

def a(_):
    return 3

def g(x,y):
    temp = x
    temp.extend(y)
    return temp

def countAAA(come):
    return come[0].count('a')

def countAA(come):
    a = sc.parallelize(come,len(come)).map(countAAA).reduce(lambda x,y: x + y)
    return a

def countA(target):
    
    if len(target) == 1:
        return target[0].count('a')

    sc = SparkContext()
    a = sc.parallelize(target, len(target)).map(countA).reduce(lambda x,y: x + y)

    sc.stop()
    return a

def testf(_):
    sc = SparkContext()
    result = sc.parallelize(range(5),1).map(a).reduce(lambda x,y: x + y)
    sc.stop()

    return result


if __name__ == "__main__":
    """
        Usage: pi [partitions]
    """
    
    # target = ['aacc']
    # target = [['aacc'], ['sdac'], ['ehga']]
    target = [[['aacc'], ['sdac'], ['ehga']],[['abcc'], ['sdac'], ['ehga']],[['abcc'], ['sdac'], ['ehga']]]
    
    # sc = SparkContext()

    nums = [1,2,3,4,5,6,7]

    # a = sc.parallelize([1,2],2).map(sample).reduce(lambda x,y: x + y)

    # result = []
    
    # result = sc.parallelize(range(5),1).map(testf).reduce(lambda x,y: x + y)



    result = countA(target)
    # result.collect()
    # print ('This is result:',result.take(result.count()))
    print ('This is result:',result)

    # sc.stop()






