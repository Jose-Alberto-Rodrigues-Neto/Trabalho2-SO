from functions.disk_utils import MOUNT_POINT, DISK_NAME, DISK_SIZE, LOOP_DEVICE
import os
import subprocess
import stat
import time

def arquivo_bytes_tam(nome: str) -> float | None:
    path = os.path.join(MOUNT_POINT, nome)
    try:
        tamanho = os.path.getsize(path)
        return tamanho
    except FileNotFoundError:
        print(f"Erro: arquivo não encontrado")
        return None
    except Exception as e:
        print(f"Erro: {e}.")
        return None

def criar_disco_virtual():
    # Criar o disco virtual se ainda não existir
    if not os.path.exists(DISK_NAME):
        with open(DISK_NAME, "wb") as file:
            file.truncate(DISK_SIZE)
        print(f"Disco virtual '{DISK_NAME}' criado com {DISK_SIZE} bytes.")
    else:
        print(f"Disco virtual '{DISK_NAME}' já existe.")

    # Formatar o disco (ext4)
    print(f"Formatando '{DISK_NAME}' como ext4...")
    subprocess.run(["sudo", "mkfs.ext4", DISK_NAME], check=True)

    # Criar ponto de montagem se não existir
    if not os.path.exists(MOUNT_POINT):
        os.makedirs(MOUNT_POINT)

    # Verificar se o disco já está montado
    result = subprocess.run(["mount"], stdout=subprocess.PIPE, text=True)
    if MOUNT_POINT in result.stdout:
        print(f"O disco já está montado em '{MOUNT_POINT}'.")
        return

    # Verificar se o dispositivo de loop já está em uso
    try:
        # Listar dispositivos de loop em uso
        loop_info = subprocess.run(
            ["sudo", "losetup", "-a"], stdout=subprocess.PIPE, text=True
        ).stdout

        # Verificar se o loop0 está em uso
        if LOOP_DEVICE in loop_info:
            print(f"O dispositivo de loop '{LOOP_DEVICE}' já está em uso. Liberando...")
            subprocess.run(["sudo", "losetup", "-d", LOOP_DEVICE], check=True)
            print(f"Dispositivo de loop '{LOOP_DEVICE}' liberado.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao verificar dispositivos de loop: {e}")
        return

    # Associar o arquivo de imagem ao dispositivo de loop
    print(f"Associando '{DISK_NAME}' a '{LOOP_DEVICE}'...")
    try:
        subprocess.run(["sudo", "losetup", LOOP_DEVICE, DISK_NAME], check=True)
        print(f"Dispositivo de loop '{LOOP_DEVICE}' associado a '{DISK_NAME}'.")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao associar o arquivo ao dispositivo de loop: {e}")
        return

    # Montar o disco
    print(f"Montando '{DISK_NAME}' em '{MOUNT_POINT}'...")
    try:
        subprocess.run(["sudo", "mount", "-o", "loop", LOOP_DEVICE, MOUNT_POINT], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Erro ao montar o disco: {e}")
        # Liberar o dispositivo de loop em caso de erro
        subprocess.run(["sudo", "losetup", "-d", LOOP_DEVICE], check=True)
        return

    # Ajustar as permissões do ponto de montagem
    uid = os.getuid()
    gid = os.getgid()
    subprocess.run(["sudo", "chown", f"{uid}:{gid}", MOUNT_POINT], check=True)

    print(f"Disco virtual montado com sucesso em '{MOUNT_POINT}'!")

def listar():
    espaco = 0
    if os.path.exists(MOUNT_POINT) and os.path.ismount(MOUNT_POINT):
        print(f"Listando arquivos em '{MOUNT_POINT}':\n")
        print(f"{'Nome':<20} {'Tamanho':<10} {'Blocos':<10} {'IO Blocos':<20} {'Inode':<10} {'Permissões':<10} {'Último acesso'}")
        print("="*90)

        for file in os.listdir(MOUNT_POINT):
            caminho = os.path.join(MOUNT_POINT, file)
            info = os.stat(caminho)
            
            tamanho = info.st_size
            inodes = info.st_ino
            blocos = info.st_blocks
            io_block = info.st_blksize
            permissoes = stat.filemode(info.st_mode)
            ultimo_acesso = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(info.st_atime))

            espaco += tamanho
            print(f"{file:<20} {tamanho:<10} {blocos:<10} {io_block:<20} {inodes:<10} {permissoes:<10} {ultimo_acesso}")

    else:
        print(f"O ponto de montagem '{MOUNT_POINT}' não existe ou não está montado.")

    print("\n=========== Armazenamento do disco ===========\n")
    espaco_ocupado = espaco / DISK_SIZE  # Espaço ocupado dividido por 1GB
    espaco_livre = (DISK_SIZE - espaco) / DISK_SIZE

    print(f"Espaço Total: 1 GB | Espaço ocupado: {espaco_ocupado} GB | Espaço livre: {espaco_livre} GB")



def desmontar_disco():
    subprocess.run(["sudo", "umount", MOUNT_POINT])

def espaco_ocupado_disco():
    espaco = 0
    for root, _, files in os.walk(MOUNT_POINT):
        for file in files:
            espaco += os.path.getsize(os.path.join(root, file))
    return espaco / (1024 * 1024 * 1024)  # Retorna espaço em GB