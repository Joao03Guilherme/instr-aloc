"""
ALgoritmo de alocação baseado no fluxo de uma rede
A implementação é feita com o algoritmo de Ford-Fulkerson
- Não contempla a possibilidade de um curso não abrir
- Não contempla a escala de -1 a 2 de preferências
"""

from random import shuffle
INF = 1e10

class Edge:
    def __init__(self, start, end, capacity):
        self.start = start 
        self.end = end 
        self.capacity = capacity 
        self.flow = 0 
        self.residual : Edge = -1 

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

class Instructor:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.allocated = False
        self.courses = []
        
    def add_course(self, course):
        if course in self.courses:
            return
        self.courses.append(course)
        
class Course:
    def __init__(self, name, id, min_instructors):
        self.name = name
        self.min_instructors = min_instructors
        self.id = id
           
def dummy_values():
    instr_names = ["Joao Guilherme", "Guilherme Penedo", 
                   "Martim Pinto", "Vasco Pires", "Bruna Fernandes"]
    courses = [("Inf1", 1), ("Algo1", 3), ("Jogos", 1)] # Course name and minimum number
    
    preferences = {}
    preferences["Martim Pinto"] = ["Inf1", "Inf1", "Algo1"]
    preferences["Joao Guilherme"] = ["Inf1", "Algo1"]
    preferences["Guilherme Penedo"] = ["Algo1", "Inf1"]
    preferences["Vasco Pires"] = ["Jogos", "Jogos", "Algo1"]
    preferences["Bruna Fernandes"] = ["Algo1", "Inf1"]
    return instr_names, courses, preferences
     
def main():
    instructor_names, course_info, preferences = dummy_values()
    number_of_instructors, number_of_courses = len(instructor_names), len(course_info)
    
    instructors, courses, ids = [], [], {} # ids maps id to course/instructor
    for i, instructor_name in enumerate(instructor_names):
        id = i + 1
        instructor = Instructor(instructor_name, id)
        ids[id] = instructor
        instructors.append(instructor)
        
    for i, c_info in enumerate(course_info):
        id = number_of_instructors + i + 1
        course = Course(c_info[0], id, c_info[1])
        ids[id] = course
        courses.append(course)
        
    for instructor in instructors:
        for course_name in preferences[instructor.name]:
            for course in courses:
                if course.name == course_name:
                    instructor.add_course(course)
                    break
                
        # shuffle(instructor.courses) # Randomize selection
                
    n = number_of_courses + number_of_instructors + 2
    s = 0 
    t = number_of_instructors + number_of_courses + 1
    
    allocated_instructors = {course : [] for course in courses}
    for x in range(2):
        solver = NetworkFlowSolver(n, s, t)
        
        for course in courses:
            if x == 0: solver.add_edge(course.id, t, course.min_instructors)
            else: solver.add_edge(course.id, t, INF)
            
        for instructor in instructors:
            if not instructor.allocated:
                solver.add_edge(s, instructor.id, 1)
                for course in instructor.courses:
                    solver.add_edge(instructor.id, course.id, 1)
            
        graph = solver.get_graph()    
        for instructor in instructors:
            if not instructor.allocated:
                for edge in graph[instructor.id]:
                    if not edge.is_residual():
                        allocated_instructors[ids[edge.end]].append(instructor)
                        instructor.allocated = True
                        
    for course, allocated_insr in allocated_instructors.items():
        print(f"COURSE : {course.name} ", end = " ")
        print(f"| ALLOCATED : {len(allocated_insr)} / {course.min_instructors}")
        for instructor in allocated_insr:
            print(f"Instructor : {instructor.name}")
            
if __name__ == "__main__":
    main()