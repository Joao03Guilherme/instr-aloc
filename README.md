# instr-aloc
Algoritmo de alocação de instrutores a cursos. \
Faz uso de algoritmos de fluxo máximo em redes. \
A descrição da solução desenhada encontra-se [aqui](https://drive.google.com/file/d/1QXTqFaD0hu9iJ6eI2EZQ1UUdWFIuJNfu/view?usp=sharing).

## Nota sobre o algoritmo 
O respositório contém duas versões do algoritmo. 
* A versão *restrita* não tem em consideração uma escala de preferências, apenas considera a possibilidade de alocar, ou não, um instrutor a um curso. Esta versão é baseada [nesta implementação](https://github.com/Joao03Guilherme/Network-Flow-Algorithms/blob/master/EdmondsKarp.py) do algoritmo de *Edmonds-Karp*.
* A versão *geral* considera uma escala de preferências, contemplando a possibilidade de um instrutor *preferir* um curso a outro. Esta versão é baseada [nesta implementação](https://github.com/Joao03Guilherme/Network-Flow-Algorithms/blob/master/MinCostFlow2.py) de um algoritmo de determinação de custo mínimo com fluxo máximo.

## Como executar?
* Obter os ficheiros com: `git clone https://github.com/Joao03Guilherme/instr-aloc`
* Na pasta _Algoritmo\_Geral_ inserir os dados nos dois ficheiros csv com a input para o algoritmo:
  * `data.csv`: as colunas são "email", "interest", "name" e "possible_months" (esta última pode ser omitida)
  * `course_data.csv`: contém dados referentes às necessidades de staff para cada curso (staff mínimo e máximo). É composto por três colunas: "course", "min_staff" e "max_staff".
* Executar o ficheiro `instr_aloc_flow.py`.
