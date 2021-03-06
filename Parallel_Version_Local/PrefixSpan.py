#coding=utf-8
__author__ = 'Prince'

import sys
import util as u
import copy
import findspark
findspark.init()

from pyspark import SparkContext



PLACE_HOLDER = '_'

class SquencePattern:
    def __init__(self, squence, support, snippet):
        self.squence = []
        self.snippets = []
        for s in squence:
            self.squence.append(list(s))
        self.support = support
        self.snippets = snippet
        # print 'sss',self.snippets

    def mergeSnippet(self, snippet1, snippet2):
        if snippet1 == []:
            return snippet2
        if snippet2 == []:
            return snippet1
        newSnippet = []
        for each1 in snippet1:
            for each2 in snippet2:
                newids = list(set(each1['ids']).intersection(each2['ids']))
                if newids != []:
                    tmpSnippet = copy.deepcopy(each1['snippet'])
                    tmpSnippet.extend(each2['snippet'])
                    # print '1',each1['snippet']
                    # print '2',each2['snippet']
                    # print '3',tmpSnippet
                    newSnippet.append({'snippet':tmpSnippet, 'ids':newids, 'weight':len(newids)})
        return newSnippet

    def append(self, p):
        if p.squence[0][0] == PLACE_HOLDER:
            # print 'yes!!!!!!!!!!!!!'
            first_e = p.squence[0]
            first_e.remove(PLACE_HOLDER)
            self.squence[-1].extend(first_e)
            self.squence.extend(p.squence[1:])
        else:
            self.squence.extend(p.squence)
            self.snippets = self.mergeSnippet(self.snippets, p.snippets)
            # print 'ss:',self.snippets
        self.support = min(self.support, p.support)

# def paraPartPrefixSpan(i, patterns, pattern, S, deltaT, threshold, control):
#     tmpPatterns = copy.deepcopy(patterns)

#     p = SquencePattern(pattern.squence, pattern.support, pattern.snippets)
#     p.append(i)
#     tmpPatterns.append(p)
#     scpd = SparkContext('spark://chris00.omni.hpcc.jp:7077', 'PatternMining_projectDatabase', pyFiles=['/home/zxu/Parallel_Version/PrefixSpan.py', '/home/zxu/Parallel_Version/util.py'])
#     p_S = build_projected_databaseD(S, p, scpd)

#     if control[0] >= control[1]: 
#         p_patterns = prefixSpan(p, p_S, deltaT, threshold, scpd)
#         scpd.stop()
#     else:
#         scpd.stop()
#         p_patterns = prefixSpanD(p, p_S, deltaT, threshold, [control[0]+1, control[1]])

#     # print '________________________', type(p_patterns),p_patterns

#     tmpPatterns.extend(p_patterns)
#     return tmpPatterns

def gup(x, y):
    # print 'x:',x,'xType:',type(x)
    # print 'y:',y,'yType:',type(y)
    x.extend(y)
    return x

# def prefixSpanD(pattern, S, deltaT, threshold, control):

#     patterns = []
#     f_list = frequent_items(S, deltaT, threshold)

#     # for i in f_list:
#     #     p = SquencePattern(pattern.squence, pattern.support, pattern.snippets)
#     #     p.append(i)
#     #     patterns.append(p)

#         # p_S = build_projected_database(S, p)
#         # # print 'ps:',p_S
#         # p_patterns = prefixSpan(p, p_S, deltaT, threshold)
#         # patterns.extend(p_patterns)
#     if len(f_list) == 0:
#         return []
#     else:
#         sc = SparkContext('spark://chris00.omni.hpcc.jp:7077', 'PatternMining_PrefixSpan', pyFiles=['/home/zxu/Parallel_Version/PrefixSpan.py','/home/zxu/Parallel_Version/util.py'])
#         patternsG = sc.parallelize(f_list).map(lambda i: paraPartPrefixSpan(i, patterns, pattern, S, deltaT, threshold, control)).reduce(gup)
#     # patterns.extend(patternsG)
#         sc.stop()
#         return patternsG

def prefixSpan(pattern, S, deltaT, threshold, scfi):
    patterns = []
    f_list = frequent_itemsD(S, deltaT, threshold, scfi)

    for i in f_list:
        p = SquencePattern(pattern.squence, pattern.support, pattern.snippets)
        p.append(i)
        patterns.append(p)

        p_S = build_projected_database(S, p)
        # print 'ps:',p_S
        p_patterns = prefixSpan(p, p_S, deltaT, threshold, scfi)
        patterns.extend(p_patterns)

    return patterns


def timeConstraint(Source, deltaT):
    S = []
    for eachTrajectory in Source:
        # print eachTrajectory
        if len(eachTrajectory['data']) == 1:
            # print 'len-1 items:',eachTrajectory
            # print 'len-1 items:',eachTrajectory[0]['place']['category']
            lastCategory = [[eachTrajectory['data'][0]['place']['category']]]
            newData = {'id': eachTrajectory['id'],'data': lastCategory}
            S.append(newData)
        else:
            if eachTrajectory['data'][1]['time'] - eachTrajectory['data'][0]['time'] <= deltaT:
                tmpTrajectory = []
                for eachPlace in eachTrajectory['data']:
                    # print eachPlace['place']['category']
                    tmpTrajectory.append([eachPlace['place']['category']])
                newData = {'id': eachTrajectory['id'],'data': tmpTrajectory}
                S.append(newData)
    # print 'S:',S
    return S

def detectTimeConstraint(element, deltaT):
    if element['time'] > deltaT:
        return False
    else:
        return True

def transfer(snippet):
    snippets = []
    for eachPlace in snippet:
        snippets.append({'snippet':[[eachPlace]], 'ids':snippet[eachPlace], 'weight':len(snippet[eachPlace])})
    return snippets

def paraCountFrequentItem(line, deltaT):
    items = {}

    s = line['data'] #get data

    trajectoryID = line['id'] #get line id

    # counted = []

    for element in s:
        item = element['place']['category']
        name = element['place']['name']
        isTimeConstraint = detectTimeConstraint(element, deltaT)
        if isTimeConstraint:
            # if item not in counted:
                # counted.append(item)
            if item in items:#exist category
                if name not in items[item]['snippet']:#new place
                    items[item]['snippet'][name] = [trajectoryID]
                    # items[item]['snippet'][name] += [trajectoryID]
                    # items[item]['weight'] += 1
                # else:#new place
                #     items[item]['snippet'][name] = [trajectoryID]
                #     items[item]['weight'] += 1
            else:#new category
                items[item] = {'snippet':{name:[trajectoryID]}, 'weight':1}

    return items

def gufi(x, y):
    for category, data in y.iteritems():
        if category in x.keys():
            for places, ids in data['snippet'].iteritems():
                if places in x[category]['snippet'].keys():
                    x[category]['snippet'][places].extend(ids)
                    tmplist = {}.fromkeys(x[category]['snippet'][places]).keys()
                    x[category]['snippet'][places] = tmplist
                else:
                    x[category]['snippet'][places] = ids
        else:
            x[category] = data
        ttlist = []
        for places, ids in x[category]['snippet'].iteritems():
            ttlist.extend(ids)
        tmplist = {}.fromkeys(ttlist).keys()
        x[category]['weight'] = len(tmplist)
    return x

def frequent_itemsD(S, deltaT, threshold, scfi):

    f_list = []

    if S is None or len(S) == 0:
        return []

    items = scfi.parallelize(S).map(lambda line: paraCountFrequentItem(line, deltaT)).reduce(gufi)
#    print items
    f_list.extend([SquencePattern([[k]], data['weight'], transfer(data['snippet']))
                   for k, data in items.iteritems()
                   if data['weight'] >= threshold])

    sorted_list = sorted(f_list, key=lambda p: p.support)
    return sorted_list    

# def frequent_items(S, deltaT, threshold):
#     items = {}
#     itemsAppear = {}
#     f_list = []

#     if S is None or len(S) == 0:
#         return []

#     for line in S:

#         s = line['data']

#         trajectoryID = line['id']

#         counted = []

#         for element in s:
#             item = element['place']['category']
#             name = element['place']['name']
#             isTimeConstraint = detectTimeConstraint(element, deltaT)
#             itemsAppear.setdefault(item,[])
#             if item not in counted and trajectoryID not in itemsAppear[item] and isTimeConstraint:
#                 itemsAppear[item] += [trajectoryID]
#                 counted.append(item)
#                 if item in items:
#                     if name in items[item]['snippet']:
#                         items[item]['snippet'][name] += [trajectoryID]
#                         items[item]['weight'] += 1
#                     else:
#                         items[item]['snippet'][name] = [trajectoryID]
#                         items[item]['weight'] += 1
#                 else:
#                     items[item] = {'snippet':{name:[trajectoryID]}, 'weight':1}

#     f_list.extend([SquencePattern([[k]], data['weight'], transfer(data['snippet']))
#                    for k, data in items.iteritems()
#                    if data['weight'] >= threshold])

#     sorted_list = sorted(f_list, key=lambda p: p.support)
#     return sorted_list

def simple(record):
    s = []
    # print 'database2:',database
    # print record['data']
    for eachplace in record['data']:
        s.append([eachplace['place']['category']])
    # print 'sps:',s
    f_s = {'data':s, 'id':record['id']}
    return f_s

def getAllIndex(s,element):
    indices = []
    count = 0
    for each in s:
        if each == element:
            indices += [count]
        count += 1
    return indices

# def paraProjectedDataBase(i, last_e):
#     p_S = []
#     f_s = simple(i)
#     # print f_s
#     s = f_s['data']
#     trajectoryID = f_s['id']
#     # print 's:',s
#     for element in s:   #places
#         is_prefix = True
#         for item in last_e:
#             if item not in element:
#                 is_prefix = False
#                 break

#         if is_prefix:
#             e_index = getAllIndex(s,element)    #full projection

#             for eachIndex in e_index:
#                 gapTime = i['data'][eachIndex]['time']
#                 p_sTmp = i['data'][eachIndex + 1:]
#                 p_s = []
#                 for each in p_sTmp:
#                     eachh = copy.deepcopy(each)
#                     eachh['time'] -= gapTime
#                     p_s.append(eachh)
#                 if len(p_s) != 0:
#                     fp_s = {'data':p_s, 'id':trajectoryID}
#                     p_S.append(fp_s)

#     return p_S


# def build_projected_databaseD(S, pattern, scpd):
#     """
#     suppose S is projected database base on pattern's prefix,
#     so we only need to use the last element in pattern to
#     build projected database
#     """
#     last_e = pattern.squence[-1]

#     p_S = scpd.parallelize(S).map(lambda i: paraProjectedDataBase(i, last_e)).reduce(gup)
    

#     return p_S

def build_projected_database(S, pattern):
    """
    suppose S is projected database base on pattern's prefix,
    so we only need to use the last element in pattern to
    build projected database
    """
    p_S = []
    last_e = pattern.squence[-1]
    for ase in S: #a sequense
        p_s = []
        f_s = simple(ase)
        # print f_s
        s = f_s['data']
        trajectoryID = f_s['id']
        # print 's:',s
        for element in s:   #places
            is_prefix = True
            for item in last_e:
                if item not in element:
                    is_prefix = False
                    break

            if is_prefix:
                e_index = getAllIndex(s,element)    #full projection
                # print 'elem:',element
                # print 's:',s
                # i_index = element.index(last_item)
                # if i_index == len(element) - 1:
                for eachIndex in e_index:
                    gapTime = ase['data'][eachIndex]['time']
                    p_sTmp = ase['data'][eachIndex + 1:]
                    p_s = []
                    for each in p_sTmp:
                        eachh = copy.deepcopy(each)
                        eachh['time'] -= gapTime
                        p_s.append(eachh)
                    if len(p_s) != 0:
                        fp_s = {'data':p_s, 'id':trajectoryID}
                        # print 'fp_s:',fp_s
                        p_S.append(fp_s)
                # else:
                    # p_s = ase[e_index:]
                    # index = element.index(last_item)
                    # # e = element[i_index:]
                    # # e[0] = PLACE_HOLDER
                    # p_s[0] = {'place': {'category': PLACE_HOLDER}}
                    # # print '111222'
                    # print 'impossible'
                # break
        # if len(p_s) != 0:
        #     p_S.append(p_s)

        # print 'p_S:',p_S

    return p_S


def print_patterns(patterns):
    for p in patterns:
        name = '['
        for each in p.squence:
            aitem = '['
            flag = False
            for item in each:
                if flag:
                    aitem += '&'
                aitem += item
                flag = True
            aitem += ']'
            name += aitem
            name += ']'
        print("pattern:{0}, support:{1}, snippet:{2}".format(name, p.support, p.snippets)) 
        # print >> ff,("pattern:{0}, support:{1}".format(name, p.support))



# if __name__ == "__main__":
#     ff = open('datas/result.txt','w')
#     S = u.read("datas/gxyseq.csv")
#     min_supp=0.01
#     count = 0
#     for each in S:
#         count += 1
#     patterns = prefixSpan(SquencePattern([], sys.maxint), S, min_supp * count)
#     print_patterns(patterns)
#     seqNums = []
#     for each in patterns:
#         seqNums.append(each.squence)
#     maxSeqs = u.maxSeq(seqNums)
#     print("The sequential patterns :")
#     for i in maxSeqs:
#         for sth in i:
#             print "[",
#             for ssth in sth:
#                 print ssth,
#             print "]",
#         print ""
#     print >> ff,"The sequential patterns :"
#     for i in maxSeqs:
#         for sth in i:
#             print >> ff,"[",
#             for ssth in sth:
#                 print >> ff,ssth,
#             print >> ff,"]",
#         print >> ff,""
#     ff.close()
#     flitedSeqs = u.fliter(maxSeqs)
#     expandedSeqs = u.expand(maxSeqs)
#     maxStages = u.genPlotDatas(maxSeqs)
#     flitedStages = u.genPlotDatas(flitedSeqs)
#     expandedStages = u.genPlotDatas(expandedSeqs)
#     allStages = []
#     allStages += [maxStages]
#     allStages += [flitedStages]
#     allStages += [expandedStages]
#     u.drawStages(allStages)
