# instr-aloc
Algoritmo de alocação de instrutores a cursos. \
Faz uso de algoritmos de fluxo máximo em redes.
A descrição da solução desenhada encontra-se [aqui](https://www.overleaf.com/read/cmsnhdyrpbrg).

## Organização
* A pasta *NetworkFlowAlgorithms* contém apenas os algoritmos de fluxo em rede que servem de base para o algoritmo de alocação de instrutores. 
* A pasta *InstrAlocAlgorithms* contém os ficheiros necessários para correr o algoritmo de alocação de instrutores. 

## Como executar?

Para alocar instrutores a cursos, basta correr [este ficheiro](https://github.com/Joao03Guilherme/instr-aloc/blob/master/InstrAlocAlgorithms/instr_aloc_flow.py).

**Pormenores:** 

* Aquando da execução, [este ficheiro](https://github.com/Joao03Guilherme/instr-aloc/blob/master/InstrAlocAlgorithms/NetworkFlow.py) tem de estar na mesma pasta do ficheiro anterior.
* A execução implica a existência de um ficheiro `data.xlsx` com a estrutura standard dos formulários After School. 
  * Nomeadamente, as primeiras 4 colunas são "Timestamp", "Nome", "Email" e "Em que meses esperas estar disponível para participar?" e as últimas 4 colunas são "Outros", "Quanto tempo demoraste a preencher o formulário?", "Comentários adicionais" e "Contacto telefónico". 
  * Entre estes extremos, encontram-se as colunas referentes aos cursos.