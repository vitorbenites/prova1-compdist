import logging
import sys

# Configuração do logger
logging.basicConfig(
    format='%(asctime)s - %(message)s',
    filename="log/app.log",
    level=logging.INFO
)

log = logging.getLogger()

# Cria um manipulador para a saída padrão
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))

# Adiciona o manipulador de console ao logger
log.addHandler(console_handler)
