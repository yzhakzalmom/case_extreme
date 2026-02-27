import pandas as pd
from pathlib import Path
from sqlalchemy import create_engine, types

# Define um mapa de tipos entre os tipos nos layouts e no SQLAlchemy
MAPA_TIPOS = {
    'VARCHAR2': types.String,
    'CHAR': types.String,
    'NUMBER': types.Numeric,
    'DATE': types.Date
}

# Retorna um dicionário contendo DataFrames com os conteúdos de cada layout
def gera_df_layouts(sigtap_dir: Path) -> dict:

    return {
        arquivo.stem.replace('_layout', ''): pd.read_csv(arquivo) # Como o conteúdo do txt de layout está estruturado em csv, lê arquivo dessa forma diretamente
        for arquivo in sigtap_dir.glob('*layout.txt') # Faz isso para cada arquivo de layout
    }

# Retorna um dict contendo DataFrames com os conteúdo de cada tabela ou relacionamento
def gera_df_tabelas(sigtap_dir: Path | None = None) -> dict:

    # Define caminho absoluto do diretório sigtap
    sigtap_dir = sigtap_dir or Path('sigtap-simplificado')

    # Define dict que armazenará conteúdos das tabelas e relacionamentos
    dict_tb_rl = {}
    # Define dict de layouts, que será necessário para a criação dos DataFrames de tabelas e relacionamentos
    dict_layouts = gera_df_layouts(sigtap_dir)

    # Para cada arquivo de tabela ou relacionamento
    for arquivo in sigtap_dir('*.txt'):
        if arquivo.stem.endswith('_layout'): # Ignora caso seja layout
            continue
        
        # Define variáveis para auxiliar a leitura dos conteúdos em texto
        nome_tb_rl = arquivo.stem
        df_layout = dict_layouts[nome_tb_rl] # Define layout da tabela atual

        # Define as especificações para leitura do conteúdo
        colspecs = list(zip(df_layout['Inicio'] - 1, df_layout['Fim']))

        # Cria DataFrame utilizando read_fwf, que aplica a especificação ao conteúdo do arquivo
        df = pd.read_fwf(
            arquivo,
            colspecs=colspecs,
            names=df_layout['Coluna'].tolist(),
            dtype=str,
            header=None
        )
        # Remove os espaços vazios nas colunas
        df = df.apply(lambda col: col.str.strip())
        dict_tb_rl[nome_tb_rl] = df

    return dict_tb_rl

# Define função que resolve o tipo recebido do layout
def resolve_tipo(tipo_layout: str, tamanho: int) -> types:

    # Extrai tipo do mapa de tipos. Caso não haja correspondência, define Text por padrão
    tipo = MAPA_TIPOS.get(tipo_layout, types.Text)

    # Retorna o tipo com o tamanho definido pelo layout
    if tipo is types.String:
        return tipo(tamanho)
    
    return tipo

#

def main():
    pass

if __name__ == "__main__":
    main()
