SELECT cpf, COUNT(*) AS quantidade
FROM stg_prontuario.PACIENTE
GROUP BY cpf
HAVING COUNT(*) > 1 -- Realiza COUNT após o agrupamento, identificando quais CPFs aparecem mais de uma vez
ORDER BY quantidade DESC