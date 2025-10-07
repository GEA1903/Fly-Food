from itertools import permutations

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


    def guloso_matriz(self):
     """    

        # 1) Encontrar R e os clientes na matriz
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                if matriz[i][j] == "R": 
                    self.ponto_origem = (i, j)
                elif matriz[i][j] == "C": # identificar se é destino da rota
                    self.pontos_entrega.append((i, j))

        if not self.ponto_origem:
            raise ValueError("Não há ponto R na matriz!")

        rota = [self.ponto_origem]
        atual = self.ponto_origem
        nao_visitados = set(self.pontos_entrega)
        distancia_total = 0

        # 2) Sempre ir para o cliente mais próximo
        while nao_visitados:
            proximo = min(nao_visitados, key=lambda c: self.distancia(atual, c))
            distancia_total += self.distancia(atual, proximo)
            rota.append(proximo)
            atual = proximo
            nao_visitados.remove(proximo)

        # 3) Voltar para R
        distancia_total += self.distancia(atual, self.ponto_origem)
        rota.append(self.ponto_origem)

        return rota, distancia_total """  
        
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
        melhor_rota_string = " ".join(melhor_rota_sequencia)

        return melhor_rota_string, menor_distancia

if __name__ == "__main__":
    # Exemplo de entrada do projeto
    matriz_exemplo = """4 5
0 0 0 0 D
0 A 0 0 0
0 0 0 0 C
R 0 B 0 0"""

    solver = FoodDelivery()
    
    # 1. Carrega os dados da matriz
    solver.ler_matriz_string(matriz_exemplo)
    
    # 2. Encontra a rota ótima
    rota, distancia = solver.melhor_rota()
    
    # 3. Imprime o resultado final
    print(f"Melhor rota encontrada: {rota}")
    print(f"Menor distância total: {distancia} dronômetros")   