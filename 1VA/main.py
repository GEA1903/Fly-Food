class FoodDelivery:
    def __init__(self, nome_arquivo='matriz.txt', valores={}):
        self.valores = valores if valores is not None else {}
        self.nome_arquivo = nome_arquivo




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
    
    def calculo_distancia(self):
        """
        Calcula o custo de viagem tomando como base a distância de Manhattan que soma os deslocamentos horizontais e verticais entre cada ponto
        """
        
