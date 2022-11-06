import logging
import logging.config

logging.config.fileConfig('sncli/logging.conf')

# create logger
logger = logging.getLogger('simpleExample')
