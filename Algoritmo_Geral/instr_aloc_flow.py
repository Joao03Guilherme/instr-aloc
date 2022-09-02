import os
import pandas as pd
from network_flow_algorithm import FastMinCostNetworkFlowSolver

INF = 999

STAFF_FORM_FILENAME ="data.csv"
OUTPUT_FILENAME = "output.csv"
COURSE_DATA_FILENAME = "course_data.csv"

# Changing python running directory
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

class Instructor:
    def __init__(self, email, id):
        self.email = email
        self.allocated = False
        self.course = None 
        self.possible_months = None
        self.id = id
        
class Course:
    def __init__(self, name, id, min_staff, max_staff):
        self.name = name
        self.min_staff = min_staff
        self.max_staff = max_staff
        self.allocated_instructors = []
        self.can_open = True
        self.id = id

class Preference:
    def __init__(self, instructor, course, preference_value : int, possible_months):
        self.instructor = instructor
        self.course = course
        self.preference_value = preference_value
        self.possible_months = possible_months

def get_course_or_instructor_by_id(course_or_instructor_list, id):
    for course_or_instructor in course_or_instructor_list:
        if course_or_instructor.id == id:
            return course_or_instructor 

def get_course_by_name(course_list, name):
    for course in course_list:
        if course.name == name:
            return course

def get_instructor_by_email(instructor_list, email):
    for instructor in instructor_list:
        if instructor.email == email:
            return instructor

def import_data():
    """Imports data from csv to python.
    It expects two csv files:
        Staff Form data: input data to have 4 columns (email, interest, name, possible_months) 
        Course Staff needs: input data to have 3 columns: course name, minimum staff and maximum staff.
    Returns:
        instructor_emails (np.ndarray): instrutors email.
        interests (dict): maps instructor email to list of interests in courses
        staff_per_course (dict): maps course_name to staff requirements (min and max)
    """
    df_staff_form = pd.read_csv(STAFF_FORM_FILENAME) 
    df_course_data = pd.read_csv(COURSE_DATA_FILENAME)

    instructor_emails = set(df_staff_form["email"].values)
    open_course_names = set(df_staff_form["name"].values)
    interests = {email : [] for email in instructor_emails}
    for email, interest, name, possible_months in df_staff_form.values:
        possible_months_list = possible_months.strip("}{").split(",")
        biased_interest = 10 ** int(interest) + len(possible_months_list) # Give more value to preference that has more months
        interests[email].append((name, biased_interest, possible_months_list))
    

    course_names = df_course_data["course"].values
    course_min_staff = df_course_data["min_staff"].values.astype(int)
    course_max_staff = df_course_data["max_staff"].values.astype(int)
    # Load minimum and maximum staff per course
    staff_per_course = {}
    for i, course_name in enumerate(course_names):
        if course_name in open_course_names: staff_per_course[course_name] = (int(course_min_staff[i]), int(course_max_staff[i]))

    for course_name in open_course_names:
        if course_name not in staff_per_course:
            raise KeyError(f"O curso '{course_name}' não tem os requisitos definidos no ficheiro '{COURSE_DATA_FILENAME}'")

    return instructor_emails, interests, staff_per_course

def output_data(course_list, instr_list):
    """Outputs result to a csv file.
    Args:
        course_list (list): List of Course objects.
        instr_list (list): List of Instructor objects.
    """
    output_data = []
    for course in course_list:
        if course.can_open:
            for instructor in course.allocated_instructors:
                output_data.append([course.name, instructor.email, instructor.possible_months])

    for instructor in instr_list:
        if not instructor.allocated:
            output_data.append(["Sem curso", instructor.email, "None"])
    
    df = pd.DataFrame(output_data)
    df.columns = ["Course", "Email", "Possible Months"]
    df.to_csv(OUTPUT_FILENAME, sep=",", index=False)
    
def build_bipartite_graph(instructor_list, course_list, preferences, tight):
    """Returns a flow network with instructors and courses as vertices
    Args:
        instructor_list (list): List of Instructor objects
        course_list (list): List of Course objects
        preferences (dict): Maps email to list of Preference objects 
        tight (bool): True if the algorithm is trying to guarantee the minimum number of instructors per course
    """
    n = len(instructor_list) + len(course_list) + 2 # Add two vertices for source and sink
    s, t = n - 1, n - 2
    edges = []

    for course in course_list:
        if course.can_open:
            n_of_allocated_instructors = len(course.allocated_instructors)
            min_staff = course.min_staff - n_of_allocated_instructors if tight else course.max_staff - n_of_allocated_instructors
            edges.append((course.id, t, min_staff, 0)) # Add edge from course to sink
    
    for instructor in instructor_list:    
        if not instructor.allocated:
            edges.append((s, instructor.id, 1, 0)) # Add edge from source to instructor
            for preference in preferences[instructor.email]:
                if preference.course.can_open:
                    edges.append((instructor.id, preference.course.id, 1, int(INF - preference.preference_value))) # Minimize cost 

    solver = FastMinCostNetworkFlowSolver(n, s, t)
    for edge in edges:
        solver.add_edge(*edge)

    return solver

def run_solver(instructor_list, course_list, preferences, tight):
    """Runs the graph-flow allocation algorithm
    Args:
        instructor_list (list): List of Instructor objects
        course_list (list): List of Course objects
        preferences (dict): Maps email to list of Preference objects 
        tight (bool): True if the algorithm is trying to guarantee the minimum number of instructors per course
    """
    solver = build_bipartite_graph(instructor_list, course_list, preferences, tight)
    graph = solver.get_graph()
    
    for instructor in instructor_list: 
        for edge in graph[instructor.id]:
            if edge.flow > 0:
                course = get_course_or_instructor_by_id(course_list, edge.end)
                for preference in preferences[instructor.email]:
                    if preference.course == course:
                        instructor.allocated = True
                        instructor.course = course 
                        instructor.possible_months = preference.possible_months
                        course.allocated_instructors.append(instructor)
                        break
                break
     
def main():
    instructor_emails, interests, staff_per_course = import_data()
    instructor_list, course_list, preferences = [], [], {email : [] for email in instructor_emails}
    
    id = 0
    for course_name, (min_staff, max_staff) in staff_per_course.items():
        course = Course(course_name, id, min_staff, max_staff)
        course_list.append(course)
        id += 1
    
    for email in instructor_emails:
        instructor = Instructor(email, id)
        instructor_list.append(instructor)
        id += 1   
   
    for instructor_email, interest_list in interests.items():
        for interest in interest_list:
            instructor = get_instructor_by_email(instructor_list, instructor_email)
            course = get_course_by_name(course_list, interest[0])
            preference_value : int = interest[1]
            possible_months : list = interest[2]
            preferences[instructor_email].append(Preference(instructor, course, preference_value, possible_months))
        
    
    # First pass is to guarantee minimum number of instructors
    run_solver(instructor_list, course_list, preferences,  True)

    # Iteratively remove courses with not enough instructors and re-run the algorithm
    for course in course_list:
        if len(course.allocated_instructors) < course.min_staff:
            course.can_open = False 
            for instructor in course.allocated_instructors:
                instructor.allocated = False 
                instructor.course = None

            run_solver(instructor_list, course_list, preferences, True)

    # Last run to allocate remaining instructors
    run_solver(instructor_list, course_list, preferences, False)
    output_data(course_list, instructor_list)
                  
if __name__ == "__main__":
    main()
