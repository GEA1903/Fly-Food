import customtkinter as ctk
from main import FoodDelivery
from frame_tela_inicial import TelaInicial
from frame_resultado import Resultado

class Program (ctk.CTk):
    def __init__(self):
        super().__init__() # inicializa a janela principal
        self.title('FlyFood')
        self.geometry('800x600+400+150') #"<largura>x<altura>+<posição_x>+<posição_y>"
        ctk.set_appearance_mode('white')

        self.atual=None

        self.mostrar_inicial()

    def trocar_tela(self, nova_tela):
        if self.atual:
              self.atual.pack_forget()
              self.atual.destroy()
        self.atual = nova_tela
        self.atual.pack(fill='both', expand=True)
        

    def mostrar_inicial(self):
            tela = TelaInicial(self)
            self.trocar_tela(tela)
        
    def mostrar_resultado(self, matriz, rota, distancia, metodo, tempo):
            tela = Resultado(self, matriz, rota, distancia, metodo, tempo)
            self.trocar_tela(tela)
if __name__ == '__main__':
    app = Program()
    app.mainloop()





    


