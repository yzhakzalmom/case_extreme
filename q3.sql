SELECT cpf, COUNT(cpf) AS quantidade -- Utiliza COUNT(cpf) em vez de COUNT(*) porque trata-se de uma coluna NOT NULL
FROM stg_prontuario.PACIENTE
GROUP BY cpf
HAVING COUNT(cpf) > 1 -- Realiza COUNT após o agrupamento, identificando quais CPFs aparecem mais de uma vez
ORDER BY quantidade DESC