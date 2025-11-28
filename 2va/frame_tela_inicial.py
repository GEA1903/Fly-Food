import customtkinter as ctk
from main import FoodDelivery
from brazil58 import Brazil58
import time
import threading

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
        self.matriz_frame.pack(pady=20, side='left', padx=40)

        self.preencher_matriz = ctk.CTkTextbox(
            self.matriz_frame,
            width=350,
            height=200,
            fg_color="#FFFFFF",
            text_color="black",
            font=('Arial', 12)
        )
        self.preencher_matriz.pack(pady=25, padx=10)
        aplicar_placeholder(self.preencher_matriz, 'Insira a matriz..')

        #Botão 
        
        botao = ctk.CTkButton(self.matriz_frame, text='Testar', 
                              fg_color='#E37F07', text_color='#050504',
                              font=('Arial', 15),
                              command=self.matriz_calculo)  # parâmetro do widget
        botao.pack( pady=40,padx=10, side='right')  # geometry managers

        #mensagens de erro
        self.label_status = ctk.CTkLabel(self, text='')
        self.label_status.pack(pady=5)

        ## frame tsp

        self.frame_tsp = ctk.CTkFrame(self.frame_rest, fg_color="#E38650", width=300, height=200)
        self.frame_tsp.pack(side="right", pady=20, padx =40)

        titulo_tsp = ctk.CTkLabel(
            self.frame_tsp,
            text="Insira um arquivo .tsp",
            font=("Arial", 15, "bold")
        )
        titulo_tsp.pack(pady=(20, 30))

        self.botao_tsp = ctk.CTkButton(
            self.frame_tsp,
            text="Selecionar arquivo",
            fg_color="#E8E5DE",
            text_color="black",
            height=40,
            command=self.carregar_arquivo_tsp
        )
        self.botao_tsp.pack(pady=20, padx=30, fill='x')

        self.label_tsp_status = ctk.CTkLabel(
            self.frame_tsp, 
            text="", 
            text_color="red"
        )
        self.label_tsp_status.pack(pady=5)

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
            self.label_status.configure(text='Nenhum ponto de entrega encontrado', text_color='red')
            return
        
        inicio=time.time()
        if n_pontos > 9:
            metodo='Algoritmo Genético'
            rota, distancia=solver.algoritimo_genetico()
        else:
            metodo='Força Bruta'
            rota, distancia = solver.melhor_rota()
        fim=time.time()
        tempo=fim - inicio
        #vai para a tela de resultados
        self.master.mostrar_resultado(matriz, rota, distancia,metodo, tempo)

    def carregar_arquivo_tsp(self):
        from tkinter.filedialog import askopenfilename
        
        caminho = askopenfilename(
            title="Selecione um arquivo TSP",
            filetypes=[("Arquivos TSPLIB", "*.tsp")]
        )

        if not caminho:
            return
        
        self.mostrar_popup_carregando()

        def tarefa():
        
            try:
                solver = Brazil58()
                solver.ler_tsp_explicit(caminho )   
                self.label_tsp_status.configure(
                    text="Arquivo carregado com sucesso!",
                    text_color="green"
                )

               
                n_pontos = len([p for p in solver.valores if p != 'R'])
                if n_pontos == 0:
                    self.label_tsp_status.configure(text="Nenhum ponto válido no arquivo.", text_color="red")
                    return

                import time
                inicio = time.time()
                if n_pontos > 9:
                    metodo = "Algoritmo Genético"
                    rota, distancia = solver.algoritmo_genetico()
                else:
                    metodo = "Força Bruta"
                    rota, distancia = solver.melhor_rota()
                fim = time.time()
                tempo = fim - inicio

                # Vai para a tela de resultados
                self.master.mostrar_resultado_tsp(solver=solver, rota=rota, distancia=distancia, metodo=metodo, tempo=tempo)

            except Exception as e:
                self.after(0, lambda: self.label_tsp_status.configure(
                text=f"Erro ao ler .tsp: {e}", text_color="red"))
            finally:
                self.after(0, self.fechar_popup_carregando)

    # Thread para não travar a interface
        threading.Thread(target=tarefa).start()
        
            
    def mostrar_popup_carregando(self,      texto="Calculando o arquivo .tsp..."):
        # Criar janela popup
        self.popup = ctk.CTkToplevel(self)
        self.popup.title("Aguarde")
        self.popup.geometry("400x180")
        self.popup.resizable(False, False)
        self.popup.grab_set()  # trava interação com o restante da UI

        label = ctk.CTkLabel(self.popup, text=texto, font=("Arial", 16))
        label.pack(pady=20)

        # Pequeno spinner visual
        self.spinner = ctk.CTkProgressBar(self.popup, mode="indeterminate")
        self.spinner.pack(pady=10)
        self.spinner.start()

    def fechar_popup_carregando(self):
        if hasattr(self, "popup"):
            self.spinner.stop()
            self.popup.destroy()