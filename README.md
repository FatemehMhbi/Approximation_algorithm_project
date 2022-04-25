# Approximation_algorithm_project
A local search implementation for tree labeling problem. //
Input: Binary tree B whose leaves are labeled a,b,c,d,... and a graph P called a pattern graph.
Output: A feasible extension of labels to the internal nodes of the binary tree. The feasibility of the extension l is defined as follows. For a given extension, we can construct a graph G(l), whose vertices are labels a,b,c,d… and two labels (say c and a) are connected by an edge if in the tree B there is a parent with the label c and the child with the label a. The extension is feasible if the graph G(l) is isomorphic to a subgraph of the pattern P.

Random input examples can be generated using simulate_input.py script. 

A feasible labeling is calculated using a local search algorithm (local_search.py).
