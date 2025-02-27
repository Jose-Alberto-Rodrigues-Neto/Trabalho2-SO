from functions.directory import espaco_ocupado_disco
from functions.disk_utils import MOUNT_POINT, NUM_TAM_LIMIT, BLOCK_SIZE
import os
import random
import struct
import mmap
import time

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
    if tam <= NUM_TAM_LIMIT: # Não sei se essa checagem é necessária
        try:
            numeros = [random.randint(0, 2**31 - 1) for _ in range(tam)]
            
            with open(path, "wb") as f:
                for num in numeros:
                    f.write(struct.pack("I", num))
            
            print(f"Arquivo '{nome_arquivo}' criado com {tam} números dentro do disco virtual.")
        
        except Exception as e:
            print(f"Erro inesperado: {e}")
    else:
        print(f"Erro inesperado: o arquivo que você tentou criar excede o limite de armazenamento de 1 bloco: {BLOCK_SIZE}")
    
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

def ordenar_arquivo_bin(nome: str):
    nome_arquivo = nome + ".bin"
    path_arquivo = os.path.join(MOUNT_POINT, nome_arquivo)
    path_huge_page = os.path.join(MOUNT_POINT, "huge_page.bin")

    try:
        start_time = time.time()

        with open(path_arquivo, "r+b") as f, open(path_huge_page, "r+b") as huge_page:
            file_size = os.path.getsize(path_arquivo)

            for offset in range(0, file_size, HUGE_PAGE_SIZE):
                chunk_size = min(HUGE_PAGE_SIZE, file_size - offset)

                with mmap.mmap(f.fileno(), chunk_size, offset=offset, access=mmap.ACCESS_READ) as mm:
                    numeros = list(struct.unpack(f"{chunk_size // 4}I", mm[:chunk_size]))

                numeros.sort()

                with mmap.mmap(huge_page.fileno(), chunk_size, access=mmap.ACCESS_WRITE) as hm:
                    hm.write(struct.pack(f"{len(numeros)}I", *numeros))

                with mmap.mmap(f.fileno(), chunk_size, offset=offset, access=mmap.ACCESS_WRITE) as mm:
                    mm.write(struct.pack(f"{len(numeros)}I", *numeros))

        end_time = time.time()

        return end_time - start_time

    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo}' ou huge page '{path_huge_page}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None

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