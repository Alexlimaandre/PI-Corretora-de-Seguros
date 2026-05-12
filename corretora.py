# =============== CORRETORRA PYTHON ================

import customtkinter as ctk               # Importa a biblioteca customtkinter para criar a interface gráfica

ctk.set_appearance_mode("dark")           # Tema escuro
ctk.set_default_color_theme("blue")       # Cor das janelas

janela = ctk.CTk()                        # Cria a janela principal
janela.title("Corretora de Seguros")      # Título da janela
janela.geometry("700x450")                # Tamanho da janela
janela.resizable(False, False)            # Impede redimensionamento


# ============= FUNÇÃO DE LOGIN =============

def login():                                                                         # define a função de login
    usuario = entry_user.get()                                                       # faz a  janela ou painel do usuario
    senha = entry_pass.get()                                                         # faz a janela ou painel da senha

    if usuario == usuario and senha == senha:                                       # condição que verifica se o usuario e senha estão corretos obs: senha e usuario estão definidos no arquivo config.py                       
        label_erro.configure(text="")                                                # Limpa mensagem de erro
        frame_login.pack_forget()                                                    # Esconde o painel de login
        frame_menu.pack(pady=20, padx=40, fill="both", expand=True)                  # se verddade mostra o painel do menu principal
    else:
        label_erro.configure(text="Usuário ou senha incorretos!", text_color="red")  # se falso mostra a mensagem de erro


#============= FRAME DE LOGIN =============

frame_login = ctk.CTkFrame(master=janela)                        # Cria o painel de login
frame_login.pack(pady=20, padx=40, fill="both", expand=True)     # Posiciona o painel na janela

ctk.CTkLabel(                                                    # Título do painel de login
    frame_login,
    text=" Corretora de Valores",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(pady=(24, 4))

ctk.CTkLabel(
    frame_login,
    text="Informe suas credenciais para continuar",
    font=ctk.CTkFont(size=12),
    text_color="gray"
).pack(pady=(0, 16))

entry_user = ctk.CTkEntry(                        # Campo de usuário
    frame_login,
    placeholder_text="Usuário",                    # Texto exibido quando vazio
    width=260,
    height=40
)
entry_user.pack(pady=8)

                               
entry_pass = ctk.CTkEntry(                        #cria o campo de senha
    frame_login,
    placeholder_text="Senha",
    show="*",                                      # Substitui caracteres por "*"
    width=260,
    height=40
)
entry_pass.pack(pady=8)                            # Posiciona o campo de senha


label_erro = ctk.CTkLabel(                       # Label para exibir mensagens de erro
    frame_login,                                          
    font=ctk.CTkFont(size=12)
)
label_erro.pack(pady=(4, 0))

# Botão de login

btn_login = ctk.CTkButton(
    frame_login,
    text="Entrar",
    command=login,                                 # Chama a função login() ao clicar
    width=260,
    height=40,
    font=ctk.CTkFont(size=14, weight="bold")
)
btn_login.pack(pady=16)



janela.bind("<Return>", lambda event: login())      # Tecla Enter também aciona o login


# ============= PAINEL  MENU PRINCIPAL=============

frame_menu = ctk.CTkFrame(master=janela)           # Cria painel do menu principal (inicialmente oculto)

ctk.CTkLabel(                                      # cria a mensagem de login bem-sucedido
    frame_menu,
    text=" login bem-sucedido! ",                  
    font=ctk.CTkFont(size=13, weight="bold"),    
    text_color="green"
).pack(pady=(30, 8))

ctk.CTkLabel(                                   
    frame_menu,                                  # Mensagem de boas-vindas após login
    text="Bem-vindo ao menu principal.",
    font=ctk.CTkFont(size=22),
    text_color="black"
).pack(pady=(0, 24))

ctk.CTkButton(
    frame_menu,
    text=" CLIENTES",                           # Botão para acessar a seção de clientes
    height=38
).pack(pady=8)

ctk.CTkButton(
    frame_menu,
    text="APÓLICES",                            # Botão para acessar a seção de apólices
    height=38
).pack(pady=8)

ctk.CTkButton(
    frame_menu,
    text="VENDAS",                                 # Botão para acessar a seção de vendas
    height=38
).pack(pady=8)




def fechar_login():                       
    """Volta para a tela de login e limpa os campos."""
    frame_menu.pack_forget()                        # Oculta o menu
    entry_user.delete(0, "end")                     # Limpa campo de usuário
    entry_pass.delete(0, "end")                     # Limpa campo de senha
    label_erro.configure(text="")                  # Limpa mensagem de erro
    frame_login.pack(pady=20, padx=40, fill="both", expand=True)  # Exibe login novamente



ctk.CTkButton(
    frame_menu,
    text="🚪 Sair",                              # Botão de sair para voltar ao login
    width=80,
    height=38,
    fg_color="gray",                        # Fundo transparente
    border_width=1,
    command=fechar_login,
).pack(pady=(16, 0))

# ============= LOOP PRINCIPAL =============

janela.mainloop()   # Mantém a janela aberta e respondendo a eventos