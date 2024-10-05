import logging

from app.settings import get_settings

from logging.handlers import RotatingFileHandler


logger = logging.getLogger(get_settings().app_name)
logger.setLevel(get_settings().log_level)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

console_handler = logging.StreamHandler()
console_handler.setLevel(get_settings().log_level)
console_handler.setFormatter(formatter)

file_handler = RotatingFileHandler(
    get_settings().log_file, maxBytes=1000000, backupCount=3)
file_handler.setLevel(get_settings().log_level)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)
