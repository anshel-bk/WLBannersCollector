from PIL import Image

from config.settings import settings


def glue_screenshot(old: str, new: str,skin: str):
    img1 = Image.open(old)
    img2 = Image.open(new)
    route_name = old.split("/")[-1].split("|")[0]
    width = img1.width + img2.width
    height = max(img1.height, img2.height)
    result = Image.new("RGB", (width, height), color=(255, 255, 255))
    result.paste(img1, (0, 0))
    result.paste(img2, (img1.width, 0))
    result.save(f"{settings.SCREENSHOTS_FILE_PATH}/{skin}/{route_name}_glue.jpg")

#
# glue_screenshot(img1=f"{settings.SCREENSHOTS_FILE_PATH}/bongacams/all_models|bongacams|OLD.png",
#                 img2=f"{settings.SCREENSHOTS_FILE_PATH}/bongacams/all_models|bongacams|NEW.png")