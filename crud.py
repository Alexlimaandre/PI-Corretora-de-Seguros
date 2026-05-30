# crud.py
# Arquivo com todas as funções de acesso ao banco de dados.
# Cada função faz UMA operação: criar, ler, atualizar ou deletar.

from conn import conexao    # importa a função que abre a conexão

conn   = conexao()                 # abre a conexão com o banco 
cursor = conn.cursor()             # cria um cursor para executar comandos SQL



#                  CREATE                   #


def create_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
    # Insere um novo cliente na tabela pessoa
    try:
        cursor.execute(
            """INSERT INTO pessoa
               (cpf_cnpj, nome_completo, email, sexo, telefone, data_nascimento, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s)""",
            (cpf, nome, email, sexo, telefone, data_nasc, status)
        )
        conn.commit()       # salva no banco — sem isso o dado NÃO é gravado
        print("Pessoa criada com sucesso!")
        return True         # avisa a interface que deu certo

    except Exception as e:
        conn.rollback()     # cancela qualquer alteração parcial se der erro
        print("Erro ao criar pessoa:", e)
        return False        # avisa a interface que deu errado


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


#                   READ                    #


def read_todas_pessoas():
    # Retorna uma lista de dicionários com todos os clientes do banco
    try:
        cursor.execute("SELECT * FROM pessoa")
        resultados = cursor.fetchall()  # pega todas as linhas retornadas
        for i in resultados:
            print(i, end="\n\n")  # imprime cada cliente com uma linha em branco entre eles

    except Exception as e:
        print("Erro ao buscar todas as pessoas:", e)
        return []  # retorna lista vazia se der erro

def read_pessoa_por_cpf(cpf):
    # Busca cliente pelo CPF — retorna dicionário ou None se não encontrar
    try:
        cursor.execute(
            """SELECT cpf_cnpj, nome_completo, email, sexo,
                      telefone, data_nascimento, status
               FROM pessoa WHERE cpf_cnpj = %s""",
            (str(cpf),)
        )
        resultado = cursor.fetchone()   # pega a primeira linha encontrada

        if resultado is None:
            return None                 # cliente não existe no banco

        # O banco retorna uma tupla — convertemos para dicionário
        # para facilitar o uso na interface (cliente['nome_completo'] etc)
        cliente = {
            "cpf_cnpj":        resultado[0],
            "nome_completo":   resultado[1],
            "email":           resultado[2],
            "sexo":            resultado[3],
            "telefone":        resultado[4],
            "data_nascimento": str(resultado[5]),   # converte data para texto
            "status":          resultado[6]
        }
        return cliente

    except Exception as e:
        print("Erro ao buscar pessoa por CPF:", e)
        return None


def read_pessoa_por_nome(nome):
    # Busca cliente pelo nome completo (sem diferenciar maiúsculas/minúsculas)
    try:
        cursor.execute(
            """SELECT cpf_cnpj, nome_completo, email, sexo,
                      telefone, data_nascimento, status
               FROM pessoa WHERE LOWER(nome_completo) = LOWER(%s)""",
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
    # Busca cliente pelo número de telefone
    try:
        cursor.execute(
            """SELECT cpf_cnpj, nome_completo, email, sexo,
                      telefone, data_nascimento, status
               FROM pessoa WHERE telefone = %s""",
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
    # Busca apólice pelo ID — retorna dicionário ou None
    try:
        cursor.execute(
            """SELECT id_apolice, id_cotacao, inicio, fim
               FROM apolice WHERE id_apolice = %s""",
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


def read_apolice_por_cotacao(id_cotacao):
    # Busca apólice pelo ID da cotação vinculada
    try:
        cursor.execute(
            """SELECT id_apolice, id_cotacao, inicio, fim
               FROM apolice WHERE id_cotacao = %s""",
            (id_cotacao,)
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
        print("Erro ao buscar apólice por cotação:", e)
        return None


def read_cotacao(id_cotacao):
    # Busca cotação pelo ID — retorna dicionário ou None
    try:
        cursor.execute(
            """SELECT id_cotacao, id_pessoa, id_seguradora,
                      id_plano, valor_cotacao, data_cotacao
               FROM cotacoes WHERE id_cotacao = %s""",
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


def read_cotacao_por_pessoa(id_pessoa):
    # Busca cotação pelo ID da pessoa vinculada
    try:
        cursor.execute(
            """SELECT id_cotacao, id_pessoa, id_seguradora,
                      id_plano, valor_cotacao, data_cotacao
               FROM cotacoes WHERE id_pessoa = %s""",
            (id_pessoa,)
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
        print("Erro ao buscar cotação por pessoa:", e)
        return None


#                  UPDATE                   #


def update_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
    # Atualiza os dados do cliente pelo CPF
    # cursor.rowcount indica quantas linhas foram afetadas
    # se for 0, o CPF não foi encontrado no banco
    try:
        cursor.execute(
            """UPDATE pessoa
               SET nome_completo=%s, email=%s, sexo=%s,
                   telefone=%s, data_nascimento=%s, status=%s
               WHERE cpf_cnpj = %s""",
            (nome, email, sexo, telefone, data_nasc, status, str(cpf))
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False    # CPF não existe no banco
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar pessoa:", e)
        return False


def update_apolice(id_apolice, inicio, fim):
    # Atualiza as datas de início e fim de uma apólice pelo ID
    try:
        cursor.execute(
            """UPDATE apolice SET inicio=%s, fim=%s
               WHERE id_apolice = %s""",
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

 #
#                  DELETE                   #


def delete_pessoa(cpf):
    # Remove um cliente pelo CPF
    # Retorna True se removeu, False se o CPF não existia
    try:
        cursor.execute(
            "DELETE FROM pessoa WHERE cpf_cnpj = %s",
            (str(cpf),)
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
    



# ============= TESTE  =============

# read_todas_pessoas()


# ===== TESTE — apague depois =====
#cursor.execute("SELECT id_pessoa, nome_completo FROM pessoa")
#print("PESSOAS:", cursor.fetchall())

#cursor.execute("SELECT id_seguradora, nome_fantasia FROM seguradora")
#print("SEGURADORAS:", cursor.fetchall())

#cursor.execute("SELECT id_plano, nome_plano FROM plano")
#print("PLANOS:", cursor.fetchall())
  
