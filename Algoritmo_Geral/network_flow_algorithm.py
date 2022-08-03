"""
Implements a min cost max flow algorithm
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