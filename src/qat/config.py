# -*- coding: utf-8 -*-

"""
Configuration module.
"""

import logging

# Run level.
__DEBUG__ = True

root_path = ''

# Logger settings.
log_level = logging.DEBUG
log_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger('QAT')
logger.setLevel(log_level)

file_logger = logging.FileHandler('qat.log')
file_logger.setLevel(log_level)
file_logger.setFormatter(log_format)

console_logger = logging.StreamHandler()
console_logger.setLevel(log_level)
console_logger.setFormatter(log_format)

logger.addHandler(file_logger)
logger.addHandler(console_logger)

data_source = [
    {'name': 'TuShare',
     'url': 'http://'},
    {'name': 'TDX',
     'url': 'C:\\zd_huatai\\vipdoc'}
]

if __DEBUG__:
    database_url = 'sqlite:///{}security.sqlite'.format(root_path)
else:
    database_url = 'postgresql://postgres:woyaofacai@192.168.56.2:5432/security'

RETRY_TIMES = 30
RETRY_INTERVAL = 10

# 通达信软件根目录
TDX_ROOT_PATH = 'c:\\zd_huatai'


class Test:
    def __init__(self):
        self.short_name = 'xx_test'

    class ShortName:
        def __init__(self):
            self.google = 'google'
            self.common = 'sh'
            self.former = 'sse'


exchange_short_name = {
    'google': 'google'
}
