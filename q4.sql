WITH

-- Armazena os CPFs duplicados em uma CTE, com base na consulta do Problema 3
cpfs_duplicados AS (
    SELECT cpf
    FROM stg_prontuario.PACIENTE
    GROUP BY cpf
    HAVING COUNT(cpf) > 1 -- realiza COUNT após o agrupamento, identificando quais CPFs aparecem mais de uma vez
),

-- Armazena um ranking com as datas de atualização mais recentes para cada cpf
pacientes_rankeados AS (
    SELECT 
        p.*,
        ROW_NUMBER() OVER (-- cria ranking entre os CPFs duplicados, utilizando a data de atualização como parâmetro para encontrar os mais recentes
            PARTITION BY p.cpf
            ORDER BY p.dt_atualizacao DESC
        ) AS ranking_mais_recente
    FROM stg_prontuario.PACIENTE p
    INNER JOIN cpfs_duplicados c -- mantém apenas os registros de paciente com CPFs dentre os CPFs duplicados
    ON p.cpf = c.cpf
)

SELECT *
FROM pacientes_rankeados
WHERE ranking_mais_recente = 1;