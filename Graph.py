import random

# Custom Graph error
class GraphError(Exception):
    pass

class Graph:
    """
    Graph Class ADT
    """

    class Edge:
        """
        Class representing an Edge in the Graph
        """
        __slots__ = ['source', 'destination']

        def __init__(self, source, destination):
            """
            DO NOT EDIT THIS METHOD!
            Class representing an Edge in a graph
            :param source: Vertex where this edge originates
            :param destination: ID of Vertex where this edge ends
            """
            self.source = source
            self.destination = destination

        def __eq__(self, other):
            return self.source == other.source and self.destination == other.destination

        def __repr__(self):
            return f"Source: {self.source} Destination: {self.destination}"

        __str__ = __repr__

    class Path:
        """
        Class representing a Path through the Graph
        """
        __slots__ = ['vertices']

        def __init__(self, vertices=[]):
            """
            DO NOT EDIT THIS METHOD!
            Class representing a path in a graph
            :param vertices: Ordered list of vertices that compose the path
            """
            self.vertices = vertices

        def __eq__(self, other):
            return self.vertices == other.vertices

        def __repr__(self):
            return f"Path: {' -> '.join([str(v) for v in self.vertices])}\n"

        __str__ = __repr__

        def add_vertex(self, vertex):
            """
            Add vertex to path
            :param vertex: vertex to add to path
            :return: None
            """
            self.vertices.append(vertex)
            return None

        def remove_vertex(self):
            """
            Removes vertex from path
            :return: exit
            """
            if self.is_empty():
                return None
            self.vertices.pop()
            return None

        def last_vertex(self):
            """
            returns the last_vertex in the path
            :return: last vertex in path
            """
            if self.is_empty():
                return None
            last = self.vertices[-1]
            return last

        def is_empty(self):
            """
            tests if path is empty
            :return: bool if path empty
            """
            if len(self.vertices) == 0:
                return True
            else:
                return False
            
    class Vertex:
        """
        Class representing a Vertex in the Graph
        """
        __slots__ = ['ID', 'edges', 'visited', 'fake']

        def __init__(self, ID):
            """
            Class representing a vertex in the graph
            :param ID : Unique ID of this vertex
            """
            self.edges = []
            self.ID = ID
            self.visited = False
            self.fake = False

        def __repr__(self):
            return f"Vertex: {self.ID}"

        __str__ = __repr__

        def __eq__(self, other):
            """
            DO NOT EDIT THIS METHOD
            :param other: Vertex to compare
            :return: Bool, True if same, otherwise False
            """
            if self.ID == other.ID and self.visited == other.visited:
                if self.fake == other.fake and len(self.edges) == len(other.edges):
                    edges = set((edge.source.ID, edge.destination) for edge in self.edges)
                    difference = [e for e in other.edges if (e.source.ID, e.destination) not in edges]
                    if len(difference) > 0:
                        return False
                    return True

        def add_edge(self, destination):
            """
            adds edge to edges list
            :param destination: edge destination
            :return: exit
            """
            new_edge = Graph.Edge(self, destination)
            self.edges.append(new_edge)

        def degree(self):
            """
            returns the amount of edges in edge_list
            :return: amount of edges
            """
            return len(self.edges)
            
        def get_edge(self, destination):
            """
            returns edges if in edge_list
            :param destination: edge destination
            :return: edge
            """
            if not self.edges:
                return None
            for item in self.edges:
                if item.destination == destination:
                    return item
            return None

        def get_edges(self):
            """
            returns list of edges
            :return: self.edges
            """
            return self.edges

        def set_fake(self):
            """
            marks vertex as fake
            :return: exit
            """
            self.fake = True

        def visit(self):
            """
            marks vertex as visited
            :return: exit
            """
            self.visited = True
        
        def is_edge(self, destination):
            """
            Removes edge from edges list
            :param destination: edge destination
            :return: bool if destination in edges
            """
            if not self.edges:
                return False
            for item in self.edges:
                if item.destination == destination:
                    return True
            return False
            
        def remove_edge(self, destination):
            """
            Removes edge from edges list
            :param destination: edge destination
            :return: exit
            """
            for item in self.edges:
                if item.destination == destination:
                    self.edges.remove(item)

    def __init__(self, size=0, connectedness=1, filename=None):
        """
        DO NOT EDIT THIS METHOD
        Construct a random DAG
        :param size: Number of vertices
        :param connectedness: Value from 0 - 1 with 1 being a fully connected graph
        :param: filename: The name of a file to use to construct the graph.
        """
        assert connectedness <= 1
        self.adj_list = {}
        self.size = size
        self.connectedness = connectedness
        self.filename = filename
        self.construct_graph()

    def __eq__(self, other):
        """
        DO NOT EDIT THIS METHOD
        Determines if 2 graphs are IDentical
        :param other: Graph Object
        :return: Bool, True if Graph objects are equal
        """
        if len(self.adj_list) == len(other.adj_list):
            for key in self.adj_list:
                if key in other.adj_list:
                    if not self.adj_list[key] == other.adj_list[key]:
                        return False
                else:
                    return False
            return True
        return False

    def generate_edges(self):
        """
        DO NOT EDIT THIS METHOD
        Generates directed edges between vertices to form a DAG
        :return: A generator object that returns a tuple of the form (source ID, destination ID)
        used to construct an edge
        """
        random.seed(10)
        for i in range(self.size):
            for j in range(i + 1, self.size):
                if random.randrange(0, 100) <= self.connectedness * 100:
                    yield [i, j]

    def get_vertex(self, ID):
        """
        search for vertex in graph
        :parameter: ID of vertex to return
        :return: vertex if in graph
        """
        
        if ID in self.adj_list:
            return self.adj_list[ID]
        else:
            return None
    
    def construct_graph(self):
        """
        Constructs a graph from a file provided or via a generator
        """
        #error and bound testing
        if self.connectedness <= 0 or self.connectedness > 1:
            raise GraphError("Improper connectedness")
        if self.filename:
            with open(self.filename) as f:
                for line in f:
                    item = line.strip().split()
                    #if key in dictionary
                    int_0 = int(item[0])
                    int_1 = int(item[1])
                    if int_0 not in self.adj_list:
                        self.adj_list[int_0] = self.Vertex(int_0)
                        if self.adj_list[int_0].get_edge(int_1) is None:
                            self.adj_list[int_0].add_edge(int_1)
                    else:
                        if not self.adj_list[int_0].is_edge(int_1):
                            self.adj_list[int_0].add_edge(int_1)
                    if int_1 not in self.adj_list:
                        self.adj_list[int_1] = self.Vertex(int_1)
        #use generator         
        else:
            if self.size <= 0:
                raise GraphError("No Filename - Improper size")
            #generator
            else:
                gen_list = self.generate_edges()
                for item in gen_list:
                    if item[0] not in self.adj_list:
                        self.adj_list[item[0]] = self.Vertex(item[0])
                        if self.adj_list[item[0]].get_edge(item[1]) is None:
                            self.adj_list[item[0]].add_edge(item[1])
                    else:
                        if not self.adj_list[item[0]].is_edge(item[1]):
                            self.adj_list[item[0]].add_edge(item[1])
                    if item[1] not in self.adj_list:
                        self.adj_list[item[1]] = self.Vertex(item[1])
         
    def BFS(self, start, target):
        """
        Traverses the graph in a BFS fashion returning a path
        :param start: vertex to start at
        :param target: vertex looking for
        :return: path to target if possible
        """
        start = self.adj_list[start]
        frontier_queue = []
        bfs_path = []
        frontier_queue.append(start)
        #bfs_path.append(start)
        the_path = self.Path([])
        discovered = {}
        #create dictionary
        while frontier_queue:
            currentv = frontier_queue.pop()
            if currentv.ID == target:
                #walkpath now
                if target in discovered:
                    bfs_path.append(target)
                    walk = target
                    while walk != start.ID:
                        edge = discovered[walk]
                        bfs_path.append(edge)
                        walk = edge
                    bfs_path.reverse()
                    for item in bfs_path:
                        the_path.add_vertex(item)
                    return the_path
            #each vertex adjV adjacent to currentV
            edge_list = currentv.get_edges()
            for item in edge_list:
                adj_ID = int(item.destination)
                adj_v = self.adj_list[adj_ID]
                if adj_v.ID not in discovered:
                    frontier_queue.append(adj_v)
                    #bfs_path.append(adj_v)
                    discovered[adj_v.ID] = currentv.ID
        no_find = self.Path([])
        return no_find

    def DFS(self, start, target, path=Path()):
        """
        Traverses the graph in a DFS fashion returning a path
        :param start: vertex to start at
        :param target: vertex looking for
        :param path: path object
        :return: path to target if possible
        """
        currentv = self.adj_list[start]
        if not currentv.visited:
            currentv.visit()
            #push to Stack
            path.add_vertex(currentv.ID)
            if path.last_vertex() == target:
                print(path)
                return path
            #iterate through all incident edges
            edge_list = currentv.get_edges()
            for item in edge_list:
                adj_ID = int(item.destination)
                adj_v = self.adj_list[adj_ID]
                print(path)
                self.DFS(adj_v.ID, target, path)
                if path.last_vertex() == target:
                    return path
            path.remove_vertex()

def fake_emails(graph, mark_fake=False):
    """
    Develops a list of vertices that lack leaving edges
    :param graph: Graph Object
    :param mark_fake: Bool for marking fake
    :return: fake_vert_list, list of "fake vertices"
    """
    def check_fake_emails(start, emails=list()):
        """
        Aids in the development of a list of vertices
        that lack leaving edges
        :param start: vertex to start at
        :param emails: list of emails
        :return: list of emails
        """
        currentV = graph.get_vertex(start)
        if not currentV.visited:
            currentV.visit()
            if currentV.degree() == 0:
                if mark_fake:
                    currentV.set_fake()
                emails.append(currentV.ID)
                return emails
            edge_list = currentV.get_edges()
            for item in edge_list[:]:
                check_fake_emails(item.destination, emails)
                if graph.get_vertex(item.destination).fake:
                    item.source.get_edges().remove(item)
                    
    fake_vert_list = []
    for key, vertex in graph.adj_list.items():
        if not graph.get_vertex(key).visited:
            check_fake_emails(key, fake_vert_list)
    return fake_vert_list
