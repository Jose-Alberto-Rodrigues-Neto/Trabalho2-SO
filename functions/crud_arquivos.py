from functions.directory import espaco_ocupado_disco, MOUNT_POINT
import os
import random
import struct

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

#Deletar
def apagar_nome(nome: str):
    nome_arquivo = nome + ".bin"
    path = os.path.join("directory", nome_arquivo)
    try:
        os.remove(path)
        print(f"Arquivo '{nome_arquivo}' deletado com sucesso.")
    except FileNotFoundError:
        print(f"Erro: Arquivo {nome_arquivo} não encontrado")
    except Exception as e:
        print(f"Erro inesperado: {e}")

def arquivo_bytes_tam(nome: str, dir: str):
    path = os.path.join(dir, nome)
    try:
        tamanho = os.path.getsize(path)
        return tamanho
    except FileNotFoundError:
        print(f"Erro: arquivo não encontrado")
        return None
    except Exception as e:
        print(f"Erro: {e}.")
        return None