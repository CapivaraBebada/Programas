from Bibliotecas import *
from Validadores import *
from Relatorios import *

''' 
    O asterísco serve para fazer todas as chamadas do Tikinter.

    A função '.mainloop()' é usada para fazer a janela ficar aberta em um tempo indeterminado. Sem ela, a janela 
    aparecerá e fechará em uma fração de segundo.
    
    Para encontrar o tamanho de cada lista no frame 2: a proporção será de 500 em relação a quantidade de listas.

                                            50 de 500 -> 10% da lista
                                            200 de 500 -> 40%
                                            125 de 500 -> 25%
                                            125 de 500 -> 25%
                                  Total: 100% da tela da lista utilizada
            
    Explicando a parte da pesquisa na lisata: vamos upor que queremos pesquisar o nome 'Mônica'. Ao ser feito a pesquisa, queremos que pesquise
    todos os nomes 'Mônica' e não apenas a primeira. A função 'LIKE' permite essa pesquisa a partir do símbolo '%' acresenctada ao final de cada
    nome. 

    Para criar um arquivo executável, basta abrir o terminal e escrever o seguinte: cxfreeze.\<nomedoarquivo>.py
    O nome do arquivo não pode ter espaço.
    Para encontrar o arquivo, vá até a pasta "build" e lá estará o executável: <nomedoarquivo>.exe
    Apenas um adendo: o arquivo deve ser copiado\movido para a pasta 'Programas - VSCODE' (no caso deste computador - Windows)
    Para o Linux, deve ter a biblioteca 'pyinstaller' e escrever o seguinte comando no terminal: 'pyinstaller --onefile --noconsole --windowed <nome>.py'

    Para garantir que não dará erro caso seja usado a função "tix" na variável 'janela', baixe a biblioteca "python3-tk' e logo em seguida, a biblioteca 'tix'
    
'''

janela = tix.Tk()

class Funcao():
    def limpar_tela(self):  # Aqui será organizado as funções atribuídas ao botão "limpar"
        self.codigo_entrada.delete(0, END)      # Tudo que for escrito, será apagado até o final
        self.nome_entrada.delete(0, END)
        self.telefone_entrada.delete(0, END)
        self.cidade_entrada.delete(0, END)

    def conecta_bd(self):       # Conectar com o Banco de Dados
        self.conn = sqlite3.connect("Clientes.bd")
        self.cursor = self.conn.cursor(); print('Conectando ao banco de dados')

    def desconecta_bd(self):     # Em SQL, a função é chamada e logo desconectada
        self.conn.close(); print('Desconecta ao banco de dados')

    def monta_tabela(self):
        self.conecta_bd()

        # Criando tabela
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS clientes(
                cod INTEGER PRIMARY KEY,
                nome_cliente CHAR(40) NOT NULL,  
                telefone INTEGER(20),               
                cidade CHAR(40)
            )
        """)
        #   "nome_cliente: nao pode ficar vazio
        #   "telefone": deve ter 20 caracteres
        self.conn.commit(); print("Banco de dados criado")
        self.desconecta_bd()

    def variaveis(self):
        self.codigo = self.codigo_entrada.get()  # Usando a função "get" para "pegar" o que for escrito
        self.nome = self.nome_entrada.get()
        self.telefone = self.telefone_entrada.get()
        self.cidade = self.cidade_entrada.get()

    def adicionar_cliente(self):
        self.variaveis()    # Será usado as informações dessa "def" para fazer os demais processos
        # Para impedir que adicione um cliente sem nome:
        if self.nome_entrada.get() ==  '':
            msg = 'É necessário que tenha um nome'
            messagebox.showinfo('ERRO!!!', msg)
        else:    
            self.conecta_bd()
            self.cursor.execute(""" INSERT INTO clientes (nome_cliente, telefone, cidade)
                VALUES(?, ?, ?)""", (self.nome, self.telefone, self.cidade))
            self.conn.commit()
            self.desconecta_bd()
            self.selecionar_lista()     # Sempre que for adicionado um cliente, será mandado para a lista
            self.limpar_tela()

    def selecionar_lista(self):
        self.listaCli.delete(*self.listaCli.get_children())
        self.conecta_bd()
        lista = self.cursor.execute(""" SELECT cod, nome_cliente, telefone, cidade FROM clientes
        ORDER BY nome_cliente ASC; """)
        # "ORDER BY" --> chamará os nomes em ordem crescente, por isso o "ASC" (ascendente)
        for i in lista:     # A lista que será armazenada os nomes adicionados
            self.listaCli.insert("", END, values=i)
        self.desconecta_bd()

    def duplo_click(self, event):   # "event": indica que será feito um evento usando essa função
        self.limpar_tela()
        self.listaCli.selection()

        for n in self.listaCli.selection():
            col1, col2, col3, col4 = self.listaCli.item(n, 'values')    # Selecionar as 4 colunas com o duplo click
            # Ao selecionar a coluna, será preenchido com as informações de cada área:
            self.codigo_entrada.insert(END, col1)
            self.nome_entrada.insert(END, col2)
            self.telefone_entrada.insert(END, col3)
            self.cidade_entrada.insert(END, col4)

    def deleta_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute("""DELETE FROM clientes WHERE cod = ? """, (self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.limpar_tela()
        self.selecionar_lista()

    def alterar_cliente(self):
        self.variaveis()
        self.conecta_bd()
        self.cursor.execute(""" UPDATE clientes SET nome_cliente = ?, telefone = ?, cidade = ?
            WHERE cod = ? """, (self.nome, self.telefone, self.cidade, self.codigo))
        self.conn.commit()
        self.desconecta_bd()
        self.selecionar_lista()
        self.limpar_tela()
        
    def busca_cliente(self):
        self.conecta_bd()
        self.listaCli.delete(*self.listaCli.get_children())   # Ao buscar, temos que limpar a lista
        # Ao buscar algum nome, precisamos que tenha o sinal "%" no final de cada nome: (explicação melhor na parte inicial do código)
        self.nome_entrada.insert(END, '%')   # A porcentagem tem caráter coringa, ele permite pesquisar tudo aquilo que foi digitado na pesquisa
        nome = self.nome_entrada.get()
        # Acessar as colunas da tabela:
        self.cursor.execute(
            """ SELECT cod, nome_cliente, telefone, cidade FROM clientes
            WHERE nome_cliente LIKE '%s' ORDER BY nome_cliente ASC""" % nome)
                # O que permite ser pesquisado tudo que foi digitado é essa função 'LIKE'

        busca_nomeCli = self.cursor.fetchall()   # Variável que fecha a pesquisa
        for i in busca_nomeCli:
            self.listaCli.insert('', END, values=i)   

        self.limpar_tela()  # Limpa a tela assim que for pesquisado
        self.desconecta_bd()

    # Criando calendário
    def calendario(self):
        # Mostrar calendário
        self.calendario1 = Calendar(self.aba2, fg='gray', bg='black', font=('Times', '9', 'bold'), 
                                   locale='pt_br')      # Indica o formato de data de acordo com o país
        self.calendario1.place(relx=0.5, rely=0.15)
        # Mostrar botão para inserir a data
        self.callData = Button(self.aba2, text='Inserir data', command=self.print_call)
        self.callData.place(relx=0.75, rely=0.03, height=25, width=100)
    def print_call(self):       # Para inserir a data na entrada
        dataIni = self.calendario1.get_date()
        self.calendario1.destroy()
        self.entrada_data.delete(0, END)
        self.entrada_data.insert(END, dataIni)
        self.callData.destroy()

        
# Aqui é possível configurar a janela
class Application(Funcao, Relatorios, Validadores):      # Também está chamando as funções Relatórios e Validadores para que sejam colocadas na tela
    # Funções a serem chamadas para rodar o código
    def __init__(self):
        self.frame_1 = None
        self.frame_2 = None
        self.janela = janela
        self.valida_entradas()
        self.frames_de_tela()
        self.tela()
        self.config_frame_1()
        self.config_frame_2()
        self.monta_tabela()
        self.selecionar_lista()
        self.Menu()
        janela.mainloop()

    # CONFIGURAÇÕES DE TELA:
    def tela(self):  # Configurações da tela
        self.janela.title('Cadastro de clientes.')  # Título da janela
        self.janela.configure(background='black')   # Cor de fundo da janela
        self.janela.geometry('850x700')                 # Definindo tamanho da janela
        self.janela.resizable(False, False)  # Permite ou não a alteração de tamanho da janela
        self.janela.maxsize(width=1000, height=800)  # Máximo de tamanho da janela
        self.janela.minsize(width=480, height=480)  # Mínimo de tamanho da janela

    '''
    A partir daqui será destinado à criação de frames. Significa que será responsável por gerar 2 telas dentro da 
    janela. Uma parte para adicionar informações e outra parte para mostrar as informações adicionadas.
    '''

    # CRIAÇÃO DOS FRAMES:
    def frames_de_tela(self):
        # Criar e escolher cor do frame                                   
        self.frame_1 = Frame(self.janela, bd=4, bg='#1b2631',   # "bg": background; "bd": border width
                             highlightbackground='white',       # Cor de borda do frame
                             highlightthickness=2)              # Grossura da borda do frame
        self.frame_1.place(relx=0.01, rely=0.01, relwidth=0.98, relheight=0.5)  # Coordenada do frame de cima
        # Abaixo, criando o frame debaixo
        self.frame_2 = Frame(self.janela, bd=4, bg='#283747', highlightbackground='white', highlightthickness=2)
        self.frame_2.place(relx=0.01, rely=0.5, relwidth=0.98, relheight=0.49)
    
    '''
    Explicação para a escolha do "place" para fazer ajustes nos frames:
        "grid" separa os frames entre linhas e colunas
        "pack" poderia ser usado, mas ficaria difícil de programá-lo futuramente (não sei o pq)
        "place" escolher uma variável para ficar fixa de acordo com as coordenadas associadas a ele (que é o ideal para esse projeto)
    '''

    # CONFIGURAÇÕES DO FRAME 1:
    def config_frame_1(self):
        # Criação de abas
        self.abas = ttk.Notebook(self.frame_1)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
            # Personalizar abas
        self.aba1.configure(background='#1b2631') 
        self.aba2.configure(background='#1b2631')
            # Adicionar nome às abas
        self.abas.add(self.aba1, text='Aba 1')
        self.abas.add(self.aba2, text='Aba 2')
            # Onde as abas se encontrarão
        self.abas.place(relx=0,rely=0, relwidth=1, relheight=0.99)
        
        # Abaixo, criação dos botões "limpar", "buscar", "novo", "alterar" e "excluir"

            # Criando Molduras para o frame:
        self.canvas_bt = Canvas(self.aba1, bd=0, bg='gray', highlightbackground='gray', highlightthickness=3)
        self.canvas_bt.place(relx=0.16, rely=0.14, relwidth=0.22, relheight=0.17)

            # Botão "Limpar"
        self.bt_limpar = Button(self.aba1, text='Limpar', bd=4,
                                bg='gray', fg='black',      # "bg": background; "fg": primeiro plano (cor da letra)
                                font=('Montserrat', 10, 'bold'),    # (x, y, z) = (tipo, tamanho, estilo de fonte)
                                command=self.limpar_tela,     # a função para o "limpar" atribuída a este botão
                                activebackground='#1b3c60', activeforeground='white')  # Mudar de cor quando clicar no botão 
        self.bt_limpar.place(relx=0.17, rely=0.15, relwidth=0.10, relheight=0.15)    # Posição do botão

            # Botão "Buscar"
        self.bt_buscar = Button(self.aba1, text='Buscar', bd=4,
                                bg='gray', fg='black',
                                font=('Montserrat', 10, 'bold'),
                                command=self.jan,       # Atribuíndo função ao botão
                                activebackground='#1b3c60', activeforeground='white')  
        self.bt_buscar.place(relx=0.27, rely=0.15, relwidth=0.10, relheight=0.15)   # Posição do botão
                # Texto_balao_buscar = 'Digite no campo NOME o cliente que deseja pesquisar'
        self.balao_buscar = tix.Balloon(self.aba1)
        self.balao_buscar.bind_widget(self.bt_buscar, balloonmsg="Clique para buscar cliente")
        self.balao_buscar.configure(bg='black')     # Não sei pq nao funciona
                             
            # Botão "Novo"
        self.bt_novo = Button(self.aba1, text='Novo',
                              bd=4, bg='gray',
                              font=('Montserrat', 10, 'bold'),
                              command=self.adicionar_cliente,
                              activebackground='#1b3c60', activeforeground='white')  
        self.bt_novo.place(relx=0.60, rely=0.15, relwidth=0.10, relheight=0.15)  # Posição do botão

            # Botão "Alterar"
        self.bt_alterar = Button(self.aba1, text='Alterar',
                                 bd=4, bg='gray',
                                 font=('Montserrat', 10, 'bold'),
                                 command=self.alterar_cliente,
                                activebackground='#1b3c60', activeforeground='white')  
        self.bt_alterar.place(relx=0.70, rely=0.15, relwidth=0.10, relheight=0.15)  # Posição do botão

            # Botão "Excluir"
        self.bt_excluir = Button(self.aba1, text='Excluir',
                                 bd=4, bg='gray',
                                 font=('Montserrat', 10, 'bold'),
                                 command=self.deleta_cliente,
                                 activebackground='#1b3c60', activeforeground='white')  
        self.bt_excluir.place(relx=0.80, rely=0.15, relwidth=0.10, relheight=0.15)  # Posição do botão
        
        

        # Input associado ao CÓDIGO
        self.lb_codigo = Label(self.aba1, text='Código',             # Colocar a palavra "código" na tela
                               bd=4, font=('Montserrat', 10, 'bold'))
        self.lb_codigo.place(relx=0.05, rely=0.09)
        self.codigo_entrada = Entry(self.aba1, bg='white',      # Colocar uma área para o input na tela
                                    fg='#1b2631', font=('Montserrat', 12, 'bold'),
                                    validate = 'key', validatecommand=self.v_codigo)     # Para validar a entrada do código com até 2 dígitos
        self.codigo_entrada.place(relx=0.03, rely=0.18, relwidth=0.1, relheight=0.1)

        # Input associado ao NOME
        self.lb_nome = Label(self.aba1, text='Nome',               # Colocar a palavra "nome" na tela
                             bd=4, font=('Montserrat', 10, 'bold'))
        self.lb_nome.place(relx=0.05, rely=0.40)
        self.nome_entrada = Entry(self.aba1, bg='White',      # Área para o input na tela
                                  fg='#1b2631', font=('Montserrat', 12, 'bold'))
        self.nome_entrada.place(relx=0.03, rely=0.49, relwidth=0.75, relheight=0.1)

        # Input para número de telefone
        self.lb_telefone = Label(self.aba1, text='Telefone',           # Colocar a palavra "Telefone" na tela
                                 bd=4, font=('Montserrat', 10, 'bold'))
        self.lb_telefone.place(relx=0.05, rely=0.67)
        self.telefone_entrada = Entry(self.aba1, bg='White',      # Área para o input na tela
                                      fg='#1b2631', font=('Montserrat', 12, 'bold'),
                                      validate = 'key', validatecommand=self.v_telefone)
        self.telefone_entrada.place(relx=0.03, rely=0.76, relwidth=0.17)

        # Input para Cidade
        self.lb_cidade = Label(self.aba1, text='Cidade',             # Colocar a palavra "Cidade" na tela
                               bd=4, font=('Montserrat', 10, 'bold'))
        self.lb_cidade.place(relx=0.52, rely=0.67)
        self.cidade_entrada = Entry(self.aba1, bg='White',      # Área para o input na tela
                                    fg='#1b2631', font=('Montserrat', 12, 'bold'))
        self.cidade_entrada.place(relx=0.5, rely=0.76, relwidth=0.28)
        
        # Para a aba 2
            # Drop down button
        self.TipVar = StringVar()
        self.TipV = ('Solteiro(a)', 'Casado(a)', 'Divorciado(a)', 'Viúvo(a)')
        self.TipVar.set('Estado civil')
        self.popupMenu = OptionMenu(self.aba2, self.TipVar, *self.TipV)
        self.popupMenu.place(relx=0.05, rely=0.1, relwidth=0.2, relheight=0.2)
            # Salvando informações:
        self.estado_civil = self.TipVar.get()
        #print(self.estado_civil)
        
        # Criando calendário
            # Criando botão
        self.bt_calendario = Button(self.aba2, text='Data', command=self.calendario)
        self.bt_calendario.place(relx=0.5, rely=0.02)
            # Criando entrada
        self.entrada_data = Entry(self.aba2, width= 10)
        self.entrada_data.place(relx=0.6, rely=0.03, height=25, width=100)
    
    # CONFIGURAÇÕES DO FRAME 2:
    def config_frame_2(self):   # A partir daqui, será organizado tudo sobre o frame 2
        self.listaCli = ttk.Treeview(self.frame_2, height=3, columns=('col_1', 'col_2', 'col_3', 'col_4'))
        self.listaCli.heading('#0', text='')      # Acessando cada coluna e adicionando um título em cada
        self.listaCli.heading('#1', text='Código')
        self.listaCli.heading('#2', text='Nome')
        self.listaCli.heading('#3', text='Telefone')
        self.listaCli.heading('#4', text='Cidade')
        # Definindo tamanho de cada lista (explicação na parte de cima do código)
        self.listaCli.column('#0', width=1)
        self.listaCli.column('#1', width=50)
        self.listaCli.column('#2', width=200)
        self.listaCli.column('#3', width=125)
        self.listaCli.column('#4', width=125)

        self.listaCli.place(relx=0.01, rely=0.05, relwidth=0.95, relheight=0.88)

        # Criando barra de rolagem
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')   # Definindo direção da barra
        self.listaCli.configure(yscroll=self.scroolLista.set)   # Adicionando a barra à "ListaCli"
        self.scroolLista.place(relx=0.96, rely=0.05, relwidth=0.03, relheight=0.88)
        self.listaCli.bind("<Double-1>", self.duplo_click)      # "bind" define tipo de interação, no caso, duplo click

    # Criação de menu
    def Menu(self):
        # Criando barra de menu
        menubar = Menu(self.janela)
        self.janela.config(menu=menubar)
        arquivo_menu_1 = Menu(menubar)
        arquivo_menu_2 = Menu(menubar)

        # Função para fechar janela
        def Quit(): self.janela.destroy()

        # Nomeando cada menu e aparecerá em formato de cascata
        menubar.add_cascade(label="Opções", menu=arquivo_menu_1)
        menubar.add_cascade(label="Relatórios", menu=arquivo_menu_2)

        # Aplicando comandos aos botões
        arquivo_menu_1.add_command(label="Sair", command=Quit)
        arquivo_menu_2.add_command(label="Limpar cliente", command=self.limpar_tela)
        
        arquivo_menu_2.add_command(label="Ficha do cliente", command=self.gerarRelatorio)
    
    # Criação de outra janela
    def jan(self):          # O nome é estranho pq no início do código já tem uma variável "janela"
        self.jan2 = Toplevel()
        self.jan2.title('Janela 2')
        self.jan2.configure(background='#0b163d')
        self.jan2.geometry('400x200')
        self.jan2.resizable(False, False)   # Tamanho fixo
        self.jan2.transient(self.jan)       # Caminho que essa janela tem
        self.jan2.focus_force()     # Ao clicar em uma janela ao fundo, ela passa a estar em primeiro plano
        self.jan2.grab_set()        # Impede de modificar a janela, seja com um click ou não click

    def valida_entradas(self):
        self.v_codigo = (self.janela.register(self.validate_entrada_codigo), '%P')
        self.v_telefone = (self.janela.register(self.validate_entrada_telefone), '%P')

        
Application()