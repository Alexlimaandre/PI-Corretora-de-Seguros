from conn import conexao, fechar_conexao

conn = conexao()
cursor = conn.cursor()


# CREATE - Pessoa
def create_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
    global conn, cursor
    try:
        conn
        cursor.execute(
            "INSERT INTO pessoa (cpf, nome, email, sexo, telefone, data_nasc, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (cpf, nome, email, sexo, telefone, data_nasc, status)
        )
        conn.commit()
        print("Pessoa criada com sucesso!")

    except Exception as e:
        print("Erro ao criar pessoa:", e)
        
    finally:
        cursor.close()
        fechar_conexao(conn)


# CREATE - Apólice
def create_apolice(cotacao, inicio, fim):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "INSERT INTO apolice (cotacao, inicio, fim) VALUES (%s, %s, %s)",
            (cotacao, inicio, fim)
        )
        conn.commit()
        print("Apólice criada com sucesso!")
        fechar_conexao(conn)
        
    except Exception as e:
        print("Erro ao criar apólice:", e)
    
    finally:
        cursor.close()
        fechar_conexao(conn)


# CREATE - Bens
def create_bens(id_pessoa, bem, desc_bem, valor_estimado):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "INSERT INTO bens (id_pessoa, bem, desc_bem, valor_estimado) VALUES (%s, %s, %s, %s)",
            (id_pessoa, bem, desc_bem, valor_estimado)
        )
        conn.commit()
        print("Bem criado com sucesso!")
        fechar_conexao(conn)
        
    except Exception as e:
        print("Erro ao criar bem:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)

# CREATE - Cotação
def create_cotacao(id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "INSERT INTO cotacao (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao) VALUES (%s, %s, %s, %s, %s)",
            (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao)
        )
        conn.commit()
        print("Cotação criada com sucesso!")
        fechar_conexao(conn)
        
    except Exception as e:
        print("Erro ao criar cotação:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# CREATE - Plano
def create_plano(id_seguradora, tipo_cobertura, nome_plano):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "INSERT INTO plano (id_seguradora, tipo_cobertura, nome_plano) VALUES (%s, %s, %s)",
            (id_seguradora, tipo_cobertura, nome_plano)
        )
        conn.commit()
        print("Plano criado com sucesso!")
        fechar_conexao(conn)
        
    except Exception as e:
        print("Erro ao criar plano:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# CREATE - Seguradora
def create_seguradora(nome_fant, cnpj, tel_suporte):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "INSERT INTO seguradora (nome_fant, cnpj, tel_suporte) VALUES (%s, %s, %s)",
            (nome_fant, cnpj, tel_suporte)
        )
        conn.commit()
        print("Seguradora criada com sucesso!")
        fechar_conexao(conn)
        
    except Exception as e:
        print("Erro ao criar seguradora:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)

# ============= // ============= #

# READ - Pessoa
def read_pessoa(cpf):
    global conn, cursor
    try:
        conexao()
        cursor.execute("SELECT * FROM pessoa WHERE cpf_cnpj = %s", (cpf,))
        pessoa = cursor.fetchone()

        if pessoa:
            print("Pessoa encontrada:", pessoa)
        else:
            print("Pessoa não encontrada.")
        fechar_conexao(conn)

    except Exception as e:
        print("Erro ao ler pessoa:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


def read_todas_pessoas():
    global conn, cursor
    try:
        conexao()
        cursor.execute("SELECT * FROM pessoa")
        pessoas = cursor.fetchall()

        for i in pessoas:
            print(i)
            
        fechar_conexao(conn)

    except Exception as e:
        print("Erro ao ler todas as pessoas:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# READ - Apólice
def read_apolice(id_apolice):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "SELECT * FROM apolice WHERE id_apolice = %s",
            (id_apolice,)
        )
        apolice = cursor.fetchone()

        if apolice:
            print("Apólice encontrada:", apolice)
        else:
            print("Apólice não encontrada.")
        fechar_conexao(conn)

    except Exception as e:
        print("Erro ao ler apólice:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


def read_todas_apolices():
    global conn, cursor
    try:
        conexao()
        cursor.execute("SELECT * FROM apolice")
        apolices = cursor.fetchall()

        for i in apolices:
            print(i)
        
        fechar_conexao(conn)
        

    except Exception as e:
        print("Erro ao ler todas as apólices:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# READ - Bens
def read_bens(id_pessoa):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "SELECT * FROM bens WHERE id_pessoa = %s",
            (id_pessoa,)
        )
        bens = cursor.fetchall()

        if bens:
            print("Bens encontrados:", bens)
        else:
            print("Nenhum bem encontrado para essa pessoa.")
        fechar_conexao(conn)
        

    except Exception as e:
        print("Erro ao ler bens:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


def read_todos_bens():
    global conn, cursor
    try:
        conexao()
        cursor.execute("SELECT * FROM bens")
        bens = cursor.fetchall()

        for i in bens:
            print(i)
        fechar_conexao(conn)
        

    except Exception as e:
        print("Erro ao ler todos os bens:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# READ - Cotação por pessoa
def read_cotacao_por_pessoa(id_pessoa):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "SELECT * FROM cotacao WHERE id_pessoa = %s",
            (id_pessoa,)
        )
        cotacoes = cursor.fetchall()

        if cotacoes:
            print("Cotações encontradas:", cotacoes)
        else:
            print("Nenhuma cotação encontrada para essa pessoa.")

    except Exception as e:
        print("Erro ao ler cotações:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# READ - Cotação por ID
def read_cotacao(id_cotacao):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "SELECT * FROM cotacao WHERE id_cotacao = %s",
            (id_cotacao,)
        )
        cotacao = cursor.fetchone()

        if cotacao:
            print("Cotação encontrada:", cotacao)
        else:
            print("Cotação não encontrada.")

    except Exception as e:
        print("Erro ao ler cotação:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


def read_todas_cotacoes():
    global conn, cursor
    try:
        conexao()
        cursor.execute("SELECT * FROM cotacao")
        cotacoes = cursor.fetchall()

        for i in cotacoes:
            print(i)

    except Exception as e:
        print("Erro ao ler todas as cotações:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# READ - Plano
def read_plano(id_plano):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "SELECT * FROM plano WHERE id_plano = %s",
            (id_plano,)
        )
        plano = cursor.fetchone()

        if plano:
            print("Plano encontrado:", plano)
        else:
            print("Plano não encontrado.")

    except Exception as e:
        print("Erro ao ler plano:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


def read_todos_planos():
    global conn, cursor
    try:
        conexao()
        cursor.execute("SELECT * FROM plano")
        planos = cursor.fetchall()

        for i in planos:
            print(i)

    except Exception as e:
        print("Erro ao ler todos os planos:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# READ - Seguradora
def read_seguradora(id_seguradora):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "SELECT * FROM seguradora WHERE id_seguradora = %s",
            (id_seguradora,)
        )
        seguradora = cursor.fetchone()

        if seguradora:
            print("Seguradora encontrada:", seguradora)
        else:
            print("Seguradora não encontrada.")

    except Exception as e:
        print("Erro ao ler seguradora:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


def read_todas_seguradoras():
    global conn, cursor
    try:
        conexao()
        cursor.execute("SELECT * FROM seguradora")
        seguradoras = cursor.fetchall()

        for i in seguradoras:
            print(i)

    except Exception as e:
        print("Erro ao ler todas as seguradoras:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)

# ============= // ============= #


# UPDATE
# def update_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
# def update_seguradora(id_seguradora, nome_fant, cnpj, tel_suporte):
# def update_cotacao(id_cotacao, id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao):
# def update_bem(id_bem, id_pessoa, bem, desc_bem, valor_estimado):
# def update_plano(id_plano, id_seguradora, tipo_cobertura, nome_plano):
# def update_apolice(id_apolice, cotacao, inicio, fim):


# DELETE - Pessoa
def delete_pessoa(cpf):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "DELETE FROM pessoa WHERE cpf = %s",
            (cpf,)
        )
        conn.commit()
        print("Pessoa deletada com sucesso!")

    except Exception as e:
        print("Erro ao deletar pessoa:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# DELETE - Seguradora
def delete_seguradora(id_seguradora):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "DELETE FROM seguradora WHERE id_seguradora = %s",
            (id_seguradora,)
        )
        conn.commit()
        print("Seguradora deletada com sucesso!")

    except Exception as e:
        print("Erro ao deletar seguradora:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# DELETE - Cotação
def delete_cotacao(id_cotacao):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "DELETE FROM cotacao WHERE id_cotacao = %s",
            (id_cotacao,)
        )
        conn.commit()
        print("Cotação deletada com sucesso!")

    except Exception as e:
        print("Erro ao deletar cotação:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# DELETE - Bem
def delete_bem(id_bem):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "DELETE FROM bens WHERE id_bem = %s",
            (id_bem,)
        )
        conn.commit()
        print("Bem deletado com sucesso!")

    except Exception as e:
        print("Erro ao deletar bem:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# DELETE - Plano
def delete_plano(id_plano):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "DELETE FROM plano WHERE id_plano = %s",
            (id_plano,)
        )
        conn.commit()
        print("Plano deletado com sucesso!")

    except Exception as e:
        print("Erro ao deletar plano:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)


# DELETE - Apólice
def delete_apolice(id_apolice):
    global conn, cursor
    try:
        conexao()
        cursor.execute(
            "DELETE FROM apolice WHERE id_apolice = %s",
            (id_apolice,)
        )
        conn.commit()
        print("Apólice deletada com sucesso!")

    except Exception as e:
        print("Erro ao deletar apólice:", e)
    finally:
        cursor.close()
        fechar_conexao(conn)

# ============= // ============= #

    
    
# read_pessoa(str(20391876503))
read_todas_pessoas()

