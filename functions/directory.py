import os
from functions.crud_arquivos import arquivo_bytes_tam

def listar():
    # Listar arquivos e pastas
    arquivos = os.listdir("directory")

    print("Arquivos encontrados:")
    for arquivo in arquivos:
        tam = arquivo_bytes_tam(arquivo, "directory")
        print(f"{arquivo} | {tam} bytes")