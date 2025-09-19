class FoodDelivery:
    def __init__(self):
        self.matriz = []
        self.ponto_origem = None
        self.pontos_entrega = {}

    def ler_matriz(self):
        print("• Use 'R' para marcar o ponto de origem (restaurante)")
        print("• Use letras (A, B, C, D...) para pontos de entrega")
        
        
        try:
            while True:
              dimensao=input().strip()
              if not dimensao:
                  print("Dimensao invalida")
                  continue
              try:
                  linhas, colunas = map(int, dimensao.split())
                  if linhas <= 0 or colunas <= 0:
                      print("As dimensoes devem ser positivas")
                      continue
                  break
              except ValueError:
    