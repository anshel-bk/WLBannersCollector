from playwright._impl._api_structures import SetCookieParam
from playwright.sync_api import Page

from config.settings import settings, IgnoredSkins, CheckedUrls


def get_skins_list(page: Page):
    req = page.request.get(settings.GROUPS_URL)
    req_json = req.json()
    skins = req_json.get("skins")
    if skins is None:
        print("Не было найдено ни одного скинхеда")
        raise ValueError
    skins = [key for key,value in skins.items()]
    print(f"Всего обнаружено скинов {len(skins)}\n"
           f"Список скинов: {'\n'.join(skins)}")
    return skins

def get_data(page: Page,skin: str):
    if skin in IgnoredSkins:
        return
    site_version = "OLD"
    collect_screenshot(page,skin,site_version)
    site_version = "NEW"
    add_new_mobile_cookies(page)
    collect_screenshot(page, skin, site_version)

def collect_screenshot(page: Page,skin: str,version: str):
    url_skin = f"{settings.SET_SKIN_URL}/{skin}"
    print(f"Проверяем {skin}")
    page.goto(url_skin)
    for url_for_check in CheckedUrls:
        url = f"{settings.MAIN_URL}/{url_for_check}"
        print(f"Проверяем URL[{url}]")
        page.goto(url)
        screenshot_name = f"{url_for_check}|{skin}|{version}.png"
        page.screenshot(path=f"{settings.SCREENSHOTS_FILE_PATH}/{skin}/{screenshot_name}", full_page=True)

def add_new_mobile_cookies(page: Page):
    cookie_1: SetCookieParam = {
        "name": "__DEV_bcm_enable_spa_whitelist",
        "value": "1",
        "domain": ".bonga14.com",
        "path": "/",
    }
    cookie_2: SetCookieParam = {
        "name": "bcm",
        "value": "1",
        "domain": ".bonga14.com",
        "path": "/"
    }
    page.context.add_cookies([cookie_1, cookie_2])

def check_new_mobile_transfer(page,url: str):
    js_script = """
        () => {
            const isReact = typeof window.jQuery == 'undefined';
            return isReact;
        }
    """
    is_new_version = page.evaluate(js_script)
    contract_check = page.locator(".bcmBody").is_visible(timeout=5000)  # bcmbody определен как контракт
    if not is_new_version or not contract_check:
        text = (
            f"Переход на новую мобильную версию не подтвержден\n"
            f"Результаты проверок:\n"
            f"Контракт: {contract_check}\n"
            f"Функциональная: {is_new_version}\n"
            f"URL: {url}\n"
        )
        print(text)
    raise ValueError("Новая мобильная версия не подтверждена")