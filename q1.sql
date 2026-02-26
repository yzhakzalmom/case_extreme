-- Cria tabela PACIENTE no schema stg_prontuario
CREATE TABLE stg_prontuario.PACIENTE (
	id SERIAL PRIMARY KEY,
	nome VARCHAR(100) NOT NULL,
	dt_nascimento DATE NOT NULL,
	cpf INT NOT NULL,
	nome_mae VARCHAR(100), -- admite null, já que essa informação pode ser desconhecida
	dt_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP -- timestamp atual inserido a cada atualização
)