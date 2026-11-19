from playwright._impl._api_structures import SetCookieParam
from playwright.sync_api import Page

from config.settings import settings, BASE_DIR
from config.urls import IgnoredSkins, CheckedUrls
from utils.screenshot_gluer import glue_screenshot


def get_skins_list(page: Page):
    failed_skins = read_txt()
    failed_first = ""
    if failed_skins:
        while failed_first.lower().strip() not in ("н","y") and failed_first.lower().strip() not in ("т","n"):
            failed_first = input(f"Были обнаружены ошибки с прошлых проверок на скинах\n{''.join(failed_skins)}\n"
                                 f"Нажмите Y чтобы проверить только их или N чтобы начать проверку всех скинов:")
        if failed_first.lower().strip() in ("н","y"):
            skins = [s.strip("\n") for s in failed_skins]
            return skins
        elif failed_first.lower().strip() in ("т","n"):
            skins = get_skins_list_by_req(page)
            return skins
    else:
        skins = get_skins_list_by_req(page)
        return skins

def get_skins_list_by_req(page):
    req = page.request.get(settings.GROUPS_URL)
    req_json = req.json()
    skins = req_json.get("skins")
    if skins is None:
        print("Не было найдено ни одного скинхеда")
        raise ValueError
    skins = [key for key, value in skins.items() if key not in IgnoredSkins]
    print(f"Всего обнаружено скинов {len(skins)}\n"
          f"Список скинов: {'\n'.join(skins)}")
    return skins

def navigate_page(page: Page,url_skin: str,skin):
    try:
        cookie_warning_18: SetCookieParam = {
            "name": settings.CookieWarning18().name,
            "value": settings.CookieWarning18().value,
            "domain": ".bongacams.quest",
            "path": "/"
        }
        page.context.add_cookies([cookie_warning_18])
        page.goto(url_skin)
        if page.locator("body").is_visible(timeout=4000):
            page.evaluate(
                """() => {
                document.body.classList.add('no_popups');
            }"""
            )
    except Exception:
        print(f"Не удалось перейти на URL [{url_skin}]")
        write_txt(skin)
        return

def get_data(page: Page,skin: str):
    site_version = "OLD"
    old_paths = collect_screenshot(page,skin,site_version)
    site_version = "NEW"
    add_new_mobile_cookies(page)
    new_paths = collect_screenshot(page, skin, site_version)
    screenshots_paths = (zip(old_paths, new_paths))
    delete_new_mobile_cookies(page)
    for screenshots in screenshots_paths:
        glue_screenshot(screenshots[0],screenshots[1],skin)


def collect_screenshot(page: Page,skin: str,version: str) -> list:
    url_skin = f"{settings.SET_SKIN_URL}/{skin}"
    paths = []
    print(f"Проверяем {skin} - Версия {version}")
    navigate_page(page,url_skin,skin)
    for url_for_check in CheckedUrls:
        url = f"{settings.MAIN_URL}/{url_for_check}"
        navigate_page(page,url,skin)
        url_for_check = "listing" if url_for_check == CheckedUrls.MAIN_URL else url_for_check
        screenshot_name = f"{url_for_check}|{skin}|{version}.png"
        path_to_screenshot = f"{settings.SCREENSHOTS_FILE_PATH}/{skin}/{screenshot_name}"
        page.screenshot(path=path_to_screenshot, full_page=True)
        paths.append(path_to_screenshot)
    return paths



def add_new_mobile_cookies(page: Page):
    cookie_1: SetCookieParam = {
        "name": "__DEV_bcm_enable_spa_whitelist",
        "value": "1",
        "domain": ".bongacams.quest",
        "path": "/",
    }
    cookie_2: SetCookieParam = {
        "name": "bcm",
        "value": "1",
        "domain": ".bongacams.quest",
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
    raise ValueError("Новая мобильная версия не подтверждена")

def delete_new_mobile_cookies(page: Page):
    page.context.clear_cookies(name="__DEV_bcm_enable_spa_whitelist")
    page.context.clear_cookies(name="bcm")

def write_txt(text):
    with open(f"{BASE_DIR}/failed_urls.txt", 'a', encoding='utf-8') as f:
        f.write(f"{text}\n")

def read_txt():
    with open(f"{BASE_DIR}/failed_urls.txt", 'r', encoding='utf-8') as f:
        text = f.readlines()
        text = set(text)
    return text

def clean_txt_log():
    with open(f"{BASE_DIR}/failed_urls.txt", 'r', encoding='utf-8') as f:
        pass