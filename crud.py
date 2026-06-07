# crud.py
# Arquivo com todas as funções de acesso ao banco de dados.
# Cada função faz UMA operação: criar, ler, atualizar ou deletar.

from conn import conexao    # importa a função que abre a conexão
conn   = conexao()                 # abre a conexão com o banco 
cursor = conn.cursor()             # cria um cursor para executar comandos SQL

#                  CREATE                   #

def create_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
    # Insere um novo cliente na tabela pessoa
    # Retorna o ID gerado se deu certo, ou False se deu erro
    try:
        cursor.execute(
            """INSERT INTO pessoa
               (cpf_cnpj, nome_completo, email, sexo, telefone, data_nascimento, status)
               VALUES (%s, %s, %s, %s, %s, %s, %s)
               RETURNING id_pessoa""",
            (cpf, nome, email, sexo, telefone, data_nasc, status)
        )

        id_gerado = cursor.fetchone()[0]

        conn.commit()       # salva no banco — sem isso o dado NÃO é gravado
        print("Pessoa criada com sucesso!")
        return id_gerado    # retorna o ID criado para a interface exibir

    except Exception as e:
        conn.rollback()     # cancela qualquer alteração parcial se der erro
        print("Erro ao criar pessoa:", e)
        return False        # avisa a interface que deu errado

def create_apolice(id_cotacao, inicio, fim):
    # Insere uma nova apólice vinculada a uma cotação
    # Retorna o ID gerado se deu certo, ou False se deu erro
    try:
        cursor.execute(
            """INSERT INTO apolice (id_cotacao, inicio, fim)
               VALUES (%s, %s, %s)
               RETURNING id_apolice""",
            (id_cotacao, inicio, fim)
        )

        id_gerado = cursor.fetchone()[0]

        conn.commit()
        print("Apólice criada com sucesso!")
        return id_gerado

    except Exception as e:
        conn.rollback()
        print("Erro ao criar apólice:", e)
        return False

def create_cotacao(id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao, status):
    # Insere uma nova cotação no banco
    # Retorna o ID gerado se deu certo, ou False se deu erro
    try:
        cursor.execute(
            """INSERT INTO cotacoes
               (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao, status)
               VALUES (%s, %s, %s, %s, %s, %s)
               RETURNING id_cotacao""",
            (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao, status)
        )

        id_gerado = cursor.fetchone()[0]

        conn.commit()
        print("Cotação criada com sucesso!")
        return id_gerado

    except Exception as e:
        conn.rollback()
        print("Erro ao criar cotação:", e)
        return False

def create_seguradora(nome, cnpj, telefone):
    # Insere uma nova seguradora no banco
    # Retorna o ID gerado se deu certo, ou False se deu erro
    try:
        cursor.execute(
            """INSERT INTO seguradora (nome_fantasia, cnpj, telefone_suporte)
               VALUES (%s, %s, %s)
               RETURNING id_seguradora""",
            (nome, cnpj, telefone)
        )

        id_gerado = cursor.fetchone()[0]

        conn.commit()
        print("Seguradora criada com sucesso!")
        return id_gerado

    except Exception as e:
        conn.rollback()
        print("Erro ao criar seguradora:", e)
        return False

def create_plano(id_seguradora, tipo_cobertura, nome_plano):
    # Insere um novo plano no banco
    # Retorna o ID gerado se deu certo, ou False se deu erro
    try:
        cursor.execute(
            """INSERT INTO plano (id_seguradora, tipo_cobertura ,nome_plano)
               VALUES (%s, %s, %s)
               RETURNING id_plano""",
            (id_seguradora, tipo_cobertura, nome_plano)
        )

        id_gerado = cursor.fetchone()[0]

        conn.commit()
        print("Plano criado com sucesso!")
        return id_gerado

    except Exception as e:
        conn.rollback()
        print("Erro ao criar plano:", e)
        return False

def create_bem(id_pessoa, tipo_bem, descricao_bem, valor_estimado):
    # Insere um novo bem no banco
    # Retorna o ID gerado se deu certo, ou False se deu erro
    try:
        cursor.execute(
            """INSERT INTO bens (id_pessoa, tipo_bem, descricao_bem, valor_estimado)
               VALUES (%s, %s, %s, %s)
               RETURNING id_bem""",
            (id_pessoa, tipo_bem, descricao_bem, valor_estimado)
        )

        id_gerado = cursor.fetchone()[0]

        conn.commit()
        print("Bem criado com sucesso!")
        return id_gerado

    except Exception as e:
        conn.rollback()
        print("Erro ao criar bem:", e)
        return False


#                  READ                     #
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
            """SELECT 
                id_pessoa,
                cpf_cnpj,
                nome_completo,
                email, 
                sexo,
                telefone,
                data_nascimento, 
                status
               FROM pessoa WHERE cpf_cnpj = %s""",
            (str(cpf),)
        )
        resultado = cursor.fetchone()   # pega a primeira linha encontrada

        if resultado is None:
            return None                 # cliente não existe no banco

        # O banco retorna uma tupla — convertemos para dicionário
        # para facilitar o uso na interface (cliente['nome_completo'] etc)
        cliente = {
            "id_pessoa":      resultado[0],
            "cpf_cnpj":        resultado[1],
            "nome_completo":   resultado[2],
            "email":           resultado[3],
            "sexo":            resultado[4],
            "telefone":        resultado[5],
            "data_nascimento": str(resultado[6]),   # converte data para texto
            "status":          resultado[7]
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

def read_apolice_por_id(id_apolice):
    # Busca apólice pelo ID — retorna dicionário ou None
    try:
        cursor.execute(
            """SELECT 
                    a.id_apolice AS id_apolice,
                    a.id_cotacao AS id_cotacao,
                    p.nome_completo AS cliente,
                    s.nome_fantasia AS seguradora,
                    pl.nome_plano AS plano,
                    c.valor_cotacao AS valor,
                    a.inicio AS inicio,
                    a.fim AS fim
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

def read_cotacao(id_cotacao):
    # Busca cotação pelo ID — retorna dicionário ou None
    try:
        cursor.execute(
            """
            SELECT
                c.id_cotacao AS id_cotacao,
                p.id_pessoa AS id_pessoa,
                p.nome_completo AS cliente,
                s.id_seguradora as id_cotacao,
                s.nome_fantasia AS seguradora,
                pl.id_plano AS id_plano,
                pl.nome_plano AS plano,
                c.valor_cotacao AS valor_cotacao,
                c.data_cotacao AS data_cotacao,
                c.status_cotacao AS status_cotacao
            FROM cotacoes c
            JOIN pessoa p
                USING(id_pessoa)
            JOIN seguradora s
                USING(id_seguradora)
            JOIN plano pl
                USING(id_plano)
            WHERE id_cotacao = %s""",
            (id_cotacao,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        venda = {
            "id_cotacao":    resultado[0],
            "id_pessoa": resultado[1],
            "nome_pessoa":     str(resultado[2]),
            "id_seguradora": resultado[3],
            "nome_fantasia": str(resultado[4]),
            "id_plano": resultado[5],
            "nome_plano":      str(resultado[6]),
            "valor_cotacao": str(resultado[7]),
            "data_cotacao":  str(resultado[8]),
            "status_cotacao": str(resultado[9])
        }
        return venda

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar cotação:", e)
        return None

def read_cotacao_por_pessoa(cpf_cnpj):
    # Busca cotação pelo CPF/CNPJ da pessoa vinculada
    try:
        cursor.execute(
            """
            SELECT
                c.id_cotacao AS id_cotacao,
                p.id_pessoa AS id_pessoa,
                p.nome_completo AS cliente,
                s.id_seguradora as id_cotacao,
                s.nome_fantasia AS seguradora,
                pl.id_plano AS id_plano,
                pl.nome_plano AS plano,
                c.valor_cotacao AS valor_cotacao,
                c.data_cotacao AS data_cotacao,
                c.status_cotacao AS status_cotacao
            FROM cotacoes c
            JOIN pessoa p
                USING(id_pessoa)
            JOIN seguradora s
                USING(id_seguradora)
            JOIN plano pl
                USING(id_plano)
            WHERE p.cpf_cnpj = %s""",
            (cpf_cnpj,)
        )
        resultado = cursor.fetchone()

        if resultado is None:
            return None

        venda = {
            "id_cotacao":    resultado[0],
            "id_pessoa": resultado[1],
            "nome_pessoa":     str(resultado[2]),
            "id_seguradora": resultado[3],
            "nome_fantasia": str(resultado[4]),
            "id_plano": resultado[5],
            "nome_plano":      str(resultado[6]),
            "valor_cotacao": str(resultado[7]),
            "data_cotacao":  str(resultado[8]),
            "status_cotacao": str(resultado[9])
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
        
        resultado = cursor.fetchone()
        seguradora = {
            "id": resultado[0],
            "nome": resultado[1],
            "cnpj": resultado[2],
            "telefone": resultado[3]
        }
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
        resultado = cursor.fetchone()

        seguradora = {
            "id": resultado[0],
            "nome": resultado[1],
            "cnpj": resultado[2],
            "telefone": resultado[3]
        }
        return seguradora

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar seguradoras:", e)
        return None
 
def read_plano_por_id(id_plano):
    try:
        cursor.execute("""
            SELECT
                p.id_plano as id_plano,
                p.nome_plano AS nome_plano,
                s.id_seguradora as id_seguradora,
                s.nome_fantasia AS seguradora,
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
            "id_plano": resultado[0],
            "nome_plano": resultado[1],
            "id_seguradora": resultado[2],
            "seguradora": resultado[3],
            "cobertura": resultado[4],
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
                p.id_plano as id_plano,
                p.nome_plano AS nome_plano,
                s.id_seguradora as id_seguradora,
                s.nome_fantasia AS seguradora,
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
            "id_plano": resultado[0],
            "nome_plano": resultado[1],
            "id_seguradora": resultado[2],
            "seguradora": resultado[3],
            "cobertura": resultado[4],
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
                p.id_pessoa as id_pessoa,
                p.nome_completo as nome_pessoa
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
            "id_pessoa": resultado[4],
            "nome_pessoa": resultado[5]
        }
        return bem

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar bem:", e)
        return None

def read_bem_por_descricao(descricao_bem):
    try:
        cursor.execute("""
            SELECT 
                b.id_bem as id_bem,
                b.descricao_bem as descricao_bem,
                b.tipo_bem as tipo_bem,
                b.valor_estimado as valor_estimado,
                p.id_pessoa as id_pessoa,
                p.nome_completo as nome_pessoa
            FROM Bens b
            JOIN pessoa p
            USING(id_pessoa)
            WHERE b.descricao_bem ILIKE %s;
            """,
            (f"%{descricao_bem}%",)
        )
        resultado = cursor.fetchone()
        if resultado is None:
            return None

        bem = {
            "id_bem": resultado[0],
            "descricao_bem": resultado[1],
            "tipo_bem": resultado[2],
            "valor_estimado": resultado[3],
            "id_pessoa": resultado[4],
            "nome_pessoa": resultado[5]
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
        nome      = nome if nome != "" else cliente_atual["nome_completo"]
        email     = email if email != "" else cliente_atual["email"]
        sexo      = sexo if sexo != "" else cliente_atual["sexo"]
        telefone  = telefone if telefone != "" else cliente_atual["telefone"]
        data_nasc = data_nasc if data_nasc != "" else cliente_atual["data_nascimento"]
        status    = status if status != "" else cliente_atual["status"]

        # Executa o UPDATE com a tabela 'pessoa' (no singular) com os valores tratados
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
        
        apolice_atual = read_apolice_por_id(id_apolice)
        if not apolice_atual:
            return False
        
        inicio = inicio if inicio != "" else apolice_atual["inicio"]
        fim = fim if fim != "" else apolice_atual["fim"]
        
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

def update_cotacao(id_cotacao, id_pessoa, id_seguradora, id_plano, valor, data, status):
    # Atualiza os dados de uma cotação pelo ID
    try:
        
        cotacao_atual = read_cotacao(id_cotacao)
        if not cotacao_atual:
            return False
        id_pessoa = id_pessoa if id_pessoa != "" else cotacao_atual["id_pessoa"]
        id_seguradora = id_seguradora if id_seguradora != "" else cotacao_atual["id_seguradora"]
        id_plano = id_plano if id_plano != "" else cotacao_atual["id_plano"]
        valor = valor if valor != "" else cotacao_atual["valor_cotacao"]
        data = data if data != "" else cotacao_atual["data_cotacao"]
        status = status if status != "" else cotacao_atual["status_cotacao"]
        
        cursor.execute(
            """UPDATE cotacoes
               SET id_pessoa=%s, id_seguradora=%s, id_plano=%s,
                   valor_cotacao=%s, data_cotacao=%s, status_cotacao=%s
               WHERE id_cotacao = %s""",
            (id_pessoa, id_seguradora, id_plano, valor, data, status, id_cotacao)
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
        
        seguradora_atual = read_seguradora_por_id(id_seguradora)
        
        if not seguradora_atual:
            return False 
        nome      = nome if nome != "" else seguradora_atual["nome"]
        cnpj      = cnpj if cnpj != "" else seguradora_atual["cnpj"]
        telefone  = telefone if telefone != "" else seguradora_atual["telefone"]

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
        
        read_plano = read_plano_por_id(id_plano)
        
        if not read_plano:
            return False
        
        id_seguradora = id_seguradora if id_seguradora != "" else read_plano["id_seguradora"]
        nome_plano = nome_plano if nome_plano != "" else read_plano["nome_plano"]
        tipo_cobertura = tipo_cobertura if tipo_cobertura != "" else read_plano["cobertura"]
        
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
        
        bem_atual = read_bem_por_id(id_bem)
        if not bem_atual:
            return False
        id_pessoa = id_pessoa if id_pessoa != "" else bem_atual["id_pessoa"]
        tipo_bem = tipo_bem if tipo_bem != "" else bem_atual["tipo_bem"]
        descricao_bem = descricao_bem if descricao_bem != "" else bem_atual["descricao_bem"]
        valor_estimado = valor_estimado if valor_estimado != "" else bem_atual["valor_estimado"]
        
        cursor.execute(
            """UPDATE bens
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

def delete_pessoa(id):
    # Remove um cliente pelo CPF
    # Retorna True se removeu, False se o CPF não existia
    try:
        cursor.execute(
            "DELETE FROM pessoa WHERE id_pessoa = %s",
            (id,))
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
            "DELETE FROM bens WHERE id_bem = %s",
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


## LISTAGEM GERAL DE CADA ITEM DA NAVEGAÇÃO

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
    

def bi_indicador_ganhos_conversao():
    """
    CARREGA  O VOLUME COMERCIAL, TAXA DE CONVERSÃO E FATURAMENTO POR TIPO.
   NÚMERO DE ORCAMENTO , CONVERTIDOS, FATURAMENTO TOTAL E POR TIPO DE CONTRATO/BEM
    """
    try:
        # 1. Total de orçamentos e convertidos (Últimos 30 dias)
        orcamentos = novas_cotacoes(30)
        total_orcamentos = orcamentos["qtd_orcamentos"] if orcamentos else 0

        cursor.execute("""
            SELECT COUNT(*) FROM Apolice
            WHERE inicio >= CURRENT_DATE - INTERVAL '30 DAY';
        """)
        total_convertidos = cursor.fetchone()[0]

        taxa_conversao = 0.0
        if total_orcamentos > 0:
            taxa_conversao = (total_convertidos / total_orcamentos) * 100

        # 2. FATURAMENTO TOTAL (Soma de todas as cotações que viraram apólices)
        cursor.execute("""
            SELECT COALESCE(SUM(c.valor_cotacao), 0) 
            FROM cotacoes c
            JOIN apolice a USING (id_cotacao);
        """)
        faturamento_total = cursor.fetchone()[0]

        # 3. FATURAMENTO POR TIPO DE CONTRATO / BEM
        cursor.execute("""
            SELECT COALESCE(b.tipo_bem, 'Não Especificado') AS tipo, SUM(c.valor_cotacao) AS total
            FROM cotacoes c
            JOIN apolice a USING (id_cotacao)
            LEFT JOIN bens b USING (id_pessoa)
            GROUP BY b.tipo_bem
            ORDER BY total DESC;
        """)
        faturamento_por_tipo = cursor.fetchall()

        return {
            "total_orcamentos": total_orcamentos,
            "total_convertidos": total_convertidos,
            "taxa_conversao": round(taxa_conversao, 2),
            "faturamento_total": float(faturamento_total),
            "faturamento_por_tipo": faturamento_por_tipo
        }
    except Exception as e:
        conn.rollback()
        print("Erro no BI Ganhos:", e)
        return None

def bi_ranking_seguradoras():
    """
    TRÁS O RANKING DE CONTRATOS E TRAZ A MARGEM DE LUCRO  POR SEGURADORA .

    """
    try:
        # Traz o nome, quantidade de contratos e a margem acumulada (simulando 15% de comissão média sobre as apólices)
        cursor.execute("""
            SELECT 
                s.nome_fantasia AS seguradora, 
                COUNT(a.id_apolice) AS total_contratos,
                COALESCE(SUM(c.valor_cotacao) * 0.15, 0) AS margem_lucro
            FROM apolice a
            JOIN cotacoes c USING (id_cotacao)
            JOIN seguradora s USING (id_seguradora)
            GROUP BY s.nome_fantasia
            ORDER BY total_contratos DESC;
        """)
        resultados = cursor.fetchall()
        
        ranking = []
        for linha in resultados:
            ranking.append({
                "seguradora": linha[0],
                "total_contratos": linha[1],
                "margem_lucro": float(linha[2])
            })
        return ranking
    except Exception as e:
        conn.rollback()
        print("Erro no BI Seguradoras:", e)
        return []

def bi_clientes_vencidos_e_vencendo():
    """
    Busca os contratos urgentes e calcula o número de apólices renovadas na carteira.
    FAZ  ALERTA DE CONTRATOS VENCENDO E NÚMERO DE APÓLICES RENOVADES
    """
    relatorio = {"vencidos": [], "vencendo": [], "renovados": 0}
    try:
        # 1. Contratos já vencidos
        cursor.execute("""
            SELECT a.id_apolice, p.nome_completo, p.telefone, a.fim
            FROM apolice a
            JOIN cotacoes c USING (id_cotacao)
            JOIN pessoa p USING (id_pessoa)
            WHERE a.fim < CURRENT_DATE
            ORDER BY a.fim ASC;
        """)
        for linha in cursor.fetchall():
            relatorio["vencidos"].append({
                "id_apolice": linha[0],
                "cliente": linha[1],
                "telefone": linha[2],
                "data_vencimento": str(linha[3])
            })

        # 2. Próximos 10 dias
        cursor.execute("""
            SELECT a.id_apolice, p.nome_completo, p.telefone, a.fim
            FROM apolice a
            JOIN cotacoes c USING (id_cotacao)
            JOIN pessoa p USING (id_pessoa)
            WHERE a.fim BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '10 DAY'
            ORDER BY a.fim ASC;
        """)
        for linha in cursor.fetchall():
            relatorio["vencendo"].append({
                "id_apolice": linha[0],
                "cliente": linha[1],
                "telefone": linha[2],
                "data_vencimento": str(linha[3])
            })

        # 3. Métrica de Apólices Renovadas (Simulação baseada em clientes recorrentes com mais de uma cotação ativa)
        cursor.execute("""
            SELECT COUNT(*) FROM apolice 
            WHERE id_cotacao IN (
                SELECT id_cotacao FROM cotacoes WHERE status_cotacao ILIKE '%renovado%' OR valor_cotacao > 0
            ) AND inicio >= CURRENT_DATE - INTERVAL '1 YEAR';
        """)
        relatorio["total_renovadas"] = cursor.fetchone()[0]

        return relatorio
    except Exception as e:
        conn.rollback()
        print("Erro no BI Renovações:", e)
        return relatorio
    
def bi_potencial_clientes():
    """
    TRÁS OS VALORES DE TODOS OS BENS ADMINISTRADOS PELA CORRETORA.
    GARANTE TRATAR OS ERROS E VALORES NULOS DO POSTGRESQL.
    """
    try:
        # 1. Busca a distribuição de clientes por status
        cursor.execute("""
            SELECT COALESCE(status, 'Sem Status'), COUNT(*) 
            FROM pessoa 
            GROUP BY status;
        """)
        status_resumo = cursor.fetchall()

        # 2. Busca o valor total do patrimônio protegido nos bens
        cursor.execute("""
            SELECT COALESCE(SUM(valor_estimado), 0) 
            FROM bens;
        """)
        resultado_bens = cursor.fetchone()
        total_protegido = float(resultado_bens[0]) if resultado_bens else 0.0

        # Se o banco retornar vazio para os status, cria um padrão para não quebrar a tela
        if not status_resumo:
            status_resumo = [("Ativo", 0)]

        return {
            "status_resumo": status_resumo,
            "total_protegido": total_protegido
        }
    except Exception as e:
        conn.rollback()
        print("Erro no BI Clientes:", e)
        # Retorna painel padrão se d der erro pra não ficar em branco
        return {
            "status_resumo": [("Erro ao carregar", 0)],
            "total_protegido": 0.0
        }    


def qtd_cliente_por_status(status=None):
    try:
        if status is None or str(status).strip() == "":
            cursor.execute("""
                SELECT COUNT(*) AS qtd_status
                FROM pessoa;
            """)
        else:
            cursor.execute("""
                SELECT COUNT(*) AS qtd_status
                FROM pessoa
                WHERE UPPER(status) = UPPER(%s);
            """, (status,))

        resultado = cursor.fetchone()

        if resultado is None:
            return {"qtd_status": 0}

        return {
            "qtd_status": resultado[0]
        }

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de clientes por status:", e)
        return {"qtd_status": 0}

def novas_apolices(dias=None):
    try:
        if dias is None or str(dias).strip() == "":
            cursor.execute("""
                SELECT COUNT(*) AS qtd_novas_apolices
                FROM apolice;
            """)
        else:
            cursor.execute("""
                SELECT COUNT(*) AS qtd_novas_apolices
                FROM apolice
                WHERE inicio >= CURRENT_DATE - (%s * INTERVAL '1' DAY);
            """, (int(dias),))

        resultado = cursor.fetchone()

        if resultado is None:
            return {"qtd_novas_apolices": 0}

        return {
            "qtd_novas_apolices": resultado[0]
        }

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de novas apólices:", e)
        return {"qtd_novas_apolices": 0}

def novas_cotacoes(dias=None):
    try:
        if dias is None or str(dias).strip() == "":
            cursor.execute("""
                SELECT COUNT(*) AS qtd_orcamentos
                FROM cotacoes;
            """)
        else:
            cursor.execute("""
                SELECT COUNT(*) AS qtd_orcamentos
                FROM cotacoes
                WHERE data_cotacao >= CURRENT_DATE - (%s * INTERVAL '1' DAY);
            """, (int(dias),))

        resultado = cursor.fetchone()

        if resultado is None:
            return {"qtd_orcamentos": 0}

        return {
            "qtd_orcamentos": resultado[0]
        }

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de orçamentos feitos:", e)
        return {"qtd_orcamentos": 0}

def apolices_vencidas(dias=None):
    try:
        if dias is None or str(dias).strip() == "":
            cursor.execute("""
                SELECT COUNT(*) AS qtd_apolices_vencidas
                FROM apolice
                WHERE fim < CURRENT_DATE;
            """)
        else:
            cursor.execute("""
                SELECT COUNT(*) AS qtd_apolices_vencidas
                FROM apolice
                WHERE fim < CURRENT_DATE
                AND fim >= CURRENT_DATE - (%s * INTERVAL '1' DAY);
            """, (int(dias),))

        resultado = cursor.fetchone()

        if resultado is None:
            return {"qtd_apolices_vencidas": 0}

        return {
            "qtd_apolices_vencidas": resultado[0]
        }

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de apólices vencidas:", e)
        return {"qtd_apolices_vencidas": 0}

def apolices_vencendo(dias=None):
    try:
        if dias is None or str(dias).strip() == "":
            dias = 30

        cursor.execute("""
            SELECT COUNT(*) AS qtd_apolices_vencendo
            FROM apolice
            WHERE fim >= CURRENT_DATE
            AND fim <= CURRENT_DATE + (%s * INTERVAL '1' DAY);
        """, (int(dias),))

        resultado = cursor.fetchone()

        if resultado is None:
            return {"qtd_apolices_vencendo": 0}

        return {
            "qtd_apolices_vencendo": resultado[0]
        }

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de apólices vencendo:", e)
        return {"qtd_apolices_vencendo": 0}

def contrato_por_seguradora():
    try:
        cursor.execute("""
            SELECT
                s.nome_fantasia AS seguradora,
                COUNT(a.id_apolice) AS qtd_contratos
            FROM apolice a
            JOIN cotacoes c
                USING(id_cotacao)
            JOIN seguradora s
                USING(id_seguradora)
            GROUP BY s.nome_fantasia
            ORDER BY qtd_contratos DESC;
        """)

        resultados = cursor.fetchall()
        contratantes = []

        for resultado in resultados:
            contratante = {
                "seguradora": resultado[0],
                "qtd_contratos": resultado[1]
            }
            contratantes.append(contratante)

        return contratantes

    except Exception as e:
        conn.rollback()
        print("Erro ao buscar indicador de contratos por seguradora:", e)
        return []
