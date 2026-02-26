-- Insere em stg_prontuario.PACIENTE a união das tabelas PACIENTE de todos os outros hospitais
-- Não traz 'id' das outras tabelas PACIENTE, já que em stg_prontuario.PACIENTE essa coluna foi definida de forma autoincremental...
-- isso evita problemas com duplicidade de ids, já que é provável que existam pacientes duplicados entre os hospitais
INSERT INTO stg_prontuario.PACIENTE (nome, dt_nascimento, cpf, nome_mae, dt_atualizacao)
SELECT nome, dt_nascimento, cpf, nome_mae, dt_atualizacao FROM stg_hospital_a
UNION ALL
SELECT nome, dt_nascimento, cpf, nome_mae, dt_atualizacao FROM stg_hospital_b
UNION ALL
SELECT nome, dt_nascimento, cpf, nome_mae, dt_atualizacao FROM stg_hospital_c