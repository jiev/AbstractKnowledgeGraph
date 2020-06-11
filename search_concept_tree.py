# coding = utf-8
import os
import networkx as nx
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import search_concept

class concept_tree:
    def __init__(self,all_concept):
        self.cp_childs_dict = dict()
        for cpName,paths in all_concept.items():
            if paths and len(paths) > 0:
                for path in paths:
                    if path and len(path) > 1:
                        if path[1] not in self.cp_childs_dict:
                            self.cp_childs_dict[path[1]] = set()
                        self.cp_childs_dict[path[1]].add(cpName)

    '''概念树子节点集搜索工具'''
    def search_hiearchy(self):
        while 1:
            wd = input('enter an concept name to search:').strip()
            # all_dict 应该是 list 的 list
            cp_set = self.cp_childs_dict.get(wd, '')
            if cp_set:
                print(wd, '子节点内容：', '\t'.join(cp_set))


if __name__ == '__main__':
    handler = search_concept.ConceptNet()
    ct = concept_tree(handler.all_dict)
    ct.search_hiearchy()


