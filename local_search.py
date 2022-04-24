#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 09:41:48 2022

@author: fatemehmohebbi
"""


import networkx as nx
import numpy as np
import random, pickle
from simulate_input import generate_example
from graph_tool.all import *


def random_labeling(tree, leaves, labeling, dfs_order):
    """returns a random labeling"""
    # dfs_order.reverse()
    for node in dfs_order:
        if tree.out_degree(node) == 0:
            continue
        else:
            child = list(tree.successors(node))
            random_number = random.uniform(0, 1)
            if random_number >= 0.5:
                labeling[node] = labeling[child[0]]
            else:
                labeling[node] = labeling[child[1]]
            # print('label of node ', node, ' is ', labeling[node])
    print(labeling)
    return labeling
    

def get_input(i):
    """returns a tree and a pattern"""
    # pattern = [(0,1), (1,2)]
    # edge_list = [(0,1), (0,2), (1,3), (1,4), (2,5), (2,6), (4,7), (4,8)]
    # G = nx.DiGraph(edge_list)
    # leaves_labeling = ['b', 'g', 'b', 'b', 'r'] 
    # pattern_graph, G, leaves_labeling = generate_example()
    
    instance = data[i]
    pattern_graph = instance['pattern']
    G = instance['tree']
    leaves_labeling = instance['leaves_labels']
    pattern = pattern_graph.edges
    root = list(nx.topological_sort(G))[0]
    dfs_order = list(nx.dfs_postorder_nodes(G, source=root))
    
    leaves = []
    labels = [] 
    counter = 0
    for i in G.nodes:
        if G.out_degree(i) == 0:
            leaves.append(i)
            labels.append(leaves_labeling[counter])
            counter = counter + 1
        else:
            labels.append('None')
    return G, leaves, leaves_labeling, labels, dfs_order, pattern


def get_neighboring_solutions(tree, labeling):
    """returns the list of all neighboring solutions of a labeling"""
    neighbor_labelings = []
    root = list(nx.topological_sort(tree))[0]
    for node in tree.nodes:
        temp_labeling = labeling[:]
        if tree.out_degree(node) == 0:
            continue
        elif node == root:
            child = list(tree.successors(node))
            if labeling[child[0]] != labeling[child[1]]:
                temp_labeling[node] = list({labeling[child[0]], labeling[child[1]]} - {labeling[node]})[0]
        else:
            child = list(tree.successors(node))
            parent = list(tree.predecessors(node))
            sibling = list(tree.successors(parent[0]))
            sibling.remove(node)
            if labeling[child[0]] == labeling[child[1]]:
                continue
            else:
                label_change = list({labeling[child[0]], labeling[child[1]]} - {labeling[node]})[0]
                if label_change == labeling[parent[0]] or labeling[parent[0]] == labeling[sibling[0]]:
                    temp_labeling[node] = label_change
                else:
                    current_node = int(node)
                    while (not (label_change == labeling[parent[0]] or labeling[parent[0]] == labeling[sibling[0]])):
                        # print('parent_check')
                        temp_labeling[current_node] = label_change
                        if current_node == root:
                            break
                        else:
                            parent = list(tree.predecessors(current_node))
                            sibling = list(tree.successors(parent[0]))
                            sibling.remove(current_node)
                            current_node = parent[0]
        neighbor_labelings.append(temp_labeling)
    print('Neighboring solutions are calculated.')
    return neighbor_labelings


def get_trans_network(tree, labeling):
    """returns the edges of the transmission network based on tree's labeling"""
    trans_edges = []
    trans_nodes = []
    labels_list = list(set(labeling))
    for node in tree.nodes:
        try:
            pos = trans_nodes.index(labeling[node])
        except:
            trans_nodes.append(labels_list.index(labeling[node]))
        if tree.out_degree(node) != 0:
            child = list(tree.successors(node))
            if labeling[child[0]] != labeling[node]:
                trans_edges.append((labels_list.index(labeling[node]), labels_list.index(labeling[child[0]])))
            elif labeling[child[1]] != labeling[node]:
                trans_edges.append((labels_list.index(labeling[node]), labels_list.index(labeling[child[1]])))
    
    
    # print('The transmission network: ', list(set(trans_edges)))
    # print(list(set(trans_nodes)))
    return list(set(trans_edges))
        

def evaluate_isomorphism(edge_list1, edge_list2):
    G_1 = nx.Graph(edge_list1)
    G_2 = nx.Graph(edge_list2)
    if check_isomorphism_graph_tool(G_1.edges, G_2.edges):
        return 0
    distance = nx.graph_edit_distance(G_1, G_2, timeout=0.8)
    print('distnace of current solution to the pattern is ', distance)
    return distance


def check_isomorphism_graph_tool(edge_list1, edge_list2):
    G_1 = Graph()
    G_2 = Graph()
    G_1.set_directed(False)
    G_2.set_directed(False)
    for i, j in edge_list1:
        G_1.add_edge(i, j)
    for i, j in edge_list2:
        G_2.add_edge(i, j)
    vm = subgraph_isomorphism(G_1, G_2, max_n=2)
    if len(vm) == 0:
        return False
    else:
        return True
        

def local_search(tree, leaves, labels, dfs, pattern):
    current_labeling = random_labeling(tree, leaves, labels, dfs)
    neighbors = get_neighboring_solutions(tree, current_labeling)
    labelings_trans_net = get_trans_network(tree, current_labeling)
    current_label_distance = evaluate_isomorphism(labelings_trans_net, pattern)
    max_iterations = 10
    counter = 0
    opt_labeling = current_labeling
    opt_distance = current_label_distance
    while current_label_distance != 0 and counter < max_iterations:
        counter = counter + 1
        print(counter)
        improvement = False
        for neighbor in neighbors:
            net = get_trans_network(tree, neighbor)
            distance_to_pattern = evaluate_isomorphism(net, pattern)
            if distance_to_pattern < current_label_distance:
                improvement = True
                current_labeling = neighbor
                opt_labeling = neighbor
                current_label_distance = distance_to_pattern
                opt_distance = distance_to_pattern
                current_net = nx.Graph(net)
        if not improvement:
            current_labeling = random_labeling(tree, leaves, labels, dfs)
            net = get_trans_network(tree, current_labeling)
            current_label_distance = evaluate_isomorphism(net, pattern)
            if current_label_distance == 0:
                return 0
            print('A random solution is generated.')
        neighbors = get_neighboring_solutions(tree, current_labeling)
    print(opt_labeling)
    print(opt_distance)
    print('distance of solution found to optimal solution is ', opt_distance)
    return opt_distance


if __name__ == '__main__':
    a_file = open("random_examples.pkl", "rb")
    data = pickle.load(a_file)
    results = []
    for i in range(len(data)):
        print('Example ', i )
        tree, leaves,leaves_label, labels, dfs, pattern = get_input(i)
        distnace_to_opt = local_search(tree, leaves, labels, dfs, pattern)
        results.append(distnace_to_opt)
    print('Local search found optimal solution for ', results.count(0), ' examples out of 300 random pattern and trees.')
    
    
    
