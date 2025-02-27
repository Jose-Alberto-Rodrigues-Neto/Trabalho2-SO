from functions.directory import espaco_ocupado_disco
from functions.disk_utils import MOUNT_POINT, HUGE_PAGE_SIZE, NUM_SIZE
import os
import random
import struct
import mmap
import time
import heapq

#Criar
def criar_nome_tam(nome: str, tam: int):
    if not os.path.ismount(MOUNT_POINT):
        print("Erro: O disco virtual não está montado!")
        return

    if espaco_ocupado_disco() >= 1:  # Verifica se o disco está cheio
        print("Erro: Não é mais possível criar arquivos, o disco está cheio!")
        return

    if tam <= 0:
        print("Erro: 'tam' deve ser maior que zero.")
        return

    nome_arquivo = f"{nome}.bin"
    path = os.path.join(MOUNT_POINT, nome_arquivo)

    if os.path.exists(path):
        print(f"Erro: O arquivo '{nome_arquivo}' já existe!")
        return
    try:
        numeros = [random.randint(0, 2**31 - 1) for _ in range(tam)]

        with open(path, "wb") as f:
            for num in numeros:
                f.write(struct.pack("I", num))

        print(f"Arquivo '{nome_arquivo}' criado com {tam} números dentro do disco virtual.")

    except Exception as e:
            print(f"Erro inesperado: {e}")

#Ler
def ler_arquivo_bin(nome: str):
    nome_arquivo = nome + ".bin"
    path = os.path.join(MOUNT_POINT, nome_arquivo)
    numeros = []

    try:
        with open(path, "rb") as f:
            while True:
                dados = f.read(4)
                if not dados:
                    break
                numero = struct.unpack("I", dados)[0]
                numeros.append(numero)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return numeros
# ler sublista do arquivo
def ler_sublista(nome: str, ini: int, fim: int):
    nome_arquivo = nome + ".bin"
    path = os.path.join(MOUNT_POINT, nome_arquivo)

    try:
        with open(path, "rb") as f:
            f.seek(ini * 4)  # Pula para o índice inicial (4 bytes por número)
            sublista = []

            for _ in range(ini, fim + 1):
                dados = f.read(4)
                if not dados:
                    break  # Sai se o final do arquivo for atingido
                numero = struct.unpack("I", dados)[0]
                sublista.append(numero)

        return sublista

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

#Ordenar
def split_file(file_path):
    temp_files = []
    with open(file_path, "rb") as f:
        count = 0
        while True:
            data = f.read(HUGE_PAGE_SIZE)
            if not data:
                break
            numbers = list(struct.unpack(f"{len(data) // NUM_SIZE}I", data))
            numbers.sort()
            temp_file = os.path.join(MOUNT_POINT, f"temp_{count}.bin")
            temp_files.append(temp_file)
            with open(temp_file, "wb") as temp_f:
                temp_f.write(struct.pack(f"{len(numbers)}I", *numbers))
            count += 1
    return temp_files

def merge_files(temp_files, output_file):
    min_heap = []
    file_pointers = []

    for i, temp_file in enumerate(temp_files):
        f = open(temp_file, "rb")
        file_pointers.append(f)
        data = f.read(NUM_SIZE)
        if data:
            num = struct.unpack("I", data)[0]
            heapq.heappush(min_heap, (num, i))

    with open(output_file, "wb") as out_f:
        while min_heap:
            num, i = heapq.heappop(min_heap)
            out_f.write(struct.pack("I", num))
            data = file_pointers[i].read(NUM_SIZE)
            if data:
                new_num = struct.unpack("I", data)[0]
                heapq.heappush(min_heap, (new_num, i))

    for f in file_pointers:
        f.close()
    for temp_file in temp_files:
        os.remove(temp_file)

def ordenar_arquivo_bin(file_name):
    start_time = time.time()
    file_path = os.path.join(MOUNT_POINT, f"{file_name}.bin")
    temp_files = split_file(file_path)
    merge_files(temp_files, file_path)
    end_time = time.time()
    print(f"Arquivo '{file_name}.bin' ordenado com sucesso.")
    return end_time - start_time

#Concatenar
def concatenar_arquivos(nome1: str, nome2: str, nome_saida: str):
    path1 = os.path.join(MOUNT_POINT, nome1 + ".bin")
    path2 = os.path.join(MOUNT_POINT, nome2 + ".bin")
    path_saida = os.path.join(MOUNT_POINT, nome_saida + ".bin")
    
    try:
        with open(path1, "rb") as f1, open(path2, "rb") as f2, open(path_saida, "wb") as f_saida:
            f_saida.write(f1.read())
            f_saida.write(f2.read())
        print(f"Arquivos '{nome1}.bin' e '{nome2}.bin' concatenados em '{nome_saida}.bin'.")
        
        apagar_nome(nome1)
        apagar_nome(nome2)
    except FileNotFoundError:
        print("Erro: Um dos arquivos não foi encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")

#Deletar
def apagar_nome(nome: str):
    nome_arquivo = nome + ".bin"
    path = os.path.join(MOUNT_POINT, nome_arquivo)
    try:
        os.remove(path)
        print(f"Arquivo '{nome_arquivo}' deletado com sucesso.")
    except FileNotFoundError:
        print(f"Erro: Arquivo {nome_arquivo} não encontrado")
    except Exception as e:
        print(f"Erro inesperado: {e}")