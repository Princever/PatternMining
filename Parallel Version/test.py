#coding=utf-8
__author__ = 'Prince'

# import pyspark as spark
from pyspark import SparkContext, SparkConf
from random import *

def sample(p):
    x, y = random(), random()
    return 1 if x*x + y*y < 1 else 0
if __name__ == "__main__":

    conf = SparkConf().setAppName('Test').setMaster('local')
    sc = SparkContext(conf = conf)

    NUM_SAMPLES = 10000000

    count = sc.parallelize(xrange(0, NUM_SAMPLES)).map(sample).reduce(lambda a, b: a + b)
    print " "
    print " "
    print "Pi is roughly %f" % (4.0 * count / NUM_SAMPLES)
    print " "
    print " "










