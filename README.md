# Approximation algorithm project: Local Search
A local search implementation for tree labeling problem. \
Input: Binary tree B whose leaves are labeled a,b,c,d,... and a graph P called a pattern graph. \
Output: A feasible extension of labels to the internal nodes of the binary tree. The feasibility of the extension l is defined as follows. For a given extension, we can construct a graph G(l), whose vertices are labels a,b,c,d… and two labels (say c and a) are connected by an edge if in the tree B there is a parent with the label c and the child with the label a. The extension is feasible if the graph G(l) is isomorphic to a subgraph of the pattern P.

Random input examples can be generated using simulate_input.py script. \
Local_search.py is a local search implementation of this problem, where w(s) = graph_edit_distance(s) if s is not isomorphic to a subgraph of P, 0 otherwise.

Local search for finding a feasible labeling: \
1- S* = Random labeling of internal nodes of the tree. \
2- t = 10. \
3- While w(S*) > 0 or iterations < t: \
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;For all S in N(S*): \
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If w(S) < w(S*): S*=S. \
 &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;If w(S*) did not decrease: S* = Random labeling of internal nodes of the tree. \

How to run using command line: \
to generate input examples: \
'python3.10 simulate_exapmles.py'\
to run the local search algorithm: \
'python3.10 local_search.py \
The name of the input file is hardcoded as 'random_examples.pkl'.
