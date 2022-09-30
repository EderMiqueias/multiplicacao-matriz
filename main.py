import time
from math import ceil
from threading import Thread
import multiprocessing


def get_matriz_from_file(file_name) -> list:
    with open(file_name, 'r') as f:
        linhas_file = f.readlines()
        linhas_file = list(map(lambda item: item.replace('\n', '').strip().split(' '), linhas_file))

        # respectivamente: MATRIZ, NUMERO DE LINHAS, NUMEROS DE COLUNAS
        return linhas_file[1:], int(linhas_file[0][0]), int(linhas_file[0][1])

def matriz_str_to_float(matriz) -> list:
    return list(list(map(lambda valor: float(valor), linha)) for linha in matriz)

def get_col(matriz, n):
    return [i[n] for i in matriz]

def get_lin(matriz, n):
    return matriz[n]

def is_matrizes_valid(m1l, m1c, m2l, m2c):
    return m1l == m2c or m2l == m1c

def exibe_tempo_execucao(inicial, final):
    total = final - inicial
    print(f"Passaram-se {'%.2f' % total} segundos")

def exibe_matriz(matriz):
    for linha in matriz:
        print(linha)

def lin_x_col(linha, coluna):
    new_value = 0
    for index, value in enumerate(linha):
        new_value += value * coluna[index]
    return new_value


# VARIAÇÕES DO CALCULO DA MATRIZ

def variacao_p1(arquivo_m1, arquivo_m2, exibir = False):
    m1, m1_linhas, m1_colunas = get_matriz_from_file(arquivo_m1)
    m2, m2_linhas, m2_colunas = get_matriz_from_file(arquivo_m2)

    if not is_matrizes_valid(m1_linhas, m1_colunas, m2_linhas, m2_colunas):
        print("A ordem das matrizes não é valido")
        return

    m1 = matriz_str_to_float(m1)
    m2 = matriz_str_to_float(m2)
    new_matriz = []

    start = time.perf_counter()
    for index in range(m1_linhas):
        linha_m1 = get_lin(m1, index)
        new_linha = []
        for index_l in range(len(linha_m1)):
            new_linha.append(lin_x_col(linha_m1, get_col(m2, index_l)))
        new_matriz.append(new_linha)
    
    if exibir:
        exibe_matriz(new_matriz)

    # REGISTRA MOMENTO DA FINALIZAÇÃO DA MULTIPLICAÇÃO
    end = time.perf_counter()
    exibe_tempo_execucao(start, end)


class VariacaoP2:
    def __init__(self) -> None:
        self.new_matriz = []
        self.m1 = []
        self.m2 = []
        self.start = None
        self.core_count = multiprocessing.cpu_count()
    
    # ao invez de calcular ela por pedaços e depois unir os mesmos
    # Optei por criar uma matriz preenchida com valores nulos
    # para posteriormente atualizar um por um atraves do index, mantendo a ordem original
    def _preenche_new_matriz(self, linhas):
        self.new_matriz = [[] for n in range(linhas)]
    
    def create_thread(self, index_inicial, index_final, is_last = False, exibir = False):
        for index in range(index_inicial, index_final):
            linha_m1 = get_lin(self.m1, index)
            new_linha = []
            for index_l in range(len(linha_m1)):
                new_linha.append(lin_x_col(linha_m1, get_col(self.m2, index_l)))
            self.new_matriz[index] = new_linha
        
        if exibir:
            exibe_matriz(self.new_matriz)
        if is_last:
            # REGISTRA MOMENTO DA FINALIZAÇÃO DA MULTIPLICAÇÃO
            end = time.perf_counter()
            exibe_tempo_execucao(self.start, end)


    def run(self, arquivo_m1, arquivo_m2, exibir = False):
        m1, m1_linhas, m1_colunas = get_matriz_from_file(arquivo_m1)
        m2, m2_linhas, m2_colunas = get_matriz_from_file(arquivo_m2)

        if not is_matrizes_valid(m1_linhas, m1_colunas, m2_linhas, m2_colunas):
            print("A ordem das matrizes não é valido")
            return

        self.m1 = matriz_str_to_float(m1)
        self.m2 = matriz_str_to_float(m2)
        self._preenche_new_matriz(m1_linhas)
        
        indexes_por_thread = ceil(m1_linhas / self.core_count)
        index_i = 0

        self.start = time.perf_counter()
        while index_i + indexes_por_thread < m1_linhas:
            index_f = index_i + indexes_por_thread
            # print(index_i, index_f)
            th = Thread(target=self.create_thread, args=(index_i, index_f))
            th.start()
            index_i = index_f

        th = Thread(target=self.create_thread, args=(index_i, m1_linhas, True, exibir))
        th.start()


class VariacaoP3(VariacaoP2):
    def __init__(self) -> None:
        super().__init__()
        self.core_count *= 2

class VariacaoP4(VariacaoP2):
    def __init__(self) -> None:
        super().__init__()
        self.core_count /= 2


# variacao_p1('4_int.txt', '4_int.txt', False)
# variacao_p1('10_float.txt', '10_float.txt')
# variacao_p1('10_int.txt', '10_int.txt')
VariacaoP2().run('4_int.txt', '4_int.txt')
VariacaoP2().run('10_int.txt', '10_int.txt')
VariacaoP2().run('1024.txt', '1024.txt')

VariacaoP3().run('4_int.txt', '4_int.txt')
VariacaoP3().run('10_int.txt', '10_int.txt')
VariacaoP3().run('1024.txt', '1024.txt')

VariacaoP4().run('4_int.txt', '4_int.txt')
VariacaoP4().run('10_int.txt', '10_int.txt')
VariacaoP4().run('1024.txt', '1024.txt')
