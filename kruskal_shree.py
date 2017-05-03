"""
    Algorithm Analysis - Programming Assignment 2
    Shree Raj Shrestha
    
    References:
    http://www.personal.kent.edu/~rmuhamma/Algorithms/MyAlgorithms/GraphAlgor/kruskalAlgor.htm
    https://www.cs.princeton.edu/courses/archive/spring13/cos423/lectures/UnionFind.pdf
"""


def initialize_vertex(vertice):
    """ Set the default value for the vertex in the partition structures
    """
    parent[vertice] = vertice
    rank[vertice] = 0


def find_root(vertice):
    """ Find root of vertex in partition structure using path compression
    """
    # Path compression
    if parent[vertice] != vertice:
        parent[vertice] = find_root(parent[vertice])
    print 'Finding root for vertex ', vertice, '--->', parent[vertice]
    return parent[vertice]


def union(root1, root2):
    """ Combine two partitions using union by rank strategy
    """
    
    if root1 != root2:
        if rank[root1] > rank[root2]:
            parent[root2] = root1
        else:
            parent[root1] = root2
            if rank[root1] == rank[root2]: rank[root2] += 1


def kruskal():
    """ The main Kruskal Algorithm
    """
    
    # Initialize partition structure
    for vertice in graph['vertices']:
        initialize_vertex(vertice)
    print 'Initializing Partitions, i.e. parent and rank \n', parent, rank
    
    # Sort the edges in nondecreasing order by weight
    edges = list(graph['edges'])
    print 'Unsorted edges %s'%str(edges)
    edges.sort()
    print 'Sorted edges %s \n'%str(edges)
    
    # Loop through each edge and add to MST avoiding cycles
    min_spanning_tree = set()
    print 'Spanning start! MST = ', min_spanning_tree
    for edge in edges:
        
        # Find parent for vertices in the edge
        weight, vertex1, vertex2 = edge
        print '\nSpanning edge ', edge
        print 'Edge contains vertex %d and %d' % (vertex1, vertex2)
        parent1 = find_root(vertex1) 
        parent2 = find_root(vertex2)
        
        # Add edge to the minimum spanning tree or ignore
        if parent1 != parent2:
            
            # Edge not already in MST, i.e. both parents not in MST, no cycle
            print 'Adding edge to MST'
            min_spanning_tree.add(edge)
            print 'Before union: parent, rank = %s, %s' % (str(parent), str(rank))
            union(parent1, parent2)
            print 'After union: parent, rank = %s, %s' % (str(parent), str(rank))
        else:
            # Avoid cycles. Vertex already in MST, i.e. not both parents in MST
            print 'Both vertices of edge in MST. Skipping edge...'
        
        print 'MST = ', min_spanning_tree
    
    return min_spanning_tree


##---- Main Program
if __name__ == '__main__':
    
    # Global graph variable
    graph = {
            'vertices': [],
            'edges': set()
    }
    
    # Read data from file and initialize graph with vertices and edges
    f = open('input.txt')
    for line in f:
        line = line.strip().split()
        for i in range(len(line)):
            weight, start, end = int(line[1]), int(line[0]), int(line[2])
            if start not in graph['vertices']:
                graph['vertices'].append(start)
            if end not in graph['vertices']:
                graph['vertices'].append(end)
        graph['edges'].add((weight, start, end))
    
    # Global variables for partition structure
    parent = dict() #--- the parent vertex of each vertex
    rank = dict()   #--- the number of vertex in the partition set
    
    # Print Kruskal's minimum Spanning Tree
    print "Generating Minimum Spanning Tree using Kruskal's MST Algorithm."
    print "Disjoint Set Data Structure and Union by Rank strategy is used.\n"
    MST = kruskal()
    print "\nMST generation complete. Vertex set:"
    print "(edge_weight, vertex1, vertex2)"
    for vertex in MST:
        print vertex