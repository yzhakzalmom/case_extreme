-- Cria CTE que relaciona atendimentos e prescrições, filtrando apenas as urgências
WITH urgencias AS (
    SELECT a.id, COUNT(pa.id_prescricao) AS qtd_prescricoes
    FROM ATENDIMENTOS a
    LEFT JOIN PRESCRICAO_ATENDIMENTOS pa -- realiza LEFT JOIN para não perder os atendimentos em que não houve prescrição, pois devem ser contados
    ON a.id = pa.id_atend
    WHERE a.tp_atend = 'U'
    GROUP BY a.id
)
SELECT AVG(qtd_prescricoes) AS media_medicamentos
FROM urgencias