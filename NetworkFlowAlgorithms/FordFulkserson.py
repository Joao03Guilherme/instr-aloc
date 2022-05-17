INF = 1e10

class Edge:
    def __init__(self, start, end, capacity):
        self.start = start 
        self.end = end 
        self.capacity = capacity 
        self.flow = 0 
        self.residual = -1 # Edge object

    def is_residual(self):
        return self.capacity == 0

    def get_remaining_capacity(self):
        return self.capacity - self.flow 

    def augment(self, bottleneck):
        self.flow += bottleneck
        self.residual.flow -= bottleneck

class NetworkFlowSolver:
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
        e1 = Edge(start, end, capacity)
        e2 = Edge(end, start, 0) # Residual edge
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
        f = self.dfs(self.s, INF)
        while f != 0:
            self.max_flow += f
            self.visited_token += 1
            f = self.dfs(self.s, INF)

    def dfs(self, node, flow):
        if node == self.t: 
            return flow # reached sink

        self.visited[node] = self.visited_token
        edges = self.graph[node]
        for edge in edges:
            if edge.get_remaining_capacity() > 0 and self.visited[edge.end] != self.visited_token:
                bottleneck = self.dfs(edge.end, min(edge.get_remaining_capacity(), flow))

                # Reached sink
                if bottleneck > 0:
                    edge.augment(bottleneck)
                    return bottleneck

        return 0

def main():
    n = 4
    s = 0 # Zero indexed
    t = 3

    solver = NetworkFlowSolver(n, s, t)
    solver.add_edge(s, 1, 28374)
    solver.add_edge(1, 2, 10)
    solver.add_edge(2, t, 234)
    print(solver.get_max_flow())

if __name__ == "__main__":
    main()