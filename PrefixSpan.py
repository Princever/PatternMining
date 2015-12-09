#coding=utf-8
__author__ = 'Prince'

import sys
import util as u
import copy



PLACE_HOLDER = '_'

class SquencePattern:
    def __init__(self, squence, support):
        self.squence = []
        # self.snippets = {}
        for s in squence:
            self.squence.append(list(s))
        self.support = support

    def append(self, p):
        if p.squence[0][0] == PLACE_HOLDER:
            first_e = p.squence[0]
            first_e.remove(PLACE_HOLDER)
            self.squence[-1].extend(first_e)
            self.squence.extend(p.squence[1:])
        else:
            self.squence.extend(p.squence)
        self.support = min(self.support, p.support)


def prefixSpan(pattern, S, deltaT, threshold):
    patterns = []
    f_list = frequent_items(S, pattern, deltaT, threshold)

    for i in f_list:
        p = SquencePattern(pattern.squence, pattern.support)
        p.append(i)
        patterns.append(p)

        p_S = build_projected_database(S, p)
        # print 'ps:',p_S
        p_patterns = prefixSpan(p, p_S, deltaT, threshold)
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

def frequent_items(S, pattern, deltaT, threshold):
    items = {}
    itemsAppear = {}
    f_list = []
    # for each in Source:
    #     print each

    # S = timeConstraint(Source, deltaT)
    # for each in S:
    #     print each
    if S is None or len(S) == 0:
        return []

    if len(pattern.squence) != 0:
        last_e = pattern.squence[-1]
    else:
        last_e = []

    for line in S:
        # print 'data:',data

        s = line['data']
        # print s
        trajectoryID = line['id']
        # print trajectoryID

        #class 1
        # is_prefix = True
        # for item in last_e:
        #     if item not in s[0]:
        #         is_prefix = False
        #         break
        # if is_prefix and len(last_e) > 0:
        #     # print 'is_prefix'
        #     index = s[0].index(last_e[-1])
            # if index < len(s[0]) - 1:
            #     # print 'hit1'
            #     for item in s[0][index + 1:]:
            #         if item in _items:
            #             _items[item] += 1
            #             # print 'hit2'
            #         else:
            #             _items[item] = 1
            #             # print 'hit3'

        #class 2    #no necessary
        # if PLACE_HOLDER in s[0]:
        #     print 'class22222222222222'
        #     for item in s[0][1:]:
        #         if item in _items:
        #             _items[item] += 1
        #         else:
        #             _items[item] = 1
        #     s = s[1:]

        #class 3
        counted = []
        # print 's:',s
        for element in s:
            item = element['place']['category']
            isTimeConstraint = detectTimeConstraint(element, deltaT)
            # print isTimeConstraint
            itemsAppear.setdefault(item,[])
            if item not in counted and trajectoryID not in itemsAppear[item] and isTimeConstraint:
                # print 'notcounted'
                itemsAppear[item] += [trajectoryID]
                counted.append(item)
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

    # f_list.extend([SquencePattern([[PLACE_HOLDER, k]], v)
    #                for k, v in _items.iteritems()
    #                if v >= threshold])
    f_list.extend([SquencePattern([[k]], v)
                   for k, v in items.iteritems()
                   if v >= threshold])

    sorted_list = sorted(f_list, key=lambda p: p.support)
    return sorted_list

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

def build_projected_database(S, pattern):
    """
    suppose S is projected database base on pattern's prefix,
    so we only need to use the last element in pattern to
    build projected database
    """
    p_S = []
    last_e = pattern.squence[-1]
    last_item = last_e[-1]
    for ase in S: #a sequense
        p_s = []
        f_s = simple(ase)
        # print f_s
        s = f_s['data']
        trajectoryID = f_s['id']
        # print 's:',s
        for element in s:   #places
            is_prefix = False
            if PLACE_HOLDER in element:
                if last_item in element and len(pattern.squence[-1]) > 1:
                    is_prefix = True
            else:
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
        print("pattern:{0}, support:{1}".format(name, p.support)) 
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
