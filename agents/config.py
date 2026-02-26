import os

USE_OPENROUTER = True
OPENROUTER_MODEL = "openai/gpt-oss-safeguard-20b"
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"
ONLY_CODE_FUNCTIONS = True
VERBOSE = True
DOCKER_NAME = "gloss-sensemaking-code"
WORK_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
USE_CSV = True
