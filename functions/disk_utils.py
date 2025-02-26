# Definições do disco virtual
DISK_NAME = "virtual_disk.img"
DISK_SIZE = 1 * 1024 * 1024 * 1024  # 1 GB
MOUNT_POINT = "mnt_virtual"
LOOP_DEVICE = "/dev/loop0"  # Dispositivo de loop fixo
BLOCK_SIZE = 4096
NUM_TAM_LIMIT = BLOCK_SIZE // 4