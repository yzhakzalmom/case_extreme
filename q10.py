from pathlib import Path
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FixedLocator
import numpy as np

# Retorna lista com as datas contidas no arquivo txt
def gerar_lista_datas() -> list:

    # Define caminho do arquivo a ser lido
    caminhos_datas = list(Path('datas').iterdir())

    # Cria lista que será preenchida com as listas de datas
    lista_datas = []

    for caminho in caminhos_datas:
    # Lê arquivo de texto contendo datas
        with open(caminho, 'r', encoding='utf-8') as f:

            # Cria lista auxiliar para preencher lista_datas
            lista_aux = []

            # Para cada data
            for linha in f:

                # Garante que não há espaços vazios na linha
                linha = linha.strip()

                # Valida tentando converter para datetime
                # Caso dê certo, adiciona o valor na lista
                try:
                    datetime.strptime(linha, '%Y-%m-%d')
                    lista_aux.append(linha)
                # Do contrário, passa para o próximo valor
                except:
                    continue

            # Adiciona conteúdo da lista auxiliar a lista_datas
            lista_datas.append(lista_aux)
    
    return lista_datas

def visualizar_atendimentos(lista_datas: list[str], titulo: str = 'Atendimentos por Dia'):

    # Garante a execução apenas se as datas forem fornecidas
    if not lista_datas:
        print("Nenhuma data fornecida.")
        return
    
    # Converte strings de data para datetime
    lista_datetime = [datetime.strptime(d, "%Y-%m-%d").date() for d in lista_datas]
    # Gera contagem dessas datas
    freq_datas = Counter(lista_datetime)

    # Ordena as datas
    datas_ordenadas = sorted(freq_datas.keys())

    # Cria lista com as quantidades de aparições de cada data
    lista_freq_datas = [freq_datas[data] for data in datas_ordenadas]

    # Define estilo e área da imagem
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(15, 5))

    # Define as cores das barras
    amplitude = np.max(lista_freq_datas) - np.min(lista_freq_datas)
    if amplitude == 0:
        quantidades_norm = np.ones(len(lista_freq_datas)) * 0.5  # Garante que todos tenham a mesma cor se houver as mesmas frequência
    else: # Normaliza quantidades para manter cores harmônicas
        quantidades_norm = (lista_freq_datas - np.min(lista_freq_datas)) / amplitude

    # Dessa forma, garante que não teremos cores muito claras ou muito escuras    
    cores = plt.cm.Blues(0.2 + 0.75 * quantidades_norm)

    # Configura as barras
    barras = ax.bar(datas_ordenadas, lista_freq_datas, color=cores, edgecolor="white", linewidth=0.2, width=4.5, zorder=2)

    # Rótulos no topo de cada barra
    for barra, qtd in zip(barras, lista_freq_datas):
        ax.text(
            barra.get_x() + barra.get_width() / 2, # Centraliza no eixo x da barra
            barra.get_height() + 0.05, # Posiciona um pouco acima da barra
            str(qtd),
            ha="center", va="bottom",
            fontsize=8, fontweight="bold", color="#1a3a5c"
        )   

    # Formatação do eixo x
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m")) # Formata datas no eixo x
    ax.xaxis.set_major_locator(FixedLocator([mdates.date2num(d) for d in datas_ordenadas])) # Força a marcação do eixo x como dias
    plt.xticks(rotation=45, ha="right", fontsize=9)

    # Formatação do eixo y
    ax.yaxis.get_major_locator().set_params(integer=True) # Marcação do eixo y deve ser inteira
    ax.set_ylim(0, max(lista_freq_datas) + 1.5) # Range do eixo y vai de 0 até o máximo + 1,5

    # Define títulos e rótulos
    ax.set_title(titulo, fontsize=15, fontweight="bold", color="#1a3a5c", pad=14)
    ax.set_xlabel("Data", fontsize=11, color="#444")
    ax.set_ylabel("Nº de Atendimentos", fontsize=11, color="#444")

    # Cria uma linha de média
    media = np.mean(lista_freq_datas)
    ax.axhline(media, color="#e05c5c", linestyle="--", linewidth=1.4, label=f"Média: {media:.1f} atend./dia", zorder=4) # Formata a legenda
    ax.legend(fontsize=10)

    # Ajusta os elementos internos da figura
    plt.tight_layout()

    return fig

def main():

    # Lista as datas presentes na pasta datas
    lista_datas = gerar_lista_datas()

    # Gera uma figura com a quantidade de atendimentos para cada lista de datas
    for i in range(len(lista_datas)):
        fig = visualizar_atendimentos(lista_datas[i])
        fig.savefig(f'figs/datas{i+1}')

if __name__ == '__main__':
    main()