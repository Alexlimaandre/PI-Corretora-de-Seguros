
erDiagram
    PESSOA ||--o{ BENS : "possui"
    PESSOA ||--o{ COTACOES : "solicita"
    SEGURADORA ||--o{ PLANO : "oferece"
    SEGURADORA ||--o{ COTACOES : "emite"
    PLANO ||--o{ COTACOES : "referencia"
    COTACOES ||--o| APOLICE : "gera"

    PESSOA {
        int id_pessoa PK
        varchar(14) cpf_cnpj
        varchar(100) nome_completo
        varchar(50) email
        char(1) sexo
        varchar(11) telefone
        date data_nascimento
        varchar(10) status
    }
    BENS {
        int id_bem PK
        int id_pessoa FK
        varchar(10) tipo_bem
        varchar(100) descricao_bem
        numeric(10_2) valor_estimado
    }
    SEGURADORA {
        int id_seguradora PK
        varchar(100) nome_fantasia
        varchar(14) cnpj
        varchar(11) telefone_suporte
    }
    PLANO {
        int id_plano PK
        int id_seguradora FK
        varchar(100) tipo_cobertura
        varchar(100) nome_plano
    }
    COTACOES {
        int id_cotacao PK
        int id_pessoa FK
        int id_seguradora FK
        int id_plano FK
        decimal(10_2) valor_cotacao
        date data_cotacao
        varchar(20) status_cotacao
    }
    APOLICE {
        int id_apolice PK
        int id_cotacao FK
        date inicio
        date fim
    }
    USUARIO {
        int id_usuario PK
        varchar(50) nome_usuario
        varchar(100) senha
    }
