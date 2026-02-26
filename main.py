import pandas as pd
from pathlib import Path, WindowsPath

# Retorna um dicionário contendo DataFrames com os conteúdos de cada layout
def gera_df_layouts(caminho_absoluto: WindowsPath) -> dict:

    # Lista os arquivos de layout presentes no caminho indicado
    lista_layouts = list(caminho_absoluto.glob('*layout.txt'))

    # Cria dict que armazenará os DataFrames de layout
    dict_layouts = {}

    for arquivo in lista_layouts:

        # Define nome da tabela, excuindo o sufixo de layout
        nome_tabela = arquivo.stem.replace('_layout', '')
        # Define caminho absoluto do layout
        caminho_layout = arquivo.resolve()

        # Como o conteúdo dos layouts em .txt está estruturado como csv, lê dessa forma e armazena no dict
        dict_layouts[nome_tabela] = pd.read_csv(caminho_layout)

    return dict_layouts

# Retorna um dict contendo DataFrames com os conteúdo de cada tabela ou relacionamento
def gera_df_tabelas() -> dict:

    # Define caminho absoluto do diretório sigtap
    sigtap_dir = Path('sigtap-simplificado')

    # Lista arquivos de tabelas e relacionamentos que não sejam layouts
    lista_tb_rl = [
        arquivo
        for arquivo in sigtap_dir.glob('*.txt')
        if not arquivo.stem.endswith('_layout')
    ]

    # Define dict que armazenará conteúdos das tabelas e relacionamentos
    dict_tb_rl = {}
    # Define dict de layouts, que será necessário para a criação dos DataFrames de tabelas e relacionamentos
    dict_layouts = gera_df_layouts(sigtap_dir)

    # Para cada arquivo de tabela ou relacionamento
    for arquivo in lista_tb_rl:
        
        # Define variáveis auxiliares para a leitura do conteúdo das tabelas e relacionamentos
        df_layout_atual = dict_layouts[nome_tb_rl] # DataFrame de layout atual
        nome_tb_rl = arquivo.stem # Nome da tabela ou relacionamento
        caminho_tb_rl = arquivo.resolve() # Caminho absoluto da tabela ou relacionamento
        lista_colunas = list(df_layout_atual['Coluna']) # Nome das colunas para essa tabela ou relacionamento
        dict_aux = {coluna: [] for coluna in lista_colunas} # Dict auxiliar à criação do DataFrame da tabela ou relacionamento

        # A partir do caminho absoluto do arquivo, abre o arquivo de texto para leitura
        with open(caminho_tb_rl, 'r', encoding='utf8') as f:

            # Para cada linha do arquivo de texto
            for linha in f:
                for row in df_layout_atual.itertuples():
                    conteudo_coluna = str(linha[row.Inicio - 1: row.Fim])
                    dict_aux[row.Coluna].append(conteudo_coluna)

        dict_tb_rl[nome_tb_rl] = pd.DataFrame(data=dict_aux, dtype=str)

    return dict_tb_rl

def main():
    pass

if __name__ == "__main__":
    main()
