import os
from deap import base, creator, tools, algorithms
import random
import time

class Brazil58:
    def __init__(self, nome_arquivo='brazil58.tsp', valores={}):
        self.valores = valores if valores is not None else {}
        self.nome_arquivo = nome_arquivo
        self.matriz = []
        self.ponto_origem = None
    
    def ler_tsp_explicit(self, nome_arquivo):
        """
        Lê um arquivo .tsp (EDGE_WEIGHT_TYPE: EXPLICIT, EDGE_WEIGHT_FORMAT: UPPER_ROW)
        e armazena:
        - self.matriz: matriz NxN de distâncias
        - self.valores: {'R': 0, 'C1': 1, 'C2': 2, ..., 'C57': 57}
        O ponto inicial 'R' é a cidade de índice 0.
        """
        pasta_script = os.path.dirname(os.path.abspath(__file__))
        caminho_completo = os.path.join(pasta_script, nome_arquivo)

        if not os.path.exists(caminho_completo):
            raise FileNotFoundError(f"Arquivo não encontrado: {caminho_completo}")

        def to_number(s):
            return int(s) if s.isdigit() else float(s)

        dimension = None
        edge_format = None
        in_section = False
        tokens = []

        with open(caminho_completo, 'r') as f:
            for raw in f:
                line = raw.strip()
                if not line:
                    continue
                if line.upper() == 'EOF':
                    break
                if in_section:
                    tokens.extend(line.split())
                    continue

                up = line.upper()
                if up.startswith('DIMENSION'):
                    dimension = int(line.split()[-1])
                elif up.startswith('EDGE_WEIGHT_FORMAT'):
                    edge_format = line.split()[-1].upper()
                elif up.startswith('EDGE_WEIGHT_SECTION'):
                    in_section = True

        if dimension is None or edge_format is None:
            raise ValueError("Cabeçalho do arquivo .tsp está incompleto.")
        if not tokens:
            raise ValueError("Nenhum dado numérico encontrado na EDGE_WEIGHT_SECTION.")

        nums = [to_number(t) for t in tokens]
        n = dimension
        matriz = [[0]*n for _ in range(n)]

        if edge_format == 'UPPER_ROW':
            idx = 0
            for i in range(n):
                for j in range(i+1, n):
                    val = nums[idx]
                    matriz[i][j] = val
                    matriz[j][i] = val
                    idx += 1
        else:
            raise NotImplementedError(f"Formato '{edge_format}' ainda não implementado.")

        # ✅ Armazena no estado interno da classe
        self.matriz = matriz
        self.valores = {'R': 0}
        for i in range(1, n):
            self.valores[f'C{i}'] = i

        print(f"Arquivo '{nome_arquivo}' lido com sucesso.")
        print(f"Dimensão: {n}")
        print(f"Ponto inicial: R (índice 0)")
        print(f"Primeira linha da matriz: {matriz[0][:10]}")

        return matriz
    
    def distancia_rota_tsp(self, sequencia_pontos):
        # CHAMAR ESSE MÉTODO DENTRO DO ALGORITMO GENÉTICO AO INVÉS DE CHAMAR O DISTANCIA_ROTA
        #
        """
        Calcula a distância total de uma rota (lista de nomes como ['C3','C10',...]).
        - Se self.matriz existir → usa a matriz de distâncias (TSP)
        - Caso contrário → usa distância Manhattan (modo grid)
        """
        if not sequencia_pontos:
            return 0

        if self.matriz:  # usa matriz do TSP
            total = 0
            origem_idx = self.valores['R']
            total += self.matriz[origem_idx][self.valores[sequencia_pontos[0]]]

            for i in range(len(sequencia_pontos) - 1):
                a = self.valores[sequencia_pontos[i]]
                b = self.valores[sequencia_pontos[i + 1]]
                total += self.matriz[a][b]

            total += self.matriz[self.valores[sequencia_pontos[-1]]][origem_idx]
            return total
        else:
            # fallback para modo grade (Manhattan)
            total = 0
            origem = self.valores['R']
            total += self.distancia(origem, self.valores[sequencia_pontos[0]])
            for i in range(len(sequencia_pontos) - 1):
                total += self.distancia(self.valores[sequencia_pontos[i]], self.valores[sequencia_pontos[i + 1]])
            total += self.distancia(self.valores[sequencia_pontos[-1]], origem)
            return total
        
#paramentros foram ajustados para melhor desempenho no Brazil58
    def algoritmo_genetico(self,
                            tamanho_populacao=500,
                            geracoes=15000,
                            taxa_mutacao=0.25,
                            taxa_crossover=0.75,
                            verbose=True):
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
            return (self.distancia_rota_tsp(rota_nomes),) # Retorna uma tupla
        #FUNCAO DE MUTAÇAO 2-OPT USADO EM TSP PARA MELHOR DESEMPENHO
        def mutacao_2opt(individuo):
            """Mutação 2-opt: inverte um segmento da rota para melhorar localmente"""
            size = len(individuo)
            if size < 2:
                return individuo,
            i, j = sorted(random.sample(range(size), 2))
            individuo[i:j+1] = reversed(individuo[i:j+1])
            return individuo,
        
        # Mapeia nomes dos pontos para índices
        toolbox.register("indices", random.sample,range(n_pontos), n_pontos) # Gera uma permutação dos índices de forma aleatória--> cria a sequencia inicial dos individuos(genotipo), garantindo a permutaão
        toolbox.register("individual",tools.initIterate,creator.Individual,toolbox.indices)#iniciacializa um individuo com o formato esperado pelo DEAP
        toolbox.register("population",tools.initRepeat,list,toolbox.individual)#Cria uma lista de individuos, chamado toolbox.individual() repetidamente --> maneira padrao de construção de população

        toolbox.register("evaluate",avaliar_individuo)#Recebe um individuo e retorna a tupla com os valores de fitness--> funcao converte indice em nome e calcula a distancia total da rota com self.distancia_rota
        #TUDO MODIFICADO A PARTIR DAQUI
        toolbox.register("mate",tools.cxPartialyMatched) #CROSSOVER PMX - melhor para TSP 
        toolbox.register("mutate", mutacao_2opt) #MUTAÇAO 2-opt - muito eficaz para TSP
        toolbox.register("select",tools.selTournament,tournsize=5) #Torneio mais seletivo

        # Cria a população inicial
        populacao = toolbox.population(n=tamanho_populacao)

        #ESTATISTICAS PARA ACOMPANHAR O PROGRESSO
        stats= tools.Statistics(lambda ind: ind.fitness.values)
        stats.register("min", min)
        stats.register("avg", lambda x: sum(val[0] for val in x) / len(x))
        stats.register("max", max)

        #HALL OF FAME: armazena o melhor individuo encontrado
        hall_of_fame = tools.HallOfFame(5)
        
        if verbose:
            print("Iniciando evolução genética...")
        
        #Algoritimo evolutivo --> mudado para eaMuPlusLambda
        populacao, logbook= algorithms.eaMuPlusLambda(  
            populacao,
            toolbox,
            mu=tamanho_populacao, 
            lambda_=tamanho_populacao, 
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
        melhor_rota_string= " ".join(rota_nomes)

        if verbose:
            print(f"Melhor solução encontrada:")
            print(f"Rota:{melhor_rota_string}") 
            print(f"Distância total: {melhor_distancia} dronômetros")
        return melhor_rota_string, melhor_distancia
    


if __name__ == "__main__":

    solver = Brazil58()

    inicio_total = time.time()
    inicio_leitura = time.time()

    solver.ler_tsp_explicit('brazil58.tsp')
    fim_leitura = time.time()

    inicio_rota = time.time()
    melhor_rota, menor_distancia = solver.algoritmo_genetico()
    fim_rota = time.time()

    fim_total = time.time()

    print(f"Melhor rota encontrada: {melhor_rota}")
    print(f"Menor distância total: {menor_distancia} dronômetros")
    print(f"Tempo de leitura da matriz: {fim_leitura - inicio_leitura:.2f} s")
    print(f"Tempo de cálculo da rota:   {fim_rota - inicio_rota:.2f} s")
    print(f"Tempo total do programa:    {fim_total - inicio_total:.2f} s")