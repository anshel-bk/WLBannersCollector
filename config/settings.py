from enum import StrEnum
from pathlib import Path
from typing import NamedTuple

from pydantic_settings import BaseSettings, SettingsConfigDict

CURRENT_FILE_PATH = Path(__file__).resolve()
BASE_DIR = CURRENT_FILE_PATH.parent.parent





class Settings(BaseSettings):
    TEST_PAGE_LOGIN: str
    TEST_PAGE_PASSWORD: str

    DEFAULT_TIMEOUT: int = 30000

    SCREENSHOT_NAME_TEMPLATE: str = "%url%_%skin_name%_NEW"

    MAIN_URL: str = "https://rt.bongacams.quest"
    GROUPS_URL: str = "https:///rus.bonga14.com/dev-action/get-skin-groups"
    SET_SKIN_URL: str = "https://rt.bongacams.quest/dev-action/set-skin-group"

    class CookieWarning18(NamedTuple):  # кука которая отвечает за обход баннера подтверждения возраста
        name: str = "warning18"
        value: str = "%5B%22ru_RU%22%5D"  # Supports default values


    SCREENSHOTS_FILE_PATH: Path = BASE_DIR / "screenshots"
    model_config = SettingsConfigDict(env_file=BASE_DIR/ ".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()

