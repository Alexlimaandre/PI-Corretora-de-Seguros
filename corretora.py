# =============== CORRETORA.PY ================

import customtkinter as ctk               # Importa a biblioteca customtkinter para criar a interface gráfica
from config import USUARIO, SENHA         # Importa as credenciais de login do arquivo config.py


ctk.set_appearance_mode("dark")           # Tema escuro
ctk.set_default_color_theme("blue")       # Cor das janelas

janela = ctk.CTk()                        # Cria a janela principal
janela.title("Corretora de Seguros")      # Título da janela
janela.geometry("700x450")                # Tamanho da janela
# janela.resizable(False, False)          # Impede redimensionamento


# ============= FUNÇÃO DE LOGIN =============

def login():                                                                         # define a função de login
    usuario = entry_user.get()                                                       # faz a janela ou painel do usuario
    senha = entry_pass.get()                                                         # faz a janela ou painel da senha

    if usuario == USUARIO and senha == SENHA:                                        # condição que verifica se o usuario e senha estão corretos
        label_erro.configure(text="")                                                # Limpa mensagem de erro
        frame_login.pack_forget()                                                    # Esconde o painel de login
        frame_menu.pack(fill="both", expand=True)                                    # mostra o painel do menu principal

    else:
        label_erro.configure(
            text="Usuário ou senha incorretos!",
            text_color="red"
        )                                                                            # se falso mostra a mensagem de erro


# ============= FRAME DE LOGIN =============

frame_login = ctk.CTkFrame(master=janela)                        # Cria o painel de login
frame_login.pack(pady=20, padx=40, fill="both", expand=True)     # Posiciona o painel na janela

ctk.CTkLabel(                                                    # Label do título do login
    frame_login,
    text=" Corretora de Valores",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(pady=(24, 4))                                             # Espaçamento superior maior para destacar o título

ctk.CTkLabel(                                                    # Label de instrução para o usuário
    frame_login,
    text="Informe seu CPF para continuar",
    font=ctk.CTkFont(size=12),
    text_color="gray"
).pack(pady=(0, 16))                                             # Espaçamento inferior maior para separar do campo de entrada


entry_user = ctk.CTkEntry(                                       # Campo de entrada para o usuário (CPF)
    frame_login,
    placeholder_text="CPF",                                      # Texto exibido quando vazio
    width=260,
    height=40
)
entry_user.pack(pady=8)                                          # Espaçamento entre os campos de entrada


entry_pass = ctk.CTkEntry(                                       # Campo de entrada para a senha
    frame_login,
    placeholder_text="Senha",
    show="*",                                                    # Substitui caracteres por "*"
    width=260,
    height=40
)
entry_pass.pack(pady=8)                                          # Espaçamento entre os campos de entrada


label_erro = ctk.CTkLabel(
    frame_login,                                                 # Label de erro (começa vazia)
    text="",
    font=ctk.CTkFont(size=12)
)
label_erro.pack(pady=(4, 0))                                     # Espaçamento superior para separar da senha


btn_login = ctk.CTkButton(                                       # cria o botão de login
    frame_login,
    text="Entrar",
    command=login,                                               # Chama a função login() ao clicar
    width=260,
    height=40,
    font=ctk.CTkFont(size=14, weight="bold")
)
btn_login.pack(pady=16)


janela.bind("<Return>", lambda event: login())                   # Tecla Enter também aciona o login


# ============= PAINEL MENU PRINCIPAL =============

frame_menu = ctk.CTkFrame(master=janela)                         # Cria o painel do menu principal inicialmente oculto

menu_aberto = False                                              # controla se o menu lateral está visível


def acessa_menu():                                               # função para mostrar ou esconder o menu lateral

    global menu_aberto

    if menu_aberto:

        frame_lateral.pack_forget()                              # fecha o menu lateral
        menu_aberto = False

    else:

        frame_lateral.pack(side="left", fill="y")                # abre o menu lateral à esquerda
        menu_aberto = True


# ============= BARRA SUPERIOR =============

frame_topbar = ctk.CTkFrame(                                     # cria a barra superior do menu principal
    frame_menu,
    height=45,
    corner_radius=0,
    fg_color="#1a1a2e"
)

frame_topbar.pack(side="top", fill="x")
frame_topbar.pack_propagate(False)                               # Impede que o frame redimensione


ctk.CTkButton(                                                   # Botão para abrir/fechar o menu lateral
    frame_topbar,
    text="☰",
    width=45,
    height=35,
    font=ctk.CTkFont(size=20),
    fg_color="transparent",
    hover_color="#2a2a4e",
    command=acessa_menu                                          # Chama a função para mostrar o menu
).pack(side="left", padx=8, pady=5)


ctk.CTkLabel(                                                    # Label do título na barra superior
    frame_topbar,
    text=" Corretora de Seguros",
    font=ctk.CTkFont(size=15, weight="bold"),
    text_color="white"
).pack(side="left", padx=4)


# ============= FUNÇÃO SAIR =============

def fechar_login():                                              # função para fechar o menu e voltar para a tela de login

    global menu_aberto                                           # controla se o menu lateral está visível

    frame_menu.pack_forget()                                     # Esconde o painel do menu principal

    frame_login.pack(                                            # Mostra o painel de login novamente
        pady=20,
        padx=40,
        fill="both",
        expand=True
    )

    entry_user.delete(0, "end")                                  # Limpa o campo de usuário
    entry_pass.delete(0, "end")                                  # Limpa o campo de senha

    if menu_aberto:                                              # Se o menu lateral estiver aberto fecha ele

        frame_lateral.pack_forget()                              # Esconde o menu lateral
        menu_aberto = False                                      # Atualiza o estado do menu para fechado


ctk.CTkButton(                                                   # Botão para sair do menu e voltar para a tela de login
    frame_topbar,
    text="Sair",
    width=80,
    height=30,
    fg_color="#c0392b",
    hover_color="#e74c3c",
    command=fechar_login                                         # Chama a função para fechar o menu e voltar para o login
).pack(side="right", padx=12, pady=7)


# ============= FRAME ENTRAL =============

frame_centro = ctk.CTkFrame(                                     # Cria o frame central do menu principal
    frame_menu,
    fg_color="transparent"
)

frame_centro.pack(fill="both", expand=True)                      # Preenche todo o espaço disponível


# ============= MENU0LATERAL =============

frame_lateral = ctk.CTkFrame(                                    # Cria o menu lateral dentro do frame central
    frame_centro,
    width=180,
    corner_radius=0,
    fg_color="#16213e"
)


ctk.CTkLabel(
    frame_lateral,
    text="MENU",
    font=ctk.CTkFont(size=12, weight="bold"),                    # Label do título do menu lateral
    text_color="gray"
).pack(
    pady=(16, 6),
    padx=12,
    anchor="w"
)                                                                 # alinhado à esquerda


# =============FRAME DI CONTEÚDO =============

frame_conteudo = ctk.CTkFrame(                                   # Cria o frame para exibir o conteúdo das seções
    frame_centro,
    fg_color="transparent"
)

frame_conteudo.pack(
    side="right",
    fill="both",
    expand=True
)


# ============= FUNÇÃO MOSTRAR SEÇÃO=============

def mostrar_secao(nome):                                         # Função para mostrar o conteúdo de cada seção

    for w in frame_conteudo.winfo_children():                    # Limpa o conteúdo anterior
        w.destroy()

    ctk.CTkLabel(                                                # Exibe o nome da seção selecionada
        frame_conteudo,
        text=nome,
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(pady=60)

    ctk.CTkLabel(                                                # cria mensagem abaixo do título
        frame_conteudo,
        text="Em construção...",
        text_color="gray"
    ).pack()

    if menu_aberto:                                              # Se o menu lateral estiver aberto fecha ele
        acessa_menu()


# =============BOTÕES DO MENU LATERAL =============

for texto, secao in [                      # Lista de seções do menu lateral com texto do botão

    (" CLIENTES", "Clientes"),
    (" APÓLICES", "Apólices"),
    (" VENDAS", "Vendas")

]:

    ctk.CTkButton(                                       # Cria os botões do menu lateral para cada seção

        frame_lateral,
        text=texto,
        anchor="w",
        width=160,
        height=40,
        fg_color="transparent",
        hover_color="#0f3460",
        font=ctk.CTkFont(size=13),
        command=lambda s=secao: mostrar_secao(s)

    ).pack(pady=3, padx=8)


# ============= LOOP PRINCIPAL =============

janela.mainloop()                                                # Mantém a janela aberta