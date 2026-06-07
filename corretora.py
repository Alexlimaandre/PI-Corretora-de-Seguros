# corretora.py
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
janela.geometry("1020x720")                # largura levemente ajustada para as duas colunas
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
    frame_login.pack(pady=45, padx=90, fill="both", expand=True)
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
    """Exibe mensagem de resultado diretamente no painel fixo da direita."""
    global label_mensagem
    if label_mensagem:
        if mensagem:
            label_mensagem.configure(text=mensagem, text_color=cor)
        else:
            label_mensagem.configure(text="Aguardando ação ou busca...")


# ============= DASHBOARD B.I. - NOVA VERSÃO =============

# Variáveis globais usadas somente no painel de B.I.
cards_indicadores = {}
cards_descricoes = {}
campo_periodo_bi = None
campo_status_bi = None
frame_ranking_seguradoras = None
label_resumo_bi = None


def obter_numero_indicador(dados, chave, padrao=0):
    """Pega um número dentro de um dicionário de indicador com segurança."""
    try:
        if dados and chave in dados and dados[chave] is not None:
            return int(dados[chave])
    except Exception:
        pass
    return padrao


def converter_periodo_dias(texto):
    """Converte o campo de dias para inteiro. Se vier vazio ou inválido, retorna None."""
    try:
        texto = str(texto).strip()
        if texto == "":
            return None
        valor = int(texto)
        if valor <= 0:
            return None
        return valor
    except Exception:
        return None


def formatar_numero_indicador(valor):
    """Formata números inteiros para os cards do dashboard."""
    try:
        return f"{int(valor):,}".replace(",", ".")
    except Exception:
        return "0"


def calcular_taxa_conversao(convertidos, total):
    """Calcula taxa de conversão entre apólices e cotações."""
    try:
        if total == 0:
            return 0
        return round((convertidos / total) * 100, 1)
    except Exception:
        return 0


def criar_card_indicador(pai, chave, titulo, valor, descricao, cor_borda, linha, coluna):
    """Cria um card visual de indicador e guarda as labels para atualização dinâmica."""
    card = ctk.CTkFrame(
        pai,
        fg_color=BRANCO,
        corner_radius=18,
        border_width=1,
        border_color=cor_borda
    )
    card.grid(row=linha, column=coluna, padx=8, pady=8, sticky="nsew")

    ctk.CTkLabel(
        card,
        text=titulo,
        font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"),
        text_color=TEXTO_SECUNDARIO,
        anchor="w"
    ).pack(fill="x", padx=16, pady=(14, 2))

    lbl_valor = ctk.CTkLabel(
        card,
        text=valor,
        font=ctk.CTkFont(family=FONTE_TITULO, size=30, weight="bold"),
        text_color=CINZA_ESCURO,
        anchor="w"
    )
    lbl_valor.pack(fill="x", padx=16, pady=(0, 2))

    lbl_desc = ctk.CTkLabel(
        card,
        text=descricao,
        font=ctk.CTkFont(family=FONTE_PADRAO, size=11),
        text_color=TEXTO_SECUNDARIO,
        anchor="w",
        justify="left",
        wraplength=180
    )
    lbl_desc.pack(fill="x", padx=16, pady=(0, 14))

    cards_indicadores[chave] = lbl_valor
    cards_descricoes[chave] = lbl_desc


def atualizar_card_indicador(chave, valor, descricao=None):
    """Atualiza o valor e a descrição de um card já criado."""
    if chave in cards_indicadores:
        cards_indicadores[chave].configure(text=str(valor))
    if descricao is not None and chave in cards_descricoes:
        cards_descricoes[chave].configure(text=str(descricao))


def limpar_frame_dashboard(frame):
    """Remove todos os widgets de um frame."""
    if frame:
        for widget in frame.winfo_children():
            widget.destroy()


def atualizar_dashboard_bi():
    """Atualiza todos os indicadores usando as funções existentes no crud.py."""
    global frame_ranking_seguradoras, label_resumo_bi

    dias = converter_periodo_dias(campo_periodo_bi.get() if campo_periodo_bi else "")
    status = campo_status_bi.get().strip() if campo_status_bi else ""

    try:
        clientes = crud.qtd_cliente_por_status(status)
        cotacoes = crud.novas_cotacoes(dias)
        apolices_novas = crud.novas_apolices(dias)
        vencidas = crud.apolices_vencidas()
        vencendo = crud.apolices_vencendo(dias if dias else 30)
        ranking = crud.contrato_por_seguradora()

        total_clientes = obter_numero_indicador(clientes, "qtd_status")
        total_orcamentos = obter_numero_indicador(cotacoes, "qtd_orcamentos")
        total_novas_apolices = obter_numero_indicador(apolices_novas, "qtd_novas_apolices")
        total_apolices_vencidas = obter_numero_indicador(vencidas, "qtd_apolices_vencidas")
        total_apolices_vencendo = obter_numero_indicador(vencendo, "qtd_apolices_vencendo")
        taxa_conversao = calcular_taxa_conversao(total_novas_apolices, total_orcamentos)

        periodo_txt = f"Últimos {dias} dias" if dias else "Base completa"
        status_txt = status.capitalize()

        atualizar_card_indicador("clientes_ativos", formatar_numero_indicador(total_clientes), f"Clientes com status {status_txt}")
        atualizar_card_indicador("orcamentos", formatar_numero_indicador(total_orcamentos), f"Cotações no período: {periodo_txt}")
        atualizar_card_indicador("novas_apolices", formatar_numero_indicador(total_novas_apolices), f"Apólices geradas no período: {periodo_txt}")
        atualizar_card_indicador("apolices_vencidas", formatar_numero_indicador(total_apolices_vencidas), "Contratos que já passaram da vigência")
        atualizar_card_indicador("apolices_vencendo", formatar_numero_indicador(total_apolices_vencendo), f"Contratos vencendo em até {dias if dias else 30} dias")
        atualizar_card_indicador("taxa_conversao", f"{taxa_conversao}%", "Apólices geradas em relação às cotações")

        if label_resumo_bi:
            label_resumo_bi.configure(
                text=(
                    f"Análise rápida: no recorte selecionado, a corretora possui "
                    f"{formatar_numero_indicador(total_orcamentos)} cotação(ões), "
                    f"{formatar_numero_indicador(total_novas_apolices)} apólice(s) convertida(s) "
                    f"e taxa aproximada de conversão de {taxa_conversao}%."
                )
            )

        limpar_frame_dashboard(frame_ranking_seguradoras)

        ctk.CTkLabel(
            frame_ranking_seguradoras,
            text="Contratos por seguradora",
            font=ctk.CTkFont(family=FONTE_TITULO, size=18, weight="bold"),
            text_color=CINZA_ESCURO,
            anchor="w"
        ).pack(fill="x", padx=16, pady=(14, 4))

        ctk.CTkLabel(
            frame_ranking_seguradoras,
            text="Ranking baseado nas apólices vinculadas às cotações.",
            font=ctk.CTkFont(family=FONTE_PADRAO, size=12),
            text_color=TEXTO_SECUNDARIO,
            anchor="w"
        ).pack(fill="x", padx=16, pady=(0, 10))

        if ranking:
            maior = max([item.get("qtd_contratos", 0) for item in ranking]) or 1

            for posicao, item in enumerate(ranking[:8], 1):
                seguradora = item.get("seguradora", "Sem nome")
                qtd = item.get("qtd_contratos", 0)
                proporcao = qtd / maior

                linha = ctk.CTkFrame(frame_ranking_seguradoras, fg_color=BRANCO, corner_radius=12)
                linha.pack(fill="x", padx=14, pady=5)

                ctk.CTkLabel(
                    linha,
                    text=f"{posicao}º",
                    width=34,
                    font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"),
                    text_color=VERDE_INSTITUCIONAL
                ).pack(side="left", padx=(10, 4), pady=10)

                info = ctk.CTkFrame(linha, fg_color="transparent")
                info.pack(side="left", fill="x", expand=True, padx=4, pady=8)

                ctk.CTkLabel(
                    info,
                    text=seguradora,
                    font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"),
                    text_color=CINZA_ESCURO,
                    anchor="w"
                ).pack(fill="x")

                barra_fundo = ctk.CTkFrame(info, fg_color="#E2E8F0", height=7, corner_radius=10)
                barra_fundo.pack(fill="x", pady=(6, 0))
                barra_fundo.pack_propagate(False)

                barra = ctk.CTkFrame(barra_fundo, fg_color=VERDE_INSTITUCIONAL, height=7, corner_radius=10)
                barra.place(relx=0, rely=0, relwidth=proporcao, relheight=1)

                ctk.CTkLabel(
                    linha,
                    text=f"{qtd}",
                    width=42,
                    font=ctk.CTkFont(family=FONTE_TITULO, size=18, weight="bold"),
                    text_color=CINZA_ESCURO
                ).pack(side="right", padx=(4, 12), pady=10)
        else:
            ctk.CTkLabel(
                frame_ranking_seguradoras,
                text="Nenhuma seguradora com contrato encontrado.",
                font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
                text_color=TEXTO_SECUNDARIO
            ).pack(padx=16, pady=20)

    except Exception as erro:
        if label_resumo_bi:
            label_resumo_bi.configure(text=f"Erro ao carregar os indicadores: {erro}")


def mostrar_dashboard_bi():
    """Monta um dashboard B.I. completo usando as consultas criadas no crud.py."""
    global campo_periodo_bi, campo_status_bi, frame_ranking_seguradoras, label_resumo_bi
    global cards_indicadores, cards_descricoes

    cards_indicadores = {}
    cards_descricoes = {}

    for componente in frame_conteudo.winfo_children():
        componente.destroy()

    frame_conteudo.configure(fg_color=CINZA_CLARO)

    dashboard = ctk.CTkFrame(frame_conteudo, fg_color=CINZA_CLARO)
    dashboard.pack(fill="both", expand=True, padx=18, pady=14)

    # Cabeçalho
    header = ctk.CTkFrame(
        dashboard,
        fg_color=VERDE_ESCURO,
        corner_radius=22,
        border_width=1,
        border_color=VERDE_INSTITUCIONAL
    )
    header.pack(fill="x", pady=(0, 14))

    texto_header = ctk.CTkFrame(header, fg_color="transparent")
    texto_header.pack(side="left", fill="both", expand=True, padx=22, pady=16)

    ctk.CTkLabel(
        texto_header,
        text="Dashboard B.I.",
        font=ctk.CTkFont(family=FONTE_TITULO, size=28, weight="bold"),
        text_color=BRANCO,
        anchor="w"
    ).pack(fill="x")

    ctk.CTkLabel(
        texto_header,
        text="Indicadores gerenciais da Frank Costa Corretora de Seguros",
        font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
        text_color="#E6FFFA",
        anchor="w"
    ).pack(fill="x", pady=(4, 0))

    filtros = ctk.CTkFrame(header, fg_color="transparent")
    filtros.pack(side="right", padx=18, pady=14)

    ctk.CTkLabel(
        filtros,
        text="Período em dias",
        font=ctk.CTkFont(family=FONTE_PADRAO, size=11, weight="bold"),
        text_color="#C6F6D5"
    ).grid(row=0, column=0, sticky="w", padx=4)

    campo_periodo_bi = ctk.CTkEntry(
        filtros,
        width=95,
        height=34,
        corner_radius=10,
        placeholder_text="30",
        fg_color=BRANCO,
        text_color=CINZA_ESCURO,
        border_color=VERDE_CLARO
    )
    campo_periodo_bi.grid(row=1, column=0, padx=4, pady=(2, 0))
    campo_periodo_bi.insert(0, "30")

    ctk.CTkLabel(
        filtros,
        text="Status cliente",
        font=ctk.CTkFont(family=FONTE_PADRAO, size=11, weight="bold"),
        text_color="#C6F6D5"
    ).grid(row=0, column=1, sticky="w", padx=4)

    campo_status_bi = ctk.CTkEntry(
        filtros,
        width=110,
        height=34,
        corner_radius=10,
        placeholder_text="Ativo",
        fg_color=BRANCO,
        text_color=CINZA_ESCURO,
        border_color=VERDE_CLARO
    )
    campo_status_bi.grid(row=1, column=1, padx=4, pady=(2, 0))
    campo_status_bi.insert(0, "Ativo")

    ctk.CTkButton(
        filtros,
        text="Atualizar",
        width=92,
        height=34,
        corner_radius=10,
        fg_color=DOURADO_PREMIUM,
        hover_color="#B8941F",
        text_color="#1A202C",
        font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"),
        command=atualizar_dashboard_bi
    ).grid(row=1, column=2, padx=(8, 0), pady=(2, 0))

    # Corpo do dashboard
    corpo = ctk.CTkFrame(dashboard, fg_color="transparent")
    corpo.pack(fill="both", expand=True)

    esquerda = ctk.CTkFrame(corpo, fg_color="transparent")
    esquerda.pack(side="left", fill="both", expand=True, padx=(0, 12))

    direita = ctk.CTkFrame(
        corpo,
        fg_color="#EEF6F1",
        corner_radius=20,
        border_width=1,
        border_color=BORDA_SUAVE,
        width=330
    )
    direita.pack(side="right", fill="both", expand=False)
    direita.pack_propagate(False)

    # Cards principais
    cards = ctk.CTkFrame(esquerda, fg_color="transparent")
    cards.pack(fill="x")

    cards.grid_columnconfigure(0, weight=1)
    cards.grid_columnconfigure(1, weight=1)
    cards.grid_columnconfigure(2, weight=1)

    criar_card_indicador(cards, "clientes_ativos", "Clientes", "0", "Clientes com status ativo", VERDE_INSTITUCIONAL, 0, 0)
    criar_card_indicador(cards, "orcamentos", "Orçamentos", "0", "Cotações no período", "#3182CE", 0, 1)
    criar_card_indicador(cards, "novas_apolices", "Novas Apólices", "0", "Contratos gerados", DOURADO_PREMIUM, 0, 2)
    criar_card_indicador(cards, "apolices_vencidas", "Apólices Vencidas", "0", "Contratos fora da vigência", VERMELHO_ERRO, 1, 0)
    criar_card_indicador(cards, "apolices_vencendo", "Apólices Vencendo", "0", "Contratos próximos do fim", "#DD6B20", 1, 1)
    criar_card_indicador(cards, "taxa_conversao", "Conversão", "0%", "Apólices sobre cotações", VERDE_CLARO, 1, 2)

    # Painel de análise
    analise = ctk.CTkFrame(
        esquerda,
        fg_color=BRANCO,
        corner_radius=20,
        border_width=1,
        border_color=BORDA_SUAVE
    )
    analise.pack(fill="both", expand=True, pady=(12, 0))

    ctk.CTkLabel(
        analise,
        text="Leitura gerencial",
        font=ctk.CTkFont(family=FONTE_TITULO, size=18, weight="bold"),
        text_color=CINZA_ESCURO,
        anchor="w"
    ).pack(fill="x", padx=18, pady=(16, 4))

    label_resumo_bi = ctk.CTkLabel(
        analise,
        text="Clique em Atualizar para carregar a análise dos indicadores.",
        font=ctk.CTkFont(family=FONTE_PADRAO, size=13),
        text_color=TEXTO_SECUNDARIO,
        anchor="w",
        justify="left",
        wraplength=560
    )
    label_resumo_bi.pack(fill="x", padx=18, pady=(0, 12))

    ctk.CTkLabel(
        analise,
        text=(
            "Este painel reúne os principais dados operacionais: clientes ativos, "
            "orçamentos realizados, apólices convertidas, contratos vencidos, "
            "contratos próximos do vencimento e desempenho por seguradora."
        ),
        font=ctk.CTkFont(family=FONTE_PADRAO, size=12),
        text_color=TEXTO_SECUNDARIO,
        anchor="w",
        justify="left",
        wraplength=560
    ).pack(fill="x", padx=18, pady=(0, 16))

    # Ranking lateral
    frame_ranking_seguradoras = ctk.CTkScrollableFrame(
        direita,
        fg_color="transparent",
        corner_radius=18
    )
    frame_ranking_seguradoras.pack(fill="both", expand=True, padx=8, pady=8)

    atualizar_dashboard_bi()

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
                label_erro_crud.configure(text="Nenhum cliente localizado!", text_color=VERMELHO_ERRO)
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
                    f"Tipo Cobertura: {plano['cobertura']}"
                )
            else:
                label_erro_crud.configure(text="Nenhum plano localizado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_plano(v1, v2, v3, v4)
            if sucesso:
                mensagem_alerta = "Plano updated com sucesso!"
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
                    f"ID Pessoa: {bem['id_pessoa']}\n"
                    f"Tipo do Bem: {bem['tipo_bem']}\n"
                    f"Descrição: {bem['descricao_bem']}\n"
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
            if sucesso:
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
                    f"ID Cotação: {apolice['id_cotacao']}\n"
                    f"Cliente: {apolice['cliente']}\n"
                    f"Seguradora: {apolice['seguradora']}\n"
                    f"Plano: {apolice['plano']}\n"
                    f"Valor: R$ {apolice['valor']}\n"
                    f"Vigência: {data_banco_para_br(apolice['inicio'])} até {data_banco_para_br(apolice['fim'])}"
                )
            else:
                label_erro_crud.configure(text="Apólice não localizada!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_apolice(v1, v2, v3)
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


    # ====== CRUD DE VENDAS (Mapeado para Cotações no seu novo banco) ======

    elif painel_usado == "Vendas":

        if chamar_acao == "Acrescentar":
            sucesso = crud.create_cotacao(v1, v2, v3, v4, data_br_para_banco(v5))
            if sucesso:
                mensagem_alerta = "Cotação registrada com sucesso!"
            else:
                label_erro_crud.configure(text="Erro ao registrar cotação.", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Pesquisar":
            venda = crud.read_cotacao(v1)
            if venda:
                mensagem_alerta = (
                    f"Registro de Cotação Encontrado!\n\n"
                    f"ID Cotação: {venda['c.id_cotacao']}\n"
                    f"Cliente: {venda['p.nome_pessoa']}\n"
                    f"Seguradora: {venda['s.nome_fantasia']}\n"
                    f"Plano: {venda['plano']}\n"
                    f"Valor Cotação: R$ {venda['c.valor_cotacao']}\n"
                    f"Data: {data_banco_para_br(venda['c.data_cotacao'])}"
                )
            else:
                label_erro_crud.configure(text="ID de cotação inexistente!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Atualizar":
            sucesso = crud.update_cotacao(v1, v2, v3, v4, v5, v6)
            if sucesso:
                mensagem_alerta = "Informações da cotação atualizadas!"
            else:
                label_erro_crud.configure(text="ID da cotação não localizado!", text_color=VERMELHO_ERRO)
                return

        elif chamar_acao == "Remover":
            sucesso = crud.delete_cotacao(v1)
            if sucesso:
                mensagem_alerta = "Cotação removida com sucesso!"
            else:
                label_erro_crud.configure(text="Nenhum registro correspondente para remover.", text_color=VERMELHO_ERRO)
                return

    # Exibe a mensagem de sucesso inline diretamente na tela da direita (Fixado)
    mostrar_mensagem_inline(mensagem_alerta, BRANCO)


# ============= CONSTRUÇÃO DINÂMICA DOS CAMPOS DO FORMULÁRIO =============

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

    lbl1, placeholder1, validador1 = None, None, None
    lbl2, placeholder2, validador2 = None, None, None
    lbl3, placeholder3, validador3 = None, None, None
    lbl4, placeholder4, validador4 = None, None, None
    lbl5, placeholder5, validador5 = None, None, None
    lbl6, placeholder6, validador6 = None, None, None
    lbl7, placeholder7, validador7 = None, None, None

    campo1_ativo = campo2_ativo = campo3_ativo = campo4_ativo = None
    campo5_ativo = campo6_ativo = campo7_ativo = None


    if nome_secao == "Clientes":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "CPF / CNPJ:", "Filtrar por CPF (Somente Números)", validador_cpf
            lbl2, placeholder2, validador2 = "Nome Completo:", "Filtrar por Nome", None
            lbl5, placeholder5, validador5 = "Telefone:", "Filtrar por Telefone (DDD + Número)", validador_telefone
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "ID do Cliente:", "Digite o ID do cliente para remover", None
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
            lbl2, placeholder2, validador2 = "ID Proprietário:", "Novo proprietário ou mantenha vazio", validador_cpf
            lbl3, placeholder3, validador3 = "Tipo Bem:", "Novo tipo (Ex: Imóvel, Veículo) ou mantenha vazio", None
            lbl4, placeholder4, validador4 = "Descrição:", "Nova descrição ou mantenha vazio", None
            lbl5, placeholder5, validador5 = "Valor Estimado R$:", "Novo valor ou mantenha vazio", None
        else:
            lbl1, placeholder1, validador1 = "ID Proprietário (CPF):", "CPF do cliente cadastrado", validador_cpf
            lbl2, placeholder2, validador2 = "Tipo Bem:", "Ex: Imóvel, Veículo, Celular", None
            lbl3, placeholder3, validador3 = "Descrição:", "Detalhes do bem (Modelo, Placa, Endereço)", None
            lbl4, placeholder4, validador4 = "Valor Estimado R$:", "Ex: 50000.00", None

    elif nome_secao == "Apolices":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "Nº Apólice:", "Código identificador da apólice", validador_apolice
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "Nº Apólice:", "Digite o Nº da apólice para remover", validador_apolice
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "Nº Apólice (Obrigatório):", "Número da apólice que deseja alterar", validador_apolice
            lbl2, placeholder2, validador2 = "ID da Cotação R$:", "Novo id da cotação ou mantenha vazio", None
            lbl3, placeholder3, validador3 = "Data Inicio:", "Nova data de início ou mantenha vazio", None
            lbl4, placeholder4, validador4 = "Data Fim:", "Nova data de término ou mantenha vazio", None
            lbl5, placeholder5, validador5 = "Valor Franquia R$:", "Novo valor de franquia ou mantenha vazio", None
        else:
            lbl1, placeholder1, validador1 = "Nº da Cotação:", "Código da cotação (Até 15 caracteres)", validador_apolice
            lbl2, placeholder2, validador2 = "Data Inicio:", "Data de início da apólice", None
            lbl3, placeholder3, validador3 = "Data Fim:", "Data de término da apólice", None

    elif nome_secao == "Vendas":
        if acao == "Pesquisar":
            lbl1, placeholder1, validador1 = "ID Cotação:", "Código da cotação", None
        elif acao == "Remover":
            lbl1, placeholder1, validador1 = "ID Cotação:", "Digite o ID para excluir", None
        elif acao == "Atualizar":
            lbl1, placeholder1, validador1 = "ID Cotação (Obrigatório):", "ID da cotação", None
            lbl2, placeholder2, validador2 = "ID Pessoa:", "Novo ID numérico da pessoa", None
            lbl3, placeholder3, validador3 = "ID Seguradora:", "Novo ID da seguradora", None
            lbl4, placeholder4, validador4 = "ID Plano:", "Novo ID do plano", None
            lbl5, placeholder5, validador5 = "Valor R$:", "Novo valor da cotação", None
            lbl6, placeholder6, validador6 = "Data Cotação:", "Nova data (AAAA-MM-DD)", None
        else:
            lbl1, placeholder1, validador1 = "ID Pessoa:", "ID numérico do cliente", None
            lbl2, placeholder2, validador2 = "ID Seguradora:", "ID da seguradora parceira", None
            lbl3, placeholder3, validador3 = "ID Plano:", "ID do plano selecionado", None
            lbl4, placeholder4, validador4 = "Valor R$:", "Ex: 1500.00", None
            lbl5, placeholder5, validador5 = "Data Cotação:", "Formato DD/MM/AAAA", None

    if lbl1:
        ctk.CTkLabel(frame_zona_inputs, text=lbl1, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo1_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder1, width=330, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador1:
            campo1_ativo.configure(validate="key", validatecommand=(validador1, "%P"))
        campo1_ativo.pack(pady=(2, 8))

    if lbl2:
        ctk.CTkLabel(frame_zona_inputs, text=lbl2, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo2_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder2, width=330, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador2:
            campo2_ativo.configure(validate="key", validatecommand=(validador2, "%P"))
        campo2_ativo.pack(pady=(2, 8))

    if lbl3:
        ctk.CTkLabel(frame_zona_inputs, text=lbl3, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo3_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder3, width=330, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador3:
            campo3_ativo.configure(validate="key", validatecommand=(validador3, "%P"))
        campo3_ativo.pack(pady=(2, 8))

    if lbl4:
        ctk.CTkLabel(frame_zona_inputs, text=lbl4, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo4_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder4, width=330, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador4:
            campo4_ativo.configure(validate="key", validatecommand=(validador4, "%P"))
        campo4_ativo.pack(pady=(2, 8))

    if lbl5:
        ctk.CTkLabel(frame_zona_inputs, text=lbl5, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo5_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder5, width=330, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador5:
            campo5_ativo.configure(validate="key", validatecommand=(validador5, "%P"))
        campo5_ativo.pack(pady=(2, 8))

    if lbl6:
        ctk.CTkLabel(frame_zona_inputs, text=lbl6, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo6_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder6, width=330, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
        if validador6:
            campo6_ativo.configure(validate="key", validatecommand=(validador6, "%P"))
        campo6_ativo.pack(pady=(2, 8))

    if lbl7:
        ctk.CTkLabel(frame_zona_inputs, text=lbl7, font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="bold"), text_color=CINZA_ESCURO, anchor="center").pack(pady=(8, 0))
        campo7_ativo = ctk.CTkEntry(frame_zona_inputs, placeholder_text=placeholder7, width=330, height=40, corner_radius=10, border_color=BORDA_SUAVE, fg_color=BRANCO, text_color=CINZA_ESCURO)
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


# ===== ===== FUNÇÕES DE PONTE PARA OS BOTÕES DO CRUD 

def acao_acrescentar_clicada():
    gerar_campos_formulario("Acrescentar", secao_painel_aberto)

def acao_pesquisar_clicada():
    gerar_campos_formulario("Pesquisar", secao_painel_aberto)

def acao_atualizar_clicada():
    gerar_campos_formulario("Atualizar", secao_painel_aberto)

def acao_remover_clicada():
    gerar_campos_formulario("Remover", secao_painel_aberto)


# ====== ====== FUNÇÃO GERAL PARA MONTAR A ESTRUTURA DO PAINEL LADO A LADO ====

frame_botoes_crud = None

def montar_estrutura_painel(nome):
    global frame_botoes_crud, frame_zona_inputs, label_erro_crud, label_mensagem

    frame_conteudo.configure(fg_color=CINZA_CLARO)

    for componente in frame_conteudo.winfo_children():
        componente.destroy()

    # Cabeçalho da seção ativa
    ctk.CTkLabel(
        frame_conteudo, 
        text=f"Painel de {nome}", 
        font=ctk.CTkFont(family=FONTE_TITULO, size=24, weight="bold"), text_color=CINZA_ESCURO
    ).pack(pady=(15, 10))

    # Frame organizador da divisão em duas colunas (Esquerda e Direita)
    frame_divisao = ctk.CTkFrame(frame_conteudo, fg_color="transparent")
    frame_divisao.pack(fill="both", expand=True, padx=15, pady=5)

    # ---------------- COLUNA ESQUERDA (Barra CRUD + Formulário) ----------------
    frame_esquerda = ctk.CTkFrame(frame_divisao, fg_color="transparent")
    frame_esquerda.pack(side="left", fill="both", expand=True, padx=(0, 10))

    # Sub-barra de ferramentas CRUD interna na esquerda
    frame_botoes_crud = ctk.CTkFrame(frame_esquerda, fg_color=BRANCO, corner_radius=16, border_width=1, border_color=BORDA_SUAVE)
    frame_botoes_crud.pack(pady=5)

    ctk.CTkButton(frame_botoes_crud, text="Acrescentar", width=100, height=34, corner_radius=8, fg_color=VERDE_INSTITUCIONAL, hover_color=VERDE_ESCURO, text_color=BRANCO, command=acao_acrescentar_clicada).pack(side="left", padx=5, pady=6)
    ctk.CTkButton(frame_botoes_crud, text="Pesquisar",   width=100, height=34, corner_radius=8, fg_color=CINZA_ESCURO, hover_color="#1A202C", text_color=BRANCO, command=acao_pesquisar_clicada).pack(side="left", padx=5, pady=6)
    ctk.CTkButton(frame_botoes_crud, text="Atualizar",   width=100, height=34, corner_radius=8, fg_color=DOURADO_PREMIUM, hover_color="#B8941F", text_color="#1A202C", command=acao_atualizar_clicada).pack(side="left", padx=5, pady=6)
    ctk.CTkButton(frame_botoes_crud, text="Remover",     width=100, height=34, corner_radius=8, fg_color=VERMELHO_ERRO, hover_color=VERMELHO_HOVER, text_color=BRANCO, command=acao_remover_clicada).pack(side="left", padx=5, pady=6)

    # Frame central com barra de rolagem onde o formulário é renderizado
    frame_zona_inputs = ctk.CTkScrollableFrame(frame_esquerda, fg_color=BRANCO, corner_radius=18, border_width=1, border_color=BORDA_SUAVE, width=380, height=380)
    frame_zona_inputs.pack(fill="both", expand=True, pady=5)

    # ---------------- COLUNA DIREITA (Visualizador Fixo de Respostas) ----------------
    frame_direita = ctk.CTkScrollableFrame(frame_divisao, fg_color=VERDE_INSTITUCIONAL, width=300, height=400, corner_radius=16, border_width=1, border_color=BORDA_SUAVE)
    frame_direita.pack(side="right", fill="both", expand=False, padx=(5, 0))

    ctk.CTkLabel(
        frame_direita, 
        text="CONSULTA", 
        font=ctk.CTkFont(family=FONTE_PADRAO, size=16, weight="bold"),  
        text_color=BRANCO
    ).pack(pady=(12, 12))

    # O label fixo agora fica dentro da janela da direita com rolagem automática se o texto for enorme
    label_mensagem = ctk.CTkLabel(
        frame_direita, 
        text="Aguardando ação ou busca...", 
        font=ctk.CTkFont(family=FONTE_PADRAO, size=12, weight="normal"), 
        justify="left", 
        wraplength=310,
        text_color=BRANCO
    )
    label_mensagem.pack(pady=5, padx=12, fill="both", expand=True)




# =========+==== SEÇÕES DE CHAMADAS DO MENU LATERAL ++

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


# =====+======= COMPONENTES DOS BOTÕES MENU LATERAL  

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
    width=175, 
    height=42, 
    corner_radius=10,
    fg_color=DOURADO_PREMIUM, 
    hover_color="#B8941F", 
    text_color="#1A202C",
    font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"), 
    command=mostrar_dashboard_bi
).pack(pady=12, padx=14)

# Espaçador interno para empurrar o botão Sair para baixo
ctk.CTkLabel(frame_lateral, text="").pack(fill="both", expand=True)

ctk.CTkButton(frame_lateral, text=" LOGOUT/SAIR", anchor="w", width=175, height=40, corner_radius=10, fg_color=VERMELHO_ERRO, hover_color=VERMELHO_HOVER, text_color=BRANCO, font=ctk.CTkFont(family=FONTE_PADRAO, size=13, weight="bold"), command=fechar_login).pack(pady=15, padx=14)


# Inicializa a execução da janela do Tkinter
janela.mainloop()