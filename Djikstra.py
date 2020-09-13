import copy

class Element:
    def __init__(self, key, value, index):
        self._key = key
        self._value = value
        self._index = index

    def __eq__(self, other):
        return self._key == other._key

    def __lt__(self, other):
        return self._key < other._key
    
    def _wipe(self):
        self._key = None
        self._value = None
        self._index = None

    def __str__(self):
        strf = "key = %s value = %s index = %s" % (self._key,self._value,self._index)
        return strf

class APQ:
    def __init__(self):
        self._heapList = []

    ''' add a new item into the priority queue with priority key, 
        and return its Element in the APQ
        create the Element, append to the list, return the Element
    '''
    def add(self, key, item):
        #if heap is empty
        if self.length() == 0:
            #create element
            elt = Element(key, item, 0)
            #append to list
            self._heapList.append(elt)
        else:
            #add a new item into the priority queue with priority key
            elt = Element(key, item, self.length())
            self._heapList.append(elt)
            self.bubbleup(elt)
        return elt

    '''return the value with the minimum key'''
    def min(self):
        #read first cell in array and return
        return self._heapList[0]

    '''remove and return the value with the minimum key'''
    def remove_min(self):
        #swap first element into last place, 
        self.swap(0,(self.length()-1))
        #pop the element,
        rmvmin = self._heapList.pop(self.length()-1)
        #bubble top element down, 
        #changing indices, 
        #return popped key,value
        if self.length() != 0:
            self.bubbledown(self._heapList[0])
        return (rmvmin._key,rmvmin._value)

    '''update the key in element to be newkey, and rebalance the APQ'''
    def update_key(self, elt, newkey):
        #update the element's key, 
        # if key less than parent's key,
        #bubble up; 
        # else bubble down
        if newkey < elt._key:
            elt._key = newkey
            self.bubbleup(elt)
        elif newkey > elt._key:
            elt._key = newkey
            self.bubbledown(elt)

    '''return the current key for element'''
    def get_key(self,elt):
        #return the element's key
        return elt._key
    
    '''remove the element from the APQ, and rebalance APQ'''
    def remove(self, elt):
        #swap last element with one in element's index
        self.swap(elt._index,(len(self._heapList)-1))
        #if swap key < parent, bubble up
        if self._heapList[elt._index]._key < self._heapList[self._parent(elt._index)]._key:
            self.bubbleup(self._heapList[elt._index])
        else: #else bubble down,
            self.bubbledown(self._heapList[elt._index])
        #pop the last element
        popoff = self._heapList.pop(len(self._heapList)-1)
        #return key,value
        return (popoff._key,popoff._value)


    def bubbleup(self,elt):
        while True:
            #if key < parent key
            if elt._index != 0 and elt._key < self._heapList[self._parent(elt._index)]._key: 
                #swap element with parent
                self.swap(elt._index,self._parent(elt._index))
            else:
                break

    def bubbledown(self,elt):
         while True:
            minLeftChild = None
            minRightChild = None
            if self._left(elt._index):
                minLeftChild = self._left(elt._index)
            if self._right(elt._index):
                 minRightChild = self._right(elt._index)
            #if both child
            if minLeftChild and minRightChild:
                if self._heapList[minLeftChild]._key > self._heapList[minRightChild]._key:
                    minChild = minRightChild
                else:
                    minChild = minLeftChild
            #if only right child
            elif minRightChild and minLeftChild == None:
                minChild = minRightChild
            #if only left child
            elif minLeftChild and minRightChild == None:
                minChild = minLeftChild 
            else:
                break
            if minChild:
                #if this key > target key
                if elt._key > self._heapList[minChild]._key:
                    #swap element with target
                    self.swap(elt._index,minChild)
                else:
                    break
                    
    def swap(self,x,y):
        self._heapList[x], self._heapList[y] = self._heapList[y], self._heapList[x]
        # update the _index attributes in he Elements after swapping 2 elmts
        self._heapList[x]._index, self._heapList[y]._index = self._heapList[y]._index , self._heapList[x]._index
    
    def _parent(self,index):
        #parent(i) = (i-1)//2
        return (((index-1)//2))

    def _left(self,index):
        #left(i) = 2*i + 1
        x = ((2*index)+1)
        if len(self._heapList)-1 < x:
            return None
        return (x)

    def _right(self,index):
        #right(i) = 2*i + 2
        x = ((2*index)+2)
        if len(self._heapList)-1 < x:
            return None
        return (x)
    
    def length(self):
        return len(self._heapList)

    def __str__(self):
        s = ""
        for i in self._heapList:
            s += "key = %s value = %s index = %s"  % (i._key, i._value, i._index)
        return s
#----------------------------------graph--------------------------------------
#from lab 06
class Vertex:
    """ A Vertex in a graph. """
    
    def __init__(self, element):
        """ Create a vertex, with data element. """
        self._element = element

    def __str__(self):
        """ Return a string representation of the vertex. """
        return str(self._element)

    def __lt__(self, v):
        return self._element < v.element()

    def element(self):
        """ Return the data for the vertex. """
        return self._element
    
class Edge:
    """ An edge in a graph.

    Implemented with an order, so can be used for directed or undirected
    graphs. Methods are provided for both. It is the job of the Graph class
    to handle them as directed or undirected.
    """
    
    def __init__(self, v, w, element):
        """ Create an edge between vertices v and w, with label element.

            element can be an arbitrarily complex structure.
        """
        self._vertices = (v,w)
        self._element = element

    def __str__(self):
        """ Return a string representation of this edge. """
        return ('(' + str(self._vertices[0]) + '--'
                   + str(self._vertices[1]) + ' : '
                   + str(self._element) + ')')

    def vertices(self):
        """ Return an ordered pair of the vertices of this edge. """
        return self._vertices

    def start(self):
        """ Return the first vertex in the ordered pair. """
        return self._vertices[0]

    def end(self):
        """ Return the second vertex in the ordered. pair. """
        return self._vertices[1]

    def opposite(self, v):
        """ Return the opposite vertex to v in this edge. """
        if self._vertices[0] == v:
            return self._vertices[1]
        elif self._vertices[1] == v:
            return self._vertices[0]
        else:
            return None

    def element(self):
        """ Return the data element for this edge. """
        return self._element

class Graph:
    """ Represent a simple graph.

        This version maintains only undirected graphs, and assumes no
        self loops.
    """

    #Implement as a Python dictionary
    #  - the keys are the vertices
    #  - the values are the edges for the corresponding vertex
    #    Each edge set is also maintained as a dictionary,
    #    with opposite vertex as the key and the edge object as the value
    
    def __init__(self):
        """ Create an initial empty graph. """
        self._structure = dict()

    def __str__(self):
        """ Return a string representation of the graph. """
        hstr = ('|V| = ' + str(self.num_vertices())
                + '; |E| = ' + str(self.num_edges()))
        vstr = '\nVertices: '
        for v in self._structure:
            vstr += str(v) + '-'
        edges = self.edges()
        estr = '\nEdges: '
        for e in edges:
            estr += str(e) + ' '
        return hstr + vstr + estr

    #--------------------------------------------------#
    #ADT methods to query the graph
    
    def num_vertices(self):
        """ Return the number of vertices in the graph. """
        return len(self._structure)

    def num_edges(self):
        """ Return the number of edges in the graph. """
        num = 0
        for v in self._structure:
            num += len(self._structure[v])    #the dict of edges for v
        return num // 2     #divide by 2, since each edege appears in the
                           #vertex list for both of its vertices

    def vertices(self):
        """ Return a list of all vertices in the graph. """
        return [key for key in self._structure]

    def get_vertex_by_label(self, element):
        """ get the first vertex that matches element. """
        for v in self._structure:
            if v.element() == element:
                return v
        return None

    def edges(self):
        """ Return a list of all edges in the graph. """
        edgelist = []
        for v in self._structure:
            for w in self._structure[v]:
                #to avoid duplicates, only return if v is the first vertex
                if self._structure[v][w].start() == v:
                    edgelist.append(self._structure[v][w])
        return edgelist

    def get_edges(self, v):
        """ Return a list of all edges incident on v. """
        if v in self._structure:
            edgelist = []
            for w in self._structure[v]:
                edgelist.append(self._structure[v][w])
            return edgelist
        return None

    def get_edge(self, v, w):
        """ Return the edge between v and w, or None. """
        if (self._structure != None
                         and v in self._structure
                         and w in self._structure[v]):
            return self._structure[v][w]
        return None

    def degree(self, v):
        """ Return the degree of vertex v. """
        return len(self._structure[v])

    #--------------------------------------------------#
    #ADT methods to modify the graph
    
    def add_vertex(self, element):
        """ Add a new vertex with data element.

            If there is already a vertex with the same data element,
            this will create another vertex instance.
        """
        v = Vertex(element)
        self._structure[v] = dict()
        return v

    def add_vertex_if_new(self, element):
        """ Add and return a vertex with element, if not already in graph.

            Checks for equality between the elements. If there is special
            meaning to parts of the element (e.g. element is a tuple, with an
            'id' in cell 0), then this method may create multiple vertices with
            the same 'id' if any other parts of element are different.

            To ensure vertices are unique for individual parts of element,
            separate methods need to be written.
        """
        for v in self._structure:
            if v.element() == element:
                #print('Already there')
                return v
        return self.add_vertex(element)

    def add_edge(self, v, w, element):
        """ Add and return an edge between two vertices v and w, with  element.

            If either v or w are not vertices in the graph, does not add, and
            returns None.
            
            If an edge already exists between v and w, this will
            replace the previous edge.
        """
        if not v in self._structure or not w in self._structure:
            return None
        e = Edge(v, w, element)
        self._structure[v][w] = e
        self._structure[w][v] = e
        return e

    def add_edge_pairs(self, elist):
        """ add all vertex pairs in elist as edges with empty elements. """
        for (v,w) in elist:
            self.add_edge(v,w,None)

    #--------------------------------------------------#
    #Additional methods to explore the graph
        
    def highestdegreevertex(self):
        """ Return the vertex with highest degree. """
        hd = -1
        hdv = None
        for v in self._structure:
            if self.degree(v) > hd:
                hd = self.degree(v)
                hdv = v
        return hdv            

    #--------------------------------------------------#
    #New methods for Lab 05
    
    def dfs_stack(self, v):
        """ Return a DFS tree from v, using a stack.        """
        marked = {}
        stack = Stack()
        stack.push((v,None))
        # print('   pushed', v, 'from None')
        while stack.length() > 0:
            (vertex,edge) = stack.pop()
            if vertex not in marked:
                # print('popped unvisited', vertex)
                marked[vertex] = edge
                for e in self.get_edges(vertex):
                    w = e.opposite(vertex)
                    stack.push((w,e))
                    # print('   pushed', w, 'from', e)
        return marked

    def dfs_stack_with_error(self, v):
        """ Return a tree from v, using a stack, but NOT a DFS tree.

        There is a logical error in the code, which means that the method
        is not generating a DFS tree (but it is iterating over all vertices
        in the graph, and does produce a tree). What is the error?

        Note that the different DFS methods may generate different DFS trees,
        depending on the order in which the edges are presented by the graph
        and on the way the particular DFS method handles that order. But that
        is not the source of the error.
        """
        marked = {v:None}
        stack = Stack()
        stack.push(v)
        while stack.length() > 0:
            vertex = stack.pop()
            for e in self.get_edges(vertex):
                w = e.opposite(vertex)
                if w not in marked:
                    marked[w] = e
                    stack.push(w)
        return marked

    def depthfirstsearch(self, v):
        """ Return a DFS tree from v. """
        marked = {v:None}
        self._depthfirstsearch(v, marked)
        return marked

    def _depthfirstsearch(self, v, marked):
        """ Do a recursive DFS from v, storing nodes in marked. """
        for e in self.get_edges(v):
            w = e.opposite(v)
            if w not in marked:
                marked[w] = e
                self._depthfirstsearch(w, marked)
                
    def breadthfirstsearch(self, v):
        """ Return a BFS tree from v. """
        marked = {v:None}
        level = [v]
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.get_edges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = e
                        nextlevel.append(x)
            level = nextlevel
        return marked

    def BFS_length(self, v):
        """ Return a BFS tree from v, with path lengths. """
        marked = {v:(None,0)}
        level = [v]
        levelint = 1
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.get_edges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = (w, levelint)
                        nextlevel.append(x)
            level = nextlevel
            levelint += 1
        return marked
    
    def breadthfirstsearchtree(self, v):
        """ Return a down-directed BFS tree from v. """
        marked = {v:[]}
        level = [v]
        while len(level) > 0:
            nextlevel = []
            for w in level:
                for e in self.get_edges(w):
                    x = e.opposite(w)
                    if x not in marked:
                        marked[x] = []
                        marked[w].append(x)
                        nextlevel.append(x)
            level = nextlevel
        return marked

    def transitiveclosure(self):
        """ Return the transitive closure using version of FloydWarshall. """
        gstar = copy.deepcopy(self)
        vs = gstar.vertices()
        n = len(vs)
        for k in range(n):
            for i in range(n):
                if i != k and gstar.get_edge(vs[i], vs[k]) is not None:
                    for j in range(n):
                        if (i != j and k != j
                                     and gstar.get_edge(vs[k],vs[j]) is not None):
                            if gstar.get_edge(vs[i],vs[j]) == None:
                                gstar.add_edge(vs[i],vs[j],1)
        return gstar

    # dijkstra
    def dijkstra(self, s):
        ''' find all shortest paths from s'''
        # apq starts as an empty APQ
        apq = APQ()
        # locs is an empty dictionary (keys are vertices, values are location in apq)
        locs = {}
        # closed starts as an empty dictionary
        closed = {}
        # preds starts as a dictionary with value for s = None
        pred = {}
        pred[s] = None
        # add s with APQ key 0 to apq, and add s:(elt returned from APQ) to locs
        locs[s] = apq.add(0,s)
        # while apq is not empty
        while apq.length() > 0:
        #   remove the min element v and its cost (key) from apq
            vcost, v = apq.remove_min()
        #   remove the entry for v from locs and preds (which returns predecessor)
            del locs[v]
        #   add an entry for v:(cost, predecessor) into closed
        #   close dict = record cost to get to v and the path it took v (explored and final)
            closed[v] = (vcost ,pred[v]) # path took to v
        #   for each edge e from v
            for e in self.get_edges(v):
        #       w is the opposite vertex to v in e
                w = e.opposite(v)
        #       if w is not in closed
                if w not in closed:
        #           newcost is v's key plus e's cost 
                    ecost = e.element()
                    newcost = vcost + ecost
        #           if w is not in locs //i.e. not yet added into apq
                    if w not in locs:
        #               add w:v to preds, 
                        pred[w] = v
        #               add w:newcost to apq, add w:(elt returned from apq) to locs
                        locs[w] = apq.add(newcost,w)
        #           else if newcost is better than w's oldcost
                    elif newcost < apq.get_key(locs[w]):                      
        #               update w:v in preds, update w's cost in apq to newcost
                        pred[w] = v
                        apq.update_key(locs[w], newcost)
        # return closed
        return closed

def graphreader(filename):
    """ Read and return the route map in filename. """
    graph = Graph()
    file = open(filename, 'r')
    entry = file.readline() #either 'Node' or 'Edge'
    num = 0
    while entry == 'Node\n':
        num += 1
        nodeid = int(file.readline().split()[1])
        vertex = graph.add_vertex(nodeid)
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'vertices and added into the graph')
    num = 0
    while entry == 'Edge\n':
        num += 1
        source = int(file.readline().split()[1])
        sv = graph.get_vertex_by_label(source)
        target = int(file.readline().split()[1])
        tv = graph.get_vertex_by_label(target)
        length = float(file.readline().split()[1])
        edge = graph.add_edge(sv, tv, length)
        file.readline() #read the one-way data
        entry = file.readline() #either 'Node' or 'Edge'
    print('Read', num, 'edges and added into the graph')
    print(graph)
    return graph

def test():
    graph = graphreader("simplegraph1.txt")
    i = graph.get_vertex_by_label(1)
    t = graph.dijkstra(i)
    for v in t:
        vcost, pred = t[v]
        print('vertex =',v ,'| pred =', pred , '| cost of the shortest path :', vcost,'|')

test()

def test2():
    graph = graphreader("simplegraph2.txt")
    i = graph.get_vertex_by_label(1)
    t = graph.dijkstra(i)
    for v in t:
        vcost, pred = t[v]
        print('vertex =',v ,', pred =', pred , '| cost of the shortest path :', vcost,'|')

test2()
