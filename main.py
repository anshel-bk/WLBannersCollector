from playwright.sync_api import sync_playwright

from config.settings import settings
from utils.services import get_skins_list, get_data


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        http_credentials = {
            "username": settings.TEST_PAGE_LOGIN,
            "password": settings.TEST_PAGE_PASSWORD,
        }
        mobile_device = p.devices["iPhone 14 Pro"]
        context = browser.new_context(**mobile_device,http_credentials=http_credentials)
        page = context.new_page()
        skins = get_skins_list(page)
        for skin in skins:
            get_data(page, skin)
        context.close()
        browser.close()



if __name__ == "__main__":
    main()
