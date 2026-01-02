import logging
import os
from .constants import LOG_PROCESS_MESSAGES_FILE, ANTTSMARTBOT_INTERNAL_WORKDIR_PATH

def init():
    if not os.path.exists(ANTTSMARTBOT_INTERNAL_WORKDIR_PATH):
        os.makedirs(ANTTSMARTBOT_INTERNAL_WORKDIR_PATH)

    if not os.path.exists(os.path.join(ANTTSMARTBOT_INTERNAL_WORKDIR_PATH, LOG_PROCESS_MESSAGES_FILE)):
        with open(os.path.join(ANTTSMARTBOT_INTERNAL_WORKDIR_PATH, LOG_PROCESS_MESSAGES_FILE), 'w') as file:
            open(os.path.join(ANTTSMARTBOT_INTERNAL_WORKDIR_PATH, LOG_PROCESS_MESSAGES_FILE), 'w').close()

    logging.basicConfig(
        filename=f'{ANTTSMARTBOT_INTERNAL_WORKDIR_PATH}/{LOG_PROCESS_MESSAGES_FILE}',
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
        )

init()
_logger = logging.getLogger(__name__)

def print_and_log(message: str):
    _logger.info(message.lstrip())
    print(message)

def output_log(message: str):
    _logger.info(message.lstrip())
    return message