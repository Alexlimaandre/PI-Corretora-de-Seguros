import customtkinter as ctk                 # Importa a biblioteca customtkinter para criar a interface gráfica
from config import USUARIO, SENHA          # Importa as credenciais de login do arquivo config.py
from functools import partial              # Importa partial para evitar o uso de lambda nos botões

ctk.set_appearance_mode("dark")           # Tema escuro
ctk.set_default_color_theme("blue")       # Cor das janelas

janela = ctk.CTk()                        # Cria a janela principal
janela.title("Corretora de Seguros")      # Título da janela
janela.geometry("600x350")                # Tamanho da janela ajustado para melhor visualização do menu fixo
# janela.resizable(False, False)          # Impede redimensionamento


# ============= FUNÇÃO DE LOGIN =============

def login():                                                                 # define a função de login
    usuario = entry_user.get()                                               # faz a janela ou painel do usuario
    senha = entry_pass.get()                                                 # faz a janela ou painel da senha

    if usuario == USUARIO and senha == SENHA:                                # condição que verifica se o usuario e senha estão corretos
        label_erro.configure(text="")                                        # Limpa mensagem de erro
        frame_login.pack_forget()                                            # Esconde o painel de login
        frame_menu.pack(fill="both", expand=True)                            # mostra o painel do menu principal
        frame_lateral.pack(side="left", fill="y")                            # Ao logar, o menu lateral já deve aparecer fixo

    else:
        label_erro.configure(
            text="Usuário ou senha incorretos!",
            text_color="red"
        )                                                                    # se falso mostra a mensagem de erro


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


# ============= BARRA SUPERIOR =============

frame_topbar = ctk.CTkFrame(                                     # cria a barra superior do menu principal
    frame_menu,
    height=45,
    corner_radius=0,
    fg_color="#1a1a2e"
)

frame_topbar.pack(side="top", fill="x")
frame_topbar.pack_propagate(False)                               # Impede que o frame redimensione


ctk.CTkLabel(                                                    # Label do título na barra superior
    frame_topbar,
    text=" Corretora de Seguros - Sistema Interno",
    font=ctk.CTkFont(size=15, weight="bold"),
    text_color="white"
).pack(side="left", padx=20)


# ============= FUNÇÃO SAIR =============

def fechar_login():                                              # função para fechar o menu e voltar para a tela de login

    frame_menu.pack_forget()                                     # Esconde o painel do menu principal
    frame_lateral.pack_forget()                                  # Garante que o menu lateral também suma

    frame_login.pack(                                            # Mostra o painel de login novamente
        pady=20,
        padx=40,
        fill="both",
        expand=True
    )

    entry_user.delete(0, "end")                                  # Limpa o campo de usuário
    entry_pass.delete(0, "end")                                  # Limpa o campo de senha


# ============= FRAME CENTRAL =============

frame_centro = ctk.CTkFrame(                                     # Cria o frame central do menu principal
    frame_menu,
    fg_color="transparent"
)

frame_centro.pack(fill="both", expand=True)                      # Preenche todo o espaço disponível


# ============= MENU LATERAL (FIXO) =============

frame_lateral = ctk.CTkFrame(                                    # Cria o menu lateral fixo
    frame_centro,
    width=180,
    corner_radius=0,
    fg_color="#16213e"
)
frame_lateral.pack_propagate(False)                              # Mantém a largura fixa


ctk.CTkLabel(
    frame_lateral,
    text="NAVEGAÇÃO",
    font=ctk.CTkFont(size=12, weight="bold"),                    # Label do título do menu lateral
    text_color="gray"
).pack(pady=(20, 10), padx=12, anchor="w")


# ============= FRAME DE CONTEÚDO =============

frame_conteudo = ctk.CTkFrame(                                   # Cria o frame para exibir o conteúdo das seções
    frame_centro,
    fg_color="transparent"
)

frame_conteudo.pack(
    side="right",
    fill="both",
    expand=True
)


# ============= FUNÇÃO MOSTRAR SEÇÃO =============

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
        text=f"Gerenciamento de {nome}",
        text_color="gray"
    ).pack()


# ============= BOTÕES DO MENU LATERAL =============

# Botões de Navegação (Fixos no topo)
# Conferida a estrutura da lista e vírgulas internas
secoes = [
    (" CLIENTES", "Clientes"),
    (" APÓLICES", "Apólices"),
    (" VENDAS", "Vendas")
]

for texto, secao in secoes:
    ctk.CTkButton(
        frame_lateral,
        text=texto,
        anchor="w",
        width=160,
        height=40,
        fg_color="transparent",
        hover_color="#0f3460",
        font=ctk.CTkFont(size=13),
        command=partial(mostrar_secao, secao)                    # Usando partial em vez de lambda para maior segurança
    ).pack(pady=3, padx=10)

# Botão SAIR (Fixo embaixo)
btn_sair_lateral = ctk.CTkButton(
    frame_lateral,
    text="SAIR",
    anchor="center",
    width=160,
    height=40,
    fg_color="#c0392b",
    hover_color="#e74c3c",
    font=ctk.CTkFont(size=13, weight="bold"),
    command=fechar_login                                         # Função fechar_login chamada corretamente
)
btn_sair_lateral.pack(side="bottom", pady=20, padx=10)           # Posiciona o botão sair na parte de baixo do menu


# ============= LOOP PRINCIPAL =============

janela.mainloop()                                                # Inicia o loop da aplicação