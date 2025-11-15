import customtkinter as ctk
from main import FoodDelivery

def aplicar_placeholder(textbox, texto_placeholder, cor_placeholder="gray"):
    # Criar o label que fica por cima
    placeholder = ctk.CTkLabel(
        textbox,
        text=texto_placeholder,
        text_color=cor_placeholder,
        anchor="nw"
    )
    placeholder.place(x=5, y=5)  # posição inicial dentro do textbox

    
    def on_focus_in(event):
        if textbox.get("1.0", "end-1c").strip() == "":
            placeholder.place_forget()  # some
    def on_focus_out(event):
        if textbox.get("1.0", "end-1c").strip() == "":
            placeholder.place(x=5, y=5)

    
    textbox.bind("<FocusIn>", on_focus_in)
    textbox.bind("<FocusOut>", on_focus_out)


class TelaInicial(ctk.CTkFrame):
    def __init__ (self, master):
        super(). __init__(master)

        #Frame topo
        self.frame_topo = ctk.CTkFrame (self, fg_color='#F54927', height=80)
        self.frame_topo.pack(fill='x')
        titulo=ctk.CTkLabel(self.frame_topo, text='FlyFood',
                            text_color='#363432', font=('Open Sans', 26, 'bold'))
        titulo.pack(pady=20)

        #Frame restante
        self.frame_rest=ctk.CTkFrame(self, fg_color='#CFCFCF')
        self.frame_rest.pack(fill='both', expand=True)

        #Frame matriz
        self.matriz_frame=ctk.CTkFrame(self.frame_rest, fg_color="#E0A66F")
        self.matriz_frame.place(relx=0.5, rely=0.4, anchor='center')

        self.preencher_matriz = ctk.CTkTextbox(
            self.matriz_frame,
            width=350,
            height=200,
            text_color='#363432',
            font=('Arial', 12)
        )
        self.preencher_matriz.pack(pady=25, padx=10)
        aplicar_placeholder(self.preencher_matriz, 'Insira a matriz..')

        #Botão 
        
        botao = ctk.CTkButton(self.matriz_frame, text='Testar', 
                              fg_color='#E37F07', text_color='#050504',
                              font=('Arial', 15),
                              command=self.matriz_calculo)  # parâmetro do widget
        botao.pack( pady=40, side='right')  # geometry managers

        #mensagens de erro
        self.label_status = ctk.CTkLabel(self, text='')
        self.label_status.pack(pady=5)

    def matriz_calculo(self):
        #leitura da matriz
        matriz= self.preencher_matriz.get('1.0', 'end').strip()
        if not matriz:
            self.label_status.configure(text='Por favor, insira uma matriz', text_color='red')
            return
        
        #importação do código original
        solver=FoodDelivery()
        try:
            solver.ler_matriz_string(matriz)
        except Exception as e:
            self.label_status.configure(text=f'Erro: {e}', text_color='red')
            return
        
        # determina se usa ag ou busca exaustiva
        n_pontos = len([p for p in solver.valores if p != 'R'])
        if n_pontos == 0:
            self.label_status.configure(text='Nenhum ponto de entrega encontrado')
            return
        if n_pontos > 9:
            metodo='Algoritmo Genético'
            rota, distancia=solver.algoritimo_genetico()
        else:
            metodo='Guloso'
            rota, distancia = solver.guloso_matriz()

        #vai para a tela de resultados
        self.master.mostrar_resultado(matriz, rota, distancia,metodo)

        
