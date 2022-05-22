# Adapted from: https://github.com/meysamaghighi/Kattis/blob/master/Min%20cost%20max%20flow/b.cpp
INF = 1e9

class NetworkFlowSolver:
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
        
    def get_graph(self):
        self.execute()
        return self.flow 
    
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

def main():
    n, m, s, t = map(int, input().split())
    solver = NetworkFlowSolver(n, s, t)
    for _ in range(m):
       u, v, c, w = map(int, input().split())
       solver.add_edge(u, v, c, w)

    print(solver.get_max_flow(), solver.get_min_cost())
                
if __name__ == "__main__":
    main()    