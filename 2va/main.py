import time
from itertools import permutations
from pathlib import Path
import random
from deap import base, creator, tools, algorithms

class FoodDelivery:
    def __init__(self, nome_arquivo='matriz.txt', valores={}):
        self.valores = valores if valores is not None else {}
        self.nome_arquivo = nome_arquivo
        self.matriz = []
        self.ponto_origem = None
        self.pontos_entrega = []
        self.linhas = 0
        self.colunas = 0
        
        
    def ler_matriz(self):  
        """
        Lê o arquivo de texto contendo a matriz e delega o processamento 
        para ler_matriz_string().
        """
        try:
            with open(self.nome_arquivo, 'r') as file:      
                conteudo= file.read()
        except FileNotFoundError:
            print("Arquivo não encontrado.")
            return None
        except Exception as e:
            print(f"Erro ao ler o arquivo: {e}")
            return None
        
        # Delega o processamento para ler_matriz_string
        return self.ler_matriz_string(conteudo)    
    
    def ler_matriz_string(self, matriz_string):
        """
        Processa uma string contendo a matriz e armazena as coordenadas relevantes.
        Suporta dois formatos:
        1. Com dimensões na primeira linha: "4 5\\n0 0 A..."
        2. Sem dimensões: "0 0 A\\n..."
        """
        try:
            # Limpa as linhas
            linhas = [linha.strip() for linha in matriz_string.strip().split('\n') if linha.strip()]
            
            if not linhas:
                raise ValueError('String vazia')
            
            # Reset do estado
            self.valores = {}
            self.matriz = []
            self.ponto_origem = None
            self.pontos_entrega = []
            self.linhas = 0
            self.colunas = 0
            
            # Verifica se a primeira linha são dimensões
            primeira_linha = linhas[0].split()
            tem_dimensoes = (len(primeira_linha) == 2 and 
                           all(item.isdigit() for item in primeira_linha))
            
            if tem_dimensoes:
                # Formato: 4 5 + DADOS
                self.linhas = int(primeira_linha[0])
                self.colunas = int(primeira_linha[1])
                dados = linhas[1:]
                
                if len(dados) != self.linhas:
                    raise ValueError(f"Número de linhas ({len(dados)}) não corresponde "
                                   f"ao especificado ({self.linhas})")
            else:
                # Formato: DADOS DIRETOS
                dados = linhas
                self.linhas = len(dados)
                self.colunas = len(dados[0].replace(' ', ''))
            
            # Processa cada linha
            for i, linha in enumerate(dados):
                # Remove espaços e converte em lista de caracteres
                chars = linha.replace(' ', '')
                
                if len(chars) != self.colunas:
                    raise ValueError(f"Linha {i+1} tem {len(chars)} colunas, "
                                   f"esperado {self.colunas}")
                
                elementos = list(chars)
                self.matriz.append(elementos)
                
                # Processa cada caractere
                for j, char in enumerate(chars):
                    if char.isalpha() and char != '0':
                        posicao = (i, j)
                        char = char.upper()
                        
                        if char == "R":
                            if self.ponto_origem:
                                raise ValueError("Múltiplos pontos 'R' encontrados")
                            self.ponto_origem = posicao
                        else:
                            if char in self.pontos_entrega:
                                raise ValueError(f"Ponto '{char}' duplicado")
                            self.pontos_entrega.append(char)
                        
                        self.valores[char] = posicao
            
            # Validação final
            if not self.ponto_origem:
                raise ValueError("Ponto de origem 'R' não encontrado na matriz")
            
            return self.valores
            
        except Exception as e:
            print(f'Erro ao processar matriz: {e}')
            # Reset em caso de erro
            self.valores = {}
            self.matriz = []
            self.ponto_origem = None
            self.pontos_entrega = []
            self.linhas = 0
            self.colunas = 0
            return None
        
     
        


    def distancia(self, p1, p2):
    # Distância Manhattan em grade
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])
    
    def distancia_rota(self,sequencia_pontos):
        if not sequencia_pontos:
            return 0
        distancia_total = 0
        ponto_origem = self.valores['R']
        # distancia de R até o primeiro ponto
        distancia_total += self.distancia(ponto_origem, self.valores[sequencia_pontos[0]])

        # distancia entre pontos consecutivos
        for i in range(len(sequencia_pontos) - 1):
            distancia_total += self.distancia(
                self.valores[sequencia_pontos[i]],
                self.valores[sequencia_pontos[i+1]]
            )
        distancia_total += self.distancia(self.valores[sequencia_pontos[-1]], ponto_origem)

        return distancia_total

    def algoritimo_genetico(self,
                            tamanho_populacao=100,
                            geracoes=500,
                            taxa_mutacao=0.15,
                            taxa_crossover=0.8,
                            verbose=False):
        '''tamano_populacao: numero de individuos em cada geração
        geracoes: numero de gerações para evoluir
        taxa_mutacao: probabilidade de mutação
        taxa_crossover: probabilidade de crossover
        verbose: se True, imprime informações do progresso
        '''
        if 'R' not in self.valores:
            raise ValueError("Ponto de origem 'R' não encontrado em self.valores!")
        pontos_entrega_nomes = [ ponto for ponto in self.valores if ponto !='R' ]
        if not pontos_entrega_nomes:
            return "", 0 # Nenhuma entrega, rota vazia e custo zero
        n_pontos = len(pontos_entrega_nomes)
        indice_para_nome = {i:pontos_entrega_nomes[i] for i in range(n_pontos)}
        
        # Configuração do DEAP
        creator.create("FitnessMin",base.Fitness,weights=(-1.0,)) # Minimizar a distância
        creator.create("Individual",list,fitness=creator.FitnessMin)  #representa uma rota(individuos)
        toolbox = base.Toolbox() # Caixa de ferramentas--> onde serao registrados os objetivos e elementos do ag

        def avaliar_individuo(individuo):
            rota_nomes= [indice_para_nome[i] for i in individuo]
            return (self.distancia_rota(rota_nomes),) # Retorna uma tupla
        
        # Mapeia nomes dos pontos para índices
        toolbox.register("indices", random.sample,range(n_pontos), n_pontos) # Gera uma permutação dos índices de forma aleatória--> cria a sequencia inicial dos individuos(genotipo), garantindo a permutaão
        toolbox.register("individual",tools.initIterate,creator.Individual,toolbox.indices)#iniciacializa um individuo com o formato esperado pelo DEAP
        toolbox.register("population",tools.initRepeat,list,toolbox.individual)#Cria uma lista de individuos, chamado toolbox.individual() repetidamente --> maneira padrao de construção de população

        toolbox.register("evaluate",avaliar_individuo)#Recebe um individuo e retorna a tupla com os valores de fitness--> funcao converte indice em nome e calcula a distancia total da rota com self.distancia_rota
        toolbox.register("mate",tools.cxOrdered) #CROSSOVER DE ORDEM (OX) de duas permutacoes
        toolbox.register("mutate", tools.mutShuffleIndexes, indpb=0.2) #MUTAÇAO POR EMBARALHAMENTO
        toolbox.register("select",tools.selTournament,tournsize=3) #Seleção por torneio: tournsize-->controla a pressao seletiva, quanto maior, melhores individuos selecionados

        # Cria a população inicial
        populacao = toolbox.population(n=tamanho_populacao)

        #ESTATISTICAS PARA ACOMPANHAR O PROGRESSO
        stats= tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", min)
        stats.register("avg", lambda x: sum(val[0] for val in x) / len(x))
        stats.register("max", max)

        #HALL OF FAME: armazena o melhor individuo encontrado
        hall_of_fame = tools.HallOfFame(1)
        
        if verbose:
            print("Iniciando evolução genética...")
        
        #Algoritimo evolutivo 
        populacao, logbook= algorithms.eaSimple(
            populacao,
            toolbox,
            cxpb=taxa_crossover,
            mutpb=taxa_mutacao,
            ngen=geracoes,
            stats=stats,
            halloffame=hall_of_fame,
            verbose=verbose
        ) 

        #MELHOR SOLUCAO ENCONTRADA--> CONVERTE INDICE PARA NOME
        melhor_individuo= hall_of_fame[0]
        melhor_distancia= melhor_individuo.fitness.values[0]
        rota_nomes= [indice_para_nome[i] for i in melhor_individuo]
        melhor_rota_string= " - ".join(rota_nomes)

        if verbose:
            print(f"Melhor solução encontrada:")
            print(f"Rota:{melhor_rota_string}") 
            print(f"Distância total: {melhor_distancia} dronômetros")
        return melhor_rota_string, melhor_distancia


 
         

    def guloso_matriz(self):
        if 'R' not in self.valores:
            raise ValueError("Ponto de origem 'R' não encontrado!")

        atual = 'R'
        visitados = ['R']
        distancia_total = 0

        # Enquanto houver pontos não visitados
        while len(visitados) < len(self.valores):
            menor_dist = float('inf')
            proximo = None

            for ponto in self.valores:
                if ponto not in visitados:
                    d = self.distancia(self.valores[atual], self.valores[ponto])
                    if d < menor_dist:
                        menor_dist = d
                        proximo = ponto

            visitados.append(proximo)
            distancia_total += menor_dist
            atual = proximo

        # Retorna ao ponto de origem
        distancia_total += self.distancia(self.valores[atual], self.valores['R'])
        visitados.append('R')
        pontos_intermediarios=visitados[1:-1]

        # 🔹 Converte a lista em string formatada
        rota_string = " - ".join(pontos_intermediarios)

        return rota_string, distancia_total
        
    def melhor_rota(self):
        '''
        Calcula a rota de menor distância usando permutações (algoritmo exaustivo, porém o mais acertivo).
        '''
        if 'R' not in self.valores:
            raise ValueError("Ponto de origem 'R' não encontrado em self.valores!")
        
        ponto_origem_coord = self.valores['R']
        
        # Obtém a lista de nomes dos pontos de entrega (excluindo 'R')
        pontos_entrega_nomes = [
            ponto for ponto in self.valores if ponto != 'R'
        ]
        if not pontos_entrega_nomes:
            return "", 0 # Nenhuma entrega, rota vazia e custo zero

        menor_distancia = float('inf')
        melhor_rota_sequencia = None
        
        for permutacao in permutations(pontos_entrega_nomes):
            distancia_atual = 0
            
            # 1. Distância de R para o primeiro ponto
            primeiro_ponto = permutacao[0]
            distancia_atual += self.distancia(
                ponto_origem_coord, self.valores[primeiro_ponto]
            )

             # 2. Distância entre os pontos de entrega sequenciais
            for i in range(len(permutacao) - 1):
                ponto_a_nome = permutacao[i]
                ponto_b_nome = permutacao[i+1]
                distancia_atual += self.distancia(
                    self.valores[ponto_a_nome], self.valores[ponto_b_nome]
                )
             # 3. Distância do último ponto de volta para R
            ultimo_ponto = permutacao[-1]
            distancia_atual += self.distancia(
                self.valores[ultimo_ponto], ponto_origem_coord
            )
            # 4. Compara e atualiza
            if distancia_atual < menor_distancia:
                menor_distancia = distancia_atual
                melhor_rota_sequencia = permutacao

            # Formata a saída no padrão "A B C D"
        melhor_rota_string = " - ".join(melhor_rota_sequencia)

        return melhor_rota_string, menor_distancia

if __name__ == "__main__":
    inicio_total = time.time()
    # Exemplo de entrada do projeto
#     matriz_exemplo = """4 5
# 0 0 0 0 D
# 0 A 0 0 0
# 0 0 0 0 C
# R 0 B 0 0"""

    # Usa o arquivo matriz.txt localizado no mesmo diretório deste script
    solver = FoodDelivery(nome_arquivo=str(Path(__file__).resolve().parent / 'matriz.txt'))
    
    inicio_leitura = time.time()
    # 1. Carrega os dados da matriz
    solver.ler_matriz()

    # print("Valores encontrados:", solver.valores) #debug
    fim_leitura = time.time()
    
    inicio_rota = time.time()
    # 2. Escolhe o método: se houver mais de 9 pontos de entrega, usa AG; caso contrário, usa o guloso
    n_pontos = len([p for p in solver.valores if p != 'R'])
    if n_pontos > 9:
        print(f"Usando algoritmo genético (pontos de entrega: {n_pontos})")
        rota, distancia = solver.algoritimo_genetico()
    else:
        print(f"Usando algoritmo de força bruta (pontos de entrega: {n_pontos})")
        rota, distancia = solver.melhor_rota()
    fim_rota = time.time()

    fim_total = time.time()
    
    # 3. Imprime o resultado final
    print(f"Melhor rota encontrada: R - {rota} - R")
    print(f"Menor distância total: {distancia} dronômetros")   

    print(f"Tempo de leitura da matriz: {fim_leitura - inicio_leitura:.2f} s")
    print(f"Tempo de cálculo da rota:   {fim_rota - inicio_rota:.2f} s")
    print(f"Tempo total do programa:    {fim_total - inicio_total:.2f} s")
