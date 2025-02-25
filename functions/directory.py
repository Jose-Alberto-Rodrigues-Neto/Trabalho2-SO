import os
import subprocess

# Definições do disco virtual
DISK_NAME = "virtual_disk.img"
DISK_SIZE = 1 * 1024 * 1024 * 1024  # 1GB
MOUNT_POINT = "mnt_virtual"
LOOP_DEVICE = "/dev/loop0"  # Dispositivo de loop fixo

def create_virtual_disk():
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

def list_files_in_virtual_disk():
    if os.path.exists(MOUNT_POINT) and os.path.ismount(MOUNT_POINT):
        print(f"Listando arquivos em '{MOUNT_POINT}':")
        for entry in os.listdir(MOUNT_POINT):
            print(entry)
    else:
        print(f"O ponto de montagem '{MOUNT_POINT}' não existe ou não está montado.")

def desmontar_disco():
    subprocess.run(["sudo", "umount", MOUNT_POINT])

def espaco_ocupado_disco():
    espaco = 0
    for root, _, files in os.walk(MOUNT_POINT):
        for file in files:
            espaco += os.path.getsize(os.path.join(root, file))
    return espaco / (1024 * 1024 * 1024)  # Retorna espaço em GB