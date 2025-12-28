import logging
import os
import sys

log_dir = "logs"
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

log_format = logging.Formatter("%(asctime)s - %(levelname)s - %(name)s - %(message)s")

def get_logger(name):
    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.INFO)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(log_format)
        logger.addHandler(console_handler)

        file_handler = logging.FileHandler(os.path.join(log_dir, "execution.log"), mode='w')
        file_handler.setFormatter(log_format)
        logger.addHandler(file_handler)

    return logger