-- Como um atendimento pode ter vários exames solicitados, vemos que se trata de uma relação 1:N.
-- Dessa forma, a melhor prática seria criar duas tabelas (ATENDIMENTOS e EXAMES) respeitando a cardinalidade de 1:N, de modo que...
-- a tabela EXAMES relacionaria um atendimento para cada exame.

-- A tabela ATENDIMENTOS teria as seguintes colunas, por exemplo:
-- id_atendimento (PK)
-- id_medico
-- id_paciente
-- dt_atendimento

-- Já a tabela EXAMES receberia id_atendimento como chave estrangeira, evidenciando o atendimento relacionado a cada um dos exames. Por exemplo:
-- id_exame (PK)
-- nome_exame
-- valor_exame
-- id_atendimento (FK que refencia ATENDIMENTOS(id_atendimento))

-- Supondo que já haveria um schema de staging unificado para os três hospitais, o código seria esse:
CREATE TABLE stg_hospital.ATENDIMENTOS (
    id_atendimento SERIAL PRIMARY KEY,
    id_medico INT NOT NULL,
    id_paciente INT NOT NULL,
    dt_atendimento DATE NOT NULL
);

CREATE TABLE stg_hospital.EXAMES (
    id_exame SERIAL PRIMARY KEY,
    nome_exame VARCHAR(100) NOT NULL,
    valor_exame NUMERIC(10,2) NOT NULL,
    id_atendimento INT NOT NULL,
    FOREIGN KEY (id_atendimento) REFERENCES stg_hospital.ATENDIMENTOS(id_atendimento)
)