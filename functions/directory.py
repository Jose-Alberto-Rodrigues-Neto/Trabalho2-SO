import os
from functions.crud_arquivos import arquivo_bytes_tam

def listar():
    # Listar arquivos e pastas
    arquivos = os.listdir("directory")
    espaco = 0
    print("Arquivos encontrados:")
    for arquivo in arquivos:
        tam = arquivo_bytes_tam(arquivo, "directory")
        espaco += tam
        print(f"{arquivo} | {tam} bytes")
    print("\n=========== Armazenamento do disco ===========")
    espaco_ocupado = espaco / 1000000000 #espaço ocupado dividido por 1GB
    espaco_livre = (1000000000 - espaco)/1000000000

    print(f"Total: 1 GB | Espaço ocupado: {espaco_ocupado} | Espaço livre: {espaco_livre}")