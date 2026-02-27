from collections import Counter

# Recebe entrada de prescrição e estoque do terminal e retorna isso em uma tupla
def input_prescricao_estoque() -> tuple:

    prescricao = input('Insira a prescrição: ')
    estoque = input('Insira o estoque: ')

    return prescricao, estoque

# Confere se a prescrição é viável de acordo com o estoque
def verifica_viabilidade_prescricao(prescricao, estoque) -> bool:

    # Cria dict Counter, que conta a frequência de cada caracter das entradas
    qtd_prescricao = Counter(prescricao)
    qtd_estoque = Counter(estoque)

    # Para cada medicamento prescrito, confere se há estoque suficiente. Se não houver, retorna False
    for medicamento in qtd_prescricao.keys():
        if qtd_prescricao[medicamento] > qtd_estoque[medicamento]:
            return False
    
    # Se o loop não retornar false, quer dizer que há estoque suficiente e a prescrição é viável
    return True


def main():
    prescricao, estoque = input_prescricao_estoque()
    print(verifica_viabilidade_prescricao(prescricao, estoque))

if __name__ == '__main__':
    main()