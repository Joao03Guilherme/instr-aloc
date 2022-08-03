# instr-aloc
Algoritmo de alocação de instrutores a cursos. \
Faz uso de algoritmos de fluxo máximo em redes. \
A descrição da solução desenhada encontra-se [aqui](https://www.overleaf.com/read/cmsnhdyrpbrg).

## Nota sobre o algoritmo geral e restrito
O respositório contém duas versões do algoritmo. A versão geral é a que é efetivamente utilizada. \
O algoritmo restrito não tem em consideração a escala de preferências de cada instrutor.

## Como executar?
* Obter os ficheiros com: `git clone https://github.com/Joao03Guilherme/instr-aloc`
* Na pasta _Algoritmo\_Geral_ inserir os dados nos dois ficheiros Excel com a input para o algoritmo:
  * `data.xlsx`: as primeiras 4 colunas são "Timestamp", "Nome", "Email", "Contacto telefónico" e "Em que meses esperas estar disponível para participar?", as restantes colunas são referentes aos cursos.
  * `course_data.xlsx`: contém dados referentes às necessidades de staff para cada curso (staff mínimo e máximo). É composto por três linhas: "Curso", "Staff Mínimo" e "Staff Máximo".
* Executar o ficheiro `instr_aloc_flow.py`.