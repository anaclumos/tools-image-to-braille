from PIL import Image
from typing import Union
import sys, os, pathlib


class termcolor:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


config = {"width": 100, "height": "auto"}


def resize(image: Image.Image, width: int, height: Union[int, str]) -> Image.Image:
    if height == "auto":
        height = int((im.height / im.width) * width)
    return image.resize((width, height))


for file in sys.argv[1:]:
    normalized_path = os.path.abspath(file)
    if not pathlib.Path(normalized_path).exists():
        print(termcolor.FAIL + "× " + termcolor.ENDC + normalized_path)
        continue
    basename = os.path.basename(normalized_path)
    dirname = os.path.dirname(normalized_path)
    im = Image.open(normalized_path)
    print(im.filename)
    print(im.size)
    print(im.width, im.height)
    newimage = resize(im, 600, "auto")
    newimage.save(dirname + "/new.png")
