import os
import logging
from dotenv import load_dotenv

load_dotenv()

YOPASS_URL = os.getenv("YOPASS_URL")
YOPASS = os.getenv("YOPASS")
IPA_HOST = os.getenv("IPA_HOST")
SESSION_EXPIRATION_MINUTES = 60

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('ipa-api.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)