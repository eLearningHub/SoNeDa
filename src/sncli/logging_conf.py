import logging
import logging.config

logging.config.fileConfig('sncli/logging.conf')
logging.basicConfig(level=logging.INFO)

# create logger
logger = logging.getLogger('sncli')
