# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 18:56:59 2021

@author: 82105
"""

'''
Basic iead: if two name appear in the same "line", their
relationship intensity +1
'''

import os, sys
import jieba, codecs, math
import jieba.posseg as pseg

# define global paths
text_path = "download_0723.txt"
names_path = "names_dict.txt"
syno_path = "synonymous_dict.txt"
to_node = "node.csv"
to_edge = "edge.csv"

# prepare res container
names = {} # saving nodes and its weight
relationships = {} # a dict of dicts, {node:{node:intensity}}
lineNames = [] # a list of lists, each item is a buffer in each paragraph
# create synonymous word map
synos_dict = {}
with codecs.open(syno_path, "r", "utf8") as f:
    for line in f.readlines():
        anick, aname = line.split("\r\n")[0].split(" ")
        synos_dict[anick] = aname
#
#print(synos_dict)
#
# create name list
name_list = []
with codecs.open(names_path, "r", "utf8") as f:
    name_list = f.read().split(" 10 nr\r\n")
#
#print(name_list)
#

# count names
print("!Start Process Nodes")
jieba.load_userdict(names_path) # load name dict
with codecs.open(text_path, "r", "utf8") as f:
    for line in f.readlines(): # process 1 paragraph
        poss = pseg.cut(line)
        lineNames.append([]) # save this paragraph
        for w in poss:
            # exploring version
            #if w.flag != "nr" or len(w.word) < 2: continue
            # defined version
            if w.word not in name_list: continue
            # check synonymous
            if w.word in synos_dict: w.word = synos_dict[w.word]
            # this name appears in current paragraph, save the times
            lineNames[-1].append(w.word)            
            if names.get(w.word) is None:
                names[w.word] = 0
                relationships[w.word] = {}
            names[w.word] += 1
    print("Nodes Got")

# check names dict
'''
for name, times in names.items():
    print(name, times)
'''

# explore relationships
print("!Start Explore Relationships")
for line in lineNames: 
    for name1 in line:
        for name2 in line:
            if name1 == name2: continue
            if relationships[name1].get(name2) is None:
                relationships[name1][name2] = 1
            else:
                relationships[name1][name2] += 1
print("Relationships Got")

# output nodes
print("!Start Outputing")
with codecs.open(to_node, "w", "gbk") as f:
    f.write("ID,Label,Weight\r\n")
    for name, times in names.items():
        f.write(name + "," + name + "," + str(times) + "\r\n")
#output relationships
with codecs.open(to_edge, "w", "gbk") as f:
    f.write("Source,Target,ID,Intensity\r\n")
    for name1, edges in relationships.items():
        for name2, intensity in edges.items():
            if intensity > 1:
                f.write(name1 + "," + name2 + "," + name1 + "," + str(intensity) + "\r\n")
print("Outputing Got")

















