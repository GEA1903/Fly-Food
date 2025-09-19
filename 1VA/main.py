class FoodDelivery:
    def __init__(self, nome_arquivo='matriz.txt', valores={}):
        self.valores = valores
        self.nome_arquivo = nome_arquivo



# Função que vai ler um arquivo de texto contendo a matriz e passa seus valores num dicionário""
    def ler_matriz(self):
        try:
            
            #Abertura e leitura do arquivo
            with open("matriz.txt", 'r') as file: 
                linhas = file.readlines()
        except FileNotFoundError:
            print("Arquivo não encontrado.")
            return None
        
        #Definição de um dicionário para armazenar as coordenadas relevantes da matriz
        
        self.valores = {}


        #Percorre cada linha e coluna da matriz, armazenando no dicionário os caracteres como chave e sua posição como valores
        for indice_linha, linha in enumerate(linhas):
            for indice_coluna, char in enumerate(linha.strip()):
                if char.isalpha() and char != '0':
                    self.valores[char] = (indice_linha, indice_coluna)
        return self.valores
    
