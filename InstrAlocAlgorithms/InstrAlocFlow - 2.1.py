from NetworkFlow import FastMinCostNetworkFlowSolver
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
    instructors = ["A", "B", "C", "D", "E"]
    courses = [("X", 1), ("Y", 2), ("Z", 1)]
    preferences = [ 
        [-1,  0, -1],
        [ 2, -1, -1],
        [-1,  2,  1],
        [-1,  2, -1],
        [ 2,  1,  0]
    ]

    return instructors, courses, preferences

def build_bipartite_graph(instr_list, course_list, preferences, tight : bool):
    n = len(instr_list) + len(course_list) + 2 # Add two vertices for source and sink
    solver = FastMinCostNetworkFlowSolver(n, n-1, n-2)
    
    id = 0 
    for course in course_list:
        min_number_instructors = course.min_instructors if tight else INF
        solver.add_edge(id, n-2, min_number_instructors, 0) # Add edge from course to sink
        id += 1
    
    for i, instructor in enumerate(instr_list):    
        solver.add_edge(n-1, id, 1, 0) # Add edge from source to instructor
        if not instructor.allocated:
            for j, preference in enumerate(preferences[i]):
                if preference != -1:
                    solver.add_edge(id, j, 1, 2 - preference) # Minimize cost 
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