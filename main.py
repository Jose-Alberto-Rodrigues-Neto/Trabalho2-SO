import os
import time
from functions.crud_arquivos import criar_nome_tam, ler_arquivo_bin, apagar_nome
from functions.directory import criar_disco_virtual, listar, desmontar_disco
from functions.disk_utils import MOUNT_POINT

if (not os.path.exists(MOUNT_POINT) or not os.path.ismount(MOUNT_POINT)): #Verifica se o disc existe ou está montado, se não, ele cria o disco
    criar_disco_virtual()

is_running = True

print("\n=================== Sistema de gerenciamento de arquivos ===================\n")

while(is_running):
    
    print("\nO que você deseja fazer:\n1 - Listar todos os arquivos do disco\n2 - Criar arquivo no disco\n3 - Apagar arquivo no disco\n4 - Resetar disco\n5 - Sair")
    x = int(input())
    match(x):
        case 1:
            os.system("clear")
            listar()
        case 2:
            os.system("clear")
            arq = str(input("\rEntre com o nome do arquivo: "))
            tam = int(input("Entre com o número total de dados dentro do arquivo: "))
            criar_nome_tam(arq, tam)
        case 3:
            os.system("clear")
            arq = str(input("\rEntre com o nome do arquivo que deseja deletar: "))
            apagar_nome(arq)
        case 4:
            os.system("clear")
            res = str(input("\rVocê tem certeza que deseja resetar o disco? (s/n): "))
            if(res == "s"):
                print("Apagando disco...")
                desmontar_disco()
                print("Disco apagado!\nRecriando disco...")
                criar_disco_virtual()
                print("Disco criado!")
        case 5:
            os.system("clear")
            print("Fim do sistema!")
            is_running = False 
    print("\n============================================================================\n")            