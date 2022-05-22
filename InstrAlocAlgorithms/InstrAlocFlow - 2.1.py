from NetworkFlow import NetworkFlowSolver

def dummy_values():
    instructors = [
    'Miguel Paço',
    'José Afonso de Oliveira Moreno Neves',
    'Inês Magessi',
    'José Alexandre',
    'João Cruz',
    'Filipa Figueiredo',
    'Rodrigo Aguiar',
    'João Romana',
    'Lucas Barata Cardoso',
    'João Miguel Catelas',
    'Francisca Vieira',
    'Francisca Fernandes',
    'Marta Conceição',
    'André Redondo',
    'Armando Fortes',
    'Beatriz Lebre Branco',
    'Carolina Lebre Branco',
    'Tiago Brogueira',
    'Patrícia dos Santos Pereira',
    'Tiago Garrão',
    'Leandro Sousa',
    'Mariana Beirão Rodrigues',
    'Marta Barata',
    'Rui Vasconcelos',
    'José Rafael Cabral Correia',
    'Tiago Viegas Dias',
    'João Batista',
    'André Vicente Duarte',
    'Pedro Brito de Sá',
    'Diogo Ralo',
    'Karim Costa',
    'Gonçalo Matos',
    'Diana',
    'Alice Coimbra',
    'Henrique Tomás Alves',
    'Carolina Pinto'
    ]
    
    courses = [
    'Programação [Instrutor (MAI)]',
    'Programação [Instrutor (JUN)]',
    'Arquitetura de Computadores II [Instrutor (JUN)]',
    'Web I [Instrutor (JUN)]',
    'Astrofísica [Instrutor (JUN)]',
    'Informática e Eletrotécnica [Ciência de Dados]',
    'Informática e Eletrotécnica [Aprendizagem Profunda]',
    'Informática e Eletrotécnica [Bases de Dados]',
    'Informática e Eletrotécnica [Circuitos Elétricos e Eletrónicos]',
    'Informática e Eletrotécnica [Compiladores]',
    'Informática e Eletrotécnica [Sistemas Operativos]',
    'Informática e Eletrotécnica [Redes de Computadores]',
    'Informática e Eletrotécnica [Cibersegurança]',
    'Informática e Eletrotécnica [Programação Funcional]',
    'Informática e Eletrotécnica [Teoria da Computação]',
    'Informática e Eletrotécnica [Modelação 3D]',
    'Informática e Eletrotécnica [Web II]',
    'Informática e Eletrotécnica [Criptografia]',
    'Matemática Pura [Álgebra Linear]',
    'Matemática Pura [Teoria de Grupos]',
    'Matemática Pura [Teoria de Números]',
    'Matemática Pura [Combinatória]',
    'Matemática para Cientistas e Engenheiros [Cálculo Integral]',
    'Matemática para Cientistas e Engenheiros [Cálculo Vetorial]',
    'Matemática para Cientistas e Engenheiros [Análise Complexa]',
    'Matemática para Cientistas e Engenheiros [Equações Diferenciais]',
    'Matemática para Cientistas e Engenheiros [Estatística]',
    'Física [Física Experimental]',
    'Física [Termodinâmica]',
    'Física [Eletromagnetismo]',
    'Física [Quântica]',
    'Física [Pontes]',
    'Biologia e Ciências da Terra [Biologia Molecular e Celular]',
    'Biologia e Ciências da Terra [Virologia e Epidemiologia]',
    'Biologia e Ciências da Terra [Engenharia do Ambiente]',
    'Biologia e Ciências da Terra [Geociências]',
    'Biologia e Ciências da Terra [Química Olímpica]'
    ]
    
    preferences = [
    [1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, 0, -1, -1, -1, 1, -1, -1, -1, -1],
    [-1, 2, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 2, 1, 2, -1, 2, 2, 2, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1],
    [1, 1, 0, 0, -1, 1, 1, 2, 0, 2, 1, 1, -1, 2, 2, -1, -1, -1, 0, 1, 0, 0, 1, 0, 0, 0, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, -1, -1, -1, -1, 0, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 0, 0, 2, 1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, 1, 0, -1, 0],
    [-1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, 1, 1, 0, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1],
    [2, 2, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 2, -1, -1, -1, 1, 1, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 0, 0, 0, 0, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1],
    [1, 1, -1, -1, -1, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, -1, 2, -1, -1, -1, 1, -1, -1, -1, 1],
    [2, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, 2, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, 2],
    [-1, -1, 2, -1, -1, 2, -1, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [2, -1, -1, -1, -1, 0, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, 0, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, 1, 2, 1, 2, -1, 0, 1, 2, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, 0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 2, 1, 1, 2, 0, -1, 2, -1, -1, -1, -1, -1, 2, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, 2, 1, 0, -1, -1],
    [1, 1, -1, 0, -1, 2, 1, 1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [1, 0, 0, 0, 0, 1, 1, 1, 2, 0, 0, 0, 0, 1, 1, 1, 0, 2, 1, 0, 0, 1, 1, 1, 1, 0, 1, 2, 1, 1, 1, 0, 1, 1, 0, 0, 0],
    [1, 1, 0, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 2, -1, -1, 0, 2, -1, 2, 0, 0, 0, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, 0, -1, -1, 0, -1, -1, -1, 2, 1, 1, 0, 0],
    [0, 0, -1, -1, -1, 2, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, 2, 2, 2, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, 2, 0, 0, 0, -1, 0, -1, 2, -1, -1, 2, -1, -1, -1, 0, -1, 0, 0, -1, 2, 2, 2, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, -1, 2, -1],
    [-1, -1, -1, -1, -1, 0, 2, 1, -1, 0, 1, 1, 0, 2, 0, 2, 1, 1, 0, -1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
    [-1, -1, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, 0, 2, 2, 1, 1, 1],
    [0, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 0, -1, -1, -1, 0, -1, 0, 0, 0, -1, 1, -1, -1, -1, 2, 1, 0, 0, 2],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 2, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 2],
    [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    ]

    return instructors, courses, preferences

class Instructor:
    def __init__(self, name, id):
        self.name = name 
        self.id = id 
        self.allocated = False 
        self.course = None
        
    def add_course(self, course):
        self.allocated = True 
        self.course = course 
        
class Course:
    def __init__(self, name, id, min_number_of_instructors):
        self.name = name 
        self.id = id 
        self.min_number_of_instructors = min_number_of_instructors

def main():
    instructors, courses, preferences = dummy_values()
    instr_list, course_list, ids = [], [], {}
    
    n = len(instructors) + len(courses) + 3
    solver = NetworkFlowSolver(n, n-1, n-2)
    
    id = 0
    for name in courses:
        course = Course(name, id, 2)
        solver.add_edge(id, n-2, 2, 0) # Add edge to sink
        ids[id] = course
        
        course_list.append(course)
        id += 1
        
    for i, name in enumerate(instructors):
        instructor = Instructor(name, id)
        solver.add_edge(n-1, id, 1, 0) # Add edge to instructor
        ids[id] = instructor
        
        for j, preference in enumerate(preferences[i]):
            if preference != -1:
                solver.add_edge(id, j, 1, 2 - preference)
             
        instr_list.append(instructor)   
        id += 1
        
    
    graph = solver.get_graph()
    for instructor in instr_list:
        for edge in graph[instructor.id]:
            if edge.flow > 0:
                print(f"{instructor.name} : {ids[edge.end].name}")
    
    
if __name__ == "__main__":
    main()