CREATE DATABASE Frank_Costa;

CREATE TABLE Pessoa (
                        id_pessoa SERIAL PRIMARY KEY,
                        cpf_cnpj VARCHAR(14) NOT NULL,
                        nome_completo VARCHAR(100) NOT NULL,
                        email VARCHAR(50) NOT NULL,
                        sexo CHAR(1) NOT NULL,
                        telefone VARCHAR(11) NOT NULL,
                        data_nascimento DATE NOT NULL,
                        status VARCHAR(10) NOT NULL
);

SELECT id_pessoa, nome_completo, email, sexo, telefone, TO_CHAR(data_nascimento, 'DD/MM/YYYY') AS data_nascimento, status FROM Pessoa;

CREATE TABLE Bens (
                      id_bem SERIAL PRIMARY KEY,
                      id_pessoa INT NOT NULL,
                      tipo_bem VARCHAR(10) NOT NULL,
                      descricao_bem VARCHAR(100) NOT NULL,
                      valor_estimado NUMERIC(10, 2) NOT NULL,
                      FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id_pessoa)
);

CREATE TABLE Seguradora (
                            id_seguradora SERIAL PRIMARY KEY,
                            nome_fantasia VARCHAR(100),
                            cnpj VARCHAR(14) NOT NULL, -- Alterado para VARCHAR para preservar zeros à esquerda
                            telefone_suporte VARCHAR(11) NOT NULL -- Alterado para VARCHAR pela mesma razão
);

CREATE TABLE Plano (
                       id_plano SERIAL PRIMARY KEY,
                       id_seguradora INT,
                       tipo_cobertura VARCHAR(100) NOT NULL,
                       nome_plano VARCHAR(100) NOT NULL,
                       FOREIGN KEY (id_seguradora) REFERENCES Seguradora(id_seguradora)
);

CREATE TABLE Cotacoes (
                          id_cotacao SERIAL PRIMARY KEY,
                          id_pessoa INT,
                          id_seguradora INT,
                          id_plano INT,
                          valor_cotacao DECIMAL(10, 2) NOT NULL, -- DECIMAL é mais preciso que FLOAT para valores financeiros
                          data_cotacao DATE NOT NULL,
                          FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id_pessoa),
                          FOREIGN KEY (id_seguradora) REFERENCES Seguradora(id_seguradora),
                          FOREIGN KEY (id_plano) REFERENCES Plano(id_plano)
);

CREATE TABLE Apolice (
                         id_apolice SERIAL PRIMARY KEY,
                         id_cotacao INT,
                         inicio DATE NOT NULL,
                         fim DATE NOT NULL,
                         FOREIGN KEY (id_cotacao) REFERENCES Cotacoes(id_cotacao)
);

