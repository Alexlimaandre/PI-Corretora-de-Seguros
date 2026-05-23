from conn import conexao, fim_conexao

conn = conexao()
cursor = conn.cursor()


# CREATE - Pessoa
def create_pessoa(cpf, nome, email, sexo, telefone, data_nasc, status):
    
    try:
        cursor.execute(
            "INSERT INTO pessoa (cpf, nome, email, sexo, telefone, data_nasc, status) VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (cpf, nome, email, sexo, telefone, data_nasc, status)
        )
        conn.commit()
        print("Pessoa criada com sucesso!")
    except Exception as e:
        print("Erro ao criar pessoa:", e)


# CREATE - Apólice
def create_apolice(cotacao, inicio, fim):
    try:
        cursor.execute(
            "INSERT INTO apolice (cotacao, inicio, fim) VALUES (%s, %s, %s)",
            (cotacao, inicio, fim)
        )
        conn.commit()
        print("Apólice criada com sucesso!")
    except Exception as e:
        print("Erro ao criar apólice:", e)


# CREATE - Bens
def create_bens(id_pessoa, bem, desc_bem, valor_estimado):
    try:
        cursor.execute(
            "INSERT INTO bens (id_pessoa, bem, desc_bem, valor_estimado) VALUES (%s, %s, %s, %s)",
            (id_pessoa, bem, desc_bem, valor_estimado)
        )
        conn.commit()
        print("Bem criado com sucesso!")
    except Exception as e:
        print("Erro ao criar bem:", e)


# CREATE - Cotação
def create_cotacao(id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao):
    try:
        cursor.execute(
            "INSERT INTO cotacao (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao) VALUES (%s, %s, %s, %s, %s)",
            (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao)
        )
        conn.commit()
        print("Cotação criada com sucesso!")
    except Exception as e:
        print("Erro ao criar cotação:", e)


# CREATE - Plano
def create_plano(id_seguradora, tipo_cobertura, nome_plano):
    try:
        cursor.execute(
            "INSERT INTO plano (id_seguradora, tipo_cobertura, nome_plano) VALUES (%s, %s, %s)",
            (id_seguradora, tipo_cobertura, nome_plano)
        )
        conn.commit()
        print("Plano criado com sucesso!")
    except Exception as e:
        print("Erro ao criar plano:", e)


# CREATE - Seguradora
def create_seguradora(nome_fant, cnpj, tel_suporte):
    try:
        cursor.execute(
            "INSERT INTO seguradora (nome_fant, cnpj, tel_suporte) VALUES (%s, %s, %s)",
            (nome_fant, cnpj, tel_suporte)
        )
        conn.commit()
        print("Seguradora criada com sucesso!")
    except Exception as e:
        print("Erro ao criar seguradora:", e)

# ============= // ============= #

# READ - Pessoa
def read_pessoa(cpf):
    try:
        conexao()
        cursor.execute("SELECT * FROM pessoa WHERE cpf_cnpj = %s", (cpf,))
        pessoa = cursor.fetchone()

        if pessoa:
            print("Pessoa encontrada:", pessoa)
        else:
            print("Pessoa não encontrada.")
        fechar_conexao(conexao())

    except Exception as e:
        print("Erro ao ler pessoa:", e)


def read_todas_pessoas():
    try:
        conexao()
        cursor.execute("SELECT * FROM pessoa")
        pessoas = cursor.fetchall()

        for i in pessoas:
            print(i)
            
        fechar_conexao()

    except Exception as e:
        print("Erro ao ler todas as pessoas:", e)


# READ - Apólice
def read_apolice(id_apolice):
    try:
        cursor.execute(
            "SELECT * FROM apolice WHERE id_apolice = %s",
            (id_apolice,)
        )
        apolice = cursor.fetchone()

        if apolice:
            print("Apólice encontrada:", apolice)
        else:
            print("Apólice não encontrada.")

    except Exception as e:
        print("Erro ao ler apólice:", e)


def read_todas_apolices():
    try:
        cursor.execute("SELECT * FROM apolice")
        apolices = cursor.fetchall()

        for i in apolices:
            print(i)

    except Exception as e:
        print("Erro ao ler todas as apólices:", e)


# READ - Bens
def read_bens(id_pessoa):
    try:
        cursor.execute(
            "SELECT * FROM bens WHERE id_pessoa = %s",
            (id_pessoa,)
        )
        bens = cursor.fetchall()

        if bens:
            print("Bens encontrados:", bens)
        else:
            print("Nenhum bem encontrado para essa pessoa.")

    except Exception as e:
        print("Erro ao ler bens:", e)


def read_todos_bens():
    try:
        cursor.execute("SELECT * FROM bens")
        bens = cursor.fetchall()

        for i in bens:
            print(i)

    except Exception as e:
        print("Erro ao ler todos os bens:", e)


# READ - Cotação por pessoa
def read_cotacao_por_pessoa(id_pessoa):
    try:
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


# READ - Cotação por ID
def read_cotacao(id_cotacao):
    try:
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


def read_todas_cotacoes():
    try:
        cursor.execute("SELECT * FROM cotacao")
        cotacoes = cursor.fetchall()

        for i in cotacoes:
            print(i)

    except Exception as e:
        print("Erro ao ler todas as cotações:", e)


# READ - Plano
def read_plano(id_plano):
    try:
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


def read_todos_planos():
    try:
        cursor.execute("SELECT * FROM plano")
        planos = cursor.fetchall()

        for i in planos:
            print(i)

    except Exception as e:
        print("Erro ao ler todos os planos:", e)


# READ - Seguradora
def read_seguradora(id_seguradora):
    try:
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


def read_todas_seguradoras():
    try:
        cursor.execute("SELECT * FROM seguradora")
        seguradoras = cursor.fetchall()

        for i in seguradoras:
            print(i)

    except Exception as e:
        print("Erro ao ler todas as seguradoras:", e)

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
    try:
        cursor.execute(
            "DELETE FROM pessoa WHERE cpf = %s",
            (cpf,)
        )
        conn.commit()
        print("Pessoa deletada com sucesso!")

    except Exception as e:
        print("Erro ao deletar pessoa:", e)


# DELETE - Seguradora
def delete_seguradora(id_seguradora):
    try:
        cursor.execute(
            "DELETE FROM seguradora WHERE id_seguradora = %s",
            (id_seguradora,)
        )
        conn.commit()
        print("Seguradora deletada com sucesso!")

    except Exception as e:
        print("Erro ao deletar seguradora:", e)


# DELETE - Cotação
def delete_cotacao(id_cotacao):
    try:
        cursor.execute(
            "DELETE FROM cotacao WHERE id_cotacao = %s",
            (id_cotacao,)
        )
        conn.commit()
        print("Cotação deletada com sucesso!")

    except Exception as e:
        print("Erro ao deletar cotação:", e)


# DELETE - Bem
def delete_bem(id_bem):
    try:
        cursor.execute(
            "DELETE FROM bens WHERE id_bem = %s",
            (id_bem,)
        )
        conn.commit()
        print("Bem deletado com sucesso!")

    except Exception as e:
        print("Erro ao deletar bem:", e)


# DELETE - Plano
def delete_plano(id_plano):
    try:
        cursor.execute(
            "DELETE FROM plano WHERE id_plano = %s",
            (id_plano,)
        )
        conn.commit()
        print("Plano deletado com sucesso!")

    except Exception as e:
        print("Erro ao deletar plano:", e)


# DELETE - Apólice
def delete_apolice(id_apolice):
    try:
        cursor.execute(
            "DELETE FROM apolice WHERE id_apolice = %s",
            (id_apolice,)
        )
        conn.commit()
        print("Apólice deletada com sucesso!")

    except Exception as e:
        print("Erro ao deletar apólice:", e)

# ============= // ============= #


def fechar_conexao():
    global conn, cursor

    if cursor:
        cursor.close()

    if conn:
        fim_conexao(conn)

    print("Conexão finalizada.")
    
    
read_pessoa(str(62034589106))