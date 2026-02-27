-- Cria tabela PACIENTE no schema stg_prontuario
-- Em vez de utilizarmos um id autoincremental, seria possível criar uma PK composta por id + hospital de origem, para manter os ids originais
CREATE TABLE stg_prontuario.PACIENTE (
	id SERIAL PRIMARY KEY, -- Considerei que novos ids serão gerados
	nome VARCHAR(100) NOT NULL,
	dt_nascimento DATE NOT NULL,
	cpf INT NOT NULL, -- Seria melhor utilizar VARCHAR, para não ignorar o zero como primeiro dígito
	nome_mae VARCHAR(100), -- admite null, já que essa informação pode ser desconhecida
	dt_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- timestamp atual inserido a cada atualização
)