from faker import Faker
import random
from datetime import timedelta

#Configura o Faker para o padrão brasileiro
fake = Faker('pt_BR')

#Nome do arquivo que será gerado
arquivo_sql = '02_carga_dados_massivos.sql'

print("Iniciando a geração de dados...")

with open(arquivo_sql, 'w', encoding='utf-8') as f:
    f.write("-- Arquivo gerado automaticamente para o projeto da faculdade\n")
    f.write("-- Limpa as tabelas existentes e reinicia os IDs (Evita duplicação ao rodar várias vezes)\n")
    f.write("TRUNCATE TABLE Apolice, Cotacoes, Bens, Plano, Seguradora, Pessoa RESTART IDENTITY CASCADE;\n\n")

    #Gerar Seguradoras
    print("Gerando Seguradoras...")
    f.write("-- INSERTS DE SEGURADORAS\n")
    seguradoras = [
        (1, 'Porto Seguro', '61198164000160', '1133334444'),
        (2, 'SulAmérica', '01938018000156', '1155556666'),
        (3, 'Bradesco Seguros', '33055146000193', '08007279966'),
        (4, 'Allianz', '06193425000133', '08000153366')
    ]
    for seg in seguradoras:
        f.write(
            f"INSERT INTO Seguradora (nome_fantasia, cnpj, telefone_suporte) VALUES ('{seg[1]}', '{seg[2]}', '{seg[3]}');\n")

    #Gerar Planos
    print("Gerando Planos...")
    f.write("\n-- INSERTS DE PLANOS\n")
    planos = [
        {'id': 1, 'id_seg': 1, 'tipo': 'Veículo', 'nome': 'Porto Auto Premium'},
        {'id': 2, 'id_seg': 2, 'tipo': 'Vida', 'nome': 'SulAmérica Vida Família'},
        {'id': 3, 'id_seg': 3, 'tipo': 'Imóvel', 'nome': 'Bradesco Residencial'},
        {'id': 4, 'id_seg': 4, 'tipo': 'Eletrônicos', 'nome': 'Allianz Celular Seguro'}
    ]
    for p in planos:
        f.write(
            f"INSERT INTO Plano (id_seguradora, tipo_cobertura, nome_plano) VALUES ({p['id_seg']}, '{p['tipo']}', '{p['nome']}');\n")

    #Gerar Pessoas (1000 registros)
    print("Gerando 100 Pessoas...")
    f.write("\n-- INSERTS DE PESSOAS\n")
    for id_pessoa in range(1, 101):
        cpf = fake.cpf().replace('.', '').replace('-', '')
        nome = fake.name().replace("'", "''")  # O replace evita erro no SQL se o nome tiver apóstrofo (ex: D'Angelo)
        email = fake.ascii_free_email()
        sexo = random.choice(['M', 'F'])
        telefone = fake.msisdn()[:11]
        nascimento = fake.date_of_birth(minimum_age=18, maximum_age=80)
        status = random.choices(['Ativo', 'Inativo'], weights=[85, 15])[0]  # 85% de chance de ser Ativo

        f.write(
            f"INSERT INTO Pessoa (cpf_cnpj, nome_completo, email, sexo, telefone, data_nascimento, status) VALUES ('{cpf}', '{nome}', '{email}', '{sexo}', '{telefone}', '{nascimento}', '{status}');\n")

    #Gerar Bens, Cotações e Apólices dinamicamente
    print("Cruzando dados (Bens, Cotações e Apólices)...")
    f.write("\n-- INSERTS DE BENS, COTAÇÕES E APÓLICES\n")

    id_cotacao_global = 1

    #Para cada pessoa gerada criar os dados complementares
    for id_pessoa in range(1, 101):

        #Cada pessoa tem de 1 a 3 bens
        num_bens = random.randint(1, 3)
        for _ in range(num_bens):
            tipo_bem = random.choice(['Veículo', 'Imóvel', 'Eletrônico', 'Vida'])
            descricao = f"Bem protegido - {fake.word().capitalize()}"
            valor = round(random.uniform(2000.00, 3500.00), 2)
            f.write(
                f"INSERT INTO Bens (id_pessoa, tipo_bem, descricao_bem, valor_estimado) VALUES ({id_pessoa}, '{tipo_bem}', '{descricao}', {valor});\n")

        #70% de chance da pessoa ter feito uma cotação
        if random.random() < 0.7:
            plano_escolhido = random.choice(planos)
            valor_cot = round(random.uniform(500.00, 8000.00), 2)
            data_cot = fake.date_between(start_date='-1y', end_date='today')

            f.write(
                f"INSERT INTO Cotacoes (id_pessoa, id_seguradora, id_plano, valor_cotacao, data_cotacao) VALUES ({id_pessoa}, {plano_escolhido['id_seg']}, {plano_escolhido['id']}, {valor_cot}, '{data_cot}');\n")

            #50% de chance da cotação ter virado uma Apólice real
            if random.random() < 0.5:
                inicio_apolice = data_cot + timedelta(days=random.randint(1, 15))
                fim_apolice = inicio_apolice + timedelta(days=365)  # 1 ano de validade
                f.write(
                    f"INSERT INTO Apolice (id_cotacao, inicio, fim) VALUES ({id_cotacao_global}, '{inicio_apolice}', '{fim_apolice}');\n")

            id_cotacao_global += 1

print(f"\nSucesso! Arquivo '{arquivo_sql}' gerado.")
