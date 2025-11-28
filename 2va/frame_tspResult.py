import customtkinter as ctk
from brazil58 import Brazil58

class ResultFrame(ctk.CTkFrame):
    def __init__(self, master, solver, rota, distancia, metodo, tempo):
        super().__init__(master)

        ctk.CTkLabel(
            self,
            text="Resultado do TSP",
            font=("Arial", 22, "bold")
        ).pack(pady=15)

        quantidade = len(solver.valores) - 1

        # Informações gerais do cálculo
        info = (
            f" Quantidade de pontos: {quantidade}\n"
            f" Método utilizado: {metodo}\n"
            f" Melhor distância: {distancia}\n"
            f" Tempo gasto: {tempo:.4f} segundos\n"
            f" Rota encontrada: {rota}\n"
        )

        ctk.CTkLabel(
            self,
            text=info,
            font=("Arial", 15),
            justify="left",
            wraplength=500
        ).pack(pady=10, fil='x')

        # Frame da matriz
        scroll=ctk.CTkScrollableFrame(self, width=800, height=400)
        scroll.pack(pady=15, padx=10, fill="both", expand=True)

        matriz = solver.matriz
        n = len(matriz)

        # Criando grid da matriz
        for i in range(n):
            for j in range(n):
                cell = ctk.CTkLabel(
                    scroll,
                    text=str(matriz[i][j]),
                    width=40,
                    height=30,
                    corner_radius=4
                )
                cell.grid(row=i, column=j, padx=1, pady=1)

        # Botão voltar
        ctk.CTkButton(
            self,
            text="Voltar",
            command=master.mostrar_inicial
        ).pack(pady=20)
