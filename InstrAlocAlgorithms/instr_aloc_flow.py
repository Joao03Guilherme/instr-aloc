from NetworkFlow import FastMinCostNetworkFlowSolver
import pandas as pd 
import os
INF = 1e10
MIN_STAFF = 5

# Changing python running directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Instructor:
    def __init__(self, name, id, email):
        self.name = name
        self.id = id
        self.email = email
        self.allocated = False
        self.course = None 
        
class Course:
    def __init__(self, name, id, min_instructors):
        self.name = name
        self.min_instructors = min_instructors
        self.id = id
        self.allocated_instructors = []

def import_data():
    df = pd.read_excel("data.xlsx") 
    preferences = df.iloc[:, 5:-4].fillna(-1).values.astype(int)  # [X:-X] depends on the Excel format
    instructors = df[["Nome","Email"]].values
    courses_names = df.columns[5:-4].values

    # Add minimum staff per course
    courses = {}
    for course_name in courses_names:
        courses[course_name] = MIN_STAFF

    return instructors, courses, preferences

def output_data(course_list, course, instructor):
    """Outputs data to a 'beautiful' Excel file.

    Args:
        course_list (list): List of courses, each course is an object.
        course (object): Course information.
        instructor (object): Instructor information.

    """
    filename = "output.xlsx"
    min_instructors_per_course = MIN_STAFF * .70
    
    output_data = []
    for course in course_list:
        if len(course.allocated_instructors) >= min_instructors_per_course:
            for instructor in course.allocated_instructors:
                output_data.append([course.name, instructor.name, instructor.email])
    df = pd.DataFrame(output_data)
    df.columns = ["Curso", "Nome", "Email"]
    
    df.to_excel(filename)
    

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
    instructors, courses, preferences = import_data()
    instr_list, course_list, ids = [], [], {}
    
    id = 0 
    for name, min_number_instructors in courses.items():
        course = Course(name, id, min_number_instructors)
        ids[id] = course
        course_list.append(course)
        id += 1
    
    for i, (name, email) in enumerate(instructors):
        instructor = Instructor(name, id, email)
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
                    
                    instructor.allocated = True
                    instructor.course = course 
                    course.allocated_instructors.append(instructor)
                    break
                
    for course in course_list:
        print(f"Course: {course.name} | Instructors: {len(course.allocated_instructors)}/{course.min_instructors}")
        for instructor in course.allocated_instructors:
            print(f"--> {instructor.name}")
            
    output_data(course_list, course, instructor)
                  
if __name__ == "__main__":
    main()
