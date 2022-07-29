"""
This file contains all network flow algorithms
"""

from queue import PriorityQueue
INF = 1e9

class WeightedEdge:
    def __init__(self, end, capacity, cost, rev):
        self.end = end
        self.capacity = capacity 
        self.cost = cost 
        self.rev = rev
        self.flow = 0
        
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
        
class FordFulkersonNetworkFlowSolver:
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
    
class FastMinCostNetworkFlowSolver:
    def __init__(self, n, s, t):
        self.n = n
        self.s = s 
        self.t = t 
        self.max_flow = 0
        self.min_cost = 0
        self.solved = False
        self.visited_token = 1
        
        self.capacity = {}
        self.flow = {}
        self.cost = {}
        self.visited = {}
        self.pi = {}
        self.p = {}
        self.initialize_containers()
        
    def initialize_containers(self):
        for i in range(self.n):
            self.capacity[i] = {j : 0 for j in range(self.n)}
            self.flow[i] = {j : 0 for j in range(self.n)}
            self.cost[i] = {j : 0 for j in range(self.n)}
            self.visited[i] = 0
            self.pi[i] = 0 
            self.p[i] = 0
            
    def add_edge(self, u, v, c, w):
        self.capacity[u][v] = c
        self.cost[u][v] = w 
    
    def get_max_flow(self):
        self.execute()
        return self.max_flow
    
    def get_min_cost(self):
        self.execute()
        return self.min_cost
    
    def execute(self):
        if self.solved:
            return
        self.solved = True 
        self.solve()
        
    def unvisit_all_nodes(self):
        self.visited_token += 1 
        
    def is_visited(self, node):
        return self.visited[node] == self.visited_token
    
    def visit(self, node):
        self.visited[node] = self.visited_token
  
    def relax(self, dist, f, s, k, cap, cos, dir):
        temp = dist[s] + self.pi[s] - self.pi[k] + cos
        if cap > 0 and temp < dist[k]:
            dist[k] = temp
            self.p[k] = (s, dir)
            f[k] = min(cap, f[s])
            
    def dijkstra(self):
        self.unvisit_all_nodes()
        dist = {i : INF for i in range(self.n)}
        dist[self.s] = 0
        
        f = {i : 0 for i in range(self.n)}
        f[self.s] = INF
        
        curr = self.s 
        while curr != -1:
            best = -1
            self.visit(curr)
            for j in range(self.n):
                if self.is_visited(j): continue
                
                self.relax(dist, f, curr, j, self.capacity[curr][j] - self.flow[curr][j], 
                           self.cost[curr][j], 1)
                self.relax(dist, f, curr, j, self.flow[j][curr], -self.cost[j][curr], -1)
                if best == -1 or dist[j] < dist[best]:
                    best = j
            curr = best
            
        for i in range(self.n):
            self.pi[i] = min(self.pi[i] + dist[i], INF)
        return f[self.t]
            
    def solve(self):
        path_flow, max_flow, min_cost = 1, 0, 0
        while path_flow != 0:
            path_flow = self.dijkstra()
            if path_flow == 0: break 
            
            max_flow += path_flow
            node = self.t 
            while node != self.s:
                if self.p[node][1] == 1:
                    self.flow[self.p[node][0]][node] += path_flow
                    min_cost += path_flow * self.cost[self.p[node][0]][node]
                else:
                    self.flow[node][self.p[node][0]] -= path_flow
                    min_cost -= path_flow * self.cost[node][self.p[node][0]]
                node = self.p[node][0]
        self.max_flow = max_flow 
        self.min_cost = min_cost

class FastMinCostNetworkFlowSolver:
    def __init__(self, n, s, t):
        self.n = n 
        self.s = s 
        self.t = t
        self.max_flow = 0 
        self.min_cost = 0
        self.solved = False
        
        self.graph = {}
        self.prio = {}
        self.curflow = {}
        self.prevedge = {}
        self.prevnode = {}
        self.pot = {}
        self.init_containers()
        
    def init_containers(self):
        for i in range(self.n):
            self.graph[i] = []
            self.prio[i] = INF
            self.curflow[i] = 0 
            self.prevedge[i] = 0 
            self.prevnode[i] = 0 
            self.pot[i] = 0
            
    def get_maximum_flow(self):
        self.execute()
        return self.max_flow
    
    def get_minimum_cost(self):
        self.execute()
        return self.min_cost
    
    def get_graph(self):
        self.execute()
        return self.graph 
    
    def execute(self):
        if self.solved:
            return 
        self.solved = True 
        self.solve()
            
    def memset(self, container, size, val):
        for i in range(size):
            container[i] = val
            
    def add_edge(self, start, end, capacity, cost):
        self.graph[start].append(WeightedEdge(end, capacity, cost, len(self.graph[end])))
        self.graph[end].append(WeightedEdge(start, 0, -cost, len(self.graph[start]) - 1))
        
    def solve(self):
        maximum_flow, minimum_cost = 0, 0
        while maximum_flow < INF:
            pq = PriorityQueue()
            pq.put(self.s)
            
            self.memset(self.prio, self.n, INF)
            self.prio[self.s] = 0
            
            finished = {}
            self.memset(finished, self.n, False)
            
            self.curflow[self.s] = INF
            while not finished[self.t] and not pq.empty():
                curr = pq.get()
                u = curr & 0xFFFFFFFF
                priou = curr >> 32
                if priou != self.prio[u]:
                    continue 
                
                finished[u] = True 
                for i in range(len(self.graph[u])):
                    edge = self.graph[u][i]
                    if edge.capacity <= edge.flow: continue 
                    
                    v = edge.end
                    nprio = self.prio[u] + edge.cost + self.pot[u] - self.pot[v]
                    if self.prio[v] > nprio:
                        self.prio[v] = nprio
                        pq.put((nprio << 32) + v)
                        self.prevnode[v] = u
                        self.prevedge[v] = i
                        self.curflow[v] = min(self.curflow[u], edge.capacity - edge.flow)
                        
            if self.prio[self.t] == INF:
                break
            
            for i in range(self.n):
                if finished[i]:
                    self.pot[i] += self.prio[i] - self.prio[self.t]
                    
            path_flow = min(self.curflow[self.t], INF - self.max_flow) 
            maximum_flow += path_flow 
            
            node = self.t 
            while node != self.s:
                edge = self.graph[self.prevnode[node]][self.prevedge[node]]
                edge.flow += path_flow 
                self.graph[node][edge.rev].flow -= path_flow 
                self.min_cost += path_flow * edge.cost 
                minimum_cost += path_flow * edge.cost
                
                node = self.prevnode[node]
                
        self.max_flow = maximum_flow
        self.min_cost = minimum_cost 