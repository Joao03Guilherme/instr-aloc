"""
ALgoritmo de alocação baseado no fluxo de uma rede
A implementação é feita com o algoritmo de Ford-Fulkerson
- Não contempla a possibilidade de um curso não abrir
- Não contempla a escala de -1 a 2 de preferências
"""

from NetworkFlow import FordFulkersonNetworkFlowSolver
INF = 1e10

class Instructor:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.allocated = False
        self.course = None
        
class Course:
    def __init__(self, name, id, min_instructors):
        self.name = name
        self.min_instructors = min_instructors
        self.id = id
        self.allocated_instructors = []
           
def dummy_values():
    instr_names = ["A", "B", "C", "D", "E"]
    courses = [("X", 1), ("Y", 3), ("Z", 1)] # Course name and minimum number of instructors
    preferences = [
        [False, True, True],
        [True, False, False],
        [True, True, True],
        [False, False, True],
        [True, True, True],
    ]
    return instr_names, courses, preferences

def build_bipartite_graph(instr_list, course_list, preferences, tight : bool):
    n = len(instr_list) + len(course_list) + 2 # Add two vertices for source and sink
    solver = FordFulkersonNetworkFlowSolver(n, n-1, n-2)
    
    id = 0 
    for course in course_list:
        min_number_instructors = course.min_instructors if tight else INF
        solver.add_edge(id, n-2, min_number_instructors) # Add edge to sink
        id += 1
    
    for i, instructor in enumerate(instr_list):    
        solver.add_edge(n-1, id, 1) # Add edge to instructor
        if not instructor.allocated:
            for j, preference in enumerate(preferences[i]):
                if preference:
                    solver.add_edge(id, j, 1) # Courses start at 0  
        id += 1
        
    return solver
     
def main():
    instructors, courses, preferences = dummy_values()
    instr_list, course_list, ids = [], [], {}
    
    id = 0 
    for name, min_number_instructors in courses:
        course = Course(name, id, min_number_instructors)
        ids[id] = course
        course_list.append(course)
        id += 1
    
    for i, name in enumerate(instructors):
        instructor = Instructor(name, id)
        ids[id] = instructor         
        instr_list.append(instructor)   
        id += 1
    
    # First pass is to guarantee minimum number of instructors
    # Second pass is to allocate remaining instructors
    for p in range(2):
        solver = build_bipartite_graph(instr_list, course_list, preferences, 1 - p)
        graph = solver.get_graph()
        
        for i in range(len(course_list), len(course_list) + len(instr_list)):
            instructor = ids[i] 
            for edge in graph[i]:
                if edge.flow > 0: 
                    course = ids[edge.end]
                    print(f"Instructor: {instructor.name} | Course: {course.name}")
                    instructor.allocated = True
                    instructor.course = course 
                    course.allocated_instructors.append(instructor)
                    break
                  
if __name__ == "__main__":
    main()