import logging

def setup_logging():
    logging.basicConfig(level=logging.INFO, filename='pi5_log.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s')
