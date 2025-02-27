import os
from functions.crud_arquivos import criar_nome_tam, ler_arquivo_bin, apagar_nome, ler_sublista, ordenar_arquivo_bin, concatenar_arquivos
from functions.directory import criar_disco_virtual, listar, desmontar_disco
from functions.disk_utils import MOUNT_POINT

if (not os.path.exists(MOUNT_POINT) or not os.path.ismount(MOUNT_POINT)): #Verifica se o disc existe ou está montado, se não, ele cria o disco
    criar_disco_virtual()

is_running = True

print("\n=================== Sistema de gerenciamento de arquivos ===================\n")

while(is_running):
    
    print("\nO que você deseja fazer:\n1 - Listar todos os arquivos do disco\n2 - Criar arquivo no disco\n3 - Apagar arquivo no disco\n4 - Ler arquivo\n5 - Ler sublista\n6 - Ordenar arquivo\n7 - Concatenar arquivos\n8 - Remontar disco\n9 - Sair")
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
            arq = str(input("Entre com o nome do arquivo que você deseja ler: "))
            data = ler_arquivo_bin(arq)
            if  data != None:
                print(data)
                print(f"Tamanho do array de dados: {len(data)}")
        case 5:
            os.system("clear")
            arq = str(input("Entre com o nome do arquivo que você deseja ler: "))
            ini = int(input("Entre com o indice inicial da sublista: "))
            fim = int(input("Entre com o indice final da sublista: "))
            data = ler_sublista(arq, ini, fim)
            if  data != None:
                print(data)
                print(f"Tamanho do array de dados: {len(data)}")
        case 6:
            os.system("clear")
            arq = str(input("Entre com o nome do aquivo que você deseja ordenar: "))
            time = ordenar_arquivo_bin(arq)
            print("Tempo para ordenar foi de ", time*1000, " milisegundos")
        case 7:
            os.system("clear")
            arq1 = str(input("Entre com o nome do primeiro arquivo a se concatenar: "))
            arq2 = str(input("Entre com o nome do segundo arquivo a se concatenar: "))
            concatenar_arquivos(arq1, arq2)
        case 8:
            os.system("clear")
            res = str(input("\rVocê tem certeza que deseja resetar o disco? (s/n): "))
            if(res == "s"):
                print("Apagando disco...")
                desmontar_disco()
                print("Disco apagado!\nRecriando disco...")
                criar_disco_virtual()
                print("Disco criado!")
        case 9:
            os.system("clear")
            print("Fim do sistema!")
            is_running = False
        

    print("\n============================================================================\n")            