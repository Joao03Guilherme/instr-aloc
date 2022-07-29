from network_flow_algorithms import FastMinCostNetworkFlowSolver
import pandas as pd 
import os

INF = 999
MIN_STAFF = 5
MAX_STAFF = 10

INPUT_OUTPUT_FILENAME="data.xlsx"
OUTPUT_FILENAME = "output.xlsx"

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
    def __init__(self, name, id, min_staff, max_staff):
        self.name = name
        self.min_staff = min_staff
        self.max_staff = max_staff
        self.id = id
        self.allocated_instructors = []
        self.can_open = True

def import_data():
    """Import data.

        It expects input data to have 5 initial columns (index, timestamp, name, email, phone, availability) and then all the preferences.
        
        Returns:
            instructors (pd.DataFrame): instrutors name and email.
            courses (pd.DataFrame): list of courses.
            preferences (pd.DataFrame): instrutors' preferences.
    """

    df = pd.read_excel(INPUT_OUTPUT_FILENAME) 
    preferences = df.iloc[:, 6:].fillna(-1).values.astype(int)  # [X:-X] depends on the Excel format
    instructors = df[["Nome","Email"]].values
    courses_names = df.columns[6:].values

    # Add minimum staff per course
    staff_per_course = {}
    for course_name in courses_names:
        staff_per_course[course_name] = (MIN_STAFF, MAX_STAFF) # Can be dynamic (e.g imported from the excel file)
        
    return instructors, staff_per_course, preferences

def output_data(course_list, course, instructor):
    """Outputs data to a 'beautiful' Excel file.

    Args:
        course_list (list): List of courses, each course is an object.
        course (object): Course information.
        instructor (object): Instructor information.
    """
    filename = "output.xlsx"
    
    output_data = []
    for course in course_list:
        if len(course.allocated_instructors) >= MIN_STAFF:
            for instructor in course.allocated_instructors:
                output_data.append([course.name, instructor.name, instructor.email])
    
    df = pd.DataFrame(output_data)
    df.columns = ["Curso", "Nome", "Email"]
    
    df.to_excel(filename)
    

def build_bipartite_graph(instr_list, course_list, preferences, id_to_course_or_instructor, tight):
    """Returns a flow network with instructors and courses
    
    Args:
        instr_list (list): List of instructors, each instructor is an object
        course_list (list): List of courses, each course is an object.
        preferences (list): List of lists, preferences[i][j] represents preference of ith instructor for the jth course
        id_to_course_or_instructor (dict): maps vertex id to instructor or course
        tight (bool): True if the algorithm is trying to guarantee the minimum number of instructors per course
    """
    n = len(instr_list) + len(course_list) + 2 # Add two vertices for source and sink
    solver = FastMinCostNetworkFlowSolver(n, n-1, n-2)

    for course in course_list:
        if course.can_open:
            n_of_allocated_instructors = len(course.allocated_instructors)
            min_staff = course.min_staff - n_of_allocated_instructors if tight else course.max_staff - n_of_allocated_instructors
            solver.add_edge(course.id, solver.t, min_staff, 0) # Add edge from course to sink
    
    for i, instructor in enumerate(instr_list):    
        if not instructor.allocated:
            solver.add_edge(solver.s, instructor.id, 1, 0) # Add edge from source to instructor
            for j, preference in enumerate(preferences[i]):
                course = id_to_course_or_instructor[j]
                if course.can_open and preference != -1:
                    solver.add_edge(instructor.id, course.id, 1, 2 - preference) # Minimize cost 

    return solver

def run_solver(instr_list, course_list, preferences, id_to_course_or_instructor, tight):
    """Runs the allocation algorithm

    Args:
        instr_list (list): List of instructor objects
        course_list (list): List of courses, each course is an object.
        preferences (list): List of lists, preferences[i][j] represents preference of ith instructor for the jth course
        id_to_course_or_instructor (dict): maps vertex id to instructor or course
        tight (bool): True if the algorithm is trying to guarantee the minimum number of instructors per course
    """
    solver = build_bipartite_graph(instr_list, course_list, preferences, id_to_course_or_instructor, tight)
    graph = solver.get_graph()
    
    for i in range(len(course_list), len(course_list) + len(instr_list)):
        instructor = id_to_course_or_instructor[i] 
        for edge in graph[i]:
            if edge.flow > 0:
                course = id_to_course_or_instructor[edge.end]
                
                instructor.allocated = True
                instructor.course = course 
                course.allocated_instructors.append(instructor)
                break
     
def main():
    instructors, staff_per_course, preferences = import_data()
    instr_list, course_list, id_to_course_or_instructor = [], [], {}
    
    id = 0 
    for name, (min_staff, max_staff) in staff_per_course.items():
        course = Course(name, id, min_staff, max_staff)
        id_to_course_or_instructor[id] = course
        course_list.append(course)
        id += 1
    
    for (name, email) in instructors:
        instructor = Instructor(name, id, email)
        id_to_course_or_instructor[id] = instructor         
        instr_list.append(instructor)   
        id += 1
   
    # First pass is to guarantee minimum number of instructors
    run_solver(instr_list, course_list, preferences, id_to_course_or_instructor, True)

    for course in course_list:
        if len(course.allocated_instructors) < course.min_staff:
            course.can_open = False 
            for instructor in course.allocated_instructors:
                instructor.allocated = False 
                instructor.course = None

            run_solver(instr_list, course_list, preferences, id_to_course_or_instructor, True)

    run_solver(instr_list, course_list, preferences, id_to_course_or_instructor, False)
    output_data(course_list, course, instructor)
                  
if __name__ == "__main__":
    main()