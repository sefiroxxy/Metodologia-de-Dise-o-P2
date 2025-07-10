import logging
from logging.handlers import RotatingFileHandler
import os

def configure_logging():
    log_file_path = os.path.join("logs", "app.log")
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Nivel de logging global
    logging.getLogger().setLevel(logging.INFO)

    # Formato del log
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Handler para consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    # Handler para archivo con rotación
    file_handler = RotatingFileHandler(
        log_file_path,
        maxBytes=1024 * 1024 * 5,  # 5 MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)

    # Opcional: Desactivar loggers de librerías externas ruidosas
    logging.getLogger("uvicorn").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("fastapi").setLevel(logging.INFO)
