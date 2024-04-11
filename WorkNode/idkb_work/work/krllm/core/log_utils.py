from ..config import LOG_DIR,LOG_LEVEL
import os
import logging

class LoggingObject:
    def __init__(self,log_name):
        self.log_path=LOG_DIR/f"{log_name}.log"
        self.logger=logging.getLogger(log_name)
        self.logger.setLevel(LOG_LEVEL)
        handler = logging.FileHandler(LOG_DIR/f'{log_name}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.propagate = False
        self.logf={
            'debug':self.logger.debug,
            'info': self.logger.info,
            'warning': self.logger.warning,
            'error': self.logger.error,
            'critical': self.logger.critical
        }

    def set_level(self,level:int):
        self.logger.setLevel(level)
    def log(self,msg,level='debug'):
        self.logf[level](msg)













