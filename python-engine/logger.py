import logging
import sys
import os
from logging.handlers import RotatingFileHandler

if not os.path.exists('logs'):
    os.makedirs('logs')

logger = logging.getLogger("AIClipper")
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    fmt='%(asctime)s | %(levelname)-8s | %(module)s:%(funcName)s | %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.INFO)

file_handler = RotatingFileHandler('logs/clipper.log', maxBytes=5*1024*1024, backupCount=3)
file_handler.setFormatter(formatter)
file_handler.setLevel(logging.DEBUG)

if not logger.handlers:
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
