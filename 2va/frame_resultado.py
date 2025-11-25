import customtkinter as ctk
from main import FoodDelivery


class Resultado(ctk.CTkFrame):
    def __init__ (self, master, matriz, rota, distancia,metodo, tempo):
        super().__init__(master)
        self.pack(fill='both', expand=True)
        
        ctk.CTkLabel(self, text='Resultado da melhor rota', font=('Arial', 18, 'bold')).pack(pady=(40, 20))

        ctk.CTkLabel(self, text=f'Método usado: {metodo}', font=('Arial', 15)).pack(pady=15)
        ctk.CTkLabel(self, text=f'Distância total: {distancia} dronômetros', font=('Arial', 15)).pack(pady=15)
        ctk.CTkLabel(self, text=f'Tempo de execução: {tempo:.2f} segundos', font=('Arial', 15)).pack(pady=15)

        #Exibição da matriz calculada

        ctk.CTkLabel(self, text="Matriz analisada:", font=('Arial', 13)).pack(pady=(20, 10))
        caixa=ctk.CTkTextbox(self, height=150)
        caixa.insert('1.0', matriz)
        caixa.configure(state='disabled')
        caixa.pack(pady=10)

        #Botão para voltar
        ctk.CTkButton(self, text='Fechar', command=self.fechar_programa).pack(pady=15, padx=10, side='right')
        ctk.CTkButton(self, text='Voltar', command=self.voltar).pack(pady=15,padx=10, side='right')
        

    def voltar(self):
        self.master.mostrar_inicial()
    def fechar_programa(self):
        self.master.destroy()

        