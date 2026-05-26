# crud.py
# Arquivo com todas as funções de acesso ao banco de dados.
# Cada função faz UMA operação: criar, ler, atualizar ou deletar.

from conn import conexao  # importa a função que abre a conexão

# Abre a conexão UMA VEZ só quando o arquivo é carregado.
# O cursor fica aberto para todas as funções usarem.
# Quando integrar com interface, NÃO feche aqui — deixe aberto.
conn   = conexao()
cursor = conn.cursor()


# ========================================= #
#                  CREATE                   #
# ========================================= #

def create_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
    # Insere um novo cliente na tabela pessoa
    try:
        cursor.execute(
            """INSERT INTO pessoa 
               (cpf_cnpj, nome_completo, email, sexo, telefone, data_nascimento, status) 
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (cpf, nome, email, sexo, telefone, data_nasc, status)
        )
        conn.commit()   # salva a operação no banco
        print("Pessoa criada com sucesso!")
        return True     # retorna True para a interface saber que deu certo

    except Exception as e:
        conn.rollback() # desfaz qualquer alteração parcial se der erro
        print("Erro ao criar pessoa:", e)
        return False    # retorna False para a interface mostrar erro


def create_apolice(id_cotacao, inicio, fim):
    # Insere uma nova apólice vinculada a uma cotação
    try:
        cursor.execute(
            """INSERT INTO apolice (id_cotacao, inicio, fim) 
               VALUES (%s, %s, %s)""",
            (id_cotacao, inicio, fim)
        )
        conn.commit()
        print("Apólice criada com sucesso!")
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao criar apólice:", e)
        return False


def create_cotacao(id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao):
    # Insere uma nova cotação no banco
    try:
        cursor.execute(
            """INSERT INTO cotacoes 
               (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao) 
               VALUES (%s, %s, %s, %s, %s)""",
            (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao)
        )
        conn.commit()
        print("Cotação criada com sucesso!")
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao criar cotação:", e)
        return False


# ========================================= #
#                   READ                    #
# ========================================= #

def read_pessoa_por_cpf(cpf):
    # Busca um cliente pelo CPF e retorna um dicionário com os dados
    # Retorna None se não encontrar
    try:
        cursor.execute(
            "SELECT cpf_cnpj, nome_completo, email, sexo, telefone, data_nascimento, status FROM pessoa WHERE cpf_cnpj = %s",
            (cpf,)
        )
        resultado = cursor.fetchone()  # pega apenas a primeira linha encontrada

        if resultado is None:
            return None  # cliente não existe

        # Converte a tupla retornada pelo banco em dicionário
        # O banco retorna: (cpf, nome, email, sexo, tel, nasc, status)
        cliente = {
            "cpf_cnpj":        resultado[0],
            "nome_completo":   resultado[1],
            "email":           resultado[2],
            "sexo":            resultado[3],
            "telefone":        resultado[4],
            "data_nascimento": str(resultado[5]),  # converte data para texto
            "status":          resultado[6]
        }
        return cliente

    except Exception as e:
        print("Erro ao buscar pessoa:", e)
        return None


def read_pessoa_por_nome(nome):
    # Busca cliente pelo nome (busca parcial com ILIKE)
    try:
        cursor.execute(
            "SELECT cpf_cnpj, nome_completo, email, sexo, telefone, data_nascimento, status FROM pessoa WHERE LOWER(nome_completo) = LOWER(%s)",
            (nome,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        cliente = {
            "cpf_cnpj":        resultado[0],
            "nome_completo":   resultado[1],
            "email":           resultado[2],
            "sexo":            resultado[3],
            "telefone":        resultado[4],
            "data_nascimento": str(resultado[5]),
            "status":          resultado[6]
        }
        return cliente

    except Exception as e:
        print("Erro ao buscar pessoa por nome:", e)
        return None


def read_pessoa_por_telefone(telefone):
    # Busca cliente pelo telefone
    try:
        cursor.execute(
            "SELECT cpf_cnpj, nome_completo, email, sexo, telefone, data_nascimento, status FROM pessoa WHERE telefone = %s",
            (telefone,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        cliente = {
            "cpf_cnpj":        resultado[0],
            "nome_completo":   resultado[1],
            "email":           resultado[2],
            "sexo":            resultado[3],
            "telefone":        resultado[4],
            "data_nascimento": str(resultado[5]),
            "status":          resultado[6]
        }
        return cliente

    except Exception as e:
        print("Erro ao buscar pessoa por telefone:", e)
        return None


def read_apolice(id_apolice):
    # Busca uma apólice pelo ID e retorna dicionário ou None
    try:
        cursor.execute(
            "SELECT id_apolice, id_cotacao, inicio, fim FROM apolice WHERE id_apolice = %s",
            (id_apolice,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        apolice = {
            "id_apolice": resultado[0],
            "id_cotacao": resultado[1],
            "inicio":     str(resultado[2]),
            "fim":        str(resultado[3])
        }
        return apolice

    except Exception as e:
        print("Erro ao buscar apólice:", e)
        return None


def read_cotacao(id_cotacao):
    # Busca uma cotação pelo ID e retorna dicionário ou None
    try:
        cursor.execute(
            "SELECT id_cotacao, id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao FROM cotacoes WHERE id_cotacao = %s",
            (id_cotacao,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        venda = {
            "id_cotacao":    resultado[0],
            "id_pessoa":     resultado[1],
            "id_seguradora": resultado[2],
            "id_plano":      resultado[3],
            "valor_cotacao": str(resultado[4]),
            "data_cotacao":  str(resultado[5])
        }
        return venda

    except Exception as e:
        print("Erro ao buscar cotação:", e)
        return None


# ========================================= #
#                  UPDATE                   #
# ========================================= #

def update_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
    # Atualiza os dados de um cliente pelo CPF
    # Retorna True se encontrou e atualizou, False se o CPF não existe
    try:
        cursor.execute(
            """UPDATE pessoa 
               SET nome_completo=%s, email=%s, sexo=%s, 
                   telefone=%s, data_nascimento=%s, status=%s
               WHERE cpf_cnpj = %s""",
            (nome, email, sexo, telefone, data_nasc, status, cpf)
        )
        conn.commit()

        # cursor.rowcount diz quantas linhas foram afetadas
        # se for 0, significa que o CPF não foi encontrado
        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar pessoa:", e)
        return False


def update_apolice(id_apolice, inicio, fim):
    # Atualiza as datas de vigência de uma apólice
    try:
        cursor.execute(
            "UPDATE apolice SET inicio=%s, fim=%s WHERE id_apolice = %s",
            (inicio, fim, id_apolice)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar apólice:", e)
        return False


def update_cotacao(id_cotacao, id_pessoa, id_seguradora, id_plano, valor, data):
    # Atualiza os dados de uma cotação pelo ID
    try:
        cursor.execute(
            """UPDATE cotacoes 
               SET id_pessoa=%s, id_seguradora=%s, id_plano=%s, 
                   valor_cotacao=%s, data_cotacao=%s
               WHERE id_cotacao = %s""",
            (id_pessoa, id_seguradora, id_plano, valor, data, id_cotacao)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar cotação:", e)
        return False


# ========================================= #
#                  DELETE                   #
# ========================================= #

def delete_pessoa(cpf):
    # Remove um cliente da tabela pelo CPF
    # Retorna True se removeu, False se não encontrou
    try:
        cursor.execute(
            "DELETE FROM pessoa WHERE cpf_cnpj = %s",
            (cpf,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao deletar pessoa:", e)
        return False


def delete_apolice(id_apolice):
    # Remove uma apólice pelo ID
    try:
        cursor.execute(
            "DELETE FROM apolice WHERE id_apolice = %s",
            (id_apolice,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao deletar apólice:", e)
        return False


def delete_cotacao(id_cotacao):
    # Remove uma cotação pelo ID
    try:
        cursor.execute(
            "DELETE FROM cotacoes WHERE id_cotacao = %s",
            (id_cotacao,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao deletar cotação:", e)
        return False