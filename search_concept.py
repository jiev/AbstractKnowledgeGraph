# coding = utf-8
import os
import networkx as nx
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt


class ConceptNet:
    def __init__(self):
        cur = "/".join(os.path.abspath(__file__).split('/')[:-1])
        self.hiearchy_file = os.path.join(cur, "dict/hiearchy.txt")
        self.concept_file = os.path.join(cur, "dict/concept_total.txt")
        self.all_dict = self.build_all_concepts()
        return

    '''加载概念边'''
    def __load_concept_edges(self, ):
        edges = []
        for line in open(self.hiearchy_file):
            line = line.strip().split(' ')
            if len(line) < 2:
                continue
            from_ = line[0].split('|')[-1]
            to_ = line[1].split('|')[-1]
            edges.append((to_, from_))
        return edges

    '''利用networkx构建有向图'''
    def __build_graph(self, edges):
        G = nx.DiGraph()
        G.add_edges_from(edges)
        return G

    '''构造底层概念词典'''
    def __build_basic_concept(self):
        concept_dict = {}
        print("loading concept edges")
        edges = self.__load_concept_edges()
        print("build grpah")
        graph = self.__build_graph(edges)
        path = nx.all_pairs_shortest_path(graph)
        for i in path:
            #python3.6 下得这么取才对
            wd = i
            path_dict = path[i]
            len_dict = {i:len(j) for i,j in path_dict.items()}
            len_dict_ = sorted(len_dict.items(), key=lambda asd:asd[1], reverse=True)
            longest_path = path_dict.get(len_dict_[0][0])
            if not longest_path:
                continue
            concept_dict[wd] = longest_path
        return concept_dict

    '''搜集主函数'''
    def build_all_concepts(self):
        all_dict = {}
        concept_dict = self.__build_basic_concept()
        print('building all concepts')
        for line in open(self.concept_file):
            line = line.strip().split('\t')
            wd = line[0]
            concepts = [i.split('|')[-1] for i in line[-1].split(',')]
            concept_path = concept_dict.get(wd, '')
            if not concept_path:
                concept_path = [[wd] + concept_dict.get(c, [c]) for c in concepts]
            else:
                concept_path = [concept_path]
            all_dict[wd] = concept_path
        return all_dict

    '''层级搜索主函数'''
    def search_hiearchy(self):
        while 1:
            wd = input('enter an wd to search:').strip()
            # all_dict 应该是 list 的 list
            paths = self.all_dict.get(wd, '')
            if paths:
                for path in paths:
                    print(wd, '抽象路径为：', '->'.join(path))

if __name__ == '__main__':
    handler = ConceptNet()
    handler.search_hiearchy()
