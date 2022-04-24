#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 13:38:15 2022

@author: fatemehmohebbi
"""


import networkx as nx
import random, string, math, pickle
import numpy as np


def generate_random_pattern(patients_list):
    """n is number of nodes and m is number of edges in the pattern,
    m should not be too large since we don't want a dense pattern, (it
    will make it hard to find feasible solution"""
    n = len(patients_list)
    r = min(n-1, 7)
    m = random.randint(n, math.floor(n * r / 2))
    random_graph = nx.gnm_random_graph(n, m)
    while not nx.is_connected(random_graph):
        random_graph = nx.gnm_random_graph(n, m)
    return random_graph


def random_labeling_for_tree(tree, pattern, pattern_labeling):
    """returns a random labeling"""
    labeling = ['None'] * len(tree.nodes)
    labeling[0] = pattern_labeling[0]
    for node in tree.nodes:
        if tree.out_degree(node) != 0:
            child = list(tree.successors(node))
            node_in_pattern = pattern_labeling.index(labeling[node])
            neighbors = list(pattern.neighbors(node_in_pattern))
            random.shuffle(neighbors)
            random_number = random.uniform(0, 1)
            if random_number < 0.3:
                labeling[child[0]] = labeling[node]
                labeling[child[1]] = labeling[node]
            elif random_number < 0.6:
                labeling[child[0]] = labeling[node]
                labeling[child[1]] = pattern_labeling[neighbors[0]]
            else:
                labeling[child[1]] = labeling[node]
                labeling[child[0]] = pattern_labeling[neighbors[0]]
    return labeling


def generate_example():
    char_list = list(string.ascii_lowercase)
    rand = random.randint(5, len(char_list))
    patients_list = char_list[:rand]
    num_of_patients = len(patients_list)
    """here I used full_rary_free, if we later have code for generating 
    a real random binary tree we can replace it"""
    random_tree = nx.full_rary_tree(2, 2 * num_of_patients -1, create_using = nx.DiGraph)
    pattern = generate_random_pattern(patients_list)
    random.shuffle(patients_list)
    tree_labeling = random_labeling_for_tree(random_tree, pattern, patients_list)
    leaves_label = []
    for node in random_tree.nodes:
        if random_tree.out_degree(node) == 0:
            leaves_label.append(tree_labeling[node])
    return pattern, random_tree, leaves_label
    
    
if __name__ == '__main__':
    examples_list = {}
    # pattern, tree, leaves_labels = generate_example()
    for i in range(3):
        pattern, tree, leaves_labels = generate_example()
        dict_ = {'pattern': pattern, 'tree': tree, 'leaves_labels': leaves_labels}
        examples_list[i] = dict_
    a_file = open("random_examples_3.pkl", "wb")
    pickle.dump(examples_list, a_file)
    a_file.close()