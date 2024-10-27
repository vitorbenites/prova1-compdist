import logging

# Configuração do logger
logging.basicConfig(format='%(asctime)s - %(message)s',
                    filename="log/app.log", level=logging.INFO)
log = logging.getLogger()
