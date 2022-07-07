import logging

logging.basicConfig(filename='app.log', filemode='w',format='%(asctime)s - %(message)s', 
datefmt='%Y-%m-%d  %H:%M:%S',level=logging.DEBUG)


def debug(str):
    logging.debug(str)

def info(str):
    logging.info(str)

def warning(str):
    logging.warning(str)

def error(str):
    logging.error(str)