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
    
def create_seguradora(nome, cnpj, telefone):
    # Insere uma nova seguradora no banco
    try:
        cursor.execute(
            """INSERT INTO seguradora (nome_fantasia, cnpj, telefone_suporte)
               VALUES (%s, %s, %s)""",
            (nome, cnpj, telefone)
        )
        conn.commit()
        print("Seguradora criada com sucesso!")
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao criar seguradora:", e)
        return False
    
def create_plano(id_seguradora, tipo_cobertura, nome_plano):
    try:
        cursor.execute(
            """INSERT INTO plano (id_seguradora, tipo_cobertura ,nome_plano)
               VALUES (%s, %s, %s)""",
            (id_seguradora, tipo_cobertura, nome_plano)
        )
        conn.commit()
        print("Plano criado com sucesso!")
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao criar plano:", e)
        return False
    
def create_bem(id_pessoa, tipo_bem, descricao_bem, valor_estimado):
    try:
        cursor.execute(
            """INSERT INTO bem (id_pessoa, tipo_bem, descricao_bem, valor_estimado)
               VALUES (%s, %s, %s, %s)""",
            (id_pessoa, tipo_bem, descricao_bem, valor_estimado)
        )
        conn.commit()
        print("Bem criado com sucesso!")
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao criar bem:", e)
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
        conn.rollback()
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
        conn.rollback()
        print("Erro ao buscar pessoa por CPF:", e)
        return None

def read_pessoa_por_nome(nome):
    # Busca cliente pelo nome completo (sem diferenciar maiúsculas/minúsculas)
    try:
        cursor.execute(
            """
            SELECT 
                id_pessoa,
                cpf_cnpj,
                nome_completo, 
                email,
                sexo,
                telefone,
                data_nascimento,
                status
            FROM pessoa 
            WHERE nome_completo ILIKE %s
            ORDER BY id_pessoa
            LIMIT 1;"""
            ,
            (f"%{nome}%",)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        cliente = {
            "id_pessoa":      resultado[0],
            "cpf_cnpj":        resultado[1],
            "nome_completo":   resultado[2],
            "email":           resultado[3],
            "sexo":            resultado[4],
            "telefone":        resultado[5],
            "data_nascimento": str(resultado[6]),
            "status":          resultado[7]
        }
        return cliente

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar pessoa por nome:", e)
        return None

def read_pessoa_por_telefone(telefone):
    # Busca cliente pelo número de telefone
    try:
        cursor.execute(
            """
            SELECT 
                id_pessoa,
                cpf_cnpj,
                nome_completo, 
                email,
                sexo,
                telefone,
                data_nascimento,
                status
            FROM pessoa 
            WHERE telefone = %s;"""
            ,
            (telefone,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        cliente = {
            "id_pessoa":      resultado[0],
            "cpf_cnpj":        resultado[1],
            "nome_completo":   resultado[2],
            "email":           resultado[3],
            "sexo":            resultado[4],
            "telefone":        resultado[5],
            "data_nascimento": str(resultado[6]),
            "status":          resultado[7]
        }
        return cliente

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar pessoa por telefone:", e)
        return None

def read_apolice(id_apolice):
    # Busca apólice pelo ID — retorna dicionário ou None
    try:
        cursor.execute(
            """SELECT 
                    a.id_apolice as id_apolice,
                    a.id_cotacao as id_cotacao,
                    p.nome_completo AS cliente,
                    s.nome_fantasia AS seguradora,
                    pl.nome_plano AS plano,
                    c.valor_cotacao AS valor,
                    a.inicio,
                    a.fim
                FROM apolice a
                JOIN cotacoes c 
                    USING(id_cotacao)
                JOIN pessoa p 
                    USING(id_pessoa)
                JOIN seguradora s 
                    USING(id_seguradora)
                JOIN plano pl 
                    USING(id_plano)
                WHERE a.id_apolice = %s;""",
            (id_apolice,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        apolice = {
            "id_apolice": resultado[0],
            "id_cotacao": resultado[1],
            "cliente": resultado[2],
            "seguradora": resultado[3],
            "plano": resultado[4],
            "valor": resultado[5],
            "inicio":     str(resultado[6]),
            "fim":        str(resultado[7])
        }
        return apolice

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar apólice:", e)
        return None

def read_apolice_por_cotacao(id_cotacao):
    # Busca apólice pelo ID da cotação vinculada
    try:
        cursor.execute(
            """SELECT 
                    a.id_apolice as id_apolice,
                    c.id_cotacao as id_cotacao,
                    p.nome_completo AS cliente,
                    s.nome_fantasia AS seguradora,
                    pl.nome_plano AS plano,
                    c.valor_cotacao AS valor,
                    a.inicio,
                    a.fim
                FROM apolice a
                JOIN cotacoes c 
                    USING(id_cotacao)
                JOIN pessoa p 
                    USING(id_pessoa)
                JOIN seguradora s 
                    USING(id_seguradora)
                JOIN plano pl 
                    USING(id_plano)
                WHERE c.id_cotacao = %s;""",
            (id_cotacao,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        apolice = {
            "id_apolice": resultado[0],
            "id_cotacao": resultado[1],
            "cliente": resultado[2],
            "seguradora": resultado[3],
            "plano": resultado[4],
            "valor": resultado[5],
            "inicio":     str(resultado[6]),
            "fim":        str(resultado[7])
        }
        return apolice

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar apólice por cotação:", e)
        return None

def read_cotacao(id_cotacao):
    # Busca cotação pelo ID — retorna dicionário ou None
    try:
        cursor.execute(
            """
            SELECT
                c.id_cotacao,
                p.nome_completo AS Cliente,
                s.nome_fantasia AS Seguradora,
                pl.nome_plano AS Plano,
                c.valor_cotacao AS "Valor Cotação",
                data_cotacao AS "Data da Cotação"
            FROM Seguradora s
            JOIN Plano pl
                USING(id_seguradora)
            JOIN Cotacoes c
                USING(id_plano)
            JOIN Pessoa p
                USING(id_pessoa)
            WHERE c.id_cotacao = %s""",
            (id_cotacao,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        venda = {
            "c.id_cotacao":    resultado[0],
            "p.nome_pessoa":     str(resultado[1]),
            "s.nome_fantasia": str(resultado[2]),
            "pl.nome_plano":      str(resultado[3]),
            "c.valor_cotacao": str(resultado[4]),
            "c.data_cotacao":  str(resultado[5])
        }
        return venda

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar cotação:", e)
        return None

def read_cotacao_por_pessoa(id_pessoa):
    # Busca cotação pelo ID da pessoa vinculada
    try:
        cursor.execute(
            """
            SELECT
                c.id_cotacao,
                p.nome_completo AS Cliente,
                s.nome_fantasia AS Seguradora,
                pl.nome_plano AS Plano,
                c.valor_cotacao AS "Valor Cotação",
                c.data_cotacao AS "Data da Cotação"
            FROM Seguradora s
            JOIN Plano pl
                USING(id_seguradora)
            JOIN Cotacoes c
                USING(id_plano)
            JOIN Pessoa p
                USING(id_pessoa)
            WHERE p.id_pessoa = %s""",
            (id_pessoa,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        venda = {
            "c.id_cotacao":    resultado[0],
            "p.nome_pessoa":     str(resultado[1]),
            "s.nome_fantasia": str(resultado[2]),
            "pl.nome_plano":      str(resultado[3]),
            "c.valor_cotacao": str(resultado[4]),
            "c.data_cotacao":  str(resultado[5])
        }
        return venda

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar cotação por pessoa:", e)
        return None
    
def read_seguradora_por_id(id_seguradora):
    try:
        cursor.execute("""
                        SELECT 
                            id_seguradora AS id,
                            nome_fantasia AS nome,
                            cnpj,
                            telefone_suporte AS telefone
                        FROM Seguradora
                        WHERE id_seguradora = %s""",
                        (id_seguradora,)
        )
        
        resultados = cursor.fetchall()
        seguradoras = []
        for resultado in resultados:
            seguradora = {
                "id": resultado[0],
                "nome": resultado[1],
                "cnpj": resultado[2],
                "telefone": resultado[3]
            }
            seguradoras.append(seguradora)
        return seguradora

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar seguradoras:", e)
        return None

def read_seguradora_por_cnpj(cnpj):
    # Retorna uma lista de dicionários com todas as seguradoras do banco
    try:
        cursor.execute("""
                        SELECT 
                            id_seguradora AS id,
                            nome_fantasia AS nome,
                            cnpj,
                            telefone_suporte AS telefone
                        FROM Seguradora
                        WHERE cnpj = %s""",
                        (cnpj,)
        )
        resultados = cursor.fetchall()
        seguradoras = []
        for resultado in resultados:
            seguradora = {
                "id": resultado[0],
                "nome": resultado[1],
                "cnpj": resultado[2],
                "telefone": resultado[3]
            }
            seguradoras.append(seguradora)
        return seguradoras

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar seguradoras:", e)
        return None
 
def read_plano_por_id(id_plano):
    try:
        cursor.execute("""
            SELECT
                p.id_plano || ' - ' || p.nome_plano AS plano_id,
                s.id_seguradora || ' - ' || s.nome_fantasia AS seguradora_id,
                p.tipo_cobertura AS cobertura
            FROM Plano p
            JOIN Seguradora s
                USING(id_seguradora)
            WHERE p.id_plano = %s
            """, 
            (id_plano,)
        )
        resultado = cursor.fetchone()
        if resultado is None:
            return None

        plano = {
            "plano_id": resultado[0],
            "seguradora_id": resultado[1],
            "cobertura": resultado[2],
        }

        return plano

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar plano:", e)
        return None
    
def read_plano_por_nome(nome_plano):
    try:
        cursor.execute("""
            SELECT
                p.id_plano || ' - ' || p.nome_plano AS plano_id,
                s.id_seguradora || ' - ' || s.nome_fantasia AS seguradora_id,
                p.tipo_cobertura AS cobertura
            FROM Plano p
            JOIN Seguradora s
                USING(id_seguradora)
            WHERE p.nome_plano ILIKE %s
            """, 
            (f"%{nome_plano}%",)
        )
        resultado = cursor.fetchone()
        if resultado is None:
            return None

        plano = {
            "plano_id": resultado[0],
            "seguradora_id": resultado[1],
            "cobertura": resultado[2],
        }

        return plano

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar plano:", e)
        return None
     
def read_bem_por_id(id_bem):
    try:
        cursor.execute("""
            SELECT 
                b.id_bem as id_bem,
                b.descricao_bem as descricao_bem,
                b.tipo_bem as tipo_bem,
                b.valor_estimado as valor_estimado,
                p.id_pessoa||' - '||p.nome_completo AS id_nome_pessoa
            FROM Bens b
            JOIN pessoa p
            USING(id_pessoa)
            WHERE id_bem = %s;
            """,
            (id_bem,)
        )
        resultado = cursor.fetchone()
        if resultado is None:
            return None

        bem = {
            "id_bem": resultado[0],
            "descricao_bem": resultado[1],
            "tipo_bem": resultado[2],
            "valor_estimado": resultado[3],
            "id_nome_pessoa": resultado[4]
        }
        return bem

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar bem:", e)
        return None


#                  UPDATE                   #

def update_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
    # Atualiza os dados do cliente pelo CPF de forma parcial
    # cursor.rowcount indica quantas linhas foram afetadas
    # se for 0, o CPF não foi encontrado no banco
    try:
        # Se o campo veio vazio da interface, buscamos o valor atual que já está no banco
        # para não apagar o dado antigo.
        cliente_atual = read_pessoa_por_cpf(cpf)
        
        if not cliente_atual:
            return False    # Se o CPF não for localizado na busca, já para aqui

        # Se o parâmetro passado for vazio, mantém o valor que já existia no banco
        nome_final      = nome if nome != "" else cliente_atual["nome_completo"]
        email_final     = email if email != "" else cliente_atual["email"]
        sexo_final      = sexo if sexo != "" else cliente_atual["sexo"]
        telefone_final  = telefone if telefone != "" else cliente_atual["telefone"]
        data_nasc_final = data_nasc if data_nasc != "" else cliente_atual["data_nascimento"]
        status_final    = status if status != "" else cliente_atual["status"]

        # Executa o UPDATE com a tabela 'pessoa' (no singular) com os valores tratados
        cursor.execute(
            """UPDATE pessoa
               SET nome_completo=%s, email=%s, sexo=%s,
                   telefone=%s, data_nascimento=%s, status=%s
               WHERE cpf_cnpj = %s""",
            (nome_final, email_final, sexo_final, telefone_final, data_nasc_final, status_final, str(cpf))
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

def update_seguradora(id_seguradora, nome, cnpj, telefone):
    # Atualiza os dados de uma seguradora pelo ID
    try:
        cursor.execute(
            """UPDATE seguradora
               SET nome_fantasia=%s, cnpj=%s, telefone_suporte=%s
               WHERE id_seguradora = %s""",
            (nome, cnpj, telefone, id_seguradora)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar seguradora:", e)
        return False
    
def update_plano(id_plano, id_seguradora, nome_plano, tipo_cobertura):
    # Atualiza os dados de um plano pelo ID
    try:
        cursor.execute(
            """UPDATE plano
               SET id_seguradora=%s, nome_plano=%s, tipo_cobertura=%s
               WHERE id_plano = %s""",
            (id_seguradora, nome_plano, tipo_cobertura, id_plano)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar plano:", e)
        return False
    
def update_bem(id_bem, id_pessoa, tipo_bem, descricao_bem, valor_estimado):
    # Atualiza os dados de um bem pelo ID
    try:
        cursor.execute(
            """UPDATE bem
               SET id_pessoa=%s, tipo_bem=%s,
                   descricao_bem=%s, valor_estimado=%s
               WHERE id_bem = %s""",
            (id_pessoa, tipo_bem, descricao_bem, valor_estimado, id_bem)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao atualizar bem:", e)
        return False


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

def delete_seguradora(id_seguradora):
    # Remove uma seguradora pelo ID
    try:
        cursor.execute(
            "DELETE FROM seguradora WHERE id_seguradora = %s",
            (id_seguradora,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao deletar seguradora:", e)
        return False
    
def delete_plano(id_plano):
    # Remove um plano pelo ID
    try:
        cursor.execute(
            "DELETE FROM plano WHERE id_plano = %s",
            (id_plano,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao deletar plano:", e)
        return False

def delete_bem(id_bem):
    # Remove um bem pelo ID
    try:
        cursor.execute(
            "DELETE FROM bem WHERE id_bem = %s",
            (id_bem,)
        )
        conn.commit()

        if cursor.rowcount == 0:
            return False
        return True

    except Exception as e:
        conn.rollback()
        print("Erro ao deletar bem:", e)
        return False


## LISTAGEM GERAL DE CADA ITEM DA NAVEGAÇÃO PARA EXIBIÇÃO NAS TELAS DE ATUALIZAR E REMOVER

def listagem_geral_pessoas():
    try:
        cursor.execute("""
                        SELECT
                            id_pessoa,
                            cpf_cnpj,
                            nome_completo,
                            email,
                            sexo,
                            telefone,
                            data_nascimento,
                            status
                        FROM pessoa
                        ORDER BY nome_completo;
                    """)
        resultados = cursor.fetchall()
        pessoas = []
        for resultado in resultados:
            pessoa = {
                "id_pessoa": resultado[0],
                "cpf_cnpj": resultado[1],
                "nome_completo": resultado[2],
                "email": resultado[3],
                "sexo": resultado[4],
                "telefone": resultado[5],
                "data_nascimento": resultado[6],
                "status": resultado[7]
            }
            pessoas.append(pessoa)
        return pessoas

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar pessoas:", e)
        return None
    
def listagem_geral_seguradoras():
    try:
        cursor.execute("""
                        SELECT
                            id_seguradora,
                            nome_fantasia,
                            cnpj,
                            telefone_suporte
                        FROM seguradora;
                    """)
        resultados = cursor.fetchall()
        seguradoras = []
        for resultado in resultados:
            seguradora = {
                "id_seguradora": resultado[0],
                "nome_fantasia": resultado[1],
                "cnpj": resultado[2],
                "telefone_suporte": resultado[3]
            }
            seguradoras.append(seguradora)
        return seguradoras

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar seguradoras:", e)
        return None
    
def listagem_geral_planos():
    try:
        cursor.execute("""
                        SELECT
                            p.id_plano as id_plano,
                            s.id_seguradora || ' - ' || s.nome_fantasia AS seguradora,
                            p.tipo_cobertura as cobertura,
                            p.nome_plano as plano
                        FROM plano p
                        JOIN seguradora s
                            USING(id_seguradora)
                        ORDER BY p.id_plano;
                    """)
        resultados = cursor.fetchall()
        planos = []
        for resultado in resultados:
            plano = {
                "id_plano": resultado[0],
                "seguradora": resultado[1],
                "cobertura": resultado[2],
                "plano": resultado[3]
            }
            planos.append(plano)
        return planos

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar planos:", e)
        return None
    
def listagem_geral_bens():
    try:
        cursor.execute(
            """
                SELECT
                    b.id_bem as id_bem,
                    p.id_pessoa || ' - ' || p.nome_completo AS pessoa,
                    b.tipo_bem as tipo_bem,
                    b.descricao_bem as descricao_bem,
                    b.valor_estimado as valor_estimado
                FROM bens b
                JOIN pessoa p
                    USING(id_pessoa);
                    """)
        resultados = cursor.fetchall()
        bens = []
        for resultado in resultados:
            bem = {
                "id_bem": resultado[0],
                "pessoa": resultado[1],
                "tipo_bem": resultado[2],
                "descricao_bem": resultado[3],
                "valor_estimado": resultado[4]
            }
            bens.append(bem)
        return bens

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar bens:", e)
        return None
    
def listagem_geral_cotacoes():
    try:
        cursor.execute(
                    """
                    SELECT
                        c.id_cotacao as id_cotacao,
                        p.id_pessoa || ' - ' || p.nome_completo AS pessoa,
                        s.id_seguradora || ' - ' || s.nome_fantasia AS seguradora,
                        pl.id_plano || ' - ' || pl.nome_plano AS plano,
                        c.valor_cotacao as valor_cotacao,
                        c.data_cotacao as data_cotacao,
                        c.status_cotacao as status_cotacao
                    FROM cotacoes c
                    JOIN pessoa p
                        ON p.id_pessoa = c.id_pessoa
                    JOIN seguradora s
                        ON s.id_seguradora = c.id_seguradora
                    JOIN plano pl
                        ON pl.id_plano = c.id_plano;
                        """)
        resultados = cursor.fetchall()
        cotacoes = []
        for resultado in resultados:
            cotacao = {
                "id_cotacao": resultado[0],
                "pessoa": resultado[1],
                "seguradora": resultado[2],
                "plano": resultado[3],
                "valor_cotacao": resultado[4],
                "data_cotacao": resultado[5],
                "status_cotacao": resultado[6]
            }
            cotacoes.append(cotacao)
        return cotacoes

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar cotações:", e)
        return None
    
def listagem_geral_apolices():
    try:
        cursor.execute("""
                        SELECT
                            a.id_apolice as id_apolice,
                            c.id_cotacao || ' - ' || p.nome_completo AS cotacao,
                            a.inicio as inicio,
                            a.fim as fim
                        FROM apolice a
                        JOIN cotacoes c
                           USING(id_cotacao)
                        JOIN pessoa p
                            USING(id_pessoa)
                    """)
        resultados = cursor.fetchall()
        apolices = []
        for resultado in resultados:
            apolice = {
                "id_apolice": resultado[0],
                "cotacao": resultado[1],
                "inicio": resultado[2],
                "fim": resultado[3]
            }
            apolices.append(apolice)
        return apolices

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar apólices:", e)
        return None
 
   
## CONSULTAS PARA OS INDICADORES DO BI ##
def qtd_cliente_por_status(status):
    try:
        cursor.execute("""  
                    SELECT 
                        status||'(s): '||COUNT(*) AS qtd_status
                    FROM pessoa
                    GROUP BY status
                    HAVING UPPER(status) = 'ATIVO';
                    """,
                    (status,)
        )
        resultado = cursor.fetchone()
        if resultado is None:
            return None

        indicador = {
            "qtd_status": resultado[1]
        }
        return indicador

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de clientes por status:", e)
        return None
    
def novas_apolices_em_x_dias(dias):
    try:
        cursor.execute("""
                    SELECT 
                        COUNT(*) AS qtd_novas_apolices
                    FROM apolice
                    WHERE inicio >= CURRENT_DATE - INTERVAL '%s' DAY;
                    """, (dias,))
        resultado = cursor.fetchone()
        if resultado is None:
            return None

        indicador = {
            "qtd_novas_apolices": resultado[0]
        }
        return indicador

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de novas apólices:", e)
        return None
    
def orcamentos_feitos_em_x_dias(dias):
    try:
        cursor.execute("""
                    SELECT 
                        COUNT(*) AS qtd_orcamentos
                    FROM cotacoes
                    WHERE data_cotacao >= CURRENT_DATE - INTERVAL '%s' DAY;
                    """, (dias,))
        resultado = cursor.fetchone()
        if resultado is None:
            return None

        indicador = {
            "qtd_orcamentos": resultado[0]
        }
        return indicador

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de orçamentos feitos:", e)
        return None