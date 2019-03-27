import logging
from circles.app import start_app

logging.basicConfig(
    format='[%(filename)s:%(lineno)s - %(funcName)20s()]%(levelname)s:%(name)s:%(message)s',
    level=logging.INFO
)

if __name__ == '__main__':
    logging.info('Start app')
    start_app()
