# Sistema Gerencial para Corretora de Seguros

## Sobre o Projeto

O Sistema Gerencial para Corretora de Seguros foi desenvolvido em parceria com a **Frank Costa Corretora de Seguros LTDA**, com o objetivo de auxiliar na organização e gestão das operações internas da empresa.

O projeto busca centralizar informações de clientes, seguradoras, planos, bens segurados, cotações e apólices, proporcionando maior controle dos dados e agilidade nos processos administrativos.

Além disso, o sistema contribui para a redução da desorganização causada pelo uso de controles descentralizados, permitindo uma visualização mais clara das informações necessárias para o dia a dia da corretora.

---

## Objetivos

* Centralizar o gerenciamento de clientes.
* Organizar o cadastro de seguradoras e planos.
* Controlar bens vinculados aos clientes.
* Registrar e acompanhar cotações de seguros.
* Gerenciar apólices de forma eficiente.
* Automatizar processos através de regras de negócio implementadas no banco de dados.
* Facilitar consultas e atualizações das informações da corretora.

---

## Funcionalidades

### Clientes

* Cadastro de clientes.
* Consulta de clientes.
* Atualização de informações.
* Remoção de registros.

### Seguradoras

* Cadastro de seguradoras.
* Consulta de seguradoras.
* Atualização de informações.
* Remoção de registros.

### Planos

* Cadastro de planos de seguro.
* Associação de planos às seguradoras.
* Consulta e atualização de dados.

### Bens

* Cadastro de bens segurados.
* Associação de bens aos clientes.
* Consulta e atualização de registros.

### Cotações

* Registro de cotações.
* Consulta de propostas.
* Atualização de status.
* Aprovação de cotações.

### Apólices

* Consulta de apólices.
* Atualização de informações.
* Controle de vigência.
* Geração automática de apólices após aprovação de cotações.

---

## Tecnologias Utilizadas

### Linguagem

* Python

### Interface Gráfica

* CustomTkinter

### Banco de Dados

* PostgreSQL

### Bibliotecas

* psycopg2
* python-dotenv
* customtkinter

---

## Estrutura do Banco de Dados

O banco de dados é composto pelas seguintes entidades:

* Pessoa
* Bens
* Seguradora
* Plano
* Cotações
* Apólice

As tabelas foram modeladas para representar o fluxo operacional de uma corretora de seguros, permitindo o relacionamento entre clientes, produtos e contratos.

---

## Regra de Negócio Implementada

O sistema possui uma trigger no PostgreSQL responsável por gerar automaticamente uma apólice quando uma cotação tem seu status alterado para **Aprovada**.

Fluxo:

Cliente → Cotação → Aprovação → Geração Automática da Apólice

---

## Equipe de Desenvolvimento

* Alexandre Lima André
* Cleverson Alves
* Gabriel William
* Jonata Augusto
* Matheus Nascimento

---

## Parceiro do Projeto

**Frank Costa Corretora de Seguros LTDA**

Projeto acadêmico desenvolvido com foco na aplicação prática de conceitos de Banco de Dados, Programação e Desenvolvimento de Sistemas.
