# Настройка логирования
import logging

def configure_logging(level = logging.WARNING):
    logging.basicConfig(
        level=level,
        datefmt='%Y-%m-%d %H:%M:%S',
        format='[%(asctime)s.%(msecs)03d] %(module)-20s:%(lineno)-3d %(levelname)-7s - %(message)s',
    )