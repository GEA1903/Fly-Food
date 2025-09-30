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
        Lê o arquivo de texto contendo a matriz e armazena as coordenadas relevantes em um dicionário.
        """
       try:
            
            with open(self.nome_arquivo, 'r') as file:      
                linhas = file.readlines()
       except FileNotFoundError:
            print("Arquivo não encontrado.")
            return None
        
        
       self.valores = {}

       for indice_linha, linha in enumerate(linhas):
            for indice_coluna, char in enumerate(linha.strip()):
                if char.isalpha() and char != '0':
                    self.valores[char] = (indice_linha, indice_coluna)
       return self.valores
    
    def ler_matriz_string(self, matriz_string):
        try:
            #LIMPA AS LINHAS
            linhas= [linha.strip() for linha in matriz_string.strip().split('\n') if linha.strip()]
            
            if not linhas:
                raise ValueError('Sting vazia')
            #RESET ESTADO
            self.valores= {}
            self.matriz= []
            self.ponto_origem=None
            self.pontos_entrega=[]
            self.linhas=0
            self.colunas=0
            
            #VERIFICA SE A PRIMEIRA LONHA SAO DIMENSOES
            primeira_linha=linhas[0].split()
            tem_dimensoes=(len(primeira_linha)==2 and all (item.isdigit() for item in primeira_linha))
            
            if tem_dimensoes:
                #FORMATO: 4 5 + DADOS
                self.linhas= int(primeira_linha[0])
                self.colunas= int(primeira_linha[1])
                
                dados_matriz= linhas[1:]
                
                if len(dados_matriz) != self.linhas:
                    raise ValueError("Numero de linhas nao corresponde ao numero de colunas")
                
                
            else:
                #FORMATO: DADOS DIRETOS
                dados= linhas
                self.linhas=len(dados)
                self.colunas=len(dados[0].replace('',''))
            
             #processa cada linha
            for i, linha in enumerate(dados):
                #REMOVE ESPACOS E CONVERTE EM LISTA DE CARACTERES
                chars=linha.replace('','')
                
                if len(chars) != self.colunas:
                    raise ValueError('Erro dectado')
                
                elementos=list(chars)
                self.matriz.append(elementos)
                
              #PROCESSA CADA CARACTERE  
            for j, char in enumerate(chars):
                if char.isalpha() and char != '0':
                    posicao=(i,j)
                    char= char.upper()
                    
                    if char=="R":
                        if self.ponto_origem:
                            raise ValueError("Multiplos pontos R")
                        self.ponto_origem= posicao
                    else:
                        if char in self.pontos_entrega:
                            raise ValueError(f'Ponto {char} duplicado')
                        
                    self.valores[char]= posicao
                    
            return self.valores
        except Exception as e:
            print(f'Error: {e}')
            #reset em caso de erro
            self.valores = {}
            self.matriz = []
            self.ponto_origem = None
            self.pontos_entrega = {}
            self.linhas = 0
            self.colunas = 0
            return None                   
        
     
        


    def distancia(self, p1, p2):
    # Distância Manhattan em grade
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


    def guloso_matriz(self, matriz):
        

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

        return rota, distancia_total   
    
    def melhor_rota(self):
        if not self.ponto_origem:
            raise ValueError
        if not self.pontos_entrega:
            raise ValueError
        
        melhor_rota=None
        melhor_distancia=float('inf')

        for ordem in permutations(self.pontos_entrega):
            rota=[self.ponto_origem] + list(ordem) + [self.ponto_origem]
   