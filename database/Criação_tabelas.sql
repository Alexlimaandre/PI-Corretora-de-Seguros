SET DATESTYLE TO POSTGRES, DMY;

DROP TABLE IF EXISTS Pessoa CASCADE;
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

DROP TABLE IF EXISTS Bens CASCADE;
CREATE TABLE Bens (
    id_bem SERIAL PRIMARY KEY,
    id_pessoa INT NOT NULL,
    tipo_bem VARCHAR(10) NOT NULL,
    descricao_bem VARCHAR(100) NOT NULL,
    valor_estimado NUMERIC(10, 2) NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id_pessoa)
        ON DELETE CASCADE
            ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Seguradora CASCADE;
CREATE TABLE Seguradora (
    id_seguradora SERIAL PRIMARY KEY,
    nome_fantasia VARCHAR(100),
    cnpj VARCHAR(14) NOT NULL,
    telefone_suporte VARCHAR(11) NOT NULL
);

DROP TABLE IF EXISTS Plano CASCADE;
CREATE TABLE Plano (
    id_plano SERIAL PRIMARY KEY,
    id_seguradora INT,
    tipo_cobertura VARCHAR(100) NOT NULL,
    nome_plano VARCHAR(100) NOT NULL,
    FOREIGN KEY (id_seguradora) REFERENCES Seguradora(id_seguradora)
        ON DELETE CASCADE
            ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Cotacoes CASCADE;
CREATE TABLE Cotacoes (
    id_cotacao SERIAL PRIMARY KEY,
    id_pessoa INT,
    id_seguradora INT,
    id_plano INT,
    valor_cotacao DECIMAL(10, 2) NOT NULL,
    data_cotacao DATE NOT NULL,
    FOREIGN KEY (id_pessoa) REFERENCES Pessoa(id_pessoa)
        ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (id_seguradora) REFERENCES Seguradora(id_seguradora)
        ON DELETE CASCADE
            ON UPDATE CASCADE,
    FOREIGN KEY (id_plano) REFERENCES Plano(id_plano)
        ON DELETE CASCADE
            ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Apolice CASCADE;
CREATE TABLE Apolice (
    id_apolice SERIAL PRIMARY KEY,
    id_cotacao INT,
    inicio DATE NOT NULL,
    fim DATE NOT NULL,
    FOREIGN KEY (id_cotacao) REFERENCES Cotacoes(id_cotacao)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);

DROP TABLE IF EXISTS Usuario CASCADE;
CREATE TABLE Usuario (
    id_usuario SERIAL PRIMARY KEY,
    nome_usuario VARCHAR(50) NOT NULL UNIQUE,
    senha VARCHAR(100) NOT NULL
);

ALTER TABLE Cotacoes ADD COLUMN status_cotacao VARCHAR(20) DEFAULT 'Pendente';

-----Trigger------
CREATE OR REPLACE FUNCTION fn_gerar_apolice_automatica()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.status_cotacao = 'Aprovada' AND OLD.status_cotacao <> 'Aprovada' THEN
        INSERT INTO Apolice (
            id_cotacao,
            inicio,
            fim
        ) VALUES (
            NEW.id_cotacao, 
            CURRENT_DATE,                  
            CURRENT_DATE + INTERVAL '1 year'                      
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_aprovar_cotacao
AFTER UPDATE OF status_cotacao ON Cotacoes
FOR EACH ROW
EXECUTE FUNCTION fn_gerar_apolice_automatica();