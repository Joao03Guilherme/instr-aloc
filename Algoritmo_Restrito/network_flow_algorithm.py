"""
Implements the Edmonds - Karp algorithm
"""
INF = 1e9

class UnweightedEdge:
    def __init__(self, start, end, capacity):
        self.start = start 
        self.end = end 
        self.capacity = capacity 
        self.flow = 0 
        self.residual : UnweightedEdge = None

    def is_residual(self):
        return self.capacity == 0

    def get_remaining_capacity(self):
        return self.capacity - self.flow 

    def augment(self, bottleneck):
        self.flow += bottleneck
        self.residual.flow -= bottleneck
    
class EdmondsKarpNetworkFlowSolver:
    def __init__(self, n, s, t):
        self.n = n
        self.s = s # Start
        self.t = t # Sink
        self.solved = False

        self.visited_token = 1
        self.visited = []

        self.max_flow = 0 
        self.graph = {}
        self.initialize_graph()

    def initialize_graph(self):
        for i in range(self.n):
            self.graph[i] = []
            self.visited.append(0)

    def add_edge(self, start, end, capacity):
        e1 = UnweightedEdge(start, end, capacity)
        e2 = UnweightedEdge(end, start, 0) # Residual edge
        e1.residual, e2.residual = e2, e1
        self.graph[start].append(e1)
        self.graph[end].append(e2)

    def get_graph(self):
        self.execute()
        return self.graph

    def get_max_flow(self):
        self.execute()
        return self.max_flow

    def execute(self):
        if self.solved: return 
        self.solved = True
        self.solve()
        
    def solve(self):
        flow = -1
        while flow != 0:
            self.visited_token += 1
            flow = self.bfs()
            self.max_flow += flow
            
    def visit(self, node):
        self.visited[node] = self.visited_token
        
    def is_visited(self, node):
        return self.visited[node] == self.visited_token
    
    def bfs(self):
        q = [self.s] # Queue
        self.visit(self.s)
        
        prev = {}
        while len(q) != 0:
            node = q.pop(0) 
            if node == self.t: break
            
            for edge in self.graph[node]:
                cap = edge.get_remaining_capacity()
                if cap > 0 and not self.is_visited(edge.end):
                    self.visit(edge.end)
                    prev[edge.end] = edge
                    q.append(edge.end)
                    
        if self.t not in prev: return 0 # Sink node is not reachable
        
        bottleNeck = INF
        node = self.t
        while node in prev:
            edge = prev[node]
            bottleNeck = min(bottleNeck, edge.get_remaining_capacity())
            node = edge.start
            
        node = self.t
        while node in prev:
            edge = prev[node]
            edge.augment(bottleNeck)
            node = edge.start
            
        return bottleNeck