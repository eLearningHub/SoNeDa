import logging
import logging.config

logging.config.fileConfig('soneda/logging.conf')
logging.basicConfig(level=logging.INFO)

# create logger
logger = logging.getLogger('soneda')
