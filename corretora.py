# main.py
# Interface gráfica do sistema de corretora de seguros
# Conectado ao banco de dados PostgreSQL via módulo crud.py

import customtkinter as ctk                # biblioteca para interface gráfica moderna
from config import USUARIO, SENHA          # credenciais de login do arquivo config.py
import crud                                # funções de acesso ao banco de dados

ctk.set_appearance_mode("light")           # identidade visual clara e corporativa
ctk.set_default_color_theme("green")       # base verde para a identidade visual

# ============= IDENTIDADE VISUAL FRANK COSTA =============
VERDE_INSTITUCIONAL = "#0F7B4D"
VERDE_ESCURO        = "#075E3A"
VERDE_CLARO         = "#34C759"
BRANCO              = "#FFFFFF"
CINZA_CLARO         = "#F5F7FA"
CINZA_ESCURO        = "#2D3748"
DOURADO_PREMIUM     = "#D4AF37"
VERMELHO_ERRO       = "#C53030"
VERMELHO_HOVER      = "#9B2C2C"
BORDA_SUAVE         = "#D9E2EC"
TEXTO_SECUNDARIO    = "#718096"
FUNDO_CARD          = "#FFFFFF"

FONTE_TITULO = "Montserrat"
FONTE_PADRAO = "Inter"

janela = ctk.CTk()                         # janela principal do sistema
janela.title("Corretora de Seguros")       # título da janela
janela.geometry("980x720")                 # tamanho da janela
janela.configure(fg_color=CINZA_CLARO)      # fundo geral corporativo

# ========== FUNÇÕES DE LIMITE DE TAMANHO =============

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

def limite_cnpj(tamanho_cnpj):            # CNPJ não ultrapassa 14 caracteres
    return len(tamanho_cnpj) <= 14


# Registra as funções para que possam ser usadas como validadores pelo Tkinter
validador_cpf      = janela.register(limita_cpf)
validador_apolice  = janela.register(limita_apolice)
validador_venda    = janela.register(limita_venda)
validador_telefone = janela.register(limita_telefone)
validador_sexo     = janela.register(limita_sexo)


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
        label_erro.configure(text="Usuário ou senha incorretos!", text_color=VERMELHO_ERRO)

def login_entrar(event):                                        # dispara o login com a tecla Enter
    login()


# ============= PAINEL DE LOGIN =============

frame_login = ctk.CTkFrame(master=janela, fg_color=FUNDO_CARD, corner_radius=22, border_width=1, border_color=BORDA_SUAVE)
frame_login.pack(pady=45, padx=90, fill="both", expand=True)

ctk.CTkLabel(frame_login, text="Frank Costa", text_color=VERDE_INSTITUCIONAL, font=ctk.CTkFont(family=FONTE_TITULO, size=32, weight="bold")).pack(pady=(44, 2))
ctk.CTkLabel(frame_login, text="Corretora de Seguros", text_color=DOURADO_PREMIUM, font=ctk.CTkFont(family=FONTE_PADRAO, size=15, weight="bold")).pack(pady=(0, 12))
ctk.CTkLabel(frame_login, text="Acesse o sistema administrativo", font=ctk.CTkFont(family=FONTE_PADRAO, size=13), text_color=CINZA_ESCURO).pack(pady=(0, 22))

entry_user = ctk.CTkEntry(frame_login, placeholder_text="LOGIN", width=300, height=44, corner_radius=12, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
entry_user.pack(pady=8)

entry_pass = ctk.CTkEntry(frame_login, placeholder_text="Senha", show="*", width=300, height=44, corner_radius=12, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
entry_pass.pack(pady=8)

label_erro = ctk.CTkLabel(frame_login, text="", font=ctk.CTkFont(size=12))
label_erro.pack(pady=(4, 0))

ctk.CTkButton(frame_login, text="Entrar", command=login, width=300, height=44, corner_radius=12, font=ctk.CTkFont(family=FONTE_PADRAO, size=14, weight="bold"), fg_color=VERDE_INSTITUCIONAL, hover_color=VERDE_ESCURO, text_color=BRANCO).pack(pady=18)

janela.bind("<Return>", login_entrar)                           # tecla Enter também aciona o login


# ============= PAINEL MENU PRINCIPAL =============

frame_menu = ctk.CTkFrame(master=janela, fg_color=CINZA_CLARO)                        # cria o painel do menu principal


# ============= BARRA SUPERIOR =============

frame_topbar = ctk.CTkFrame(frame_menu, height=58, corner_radius=0, fg_color=VERDE_INSTITUCIONAL)
frame_topbar.pack(side="top", fill="x")
frame_topbar.pack_propagate(False)

ctk.CTkLabel(frame_topbar, text=" Frank Costa Corretora de Seguros", font=ctk.CTkFont(family=FONTE_TITULO, size=17, weight="bold"), text_color=BRANCO).pack(side="left", padx=22)
ctk.CTkLabel(frame_topbar, text="Sistema de Gestão Comercial", font=ctk.CTkFont(family=FONTE_PADRAO, size=12), text_color="#E6FFFA").pack(side="right", padx=22)


# ============= FUNÇÃO SAIR =============

def fechar_login():                                             # fecha o menu e volta para a tela de login
    frame_menu.pack_forget()
    frame_lateral.pack_forget()
    frame_login.pack(pady=20, padx=40, fill="both", expand=True)
    entry_user.delete(0, "end")
    entry_pass.delete(0, "end")


# ============= PAINEL CENTRAL =============

frame_centro = ctk.CTkFrame(frame_menu, fg_color=CINZA_CLARO)
frame_centro.pack(fill="both", expand=True)


# ============= MENU LATERAL =============

frame_lateral = ctk.CTkFrame(frame_centro, width=205, corner_radius=0, fg_color=VERDE_ESCURO)
frame_lateral.pack_propagate(False)

ctk.CTkLabel(frame_lateral, text="MENU PRINCIPAL", font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color="#C6F6D5").pack(pady=(24, 14), padx=16, anchor="w")


# ============= PAINEL DE CONTEÚDO =============

frame_conteudo = ctk.CTkFrame(frame_centro, fg_color=CINZA_CLARO)
frame_conteudo.pack(side="right", fill="both", expand=True)


# ============= VARIÁVEIS GLOBAIS DOS INPUTS =============

campo1_ativo  = None   # armazena referência do campo 1 ativo no formulário
campo2_ativo  = None
campo3_ativo  = None
campo4_ativo  = None
campo5_ativo  = None
campo6_ativo  = None
campo7_ativo  = None
label_erro_crud  = None  # referência ao label de erro do CRUD atual
label_mensagem   = None  # referência ao label de mensagem de sucesso/info inline de forma fixa
painel_usado     = ""    # indica qual seção está aberta
chamar_acao      = ""    # indica qual ação está ativa
frame_zona_inputs = None # referência ao frame de campos


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


# ============= FUNÇÃO AUXILIAR: CONVERTE DATA DO BANCO PARA BR =============

def data_banco_para_br(data_banco):
    """Converte AAAA-MM-DD para DD/MM/AAAA para exibir nos campos."""
    try:
        partes = str(data_banco).strip().split("-")
        if len(partes) == 3:
            ano, mes, dia = partes
            return f"{dia}/{mes}/{ano}"
    except Exception:
        pass
    return str(data_banco)                                      # retorna original se não conseguir converter


# ============= FUNÇÃO DE MENSAGEM INLINE =============

def mostrar_mensagem_inline(mensagem, cor=VERDE_INSTITUCIONAL):
    """Exibe mensagem de resultado diretamente no painel, abaixo do formulário."""
    global label_mensagem
    if label_mensagem:
        if mensagem:
            label_mensagem.configure(text=mensagem, text_color=cor, fg_color=BRANCO, corner_radius=14)
        else:
            label_mensagem.configure(text="", fg_color="transparent")


# ============= FUNÇÕES DE CLIQUE PARA OS BOTÕES DE B.I. =============

def bi_faturamento_clicado():
    mostrar_mensagem_inline("A processar indicador de Ganhos: Carregando Faturamento Acumulado da carteira...", "lightblue")

def bi_seguradoras_clicado():
    mostrar_mensagem_inline("A processar indicador de Desempenho: Calculando Ranking de Vendas por Seguradora...", "lightblue")

def bi_renovacoes_clicado():
    mostrar_mensagem_inline("A processar indicador de Metas: Buscando apólices com término nos próximos 30 dias...", "lightblue")

def bi_clientes_clicado():
    mostrar_mensagem_inline("A processar indicador de Potencial: Analisando dados demográficos dos clientes ativos...", "lightblue")


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
    mostrar_mensagem_inline("")                                 # limpa mensagem de sucesso anterior

    # --- VALIDAÇÃO DE CAMPOS ---
    if chamar_acao == "Acrescentar":                            # todos os campos devem estar preenchidos ao inserir
        if (campo1_ativo and not v1) or (campo2_ativo and not v2) or \
           (campo3_ativo and not v3) or (campo4_ativo and not v4) or \
           (campo5_ativo and not v5) or (campo6_ativo and not v6) or \
           (campo7_ativo and not v7):
            label_erro_crud.configure(text="Preencha todos os campos do formulário para acrescentar!", text_color=VERMELHO_ERRO)
            return

    elif chamar_acao == "Atualizar":                            # apenas o identificador (campo 1) é estritamente obrigatório
        if not v1:
            label_erro_crud.configure(text="Preencha o campo identificador obrigatório para atualizar!", text_color=VERMELHO_ERRO)
            return

    elif chamar_acao == "Pesquisar":                            # pelo menos um campo deve ser preenchido
        if not v1 and not v2 and not v3 and not v4 and not v5:
            label_erro_crud.configure(text="Preencha pelo menos um campo para buscar!", text_color=VERMELHO_ERRO)
            return

    elif chamar_acao == "Remover":                              # campo 1 obrigatório para remover
        if not v1:
            label_erro_crud.configure(text="Informe o campo de identificação para localizar o registro.", text_color=VERMELHO_ERRO)
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
                label_erro_crud.configure(text="Erro ao salvar no banco. Verifique os dados.", text_color=VERMELHO_ERRO)
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
                    f"ID: {cliente['id_pessoa']}\n"
                    f"CPF/CNPJ: {cliente['cpf_cnpj']}\n"
                    f"Nome: {cliente['nome_completo']}\n"
                    f"Email: {cliente['email']}\n"
                    f"Sexo: {cliente['sexo']}\n"
                    f"Telefone: {cliente['telefone']}\n"
                    f"Nascimento: {data_banco_para_br(cliente['data_nascimento'])}\n"
                    f"Status: {cliente['status']}"
                )
            else:
                label_erro_crud.configure(text="Nenhum cliente localizado!", text_color="#e74c3c")
                return

        elif chamar_acao == "Atualizar":
            v6_banco = data_br_para_banco(v6) if v6 else ""     # converte data caso preenchida
            sucesso = crud.update_pessoa(v1, v2, v3, v4.upper(), v5, v6_banco, v7)
            if sucesso:
                mensagem_alerta = "Dados do cliente atualizados com sucesso!"
            else:
                label_erro_crud.configure(text="CPF/CNPJ não encontrado ou erro na atualização!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_pessoa(v1)
            if sucesso:
                mensagem_alerta = "Cliente removido com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao remover ou cliente não encontrado.", text_color=VERMELHO_ERRO)
                return


    # ====== CRUD DE SEGURADORAS ======

    elif painel_usado == "Seguradoras":

        if chamar_acao == "Acrescentar":
            sucesso = crud.create_seguradora(v1, v2, v3)        # nome_fantasia, cnpj, telefone_suporte
            if sucesso:
                mensagem_alerta = "Seguradora adicionada com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao salvar seguradora no banco.", text_color=VERMELHO_ERRO)
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
                label_erro_crud.configure(text="Nenhuma seguradora localizada!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_seguradora(v1, v2, v3, v4)
            if sucesso:
                mensagem_alerta = "Seguradora atualizada com sucesso!"
            else:
                label_erro_crud.configure(text="ID de seguradora não encontrado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_seguradora(v1)
            if sucesso:
                mensagem_alerta = "Seguradora removida com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhuma seguradora encontrada para remoção!", text_color=VERMELHO_ERRO)
                return


    # ====== CRUD DE PLANOS ======

    elif painel_usado == "Planos":

        if chamar_acao == "Acrescentar":
            sucesso = crud.create_plano(v1, v2, v3)             # id_seguradora, tipo_cobertura, nome_plano
            if sucesso:
                mensagem_alerta = "Plano cadastrado com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao salvar plano no banco.", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Pesquisar":
            plano = None
            if v1:
                plano = crud.read_plano_por_id(v1)
            elif v2:
                plano = crud.read_plano_por_nome(v2)

            if plano:
                mensagem_alerta = (
                    f"Plano localizado!\n\n"
                    f"ID Plano: {plano['id_plano']}\n"
                    f"ID Seguradora: {plano['id_seguradora']}\n"
                    f"Nome do Plano: {plano['nome_plano']}\n"
                    f"Tipo Cobertura: {plano['tipo_cobertura']}"
                )
            else:
                label_erro_crud.configure(text="Nenhum plano localizado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_plano(v1, v2, v3, v4)
            if sucesso:
                mensagem_alerta = "Plano atualizado com sucesso!"
            else:
                label_erro_crud.configure(text="ID de plano não encontrado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_plano(v1)
            if sucesso:
                mensagem_alerta = "Plano removido com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhum plano encontrado para remoção!", text_color=VERMELHO_ERRO)
                return


    # ====== CRUD DE BENS ======

    elif painel_usado == "Bens":

        if chamar_acao == "Acrescentar":
            sucesso = crud.create_bem(v1, v2, v3, v4)
            if sucesso:
                mensagem_alerta = "Bem adicionado com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao salvar bem no banco.", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Pesquisar":
            bem = crud.read_bem_por_id(v1)
            if bem:
                mensagem_alerta = (
                    f"Bem encontrado!\n\n"
                    f"ID Bem: {bem['id_bem']}\n"
                    f"Tipo do Bem: {bem['tipo_bem']}\n"
                    f"Descrição: {bem['descricao']}\n"
                    f"Valor Estimado: R$ {bem['valor_estimado']}"
                )
            else:
                label_erro_crud.configure(text="Nenhum bem localizado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_bem(v1, v2, v3, v4, v5)
            if sucesso:
                mensagem_alerta = "Bem atualizado com sucesso!"
            else:
                label_erro_crud.configure(text="ID do bem não encontrado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_bem(v1)
            if  sucesso:
                mensagem_alerta = "Bem removido com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhum bem encontrado para exclusão!", text_color=VERMELHO_ERRO)
                return


    # ====== CRUD DE APÓLICES ======

    elif painel_usado == "Apolices":

        if chamar_acao == "Acrescentar":
            sucesso = crud.create_apolice(v1, v2, v3, v4, v5)
            if sucesso:
                mensagem_alerta = "Apólice registrada com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao criar apólice. Verifique os dados.", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Pesquisar":
            apolice = crud.read_apolice_por_id(v1)
            if apolice:
                mensagem_alerta = (
                    f"Apólice encontrada!\n\n"
                    f"Nº Apólice: {apolice['id_apolice']}\n"
                    f"ID Bem: {apolice['id_bem']}\n"
                    f"ID Plano: {apolice['id_plano']}\n"
                    f"Franquia: R$ {apolice['valor_franquia']}\n"
                    f"Prêmio: R$ {apolice['valor_premio']}"
                )
            else:
                label_erro_crud.configure(text="Apólice não localizada!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_apolice(v1, v2, v3, v4, v5)
            if sucesso:
                mensagem_alerta = "Apólice modificada com sucesso!"
            else:
                label_erro_crud.configure(text="Nº de apólice não cadastrado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_apolice(v1)
            if sucesso:
                mensagem_alerta = "Apólice removida do sistema com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao deletar ou apólice não existente.", text_color=VERMELHO_ERRO)
                return


    # ====== CRUD DE VENDAS ======

    elif painel_usado == "Vendas":

        if chamar_acao == "Acrescentar":
            v4_banco = data_br_para_banco(v4)                   # data de vigência inicio
            v5_banco = data_br_para_banco(v5)                   # data de vigência fim
            sucesso = crud.create_venda(v1, v2, v3, v4_banco, v5_banco)
            if sucesso:
                mensagem_alerta = "Venda concluída com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao registrar venda.", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Pesquisar":
            venda = crud.read_venda_por_id(v1)
            if venda:
                mensagem_alerta = (
                    f"Registro de Venda Encontrado!\n\n"
                    f"ID Venda: {venda['id_venda']}\n"
                    f"Nº Apólice: {venda['id_apolice']}\n"
                    f"CPF Cliente: {venda['cpf_cnpj']}\n"
                    f"Vigência Início: {data_banco_para_br(venda['data_vigencia_inicio'])}\n"
                    f"Vigência Fim: {data_banco_para_br(venda['data_vigencia_fim'])}"
                )
            else:
                label_erro_crud.configure(text="ID de venda inexistente!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Atualizar":
            v4_banco = data_br_para_banco(v4) if v4 else ""
            v5_banco = data_br_para_banco(v5) if v5 else ""
            sucesso = crud.update_venda(v1, v2, v3, v4_banco, v5_banco)
            if sucesso:
                mensagem_alerta = "Informações da venda atualizadas!"
            else:
                label_erro_crud.configure(text="ID da venda não localizado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_venda(v1)
            if sucesso:
                mensagem_alerta = "Venda removida com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhum registro de venda correspondente para remover.", text_color=VERMELHO_ERRO)
                return

    # Exibe a mensagem de sucesso inline diretamente na tela sem pop-up externo
    mostrar_mensagem_inline(mensagem_alerta, VERDE_INSTITUCIONAL)


# ====== === CONSTRUÇÃO DINÂMICA DOS CAMPOS DO FORMULÁRIO    =========

def gerar_campos_formulario(acao, nome_secao):
    global campo1_ativo, campo2_ativo, campo3_ativo, campo4_ativo
    global campo5_ativo, campo6_ativo, campo7_ativo
    global painel_usado, chamar_acao, label_erro_crud
    
    painel_usado = nome_secao
    chamar_acao = acao

    for w in frame_zona_inputs.winfo_children():
        w.destroy()

    ctk.CTkLabel(
        frame_zona_inputs, 
        text=f"Formulário para: {acao} {nome_secao[:-1]}", 
        font=ctk.CTkFont(family=FONTE_PADRAO, size=15, weight="bold"), 
        text_color=VERDE_INSTITUCIONAL
    ).pack(pady=(0, 15))

    # Variáveis locais para configuração dinâmica das Labels e Placeholders
    lbl1, placeholder1, validador1 = None, None, None
    lbl2, placeholder2, validador2 = None, None, None
    lbl3, placeholder3, validador3 = None, None, None
    lbl4, placeholder4, validador4 = None, None, None
    lbl5, placeholder5, validador5 = None, None, None
    lbl6, placeholder6, validador6 = None, None, None
    lbl7, placeholder7, validador7 = None, None, None

    # Redefine referências globais de inputs
    campo1_ativo = campo2_ativo = campo3_ativo = campo4_ativo = None
    campo5_ativo = campo6_ativo = campo7_ativo = None


    if nome_secao == "Clientes":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "CPF / CNPJ:", "Filtrar por CPF (Somente Números)", validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo:", "Filtrar por Nome", None
            lbl5, placeholder5, validador5 = "Telefone:", "Filtrar por Telefone (DDD + Número)", validador_telefone
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "ID do Cliente:", "Digite o ID do cliente para remover", validador_cpf
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "CPF / CNPJ (Obrigatório):", "CPF do cliente que deseja alterar", validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo:", "Novo nome ou mantenha vazio", None
            lbl3, placeholder3, validador3 = "E-mail:", "Novo e-mail ou mantenha vazio", None
            lbl4, placeholder4, validador4 = "Sexo (M/F/O):", "Novo Sexo ou mantenha vazio", validador_sexo
            lbl5, placeholder5, validador5 = "Telefone:", "Novo telefone ou mantenha vazio", validador_telefone
            lbl6, placeholder6, validador6 = "Data de Nascimento:", "Nova Data (DD/MM/AAAA) ou mantenha vazio", None
            lbl7, placeholder7, validador7 = "Status (Ativo/Inativo):", "Novo status ou mantenha vazio", None
        else: # Acrescentar
            lbl1, placeholder1, validador1 = "CPF / CNPJ:", "Digite apenas números (11 dígitos)", validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo:", "Nome do cliente", None
            lbl3, placeholder3, validador3 = "E-mail:", "exemplo@dominio.com", None
            lbl4, placeholder4, validador4 = "Sexo (M/F/O):", "M para Masculino, F para Feminino, O para Outros", validador_sexo
            lbl5, placeholder5, validador5 = "Telefone:", "DDD + Número (Apenas números)", validador_telefone
            lbl6, placeholder6, validador6 = "Data de Nascimento:", "Formato DD/MM/AAAA", None
            lbl7, placeholder7, validador7 = "Status (Ativo/Inativo):", "Padrão: Ativo", None

    elif nome_secao == "Seguradoras":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Seguradora:", "Filtrar pelo Código ID", None
            lbl2, placeholder2, validador2 = "CNPJ:", "Filtrar pelo CNPJ", None
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "ID da Seguradora:", "Digite o ID da seguradora para remover", None
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "ID Seguradora (Obrigatório):", "ID para localizar a seguradora", None
            lbl2, placeholder2, validador2 = "Nome Fantasia:", "Novo Nome Fantasia ou mantenha vazio", None
            lbl3, placeholder3, validador3 = "CNPJ:", "Novo CNPJ ou mantenha vazio", None
            lbl4, placeholder4, validador4 = "Telefone Suporte:", "Novo telefone ou mantenha vazio", None
        else:
            lbl1, placeholder1, validador1 = "Nome Fantasia:", "Nome da seguradora", None
            lbl2, placeholder2, validador2 = "CNPJ:", "CNPJ da seguradora", None
            lbl3, placeholder3, validador3 = "Telefone Suporte:", "Telefone de suporte", None

    elif nome_secao == "Planos":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Plano:", "Filtrar pelo ID do plano", None
            lbl2, placeholder2, validador2 = "Nome Plano:", "Filtrar pelo nome do plano", None
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "ID Plano:", "Digite o ID do plano para remover", None
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "ID Plano (Obrigatório):", "ID para localizar o plano", None
            lbl2, placeholder2, validador2 = "ID Seguradora:", "Novo ID da seguradora ou mantenha vazio", None
            lbl3, placeholder3, validador3 = "Tipo Cobertura:", "Novo Tipo (Ex: Total, Parcial) ou mantenha vazio", None
            lbl4, placeholder4, validador4 = "Nome Plano:", "Novo nome do plano ou mantenha vazio", None
        else:
            lbl1, placeholder1, validador1 = "ID Seguradora:", "ID da seguradora vinculada", None
            lbl2, placeholder2, validador2 = "Tipo Cobertura:", "Ex: Total, Parcial", None
            lbl3, placeholder3, validador3 = "Nome Plano:", "Nome do plano", None

    elif nome_secao == "Bens":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Bem:", "Filtrar pelo ID do bem", None
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "ID do Bem:", "Digite o ID do bem para remover", None
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "ID Bem (Obrigatório):", "ID para localizar a bem", None
            lbl2, placeholder2, validador2 = "Tipo Bem:", "Novo tipo (Ex: Imóvel, Veículo) ou mantenha vazio", None
            lbl3, placeholder3, validador3 = "Descrição:", "Nova descrição ou mantenha vazio", None
            lbl4, placeholder4, validador4 = "Valor Estimado R$:", "Novo valor ou mantenha vazio", None
            lbl5, placeholder5, validador5 = "ID Proprietário (CPF):", "Novo CPF do proprietário ou mantenha vazio", validador_cpf
        else:
            lbl1, placeholder1, validador1 = "Tipo Bem:", "Ex: Imóvel, Veículo, Celular", None
            lbl2, placeholder2, validador2 = "Descrição:", "Detalhes do bem (Modelo, Placa, Endereço)", None
            lbl3, placeholder3, validador3 = "Valor Estimado R$:", "Ex: 50000.00", None
            lbl4, placeholder4, validador4 = "ID Proprietário (CPF):", "CPF do cliente cadastrado", validador_cpf

    elif nome_secao == "Apolices":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "Nº Apólice:", "Código identificador da apólice", validador_apolice
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "Nº Apólice:", "Digite o Nº da apólice para remover", validador_apolice
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "Nº Apólice (Obrigatório):", "Número da apólice que deseja alterar", validador_apolice
            lbl2, placeholder2, validador2 = "ID Bem:", "Novo ID do Bem ou mantenha vazio", None
            lbl3, placeholder3, validador3 = "ID Plano:", "Novo ID do Plano ou mantenha vazio", None
            lbl4, placeholder4, validador4 = "Valor Franquia R$:", "Novo valor de franquia ou mantenha vazio", None
            lbl5, placeholder5, validador5 = "Valor Prêmio R$:", "Novo valor de prêmio ou mantenha vazio", None
        else:
            lbl1, placeholder1, validador1 = "Nº Apólice:", "Código da apólice (Até 15 caracteres)", validador_apolice
            lbl2, placeholder2, validador2 = "ID Bem:", "ID do bem associado", None
            lbl3, placeholder3, validador3 = "ID Plano:", "ID do plano associado", None
            lbl4, placeholder4, validador4 = "Valor Franquia R$:", "Valor pago em caso de sinistro", None
            lbl5, placeholder5, validador5 = "Valor Prêmio R$:", "Custo total da apólice", None

    elif nome_secao == "Vendas":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Venda:", "Código de identificação da venda", validador_venda
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "ID Venda:", "Digite o ID da venda para excluir", validador_venda
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "ID Venda (Obrigatório):", "ID da venda que deseja alterar", validador_venda
            lbl2, placeholder2, validador2 = "Nº Apólice:", "Novo número da apólice ou mantenha vazio", validador_apolice
            lbl3, placeholder3, validador3 = "CPF do Cliente:", "Novo CPF do cliente ou mantenha vazio", validador_cpf
            lbl4, placeholder4, validador4 = "Vigência Início:", "Nova data de início (DD/MM/AAAA) ou mantenha vazio", None
            lbl5, placeholder5, validador5 = "Vigência Fim:", "Nova data de término (DD/MM/AAAA) ou mantenha vazio", None
        else:
            lbl1, placeholder1, validador1 = "ID Venda:", "Código da venda (Até 10 caracteres)", validador_venda
            lbl2, placeholder2, validador2 = "Nº Apólice:", "Número da apólice contratada", validador_apolice
            lbl3, placeholder3, validador3 = "CPF do Cliente:", "CPF do cliente comprador", validador_cpf
            lbl4, placeholder4, validador4 = "Vigência Início:", "Formato DD/MM/AAAA", None
            lbl5, placeholder5, validador5 = "Vigência Fim:", "Formato DD/MM/AAAA", None

    # Geração dos widgets com base nas definições dinâmicas acima
  
    if lbl1:
        ctk.CTkLabel(frame_zona_inputs, text=lbl1, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo1_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder1, width=380, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador1:
            campo1_ativo.configure(validate="key", validatecommand=(validador1, "%P"))
        campo1_ativo.pack(pady=(2, 8))

    if lbl2:
        ctk.CTkLabel(frame_zona_inputs, text=lbl2, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo2_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder2, width=380, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador2:
            campo2_ativo.configure(validate="key", validatecommand=(validador2, "%P"))
        campo2_ativo.pack(pady=(2, 8))

    if lbl3:
        ctk.CTkLabel(frame_zona_inputs, text=lbl3, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo3_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder3, width=380, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador3:
            campo3_ativo.configure(validate="key", validatecommand=(validador3, "%P"))
        campo3_ativo.pack(pady=(2, 8))

    if lbl4:
        ctk.CTkLabel(frame_zona_inputs, text=lbl4, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo4_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder4, width=380, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador4:
            campo4_ativo.configure(validate="key", validatecommand=(validador4, "%P"))
        campo4_ativo.pack(pady=(2, 8))

    if lbl5:
        ctk.CTkLabel(frame_zona_inputs, text=lbl5, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo5_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder5, width=380, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador5:
            campo5_ativo.configure(validate="key", validatecommand=(validador5, "%P"))
        campo5_ativo.pack(pady=(2, 8))

    if lbl6:
        ctk.CTkLabel(frame_zona_inputs, text=lbl6, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo6_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder6, width=380, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador6:
            campo6_ativo.configure(validate="key", validatecommand=(validador6, "%P"))
        campo6_ativo.pack(pady=(2, 8))

    if lbl7:
        ctk.CTkLabel(frame_zona_inputs, text=lbl7, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo7_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder7, width=380, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador7:
            campo7_ativo.configure(validate="key", validatecommand=(validador7, "%P"))
        campo7_ativo.pack(pady=(2, 8))

    # ---- Botão de confirmação ----
    ctk.CTkButton(
        frame_zona_inputs, 
        text=f"Confirmar {acao}", 
        fg_color=VERDE_INSTITUCIONAL, 
        hover_color=VERDE_ESCURO, 
        text_color=BRANCO,
        corner_radius=10,
        width=220, 
        height=40, 
        command=confirma_crud
    ).pack(pady=12)

    # Label para exibição de erros de validação localizados
    label_erro_crud = ctk.CTkLabel(
        frame_zona_inputs, 
        text="", 
        font=ctk.CTkFont(size=12, weight="bold"), 
        text_color=VERMELHO_ERRO
    )
    label_erro_crud.pack(pady=(0, 5))


# =====  ===== FUNÇÕES DE PONTE PARA OS BOTÕES DO CRUD 

def acao_acrescentar_clicada():
    gerar_campos_formulario("Acrescentar", secao_painel_aberto)

def acao_pesquisar_clicada():
    gerar_campos_formulario("Pesquisar", secao_painel_aberto)

def acao_atualizar_clicada():
    gerar_campos_formulario("Atualizar", secao_painel_aberto)

def acao_remover_clicada():
    gerar_campos_formulario("Remover", secao_painel_aberto)


# ====== ====== FUNÇÃO GERAL PARA MONTAR A ESTRUTURA DO PAINEL ====

frame_botoes_crud = None

def montar_estrutura_painel(nome):
    global frame_botoes_crud, frame_zona_inputs, label_erro_crud, label_mensagem

    for componente in frame_conteudo.winfo_children():
        componente.destroy()

    # +++++++++++ Criação do cabeçalho da seção ativa
    ctk.CTkLabel(
        frame_conteudo, 
        text=f"Painel de {nome}", 
        font=ctk.CTkFont(family=FONTE_TITULO, size=24, weight="bold"), text_color=CINZA_ESCURO
    ).pack(pady=(20, 15))

    # Sub-barra de ferramentas CRUD (Botões de ação superior internos)
    frame_botoes_crud = ctk.CTkFrame(frame_conteudo, fg_color=BRANCO, corner_radius=16, border_width=1, border_color=BORDA_SUAVE)
    frame_botoes_crud.pack(pady=10, padx=20)

    ctk.CTkButton(frame_botoes_crud, text="Acrescentar", width=125, height=36, corner_radius=10, fg_color=VERDE_INSTITUCIONAL, hover_color=VERDE_ESCURO, text_color=BRANCO, command=acao_acrescentar_clicada).pack(side="left", padx=7, pady=10)
    ctk.CTkButton(frame_botoes_crud, text="Pesquisar",   width=125, height=36, corner_radius=10, fg_color=CINZA_ESCURO, hover_color="#1A202C", text_color=BRANCO, command=acao_pesquisar_clicada).pack(side="left", padx=7, pady=10)
    ctk.CTkButton(frame_botoes_crud, text="Atualizar",   width=125, height=36, corner_radius=10, fg_color=DOURADO_PREMIUM, hover_color="#B8941F", text_color="#1A202C", command=acao_atualizar_clicada).pack(side="left", padx=7, pady=10)
    ctk.CTkButton(frame_botoes_crud, text="Remover",     width=125, height=36, corner_radius=10, fg_color=VERMELHO_ERRO, hover_color=VERMELHO_HOVER, text_color=BRANCO, command=acao_remover_clicada).pack(side="left", padx=7, pady=10)

    # Frame central com barra de rolagem onde o formulário é renderizado dinamicamente
    frame_zona_inputs = ctk.CTkScrollableFrame(frame_conteudo, fg_color=BRANCO, corner_radius=18, border_width=1, border_color=BORDA_SUAVE, width=520, height=350)
    frame_zona_inputs.pack(fill="both", expand=True, padx=28, pady=8)

    # LABEL FIXo: Onde as respostas e dados de sucesso são mostrados 
    label_mensagem = ctk.CTkLabel(
        frame_conteudo, 
        text="", 
        font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="normal"), 
        justify="left", 
        wraplength=700,
        text_color=CINZA_ESCURO,
        fg_color="transparent",
        corner_radius=14
    )
    label_mensagem.pack(pady=15, padx=28, fill="x")


# ======== SEÇÃO NOVA: VISUAL DO DASHBOARD B.I. ======

def mostrar_dashboard_bi():
    global label_mensagem
    
    # Limpa toda a tela central de trabalho
    for componente in frame_conteudo.winfo_children():
        componente.destroy()

    # Título principal do Dashboard de B. I.
    ctk.CTkLabel(
        frame_conteudo, 
        text=" CONSULTAS - B.I.", 
        font=ctk.CTkFont(size=22, weight="bold"),
        text_color="#2ecc71"
    ).pack(pady=(25, 10))

    ctk.CTkLabel(
        frame_conteudo, 
        text="Consultas Analíticas", 
        font=ctk.CTkFont(size=13),
        text_color="gray"
    ).pack(pady=(0, 20))

    # Frame organizador para alinhar os 4 botões lado a lado perfeitamente
    frame_grid_botoes = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_grid_botoes.pack(pady=15, padx=20, fill="x")

    # Criação dos 4 botões de indicadores de B.I.
    ctk.CTkButton(
        frame_grid_botoes, 
        text=" Faturamento", 
        width=140, 
        height=60, 
        fg_color="#27ae60", 
        hover_color="#2ecc71", 
        font=ctk.CTkFont(size=12, weight="bold"),
        command=bi_faturamento_clicado
    ).pack(side="left", padx=8, expand=True)

    ctk.CTkButton(
        frame_grid_botoes, 
        text="Seguradoras", 
        width=140, 
        height=60, 
        fg_color="#2980b9", 
        hover_color="#3498db", 
        font=ctk.CTkFont(size=12, weight="bold"),
        command=bi_seguradoras_clicado
    ).pack(side="left", padx=8, expand=True)

    ctk.CTkButton(
        frame_grid_botoes, 
        text="Renovações", 
        width=140, 
        height=60, 
        fg_color="#d35400", 
        hover_color="#e67e22", 
        font=ctk.CTkFont(size=12, weight="bold"),
        command=bi_renovacoes_clicado
    ).pack(side="left", padx=8, expand=True)

    ctk.CTkButton(
        frame_grid_botoes, 
        text="Clientes", 
        width=140, 
        height=60, 
        fg_color="#8e44ad", 
        hover_color="#9b59b6", 
        font=ctk.CTkFont(size=12, weight="bold"),
        command=bi_clientes_clicado
    ).pack(side="left", padx=8, expand=True)

    # Divisor visual  para separar os botões da área de resposta
    ctk.CTkFrame(frame_conteudo, height=2, fg_color="#2c3e50").pack(fill="x", padx=40, pady=25)

    # Espaço reservado fixo onde os dados das tabelas de agregação vão aparecer 
    label_mensagem = ctk.CTkLabel(
        frame_conteudo, 
        text="Selecione um indicador acima para exibir consulta", 
        font=ctk.CTkFont(size=14, weight="normal"), 
        justify="center", 
        wraplength=650,
        text_color="#bdc3c7"
    )
    label_mensagem.pack(pady=10, padx=20, fill="both", expand=True)


# ============= SEÇÕES DE CHAMADAS DO MENU LATERAL =============

secao_painel_aberto = ""

def mostrar_tela_clientes():
    global secao_painel_aberto
    secao_painel_aberto = "Clientes"
    montar_estrutura_painel("Clientes")
    gerar_campos_formulario("Pesquisar", "Clientes") # Abre na pesquisa por padrão

def mostrar_secao_seguradoras():
    global secao_painel_aberto
    secao_painel_aberto = "Seguradoras"
    montar_estrutura_painel("Seguradoras")
    gerar_campos_formulario("Pesquisar", "Seguradoras")

def mostrar_secao_planos():
    global secao_painel_aberto
    secao_painel_aberto = "Planos"
    montar_estrutura_painel("Planos")
    gerar_campos_formulario("Pesquisar", "Planos")

def mostrar_secao_bens():
    global secao_painel_aberto
    secao_painel_aberto = "Bens"
    montar_estrutura_painel("Bens")
    gerar_campos_formulario("Pesquisar", "Bens")

def mostrar_secao_apolices():
    global secao_painel_aberto
    secao_painel_aberto = "Apolices"
    montar_estrutura_painel("Apolices")
    gerar_campos_formulario("Pesquisar", "Apolices")

def mostrar_secao_vendas():
    global secao_painel_aberto
    secao_painel_aberto = "Vendas"
    montar_estrutura_painel("Vendas")
    gerar_campos_formulario("Pesquisar", "Vendas")


# ============= COMPONENTES DO MENU LATERAL (BOTÕES) =============

ctk.CTkButton(frame_lateral, text=" CLIENTES",    anchor="w", width=175, height=40, corner_radius=10, fg_color="transparent", hover_color=VERDE_INSTITUCIONAL, text_color=BRANCO, font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"), command=mostrar_tela_clientes).pack(pady=3, padx=14)
ctk.CTkButton(frame_lateral, text=" SEGURADORAS", anchor="w", width=175, height=40, corner_radius=10, fg_color="transparent", hover_color=VERDE_INSTITUCIONAL, text_color=BRANCO, font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"), command=mostrar_secao_seguradoras).pack(pady=3, padx=14)
ctk.CTkButton(frame_lateral, text=" PLANOS",      anchor="w", width=175, height=40, corner_radius=10, fg_color="transparent", hover_color=VERDE_INSTITUCIONAL, text_color=BRANCO, font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"), command=mostrar_secao_planos).pack(pady=3, padx=14)
ctk.CTkButton(frame_lateral, text=" BENS",        anchor="w", width=175, height=40, corner_radius=10, fg_color="transparent", hover_color=VERDE_INSTITUCIONAL, text_color=BRANCO, font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"), command=mostrar_secao_bens).pack(pady=3, padx=14)
ctk.CTkButton(frame_lateral, text=" APÓLICES",    anchor="w", width=175, height=40, corner_radius=10, fg_color="transparent", hover_color=VERDE_INSTITUCIONAL, text_color=BRANCO, font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"), command=mostrar_secao_apolices).pack(pady=3, padx=14)
ctk.CTkButton(frame_lateral, text=" VENDAS",      anchor="w", width=175, height=40, corner_radius=10, fg_color="transparent", hover_color=VERDE_INSTITUCIONAL, text_color=BRANCO, font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"), command=mostrar_secao_vendas).pack(pady=3, padx=14)

# ===== BOTÃO  B.I. NO MENU LATERAL
ctk.CTkButton(
    frame_lateral, 
    text="  DASHBOARD B.I.", 
    anchor="w", 
    width=160, 
    height=42, 
    fg_color="#024d0d", 
    hover_color="#17b978", 
    font=ctk.CTkFont(size=13, weight="bold"), 
    command=mostrar_dashboard_bi
).pack(pady=12, padx=10)

# Espaçador interno para empurrar o botão Sair para baixo
ctk.CTkLabel(frame_lateral, text="").pack(fill="both", expand=True)

ctk.CTkButton(frame_lateral, text=" LOGOUT / SAIR", anchor="w", width=160, height=38, fg_color=VERMELHO_ERRO, hover_color=VERMELHO_HOVER, text_color=BRANCO, font=ctk.CTkFont(size=13, weight="bold"), command=fechar_login).pack(pady=15, padx=10)


# Inicializa a execução da janela do Tkinter
janela.mainloop()