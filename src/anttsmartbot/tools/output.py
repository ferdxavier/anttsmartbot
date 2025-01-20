import logging
from .constants import LOG_PROCESS_MESSAGES_FILE, ANTTSMARTBOT_INTERNAL_WORKDIR_PATH

logging.basicConfig(
    filename=f'{ANTTSMARTBOT_INTERNAL_WORKDIR_PATH}/{LOG_PROCESS_MESSAGES_FILE}',
    level=logging.INFO,
    format='%(asctime)s - %(message)s'
)

logger = logging.getLogger(__name__)

def print_and_log(message: str):
    logger.info(message.lstrip())
    print(message)

def output_log(message: str):
    logger.info(message.lstrip())
    return message