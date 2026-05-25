import customtkinter as ctk                 # Importei a biblioteca customtkinter para criar a interface gráfica
from config import USUARIO, SENHA          # Importando as credenciais de login do arquivo config.py

ctk.set_appearance_mode("dark")            # escolhi tema escuro
ctk.set_default_color_theme("blue")       # Cor das janelas

janela = ctk.CTk()                         # Criou a janela principal
janela.title("Corretora de Seguros")       # titulo da janela
janela.geometry("850x650")                 # tamanho da janela


# ============= BANCO DE DADOS TEMPORÁRIO =============

bd_clientes = []                           # banco temporário até integração
bd_apolices = []
bd_vendas = []


# ============= FUNÇÕES DE LIMITE DE TAMANHO =============

def limita_cpf(tamanho_texto):             # faz o CPF não ultrapassar 11 números
    return len(tamanho_texto) <= 11

def limita_apolice(texto_atual):           # apólice não ultrapassa 15 caracteres
    return len(texto_atual) <= 15

def limita_venda(texto_atual):             # ID da venda não ultrapassa 10 caracteres
    return len(texto_atual) <= 10

def limita_telefone(texto_atual):          # telefone não ultrapassa 11 caracteres (DDD + número)
    return len(texto_atual) <= 11


# Registra as funções para que possam ser usadas como validadores
validador_cpf      = janela.register(limita_cpf)
validador_apolice  = janela.register(limita_apolice)
validador_venda    = janela.register(limita_venda)
validador_telefone = janela.register(limita_telefone)


# ============= JANELA DE RESPOSTA (POPUP DE SUCESSO) =============

def mostrar_msg_sucesso(mensagem):         # exibe janela de aviso após operações do CRUD
    popup = ctk.CTkToplevel(janela)        # cria uma nova janela pop-up
    popup.title("Aviso do Sistema")        # nome da janela
    popup.geometry("400x220")             # tamanho da janela
    popup.grab_set()                       # impede interação com a janela principal enquanto o pop-up estiver aberto

    ctk.CTkLabel(
        popup,
        text=mensagem,
        font=ctk.CTkFont(size=13, weight="bold"),
        wraplength=350
    ).pack(pady=(30, 20))

    ctk.CTkButton(
        popup,
        text="OK",
        width=100,
        command=popup.destroy
    ).pack()


# ============= FUNÇÃO DE LOGIN =============

def login():                                                    # define a função de login
    usuario = entry_user.get()                                  # pega o texto digitado no campo de usuário
    senha   = entry_pass.get()                                  # pega o texto digitado no campo de senha

    if usuario == USUARIO and senha == SENHA:                   # verifica se usuário e senha estão corretos
        label_erro.configure(text="")                           # limpa mensagem de erro anterior
        frame_login.pack_forget()                               # esconde o painel de login
        frame_menu.pack(fill="both", expand=True)               # mostra o painel do menu principal
        frame_lateral.pack(side="left", fill="y")               # exibe o menu lateral fixo
        mostrar_tela_clientes()                                 # exibe a seção de clientes por padrão
    else:
        label_erro.configure(
            text="Usuário ou senha incorretos!",
            text_color="red"
        )

def login_entrar(event):                                        # dispara o login com a tecla Enter
    login()


# ============= PAINEL DE LOGIN =============

frame_login = ctk.CTkFrame(master=janela)                       # cria o painel de login
frame_login.pack(pady=20, padx=40, fill="both", expand=True)    # posiciona o painel na janela

ctk.CTkLabel(
    frame_login,
    text=" Corretora de Valores ",
    text_color="green",
    font=ctk.CTkFont(size=20, weight="bold")
).pack(pady=(24, 4))

ctk.CTkLabel(
    frame_login,
    text="Informe seu LOGIN para continuar",
    font=ctk.CTkFont(size=12),
    text_color="white"
).pack(pady=(0, 16))

entry_user = ctk.CTkEntry(
    frame_login,
    placeholder_text="LOGIN",
    width=260,
    height=40
)
entry_user.pack(pady=8)

entry_pass = ctk.CTkEntry(
    frame_login,
    placeholder_text="Senha",
    show="*",                                                    # substitui caracteres por "*"
    width=260,
    height=40
)
entry_pass.pack(pady=8)

label_erro = ctk.CTkLabel(
    frame_login,
    text="",                                                     # label de erro começa vazia
    font=ctk.CTkFont(size=12)
)
label_erro.pack(pady=(4, 0))

btn_login = ctk.CTkButton(
    frame_login,
    text="Entrar",
    command=login,
    width=260,
    height=40,
    font=ctk.CTkFont(size=14, weight="bold"),
    fg_color="green",
    hover_color="darkgreen"
)
btn_login.pack(pady=16)

janela.bind("<Return>", login_entrar)                           # tecla Enter também aciona o login


# ============= PAINEL MENU PRINCIPAL =============

frame_menu = ctk.CTkFrame(master=janela)                        # cria o painel do menu principal


# ============= BARRA SUPERIOR =============

frame_topbar = ctk.CTkFrame(
    frame_menu,
    height=45,
    corner_radius=0,
    fg_color="#1a1a2e"
)
frame_topbar.pack(side="top", fill="x")
frame_topbar.pack_propagate(False)                              # impede que o painel redimensione

ctk.CTkLabel(
    frame_topbar,
    text=" Corretora de Seguros - Sistema Interno",
    font=ctk.CTkFont(size=15, weight="bold"),
    text_color="white"
).pack(side="left", padx=20)


# ============= FUNÇÃO SAIR =============

def fechar_login():                                             # fecha o menu e volta para a tela de login
    frame_menu.pack_forget()                                    # esconde o painel do menu principal
    frame_lateral.pack_forget()                                 # esconde o menu lateral

    frame_login.pack(pady=20, padx=40, fill="both", expand=True)  # exibe o painel de login novamente

    entry_user.delete(0, "end")                                 # limpa o campo de usuário
    entry_pass.delete(0, "end")                                 # limpa o campo de senha


# ============= PAINEL CENTRAL =============

frame_centro = ctk.CTkFrame(frame_menu, fg_color="transparent") # cria o frame central do menu principal
frame_centro.pack(fill="both", expand=True)                     # preenche todo o espaço disponível


# ============= MENU LATERAL =============

frame_lateral = ctk.CTkFrame(
    frame_centro,
    width=180,
    corner_radius=0,
    fg_color="#16213e"
)
frame_lateral.pack_propagate(False)                             # mantém a largura fixa

ctk.CTkLabel(
    frame_lateral,
    text="NAVEGAÇÃO",
    font=ctk.CTkFont(size=12, weight="bold"),
    text_color="gray"
).pack(pady=(20, 10), padx=12, anchor="w")


# ============= PAINEL DE CONTEÚDO =============

frame_conteudo = ctk.CTkFrame(frame_centro, fg_color="transparent")  # painel para exibir o conteúdo das seções
frame_conteudo.pack(side="right", fill="both", expand=True)


# ============= VARIÁVEIS GLOBAIS DOS INPUTS =============

campo1_ativo  = None   # armazena referência ao widget Entry do campo 1 ativo no formulário
campo2_ativo  = None
campo3_ativo  = None
campo4_ativo  = None
campo5_ativo  = None
campo6_ativo  = None
campo7_ativo  = None
label_erro_crud = None # referência ao label de erro do CRUD atual
painel_usado  = ""     # indica qual seção está aberta (Clientes, Apólices, Vendas)
chamar_acao   = ""     # indica qual ação está ativa (Acrescentar, Pesquisar, Atualizar, Remover)


# ============= FUNÇÃO DE CONFIRMAÇÃO DO CRUD =============

def confirma_crud():
    global campo1_ativo, campo2_ativo, campo3_ativo, campo4_ativo
    global campo5_ativo, campo6_ativo, campo7_ativo
    global painel_usado, chamar_acao, label_erro_crud
    global bd_clientes, bd_apolices, bd_vendas

    # Coleta os valores digitados em cada campo, removendo espaços extras
    v1 = campo1_ativo.get().strip() if campo1_ativo else ""
    v2 = campo2_ativo.get().strip() if campo2_ativo else ""
    v3 = campo3_ativo.get().strip() if campo3_ativo else ""
    v4 = campo4_ativo.get().strip() if campo4_ativo else ""
    v5 = campo5_ativo.get().strip() if campo5_ativo else ""
    v6 = campo6_ativo.get().strip() if campo6_ativo else ""
    v7 = campo7_ativo.get().strip() if campo7_ativo else ""

    label_erro_crud.configure(text="")                          # limpa erro anterior antes de validar

    # --- VALIDAÇÃO: campos obrigatórios ---
    if chamar_acao in ["Acrescentar", "Atualizar"]:             # todos os campos devem estar preenchidos
        if (campo1_ativo and not v1) or (campo2_ativo and not v2) or \
           (campo3_ativo and not v3) or (campo4_ativo and not v4) or \
           (campo5_ativo and not v5) or (campo6_ativo and not v6) or \
           (campo7_ativo and not v7):
            label_erro_crud.configure(
                text="Erro: Preencha todos os campos do formulário!",
                text_color="#e74c3c"
            )
            return

    elif chamar_acao == "Pesquisar":                            # pelo menos um campo deve ser preenchido
        if not v1 and not v2 and not v5:
            label_erro_crud.configure(
                text="Erro: Preencha pelo menos um campo para buscar!",
                text_color="#e74c3c"
            )
            return

    elif chamar_acao == "Remover":                              # CPF obrigatório para remover
        if not v1:
            label_erro_crud.configure(
                text="Erro: Informe o CPF/CNPJ para localizar o cliente.",
                text_color="#e74c3c"
            )
            return

    mensagem_alerta = "Operação realizada com sucesso!"


    # ====== 1. CRUD DE CLIENTES ======

    if painel_usado == "Clientes":

        if chamar_acao == "Acrescentar":                        # cria dicionário com os dados e adiciona ao bd
            novo_cliente = {
                "cpf_cnpj":        v1,
                "nome_completo":   v2,
                "email":           v3,
                "sexo":            v4,
                "telefone":        v5,
                "data_nascimento": v6,
                "status":          v7
            }
            bd_clientes.append(novo_cliente)
            mensagem_alerta = "Cliente adicionado com sucesso"

        elif chamar_acao == "Pesquisar":                        # busca por CPF, nome ou telefone
            cliente_encontrado = None
            for cliente in bd_clientes:
                if (v1 and cliente["cpf_cnpj"] == v1) or \
                   (v2 and cliente["nome_completo"].lower() == v2.lower()) or \
                   (v5 and cliente["telefone"] == v5):
                    cliente_encontrado = cliente
                    break

            if cliente_encontrado:
                mensagem_alerta = (
                    f"Cliente encontrado!\n\n"
                    f"CPF/CNPJ: {cliente_encontrado['cpf_cnpj']}\n"
                    f"Nome: {cliente_encontrado['nome_completo']}\n"
                    f"Email: {cliente_encontrado['email']}\n"
                    f"Sexo: {cliente_encontrado['sexo']}\n"
                    f"Telefone: {cliente_encontrado['telefone']}\n"
                    f"Nascimento: {cliente_encontrado['data_nascimento']}\n"
                    f"Status: {cliente_encontrado['status']}"
                )
            else:
                label_erro_crud.configure(
                    text="Erro: Nenhum cliente localizado!",
                    text_color="#e74c3c"
                )
                return

        elif chamar_acao == "Atualizar":                        # localiza pelo CPF e atualiza os demais campos
            atualizou = False
            for cliente in bd_clientes:
                if cliente["cpf_cnpj"] == v1:
                    cliente["nome_completo"]   = v2
                    cliente["email"]           = v3
                    cliente["sexo"]            = v4
                    cliente["telefone"]        = v5
                    cliente["data_nascimento"] = v6
                    cliente["status"]          = v7
                    atualizou = True
                    break

            if atualizou:
                mensagem_alerta = "Dados atualizados com sucesso"
            else:
                label_erro_crud.configure(
                    text="Erro: CPF/CNPJ não cadastrado para atualização!",
                    text_color="#e74c3c"
                )
                return

        elif chamar_acao == "Remover":
            # PASSO 1: verifica se o cliente existe antes de abrir qualquer popup
            posicao_remover = -1
            for i, cliente in enumerate(bd_clientes):
                if cliente["cpf_cnpj"] == v1:                  # busca exclusivamente pelo CPF
                    posicao_remover = i
                    break

            # PASSO 2: cliente não encontrado → mostra erro e encerra, SEM abrir popup
            if posicao_remover == -1:
                label_erro_crud.configure(
                    text="Cliente não consta no sistema. Confira os dados informados.",
                    text_color="#e74c3c"
                )
                return

            # PASSO 3: cliente existe → exibe popup de confirmação com os dados dele
            cliente_alvo = bd_clientes[posicao_remover]

            popup_confirm = ctk.CTkToplevel(janela)
            popup_confirm.title("Confirmar Exclusão")
            popup_confirm.geometry("420x230")
            popup_confirm.grab_set()                            # bloqueia a janela principal durante a confirmação

            ctk.CTkLabel(
                popup_confirm,
                text=(
                    f"Tem certeza que deseja excluir o cliente?\n\n"
                    f"Nome: {cliente_alvo['nome_completo']}\n"
                    f"CPF/CNPJ: {cliente_alvo['cpf_cnpj']}\n"
                    f"Telefone: {cliente_alvo['telefone']}"
                ),
                font=ctk.CTkFont(size=13),
                wraplength=380,
                justify="center"
            ).pack(pady=(25, 20))

            frame_btns = ctk.CTkFrame(popup_confirm, fg_color="transparent")
            frame_btns.pack()

            def confirmar_exclusao():                           # executado somente se o usuário clicar "Sim"
                del bd_clientes[posicao_remover]
                popup_confirm.destroy()
                mostrar_msg_sucesso("Cliente removido com sucesso!")

            ctk.CTkButton(
                frame_btns,
                text="Sim, Remover",
                fg_color="#c0392b",
                hover_color="#e74c3c",
                width=130,
                command=confirmar_exclusao
            ).pack(side="left", padx=10)

            ctk.CTkButton(
                frame_btns,
                text="Cancelar",
                fg_color="#34495e",
                hover_color="#2c3e50",
                width=130,
                command=popup_confirm.destroy                   # fecha sem fazer nada
            ).pack(side="left", padx=10)

            return  # interrompe o fluxo: o sucesso só vem via confirmar_exclusao()


    # ====== 2. CRUD DE APÓLICES ======

    elif painel_usado == "Apólices":

        if chamar_acao == "Acrescentar":
            nova_apolice = {
                "id_apolice": v1,
                "id_cotacao": v2,
                "inicio":     v3,
                "fim":        v4
            }
            bd_apolices.append(nova_apolice)
            mensagem_alerta = "Apólice adicionada com sucesso"

        elif chamar_acao == "Pesquisar":
            apolice_encontrada = None
            for apolice in bd_apolices:
                if (v1 and apolice["id_apolice"] == v1) or \
                   (v2 and apolice["id_cotacao"] == v2):
                    apolice_encontrada = apolice
                    break

            if apolice_encontrada:
                mensagem_alerta = (
                    f"Apólice localizada!\n\n"
                    f"ID Apólice: {apolice_encontrada['id_apolice']}\n"
                    f"ID Cotação: {apolice_encontrada['id_cotacao']}\n"
                    f"Início Vigência: {apolice_encontrada['inicio']}\n"
                    f"Fim Vigência: {apolice_encontrada['fim']}"
                )
            else:
                label_erro_crud.configure(
                    text="Erro: Nenhuma apólice localizada!",
                    text_color="#e74c3c"
                )
                return

        elif chamar_acao == "Atualizar":                        # localiza pelo ID da apólice e atualiza datas
            atualizou = False
            for apolice in bd_apolices:
                if apolice["id_apolice"] == v1:
                    apolice["inicio"] = v3
                    apolice["fim"]    = v4
                    atualizou = True
                    break

            if atualizou:
                mensagem_alerta = "Apólice atualizada com sucesso"
            else:
                label_erro_crud.configure(
                    text="Erro: ID de apólice não cadastrado!",
                    text_color="#e74c3c"
                )
                return

        elif chamar_acao == "Remover":                          # localiza pelo ID da apólice ou cotação e remove
            posicao_remover = -1
            for i, apolice in enumerate(bd_apolices):
                if (v1 and apolice["id_apolice"] == v1) or \
                   (v2 and apolice["id_cotacao"] == v2):
                    posicao_remover = i
                    break

            if posicao_remover != -1:
                del bd_apolices[posicao_remover]
                mensagem_alerta = "Apólice removida com sucesso"
            else:
                label_erro_crud.configure(
                    text="Erro: Nenhuma apólice encontrada para remoção!",
                    text_color="#e74c3c"
                )
                return


    # ====== 3. CRUD DE VENDAS ======

    elif painel_usado == "Vendas":

        if chamar_acao == "Acrescentar":
            nova_venda = {
                "id_cotacao":    v1,
                "id_pessoa":     v2,
                "id_seguradora": v3,
                "id_plano":      v4,
                "valor_cotacao": v5,
                "data_cotacao":  v6
            }
            bd_vendas.append(nova_venda)
            mensagem_alerta = "Venda registrada com sucesso"

        elif chamar_acao == "Pesquisar":
            venda_encontrada = None
            for venda in bd_vendas:
                if (v1 and venda["id_cotacao"] == v1) or \
                   (v2 and venda["id_pessoa"] == v2):
                    venda_encontrada = venda
                    break

            if venda_encontrada:
                mensagem_alerta = (
                    f"Dados da venda carregados!\n\n"
                    f"ID Cotação: {venda_encontrada['id_cotacao']}\n"
                    f"ID Pessoa: {venda_encontrada['id_pessoa']}\n"
                    f"ID Seguradora: {venda_encontrada['id_seguradora']}\n"
                    f"ID Plano: {venda_encontrada['id_plano']}\n"
                    f"Valor: R$ {venda_encontrada['valor_cotacao']}\n"
                    f"Data: {venda_encontrada['data_cotacao']}"
                )
            else:
                label_erro_crud.configure(
                    text="Erro: Registro de venda não localizado!",
                    text_color="#e74c3c"
                )
                return

        elif chamar_acao == "Atualizar":                        # localiza pelo ID da cotação e atualiza os demais
            atualizou = False
            for venda in bd_vendas:
                if venda["id_cotacao"] == v1:
                    venda["id_pessoa"]     = v2
                    venda["id_seguradora"] = v3
                    venda["id_plano"]      = v4
                    venda["valor_cotacao"] = v5
                    venda["data_cotacao"]  = v6
                    atualizou = True
                    break

            if atualizou:
                mensagem_alerta = "Venda modificada com sucesso"
            else:
                label_erro_crud.configure(
                    text="Erro: ID de cotação não cadastrado!",
                    text_color="#e74c3c"
                )
                return

        elif chamar_acao == "Remover":                          # localiza pelo ID da cotação ou pessoa e remove
            posicao_remover = -1
            for i, venda in enumerate(bd_vendas):
                if (v1 and venda["id_cotacao"] == v1) or \
                   (v2 and venda["id_pessoa"] == v2):
                    posicao_remover = i
                    break

            if posicao_remover != -1:
                del bd_vendas[posicao_remover]
                mensagem_alerta = "Venda excluída com sucesso"
            else:
                label_erro_crud.configure(
                    text="Erro: Registro de venda não encontrado para remoção!",
                    text_color="#e74c3c"
                )
                return

    # --- Limpeza dos campos após operação bem-sucedida ---
    for campo in [campo1_ativo, campo2_ativo, campo3_ativo,
                  campo4_ativo, campo5_ativo, campo6_ativo, campo7_ativo]:
        if campo:
            campo.configure(state="normal")                     # garante que campos desabilitados também sejam limpos
            campo.delete(0, "end")

    mostrar_msg_sucesso(mensagem_alerta)                        # exibe o popup de resultado final


# ============= CONSTRUÇÃO DINÂMICA DOS CAMPOS DO FORMULÁRIO =============

def gerar_campos_formulario(acao, nome_secao):
    global campo1_ativo, campo2_ativo, campo3_ativo, campo4_ativo
    global campo5_ativo, campo6_ativo, campo7_ativo
    global painel_usado, chamar_acao, label_erro_crud

    painel_usado = nome_secao
    chamar_acao  = acao

    # Limpa o formulário anterior antes de gerar o novo
    for w in frame_zona_inputs.winfo_children():
        w.destroy()

    # Título do formulário atual
    ctk.CTkLabel(
        frame_zona_inputs,
        text=f"Formulário para: {acao} {nome_secao[:-1]}",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="#3498db"
    ).pack(pady=(10, 5))

    # Inicializa todas as variáveis de rótulo, placeholder e validador como None
    lbl1, placeholder1, validador1 = None, None, None
    lbl2, placeholder2, validador2 = None, None, None
    lbl3, placeholder3, validador3 = None, None, None
    lbl4, placeholder4, validador4 = None, None, None
    lbl5, placeholder5, validador5 = None, None, None
    lbl6, placeholder6, validador6 = None, None, None
    lbl7, placeholder7, validador7 = None, None, None

    # ---- Define quais campos aparecem para cada seção e ação ----

    if nome_secao == "Clientes":
        if acao == "Pesquisar":                                 # busca por CPF, nome ou telefone
            lbl1, placeholder1, validador1 = "CPF/CNPJ (Filtro):",      "Deixe vazio para filtrar por outro", validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo (Filtro):",  "Deixe vazio para filtrar por outro", None
            lbl5, placeholder5, validador5 = "Telefone (Filtro):",       "Deixe vazio para filtrar por outro", validador_telefone

        elif acao == "Remover":                                 # apenas CPF editável; demais preenchidos automaticamente
            lbl1, placeholder1, validador1 = "CPF/CNPJ:",       "Digite o CPF para buscar",      validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo:",  "Preenchido automaticamente",    None
            lbl3, placeholder3, validador3 = "Email:",          "Preenchido automaticamente",    None
            lbl5, placeholder5, validador5 = "Telefone:",       "Preenchido automaticamente",    validador_telefone

        else:                                                   # Acrescentar e Atualizar usam todos os campos
            lbl1, placeholder1, validador1 = "CPF/CNPJ (Max 11):",            "Digite apenas números",    validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo:",                "Nome da pessoa",           None
            lbl3, placeholder3, validador3 = "Email:",                        "exemplo@email.com",        None
            lbl4, placeholder4, validador4 = "Sexo (M/F):",                   "Apenas 1 caractere",       None
            lbl5, placeholder5, validador5 = "Telefone (Max 11):",            "DDD + Número",             validador_telefone
            lbl6, placeholder6, validador6 = "Data de Nascimento (AAAA-MM-DD):", "Formato do Banco (Date)", None
            lbl7, placeholder7, validador7 = "Status (Ativo/Inativo):",       "Status cadastral",         None

    elif nome_secao == "Apólices":
        if acao in ["Pesquisar", "Remover"]:                    # busca por ID da apólice ou cotação
            lbl1, placeholder1, validador1 = "ID Apólice (Filtro):", "Filtrar por ID da Apólice", validador_apolice
            lbl2, placeholder2, validador2 = "ID Cotação (Filtro):", "Filtrar por ID da Cotação", validador_venda
        else:                                                   # Acrescentar e Atualizar usam todos os campos
            lbl1, placeholder1, validador1 = "ID Apólice (id_apolice):", "Código identificador",          validador_apolice
            lbl2, placeholder2, validador2 = "ID Cotação (id_cotacao):", "Chave estrangeira de Cotações", validador_venda
            lbl3, placeholder3, validador3 = "Data Início (AAAA-MM-DD):", "Início do seguro",             None
            lbl4, placeholder4, validador4 = "Data Fim (AAAA-MM-DD):",   "Fim do seguro",                None

    elif nome_secao == "Vendas":
        if acao in ["Pesquisar", "Remover"]:                    # busca por ID da cotação ou pessoa
            lbl1, placeholder1, validador1 = "ID Cotação (Filtro):", "Filtrar por Cotação",       validador_venda
            lbl2, placeholder2, validador2 = "ID Pessoa (Filtro):",  "Filtrar por ID do cliente", None
        else:                                                   # Acrescentar e Atualizar usam todos os campos
            lbl1, placeholder1, validador1 = "ID Cotação (id_cotacao):", "Código identificador",          validador_venda
            lbl2, placeholder2, validador2 = "ID Pessoa (id_pessoa):",   "Chave estrangeira de Pessoa",   None
            lbl3, placeholder3, validador3 = "ID Seguradora:",           "Chave estrangeira de Seguradora", None
            lbl4, placeholder4, validador4 = "ID Plano:",                "Chave estrangeira de Plano",    None
            lbl5, placeholder5, validador5 = "Valor da Cotação R$:",     "Preço calculado",               None
            lbl6, placeholder6, validador6 = "Data Cotação (AAAA-MM-DD):", "Data do processamento",       None

    # ---- Renderiza os campos conforme as variáveis definidas acima ----

    campo1_ativo = None
    if lbl1:
        ctk.CTkLabel(frame_zona_inputs, text=lbl1, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2, 0))
        campo1_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder1, width=340, height=30)
        if validador1: campo1_ativo.configure(validate="key", validatecommand=(validador1, "%P"))
        campo1_ativo.pack(pady=(2, 4))

    campo2_ativo = None
    if lbl2:
        ctk.CTkLabel(frame_zona_inputs, text=lbl2, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2, 0))
        campo2_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder2, width=340, height=30)
        if validador2: campo2_ativo.configure(validate="key", validatecommand=(validador2, "%P"))
        campo2_ativo.pack(pady=(2, 4))

    campo3_ativo = None
    if lbl3:
        ctk.CTkLabel(frame_zona_inputs, text=lbl3, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2, 0))
        campo3_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder3, width=340, height=30)
        if validador3: campo3_ativo.configure(validate="key", validatecommand=(validador3, "%P"))
        campo3_ativo.pack(pady=(2, 4))

    campo4_ativo = None
    if lbl4:
        ctk.CTkLabel(frame_zona_inputs, text=lbl4, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2, 0))
        campo4_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder4, width=340, height=30)
        if validador4: campo4_ativo.configure(validate="key", validatecommand=(validador4, "%P"))
        campo4_ativo.pack(pady=(2, 4))

    campo5_ativo = None
    if lbl5:
        ctk.CTkLabel(frame_zona_inputs, text=lbl5, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2, 0))
        campo5_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder5, width=340, height=30)
        if validador5: campo5_ativo.configure(validate="key", validatecommand=(validador5, "%P"))
        campo5_ativo.pack(pady=(2, 4))

    campo6_ativo = None
    if lbl6:
        ctk.CTkLabel(frame_zona_inputs, text=lbl6, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2, 0))
        campo6_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder6, width=340, height=30)
        if validador6: campo6_ativo.configure(validate="key", validatecommand=(validador6, "%P"))
        campo6_ativo.pack(pady=(2, 4))

    campo7_ativo = None
    if lbl7:
        ctk.CTkLabel(frame_zona_inputs, text=lbl7, font=ctk.CTkFont(size=12)).pack(anchor="w", pady=(2, 0))
        campo7_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder7, width=340, height=30)
        if validador7: campo7_ativo.configure(validate="key", validatecommand=(validador7, "%P"))
        campo7_ativo.pack(pady=(2, 4))

    # ---- Bloco exclusivo do Remover Clientes: busca automática ao sair do campo CPF ----

    if nome_secao == "Clientes" and acao == "Remover":

        # Desabilita campos 2, 3 e 5 para que só sejam preenchidos automaticamente
        for campo in [campo2_ativo, campo3_ativo, campo5_ativo]:
            if campo:
                campo.configure(state="disabled")

        def buscar_cliente_por_cpf(event=None):
            """Dispara ao sair do campo CPF (FocusOut ou Enter) e preenche os demais campos."""
            cpf_digitado = campo1_ativo.get().strip()

            # Limpa campos automáticos e erro antes de cada nova busca
            label_erro_crud.configure(text="")
            for campo in [campo2_ativo, campo3_ativo, campo5_ativo]:
                if campo:
                    campo.configure(state="normal")
                    campo.delete(0, "end")
                    campo.configure(state="disabled")

            if not cpf_digitado:                                # se o CPF estiver vazio, não faz nada
                return

            # Percorre o bd procurando o CPF digitado
            cliente_encontrado = None
            for cliente in bd_clientes:
                if cliente["cpf_cnpj"] == cpf_digitado:
                    cliente_encontrado = cliente
                    break

            if cliente_encontrado is None:                      # CPF não existe no bd
                label_erro_crud.configure(
                    text="Cliente não consta no sistema. Confira os dados informados.",
                    text_color="#e74c3c"
                )
                return

            # CPF encontrado: preenche os campos automaticamente com os dados do cliente
            for campo, valor in [
                (campo2_ativo, cliente_encontrado["nome_completo"]),
                (campo3_ativo, cliente_encontrado["email"]),
                (campo5_ativo, cliente_encontrado["telefone"]),
            ]:
                if campo:
                    campo.configure(state="normal")
                    campo.delete(0, "end")
                    campo.insert(0, valor)
                    campo.configure(state="disabled")           # volta a desabilitar após preencher

        # Vincula a busca ao evento de saída do campo CPF e também ao Enter
        campo1_ativo.bind("<FocusOut>", buscar_cliente_por_cpf)
        campo1_ativo.bind("<Return>",   buscar_cliente_por_cpf)

    # ---- Botão de confirmação ----
    ctk.CTkButton(
        frame_zona_inputs,
        text=f"Confirmar {acao}",
        fg_color="#27ae60",
        hover_color="#2ecc71",
        width=200,
        height=35,
        command=confirma_crud
    ).pack(pady=12)

    # Label de erro posicionado abaixo do botão para ficar sempre visível
    label_erro_crud = ctk.CTkLabel(
        frame_zona_inputs,
        text="",
        font=ctk.CTkFont(size=12, weight="bold"),
        text_color="#e74c3c"
    )
    label_erro_crud.pack(pady=(0, 10))


# ============= FUNÇÕES DE PONTE PARA OS BOTÕES DO CRUD =============

def acao_acrescentar_clicada():
    gerar_campos_formulario("Acrescentar", secao_painel_aberto)

def acao_pesquisar_clicada():
    gerar_campos_formulario("Pesquisar", secao_painel_aberto)

def acao_atualizar_clicada():
    gerar_campos_formulario("Atualizar", secao_painel_aberto)

def acao_remover_clicada():
    gerar_campos_formulario("Remover", secao_painel_aberto)


# ============= FUNÇÃO GERAL PARA MONTAR A ESTRUTURA DO PAINEL =============

secao_painel_aberto = ""

def montar_estrutura_painel(nome):
    global frame_zona_inputs, secao_painel_aberto
    secao_painel_aberto = nome

    for w in frame_conteudo.winfo_children():                   # limpa o conteúdo anterior
        w.destroy()

    ctk.CTkLabel(
        frame_conteudo,
        text=f"Painel de {nome}",
        font=ctk.CTkFont(size=22, weight="bold")
    ).pack(pady=(20, 15))

    frame_botoes_crud = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_botoes_crud.pack(pady=10)

    ctk.CTkButton(frame_botoes_crud, text="Acrescentar", width=110, height=35,                                             command=acao_acrescentar_clicada).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_crud, text="Pesquisar",   width=110, height=35, fg_color="#34495e", hover_color="#2c3e50", command=acao_pesquisar_clicada).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_crud, text="Atualizar",   width=110, height=35, fg_color="#2980b9", hover_color="#3498db", command=acao_atualizar_clicada).pack(side="left", padx=5)
    ctk.CTkButton(frame_botoes_crud, text="Remover",     width=110, height=35, fg_color="#c0392b", hover_color="#e74c3c", command=acao_remover_clicada).pack(side="left", padx=5)

    # CTkScrollableFrame garante scroll automático quando o conteúdo ultrapassar a altura da janela
    frame_zona_inputs = ctk.CTkScrollableFrame(frame_conteudo, fg_color="transparent")
    frame_zona_inputs.pack(pady=10, fill="both", expand=True)


# ============= FUNÇÕES DE PONTE PARA O MENU LATERAL =============

def mostrar_tela_clientes():
    montar_estrutura_painel("Clientes")

def mostrar_secao_apolices():
    montar_estrutura_painel("Apólices")

def mostrar_secao_vendas():
    montar_estrutura_painel("Vendas")


# ============= BOTÕES DO MENU LATERAL =============

ctk.CTkButton(frame_lateral, text=" CLIENTES", anchor="w", width=160, height=40, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_tela_clientes).pack(pady=3, padx=10)
ctk.CTkButton(frame_lateral, text=" APÓLICES", anchor="w", width=160, height=40, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_apolices).pack(pady=3, padx=10)
ctk.CTkButton(frame_lateral, text=" VENDAS",   anchor="w", width=160, height=40, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_vendas).pack(pady=3, padx=10)

# Botão SAIR fixo na parte inferior do menu lateral
btn_sair_lateral = ctk.CTkButton(
    frame_lateral,
    text="SAIR",
    anchor="center",
    width=160,
    height=40,
    fg_color="#c0392b",
    hover_color="#e74c3c",
    font=ctk.CTkFont(size=13, weight="bold"),
    command=fechar_login
)
btn_sair_lateral.pack(side="bottom", pady=20, padx=10)


# ============= LOOP PRINCIPAL =============

janela.mainloop()