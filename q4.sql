WITH

-- Armazena os CPFs duplicados em uma CTE, com base na consulta do Problema 3
cpfs_duplicados AS (
    SELECT cpf
    FROM stg_prontuario.PACIENTE
    GROUP BY cpf
    HAVING COUNT(cpf) > 1 -- realiza COUNT após o agrupamento, identificando quais CPFs aparecem mais de uma vez
)

-- Apresenta apenas os registros mais recentes dos pacientes com CPFs duplicados
SELECT p.*,
    ROW_NUMBER() OVER( -- cria ranking entre os CPFs duplicados, utilizando a data de atualização como parâmetro para encontrar os mais recentes
        PARTITION BY cpf
        ORDER BY dt_atualizacao DESC
    ) AS ranking_mais_recente
FROM stg_prontuario.PACIENTE p
INNER JOIN cpfs_duplicados c -- mantém apenas os registros de paciente com CPFs dentre os CPFs duplicados
ON p.cpf = c.cpf
WHERE ranking_mais_recente = 1 -- após ordenar decrescentemente cada partição de CPF, basta selecionar o primeiro lugar do ranking para ter o registo mais recente