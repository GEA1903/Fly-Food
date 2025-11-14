import customtkinter as ctk
from main import FoodDelivery


class Resultado(ctk.CTkFrame):
    def __init__ (self, master, matriz, rota, distancia,metodo):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        
        ctk.CTkLabel(self, text='Resultado da melhor rota').pack(pady=10)

        ctk.CTkLabel(self, text=f'Método usado:{metodo}').pack(pady=5)
        ctk.CTkLabel(self, text=f'Distância total: {distancia} dronômetros').pack(pady=5)

        #Exibição da matriz calculada

        ctk.CTkLabel(self, text="Matriz analisada:").pack(pady=10)
        caixa=ctk.CTkTextbox(self, height=150)
        caixa.insert('1.0', matriz)
        caixa.configure(state='disabled')
        caixa.pack(pady=10)

        #Botão para voltar
        ctk.CTkButton(self, text='Voltar', command=self.voltar).pack(pady=15, side='right')

    def voltar(self):
        self.master.mostrar_inicial()

        