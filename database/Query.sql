SELECT
    p.nome_completo AS "Cliente",
    p.cpf_cnpj AS "Documento",
    s.nome_fantasia AS "Seguradora",
    pl.nome_plano AS "Plano Simulado",
    c.valor_cotacao AS "Valor (R$)",
    c.data_cotacao AS "Data da Cotação"
FROM Cotacoes c
         INNER JOIN Pessoa p ON c.id_pessoa = p.id_pessoa
         INNER JOIN Plano pl ON c.id_plano = pl.id_plano
         INNER JOIN Seguradora s ON c.id_seguradora = s.id_seguradora
ORDER BY c.valor_cotacao DESC
LIMIT 20;