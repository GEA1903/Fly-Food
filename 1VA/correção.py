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
        