# main.py
# Interface gráfica do sistema de corretora de seguros
# Conectado ao banco de dados PostgreSQL via módulo crud.py

import customtkinter as ctk                # biblioteca para interface gráfica moderna
from config import USUARIO, SENHA          # credenciais de login do arquivo config.py
import crud                                # funções de acesso ao banco de dados

ctk.set_appearance_mode("dark")            # tema escuro
ctk.set_default_color_theme("blue")        # cor padrão dos botões

janela = ctk.CTk()                         # janela principal do sistema
janela.title("Corretora de Seguros")       # título da janela
janela.geometry("850x650")                 # tamanho da janela


# ============= FUNÇÕES DE LIMITE DE TAMANHO =============

def limita_cpf(tamanho_cpf):               # faz o CPF não ultrapassar 11 números
    return len(tamanho_cpf) <= 11

def limita_apolice(tamanho_apolice):       # apólice não ultrapassa 15 caracteres
    return len(tamanho_apolice) <= 15

def limita_venda(texto_idvenda):           # ID da venda não ultrapassa 10 caracteres
    return len(texto_idvenda) <= 10

def limita_telefone(texto_telefone):       # telefone não ultrapassa 11 caracteres (DDD + número)
    return len(texto_telefone) <= 11

def limita_sexo(texto_sexo):               # sexo deve ser vazio ou 1 caractere válido (M, F ou O)
    if texto_sexo == "":                   # permite apagar o campo
        return True
    if len(texto_sexo) > 1:               # bloqueia mais de 1 caractere
        return False
    return texto_sexo.upper() in ["M", "F", "O"]


# Registra as funções para que possam ser usadas como validadores pelo Tkinter
validador_cpf      = janela.register(limita_cpf)
validador_apolice  = janela.register(limita_apolice)
validador_venda    = janela.register(limita_venda)
validador_telefone = janela.register(limita_telefone)
validador_sexo     = janela.register(limita_sexo)


# ============= JANELA DE RESPOSTA (POPUP DE SUCESSO) =============

def mostrar_msg_sucesso(mensagem):         # exibe janela de aviso após operações do CRUD
    popup = ctk.CTkToplevel(janela)        # cria uma nova janela pop-up
    popup.title("Aviso do Sistema")        # nome da janela
    popup.geometry("400x220")              # tamanho da janela
    popup.grab_set()                       # impede interação com a janela principal enquanto o pop-up estiver aberto

    ctk.CTkLabel(
        popup,
        text=mensagem,
        font=ctk.CTkFont(size=13, weight="bold"),
        wraplength=350
    ).pack(pady=(30, 20))

    ctk.CTkButton(popup, text="OK", width=100, command=popup.destroy).pack()


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
        label_erro.configure(text="Usuário ou senha incorretos!", text_color="red")

def login_entrar(event):                                        # dispara o login com a tecla Enter
    login()


# ============= PAINEL DE LOGIN =============

frame_login = ctk.CTkFrame(master=janela)
frame_login.pack(pady=20, padx=40, fill="both", expand=True)

ctk.CTkLabel(frame_login, text=" Corretora de Valores ", text_color="green", font=ctk.CTkFont(size=20, weight="bold")).pack(pady=(24, 4))
ctk.CTkLabel(frame_login, text="Informe seu LOGIN para continuar", font=ctk.CTkFont(size=12), text_color="white").pack(pady=(0, 16))

entry_user = ctk.CTkEntry(frame_login, placeholder_text="LOGIN", width=260, height=40)
entry_user.pack(pady=8)

entry_pass = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*", width=260, height=40)
entry_pass.pack(pady=8)

label_erro = ctk.CTkLabel(frame_login, text="", font=ctk.CTkFont(size=12))
label_erro.pack(pady=(4, 0))

ctk.CTkButton(frame_login, text="Entrar", command=login, width=260, height=40, font=ctk.CTkFont(size=14, weight="bold"), fg_color="green", hover_color="darkgreen").pack(pady=16)

janela.bind("<Return>", login_entrar)                           # tecla Enter também aciona o login


# ============= PAINEL MENU PRINCIPAL =============

frame_menu = ctk.CTkFrame(master=janela)                        # cria o painel do menu principal


# ============= BARRA SUPERIOR =============

frame_topbar = ctk.CTkFrame(frame_menu, height=45, corner_radius=0, fg_color="#1a1a2e")
frame_topbar.pack(side="top", fill="x")
frame_topbar.pack_propagate(False)

ctk.CTkLabel(frame_topbar, text=" Corretora de Seguros - Sistema Interno", font=ctk.CTkFont(size=15, weight="bold"), text_color="white").pack(side="left", padx=20)


# ============= FUNÇÃO SAIR =============

def fechar_login():                                             # fecha o menu e volta para a tela de login
    frame_menu.pack_forget()
    frame_lateral.pack_forget()
    frame_login.pack(pady=20, padx=40, fill="both", expand=True)
    entry_user.delete(0, "end")
    entry_pass.delete(0, "end")


# ============= PAINEL CENTRAL =============

frame_centro = ctk.CTkFrame(frame_menu, fg_color="transparent")
frame_centro.pack(fill="both", expand=True)


# ============= MENU LATERAL =============

frame_lateral = ctk.CTkFrame(frame_centro, width=180, corner_radius=0, fg_color="#16213e")
frame_lateral.pack_propagate(False)

ctk.CTkLabel(frame_lateral, text="NAVEGAÇÃO", font=ctk.CTkFont(size=12, weight="bold"), text_color="gray").pack(pady=(20, 10), padx=12, anchor="w")


# ============= PAINEL DE CONTEÚDO =============

frame_conteudo = ctk.CTkFrame(frame_centro, fg_color="transparent")
frame_conteudo.pack(side="right", fill="both", expand=True)


# ============= VARIÁVEIS GLOBAIS DOS INPUTS =============

campo1_ativo  = None   # armazena referência do campo 1 ativo no formulário
campo2_ativo  = None
campo3_ativo  = None
campo4_ativo  = None
campo5_ativo  = None
campo6_ativo  = None
campo7_ativo  = None
label_erro_crud = None # referência ao label de erro do CRUD atual
painel_usado  = ""     # indica qual seção está aberta
chamar_acao   = ""     # indica qual ação está ativa


# ============= FUNÇÃO AUXILIAR: CONVERTE DATA BR PARA BANCO =============

def data_br_para_banco(data_br):
    """Converte DD/MM/AAAA para AAAA-MM-DD antes de enviar ao banco."""
    try:
        partes = data_br.strip().split("/")
        if len(partes) == 3:
            dia, mes, ano = partes
            return f"{ano}-{mes.zfill(2)}-{dia.zfill(2)}"
    except Exception:
        pass
    return data_br                                              # retorna original se não conseguir converter


# ============= FUNÇÃO DE CONFIRMAÇÃO DO CRUD =============

def confirma_crud():
    global campo1_ativo, campo2_ativo, campo3_ativo, campo4_ativo
    global campo5_ativo, campo6_ativo, campo7_ativo
    global painel_usado, chamar_acao, label_erro_crud

    # Coleta os valores digitados em cada campo, removendo espaços extras
    v1 = campo1_ativo.get().strip() if campo1_ativo else ""
    v2 = campo2_ativo.get().strip() if campo2_ativo else ""
    v3 = campo3_ativo.get().strip() if campo3_ativo else ""
    v4 = campo4_ativo.get().strip() if campo4_ativo else ""
    v5 = campo5_ativo.get().strip() if campo5_ativo else ""
    v6 = campo6_ativo.get().strip() if campo6_ativo else ""
    v7 = campo7_ativo.get().strip() if campo7_ativo else ""

    label_erro_crud.configure(text="")                          # limpa erro anterior

    # --- VALIDAÇÃO DE CAMPOS ---
    if chamar_acao in ["Acrescentar", "Atualizar"]:             # todos os campos devem estar preenchidos
        if (campo1_ativo and not v1) or (campo2_ativo and not v2) or \
           (campo3_ativo and not v3) or (campo4_ativo and not v4) or \
           (campo5_ativo and not v5) or (campo6_ativo and not v6) or \
           (campo7_ativo and not v7):
            label_erro_crud.configure(text="Preencha todos os campos do formulário!", text_color="#e74c3c")
            return

    elif chamar_acao == "Pesquisar":                            # pelo menos um campo deve ser preenchido
        if not v1 and not v2 and not v3 and not v4 and not v5:
            label_erro_crud.configure(text="Preencha pelo menos um campo para buscar!", text_color="#e74c3c")
            return

    elif chamar_acao == "Remover":                              # campo 1 obrigatório para remover
        if not v1:
            label_erro_crud.configure(text="Informe o campo de identificação para localizar o registro.", text_color="#e74c3c")
            return

    mensagem_alerta = ""


    # ====== CRUD DE CLIENTES ======

    if painel_usado == "Clientes":

        if chamar_acao == "Acrescentar":
            v6_banco = data_br_para_banco(v6)                   # converte data nascimento para formato do banco
            sucesso = crud.create_pessoa(v1, v2, v3, v4.upper(), v5, v6_banco, v7)
            if sucesso:
                mensagem_alerta = "Cliente adicionado com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao salvar no banco. Verifique os dados.", text_color="#e74c3c")
                return

        elif chamar_acao == "Pesquisar":
            cliente = None
            if v1:
                cliente = crud.read_pessoa_por_cpf(v1)
            elif v2:
                cliente = crud.read_pessoa_por_nome(v2)
            elif v5:
                cliente = crud.read_pessoa_por_telefone(v5)

            if cliente:
                mensagem_alerta = (
                    f"Cliente encontrado!\n\n"
                    f"CPF/CNPJ: {cliente['cpf_cnpj']}\n"
                    f"Nome: {cliente['nome_completo']}\n"
                    f"Email: {cliente['email']}\n"
                    f"Sexo: {cliente['sexo']}\n"
                    f"Telefone: {cliente['telefone']}\n"
                    f"Nascimento: {cliente['data_nascimento']}\n"
                    f"Status: {cliente['status']}"
                )
            else:
                label_erro_crud.configure(text="Nenhum cliente localizado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Atualizar":
            v6_banco = data_br_para_banco(v6)                   # converte data nascimento para formato do banco
            sucesso = crud.update_pessoa(v1, v2, v3, v4.upper(), v5, v6_banco, v7)
            if sucesso:
                mensagem_alerta = "Dados atualizados com sucesso!"
            else:
                label_erro_crud.configure(text="CPF/CNPJ não encontrado para atualização!", text_color="#e74c3c")
                return

        elif chamar_acao == "Remover":
            cliente_alvo = crud.read_pessoa_por_cpf(v1)

            if cliente_alvo is None:
                label_erro_crud.configure(text="Cliente não consta no sistema. Confira os dados informados.", text_color="#e74c3c")
                return

            popup_confirm = ctk.CTkToplevel(janela)
            popup_confirm.title("Confirmar Exclusão")
            popup_confirm.geometry("420x230")
            popup_confirm.grab_set()

            ctk.CTkLabel(
                popup_confirm,
                text=(
                    f"Tem certeza que deseja excluir o cliente?\n\n"
                    f"Nome: {cliente_alvo['nome_completo']}\n"
                    f"CPF/CNPJ: {cliente_alvo['cpf_cnpj']}\n"
                    f"Telefone: {cliente_alvo['telefone']}"
                ),
                font=ctk.CTkFont(size=13), wraplength=380, justify="center"
            ).pack(pady=(25, 20))

            frame_btns = ctk.CTkFrame(popup_confirm, fg_color="transparent")
            frame_btns.pack()

            def confirmar_exclusao():
                sucesso = crud.delete_pessoa(cliente_alvo["cpf_cnpj"])
                popup_confirm.destroy()
                if sucesso:
                    mostrar_msg_sucesso("Cliente removido com sucesso!")
                else:
                    mostrar_msg_sucesso("Erro ao remover. Tente novamente.")

            ctk.CTkButton(frame_btns, text="Sim, Remover", fg_color="#c0392b", hover_color="#e74c3c", width=130, command=confirmar_exclusao).pack(side="left", padx=10)
            ctk.CTkButton(frame_btns, text="Cancelar", fg_color="#34495e", hover_color="#2c3e50", width=130, command=popup_confirm.destroy).pack(side="left", padx=10)
            return


    # ====== CRUD DE SEGURADORAS ======

    elif painel_usado == "Seguradoras":

        if chamar_acao == "Acrescentar":
            sucesso = crud.create_seguradora(v1, v2, v3)       # nome_fantasia, cnpj, telefone_suporte
            if sucesso:
                mensagem_alerta = "Seguradora adicionada com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao salvar seguradora no banco.", text_color="#e74c3c")
                return

        elif chamar_acao == "Pesquisar":
            seguradoras = None
            if v1:
                seguradoras = crud.read_seguradora_por_id(v1)
            elif v2:
                seguradoras = crud.read_seguradora_por_cnpj(v2)

            if seguradoras:
                mensagem_alerta = (
                    f"Seguradora encontrada!\n\n"
                    f"ID: {seguradoras['id']}\n"
                    f"Nome: {seguradoras['nome']}\n"
                    f"CNPJ: {seguradoras['cnpj']}\n"
                    f"Telefone Suporte: {seguradoras['telefone']}"
                )
            else:
                label_erro_crud.configure(text="Nenhuma seguradora localizada!", text_color="#e74c3c")
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_seguradora(v1, v2, v3, v4)
            if sucesso:
                mensagem_alerta = "Seguradora atualizada com sucesso!"
            else:
                label_erro_crud.configure(text="ID de seguradora não encontrado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_seguradora(v1)
            if sucesso:
                mensagem_alerta = "Seguradora removida com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhuma seguradora encontrada para remoção!", text_color="#e74c3c")
                return


    # ====== CRUD DE PLANOS ======

    elif painel_usado == "Planos":

        if chamar_acao == "Acrescentar":
            sucesso = crud.create_plano(v1, v2, v3)
            if sucesso:
                mensagem_alerta = "Plano adicionado com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao salvar plano no banco.", text_color="#e74c3c")
                return

        elif chamar_acao == "Pesquisar":
            planos = None
            
            if v1:
                planos = crud.read_plano_por_id(v1)
            elif v2:
                planos = crud.read_plano_por_nome(v2)

            if planos:
                mensagem_alerta = (
                    f"Plano encontrado!\n\n"
                    f"ID - Plano: {planos['plano_id']}\n"
                    f"ID - Seguradora: {planos['seguradora_id']}\n"
                    f"Tipo Cobertura: {planos['cobertura']}\n"
                )
            else:
                label_erro_crud.configure(text="Nenhum plano localizado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_plano(v1, v2, v3, v4)
            if sucesso:
                mensagem_alerta = "Plano atualizado com sucesso!"
            else:
                label_erro_crud.configure(text="ID de plano não encontrado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_plano(v1)
            if sucesso:
                mensagem_alerta = "Plano removido com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhum plano encontrado para remoção!", text_color="#e74c3c")
                return


    # ====== CRUD DE BENS ======

    elif painel_usado == "Bens":

        if chamar_acao == "Acrescentar":
            sucesso = crud.create_bem(v1, v2, v3, v4)
            if sucesso:
                mensagem_alerta = "Bem adicionado com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao salvar bem no banco.", text_color="#e74c3c")
                return

        elif chamar_acao == "Pesquisar":
            bem = crud.read_bem_por_id(v1)

            if bem:
                mensagem_alerta = (
                    f"Bem encontrado!\n\n"
                    f"ID Bem: {bem['id_bem']}\n"
                    f"ID Pessoa: {bem['id_pessoa']}\n"
                    f"Tipo: {bem['tipo_bem']}\n"
                    f"Descrição: {bem['descricao_bem']}\n"
                    f"Valor Estimado: R$ {bem['valor_estimado']}"
                )
            else:
                label_erro_crud.configure(text="Nenhum bem localizado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_bem(v1, v2, v3, v4)
            if sucesso:
                mensagem_alerta = "Bem atualizado com sucesso!"
            else:
                label_erro_crud.configure(text="ID de bem não encontrado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_bem(v1)
            if sucesso:
                mensagem_alerta = "Bem removido com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhum bem encontrado para remoção!", text_color="#e74c3c")
                return


    # ====== CRUD DE APÓLICES ======

    elif painel_usado == "Apólices":

        if chamar_acao == "Acrescentar":
            v3_banco = data_br_para_banco(v3)                   # converte data início para formato do banco
            v4_banco = data_br_para_banco(v4)                   # converte data fim para formato do banco
            sucesso = crud.create_apolice(v2, v3_banco, v4_banco)
            if sucesso:
                mensagem_alerta = "Apólice adicionada com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao salvar apólice no banco.", text_color="#e74c3c")
                return

        elif chamar_acao == "Pesquisar":
            apolice = None
            if v1:
                apolice = crud.read_apolice(v1)
            elif v2:
                apolice = crud.read_apolice_por_cotacao(v2)

            if apolice:
                mensagem_alerta = (
                    f"Apólice localizada!\n\n"
                    f"ID Apólice: {apolice['id_apolice']}\n"
                    f"ID Cotação: {apolice['id_cotacao']}\n"
                    f"Início Vigência: {apolice['inicio']}\n"
                    f"Fim Vigência: {apolice['fim']}"
                )
            else:
                label_erro_crud.configure(text="Nenhuma apólice localizada!", text_color="#e74c3c")
                return

        elif chamar_acao == "Atualizar":
            v3_banco = data_br_para_banco(v3)
            v4_banco = data_br_para_banco(v4)
            sucesso = crud.update_apolice(v1, v3_banco, v4_banco)
            if sucesso:
                mensagem_alerta = "Apólice atualizada com sucesso!"
            else:
                label_erro_crud.configure(text="ID de apólice não encontrado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_apolice(v1)
            if sucesso:
                mensagem_alerta = "Apólice removida com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhuma apólice encontrada para remoção!", text_color="#e74c3c")
                return


    # ====== CRUD DE VENDAS (cotacoes) ======

    elif painel_usado == "Vendas":

        if chamar_acao == "Acrescentar":
            v6_banco = data_br_para_banco(v6)                   # converte data cotação para formato do banco
            sucesso = crud.create_cotacao(v2, v3, v4, v5, v6_banco)
            if sucesso:
                mensagem_alerta = "Venda registrada com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao registrar venda no banco.", text_color="#e74c3c")
                return

        elif chamar_acao == "Pesquisar":
            venda = None
            if v1:
                venda = crud.read_cotacao(v1)
            elif v2:
                venda = crud.read_cotacao_por_pessoa(v2)

            if venda:
                mensagem_alerta = (
                    f"Venda encontrada!\n\n"
                    f"ID Cotação: {venda['c.id_cotacao']}\n"
                    f"Nome Pessoa: {venda['p.nome_pessoa']}\n"
                    f"Nome Seguradora: {venda['s.nome_fantasia']}\n"
                    f"Nome Plano: {venda['pl.nome_plano']}\n"
                    f"Valor: R$ {venda['c.valor_cotacao']}\n"
                    f"Data: {venda['c.data_cotacao']}"
                )
            else:
                label_erro_crud.configure(text="Nenhuma venda localizada!", text_color="#e74c3c")
                return

        elif chamar_acao == "Atualizar":
            v6_banco = data_br_para_banco(v6)
            sucesso = crud.update_cotacao(v1, v2, v3, v4, v5, v6_banco)
            if sucesso:
                mensagem_alerta = "Venda atualizada com sucesso!"
            else:
                label_erro_crud.configure(text="ID de cotação não encontrado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_cotacao(v1)
            if sucesso:
                mensagem_alerta = "Venda removida com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhuma venda encontrada para remoção!", text_color="#e74c3c")
                return

    # --- Limpeza dos campos após operação bem-sucedida ---
    for campo in [campo1_ativo, campo2_ativo, campo3_ativo,
                  campo4_ativo, campo5_ativo, campo6_ativo, campo7_ativo]:
        if campo:
            campo.configure(state="normal")
            campo.delete(0, "end")

    mostrar_msg_sucesso(mensagem_alerta)                        # exibe o popup de resultado final


# ============= CONSTRUÇÃO DINÂMICA DOS CAMPOS DO FORMULÁRIO =============

def gerar_campos_formulario(acao, nome_secao):
    global campo1_ativo, campo2_ativo, campo3_ativo, campo4_ativo
    global campo5_ativo, campo6_ativo, campo7_ativo
    global painel_usado, chamar_acao, label_erro_crud

    painel_usado = nome_secao
    chamar_acao  = acao

    for w in frame_zona_inputs.winfo_children():
        w.destroy()

    ctk.CTkLabel(
        frame_zona_inputs,
        text=f"Formulário para: {acao} {nome_secao[:-1]}",
        font=ctk.CTkFont(size=14, weight="bold"),
        text_color="#3498db"
    ).pack(pady=(10, 5))

    lbl1, placeholder1, validador1 = None, None, None
    lbl2, placeholder2, validador2 = None, None, None
    lbl3, placeholder3, validador3 = None, None, None
    lbl4, placeholder4, validador4 = None, None, None
    lbl5, placeholder5, validador5 = None, None, None
    lbl6, placeholder6, validador6 = None, None, None
    lbl7, placeholder7, validador7 = None, None, None

    # ---- Define quais campos aparecem para cada seção e ação ----

    if nome_secao == "Clientes":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "CPF/CNPJ (Filtro):",     "Deixe vazio para filtrar por outro", validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo (Filtro):", "Deixe vazio para filtrar por outro", None
            lbl5, placeholder5, validador5 = "Telefone (Filtro):",      "Deixe vazio para filtrar por outro", validador_telefone

        elif acao == "Remover":
            # Seguir a mesma linha dos outros....apagar somente com o ID
            lbl2, placeholder2, validador2 = "ID do Cliente:", "Digite o ID do cliente para remover", None
            # lbl1, placeholder1, validador1 = "CPF/CNPJ:",      "Digite o CPF para buscar",   validador_cpf
            # lbl2, placeholder2, validador2 = "Nome Completo:", "Preenchido automaticamente", None
            # lbl3, placeholder3, validador3 = "Email:",         "Preenchido automaticamente", None
            # lbl5, placeholder5, validador5 = "Telefone:",      "Preenchido automaticamente", validador_telefone

        else:                                                   # Acrescentar e Atualizar
            lbl1, placeholder1, validador1 = "CPF/CNPJ (Max 11):",          "Digite apenas números",  validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo:",              "Nome da pessoa",          None
            lbl3, placeholder3, validador3 = "Email:",                      "exemplo@email.com",       None
            lbl4, placeholder4, validador4 = "Sexo (M/F/O):",               "M, F ou O",               validador_sexo  # ← validador aplicado
            lbl5, placeholder5, validador5 = "Telefone (Max 11):",          "DDD + Número",            validador_telefone
            lbl6, placeholder6, validador6 = "Data de Nascimento (DD/MM/AAAA):", "Ex: 20/02/1990",    None
            lbl7, placeholder7, validador7 = "Status (Ativo/Inativo):",     "Status cadastral",        None

    elif nome_secao == "Seguradoras":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Seguradora:", "Filtrar pelo ID da seguradora", None
            lbl2, placeholder2, validador2 = "CNPJ:",          "Filtrar pelo CNPJ",             None
        elif acao == "Remover":
            lbl2, placeholder2, validador2 = "ID da Seguradora:", "Digite o ID da seguradora para remover", None
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "ID Seguradora (obrigatório):", "ID para localizar a seguradora", None
            lbl2, placeholder2, validador2 = "Nome Fantasia:",               "Nome da seguradora",             None
            lbl3, placeholder3, validador3 = "CNPJ:",                        "CNPJ da seguradora",             None
            lbl4, placeholder4, validador4 = "Telefone Suporte:",            "Telefone de suporte",            None
        else:
            lbl1, placeholder1, validador1 = "Nome Fantasia:",    "Nome da seguradora",  None
            lbl2, placeholder2, validador2 = "CNPJ:",             "CNPJ da seguradora",  None
            lbl3, placeholder3, validador3 = "Telefone Suporte:", "Telefone de suporte", None

    elif nome_secao == "Planos":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Plano:", "Filtrar pelo ID do plano", None
            lbl2, placeholder2, validador2 = "Nome Plano:", "Filtrar pelo nome do plano", None
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "ID Plano:", "Digite o ID do plano para remover", None
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "ID Plano (obrigatório):", "ID para localizar o plano",  None
            lbl2, placeholder2, validador2 = "ID Seguradora:",          "ID da seguradora vinculada", None
            lbl3, placeholder3, validador3 = "Tipo Cobertura:",         "Ex: Total, Parcial",         None
            lbl4, placeholder4, validador4 = "Nome Plano:",             "Nome do plano",              None
        else:
            lbl1, placeholder1, validador1 = "ID Seguradora:",  "ID da seguradora vinculada", None
            lbl2, placeholder2, validador2 = "Tipo Cobertura:", "Ex: Total, Parcial",         None
            lbl3, placeholder3, validador3 = "Nome Plano:",     "Nome do plano",              None

    elif nome_secao == "Bens":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Bem:", "Filtrar pelo ID do bem", None
        elif acao == "Remover":
            lbl2, placeholder2, validador2 = "ID do Bem:", "Digite o ID do bem para remover", None
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "ID Bem (obrigatório):", "ID para localizar o bem", None
            lbl2, placeholder2, validador2 = "Tipo Bem:",             "Ex: Imóvel, Veículo",     None
            lbl3, placeholder3, validador3 = "Descrição:",            "Descrição do bem",        None
            lbl4, placeholder4, validador4 = "Valor Estimado R$:",    "Ex: 50000.00",            None
        else:
            lbl1, placeholder1, validador1 = "ID Pessoa:",         "ID do dono do bem",   None
            lbl2, placeholder2, validador2 = "Tipo Bem:",          "Ex: Imóvel, Veículo", None
            lbl3, placeholder3, validador3 = "Descrição:",         "Descrição do bem",    None
            lbl4, placeholder4, validador4 = "Valor Estimado R$:", "Ex: 50000.00",        None

    elif nome_secao == "Apólices":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Apólice (Filtro):", "Filtrar por ID da Apólice", validador_apolice
            lbl2, placeholder2, validador2 = "ID Cotação (Filtro):", "Filtrar por ID da Cotação", validador_venda
        elif acao == "Remover":
            lbl2, placeholder2, validador2 = "ID da Apólice:", "Digite o ID da apólice para remover", None
        else:
            lbl1, placeholder1, validador1 = "ID Apólice (id_apolice):",   "Código identificador",          validador_apolice
            lbl2, placeholder2, validador2 = "ID Cotação (id_cotacao):",   "Chave estrangeira de Cotações", validador_venda
            lbl3, placeholder3, validador3 = "Data Início (DD/MM/AAAA):",  "Ex: 01/01/2024",               None
            lbl4, placeholder4, validador4 = "Data Fim (DD/MM/AAAA):",     "Ex: 01/01/2025",               None

    elif nome_secao == "Vendas":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Cotação:", "Filtrar por Cotação",       validador_venda
            lbl2, placeholder2, validador2 = "ID Pessoa:",  "Filtrar por ID do cliente", None
        elif acao == "Remover":
            lbl2, placeholder2, validador2 = "ID da Venda:", "Digite o ID da venda para remover", None
        else:
            lbl1, placeholder1, validador1 = "ID Cotação (id_cotacao):", "Código identificador",            validador_venda
            lbl2, placeholder2, validador2 = "ID Pessoa (id_pessoa):",   "Chave estrangeira de Pessoa",     None
            lbl3, placeholder3, validador3 = "ID Seguradora:",           "Chave estrangeira de Seguradora", None
            lbl4, placeholder4, validador4 = "ID Plano:",                "Chave estrangeira de Plano",      None
            lbl5, placeholder5, validador5 = "Valor da Cotação R$:",     "Preço calculado",                 None
            lbl6, placeholder6, validador6 = "Data Cotação (DD/MM/AAAA):", "Ex: 20/05/2025",               None

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

        for campo in [campo2_ativo, campo3_ativo, campo5_ativo]:
            if campo:
                campo.configure(state="disabled")

        def buscar_cliente_por_cpf(event=None):
            cpf_digitado = campo1_ativo.get().strip()

            label_erro_crud.configure(text="")
            for campo in [campo2_ativo, campo3_ativo, campo5_ativo]:
                if campo:
                    campo.configure(state="normal")
                    campo.delete(0, "end")
                    campo.configure(state="disabled")

            if not cpf_digitado:
                return

            cliente_encontrado = crud.read_pessoa_por_cpf(str(cpf_digitado))

            if cliente_encontrado is None:
                label_erro_crud.configure(
                    text="Cliente não consta no sistema. Confira os dados informados.",
                    text_color="#e74c3c"
                )
                return

            for campo, valor in [
                (campo2_ativo, cliente_encontrado["nome_completo"]),
                (campo3_ativo, cliente_encontrado["email"]),
                (campo5_ativo, cliente_encontrado["telefone"]),
            ]:
                if campo:
                    campo.configure(state="normal")
                    campo.delete(0, "end")
                    campo.insert(0, valor)
                    campo.configure(state="disabled")

        campo1_ativo.bind("<FocusOut>", buscar_cliente_por_cpf)
        campo1_ativo.bind("<Return>",   buscar_cliente_por_cpf)

    # ---- Botão de confirmação ---- #
    ctk.CTkButton(
        frame_zona_inputs,
        text=f"Confirmar {acao}",
        fg_color="#27ae60",
        hover_color="#2ecc71",
        width=200,
        height=35,
        command=confirma_crud
    ).pack(pady=12)

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

    for w in frame_conteudo.winfo_children():
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

    frame_zona_inputs = ctk.CTkScrollableFrame(frame_conteudo, fg_color="transparent")
    frame_zona_inputs.pack(pady=10, fill="both", expand=True)


# ============= FUNÇÕES DE PONTE PARA O MENU LATERAL =============

def mostrar_tela_clientes():
    montar_estrutura_painel("Clientes")

def mostrar_secao_seguradoras():
    montar_estrutura_painel("Seguradoras")

def mostrar_secao_planos():
    montar_estrutura_painel("Planos")

def mostrar_secao_bens():
    montar_estrutura_painel("Bens")

def mostrar_secao_apolices():
    montar_estrutura_painel("Apólices")

def mostrar_secao_vendas():
    montar_estrutura_painel("Vendas")


# ============= BOTÕES DO MENU LATERAL =============

ctk.CTkButton(frame_lateral, text=" CLIENTES",    anchor="w", width=160, height=38, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_tela_clientes).pack(pady=2, padx=10)
ctk.CTkButton(frame_lateral, text=" SEGURADORAS", anchor="w", width=160, height=38, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_seguradoras).pack(pady=2, padx=10)
ctk.CTkButton(frame_lateral, text=" PLANOS",      anchor="w", width=160, height=38, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_planos).pack(pady=2, padx=10)
ctk.CTkButton(frame_lateral, text=" BENS",        anchor="w", width=160, height=38, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_bens).pack(pady=2, padx=10)
ctk.CTkButton(frame_lateral, text=" APÓLICES",    anchor="w", width=160, height=38, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_apolices).pack(pady=2, padx=10)
ctk.CTkButton(frame_lateral, text=" VENDAS",      anchor="w", width=160, height=38, fg_color="transparent", hover_color="#0f3460", font=ctk.CTkFont(size=13), command=mostrar_secao_vendas).pack(pady=2, padx=10)

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
