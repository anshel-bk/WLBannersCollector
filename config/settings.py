from enum import StrEnum
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_FILE_PATH = Path(__file__).resolve()
BASE_DIR = CURRENT_FILE_PATH.parent.parent

class IgnoredSkins(StrEnum):
    SKIN_1 = "bongacams_zerkalo"
    SKIN_2 = "bongacamslab"
    SKIN_3 = "bongacams_info"
    SKIN_4 = "bongocams_info"
    SKIN_5 = "bongacams_quest"

class CheckedUrls(StrEnum):
    MAIN_URL = "listing"
    ALL_MODELS = "all_models"



class Settings(BaseSettings):
    TEST_PAGE_LOGIN: str
    TEST_PAGE_PASSWORD: str

    SCREENSHOT_NAME_TEMPLATE: str = "%url%_%skin_name%_NEW"

    MAIN_URL: str = "https://rt.bongacams.quest"
    GROUPS_URL: str = "https:///rus.bonga14.com/dev-action/get-skin-groups"
    SET_SKIN_URL: str = "https://rt.bongacams.quest/dev-action/set-skin-group"


    SCREENSHOTS_FILE_PATH: Path = BASE_DIR / "screenshots"
    model_config = SettingsConfigDict(env_file=BASE_DIR/ ".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

