from argparse import ArgumentError
from network_flow_algorithm import FastMinCostNetworkFlowSolver
import pandas as pd 
import os

INF = 999

INPUT_OUTPUT_FILENAME="data.xlsx"
OUTPUT_FILENAME = "output.xlsx"
INPUT_COURSE_DATA_FILENAME = "course_data.xlsx"

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
    It expects two excel files:
        Staff Form data: input data to have 5 initial columns (index, timestamp, name, email, phone, availability) and then all the preferences.
        Course Staff needs: input data to have 3 rows: course name, minimum staff and maximum staff.
    Returns:
        instructors (pd.DataFrame): instrutors name and email.
        courses (pd.DataFrame): list of courses.
        preferences (pd.DataFrame): instrutors' preferences.
    """
    df_staff_form = pd.read_excel(INPUT_OUTPUT_FILENAME) 
    df_course_needs = pd.read_excel(INPUT_COURSE_DATA_FILENAME)

    preferences = df_staff_form.iloc[:, 6:].fillna(-1).values.astype(int)  # [X:-X] depends on the Excel format
    instructors = df_staff_form[["Nome","Email"]].values
    open_course_names = df_staff_form.columns[6:].values
    
    course_names = df_course_needs.columns[1:].values
    course_min_staff = df_course_needs.iloc[0, 1:].values.astype(int)
    course_max_staff = df_course_needs.iloc[1, 1:].values.astype(int)

    print
    # Load minimum and maximum staff per course
    staff_per_course = {}
    for i, course_name in enumerate(course_names):
        if course_min_staff[i] > course_max_staff[i]:
            raise ArgumentError # Min Staff must not be greater than max staff

        staff_per_course[course_name] = (int(course_min_staff[i]), int(course_max_staff[i])) 
        
    # Get data only for open courses
    staff_per_open_course = {}
    for course_name in open_course_names:
        staff_per_open_course[course_name] = staff_per_course[course_name]

    return instructors, staff_per_open_course, preferences

def output_data(course_list, instr_list):
    """Outputs data to a 'beautiful' Excel file.
    Args:
        course_list (list): List of courses, each course is an object.
        instr_list (list): List of instructors.
        course (object): Course information.
        instructor (object): Instructor information.
    """
    output_data = []
    for course in course_list:
        if course.can_open:
            for instructor in course.allocated_instructors:
                output_data.append([course.name, instructor.name, instructor.email])

    for instructor in instr_list:
        if not instructor.allocated:
            output_data.append(["Sem curso", instructor.name, instructor.email])
    
    df = pd.DataFrame(output_data)
    df.columns = ["Curso", "Nome", "Email"]
    df.to_excel(OUTPUT_FILENAME)
    

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
    s, t = n - 1, n - 2
    edges = []

    for course in course_list:
        if course.can_open:
            n_of_allocated_instructors = len(course.allocated_instructors)
            min_staff = course.min_staff - n_of_allocated_instructors if tight else course.max_staff - n_of_allocated_instructors
            edges.append((course.id, t, min_staff, 0)) # Add edge from course to sink
    
    for i, instructor in enumerate(instr_list):    
        if not instructor.allocated:
            edges.append((s, instructor.id, 1, 0)) # Add edge from source to instructor
            for j, preference in enumerate(preferences[i]):
                course = id_to_course_or_instructor[j]
                if course.can_open and preference != -1:
                    edges.append((instructor.id, course.id, 1, int(2 - preference))) # Minimize cost 

    solver = FastMinCostNetworkFlowSolver(n, s, t)
    for edge in edges:
        solver.add_edge(*edge)

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
    instructor_list, course_list, id_to_course_or_instructor = [], [], {}
    
    id = 0 
    for name, (min_staff, max_staff) in staff_per_course.items():
        course = Course(name, id, min_staff, max_staff)
        id_to_course_or_instructor[id] = course
        course_list.append(course)
        id += 1
    
    for (name, email) in instructors:
        instructor = Instructor(name, id, email)
        id_to_course_or_instructor[id] = instructor         
        instructor_list.append(instructor)   
        id += 1
   
    # First pass is to guarantee minimum number of instructors
    run_solver(instructor_list, course_list, preferences, id_to_course_or_instructor, True)

    # Iteratively remove courses with not enough instructors and re-run the algorithm
    for course in course_list:
        if len(course.allocated_instructors) < course.min_staff:
            course.can_open = False 
            for instructor in course.allocated_instructors:
                instructor.allocated = False 
                instructor.course = None

            run_solver(instructor_list, course_list, preferences, id_to_course_or_instructor, True)

    # Last run to allocate remaining instructors
    run_solver(instructor_list, course_list, preferences, id_to_course_or_instructor, False)
    output_data(course_list, instructor_list)
                  
if __name__ == "__main__":
    main()