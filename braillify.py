from PIL import Image
import sys, os, pathlib


class termcolor:
    OKGREEN = "\033[92m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"


class braille_config:
    # 2 * 3 braille
    base = 0x2800
    width = 2
    height = 3


hex_threshold = 128


def resize(image: Image.Image, width: int, height: int) -> Image.Image:
    if height == 0:
        height = int(im.height / im.width * width)
    if height % braille_config.height != 0:
        height = int(braille_config.height * (height // braille_config.height))
    if width % braille_config.width != 0:
        width = int(braille_config.width * (width // braille_config.width))
    return image.resize((width, height))


def grayscale(red: int, green: int, blue: int) -> int:
    return int(0.2126 * red + 0.7152 * green + 0.0722 * blue)


for file in sys.argv[1:]:
    normalized_path = os.path.abspath(file)
    if not pathlib.Path(normalized_path).exists():
        print(termcolor.FAIL + "× " + termcolor.ENDC + normalized_path)
        continue
    basename = os.path.basename(normalized_path)
    dirname = os.path.dirname(normalized_path)
    im = Image.open(normalized_path)

    # (image, weight, height). 0 as height means auto
    resized_image = resize(im, 300, 0)
    resized_image.save(dirname + "/new.png")

    px = resized_image.load()
    answer = ""
    for h in range(0, resized_image.height, braille_config.height):
        for w in range(0, resized_image.width, braille_config.width):
            braille = [False] * braille_config.width * braille_config.height
            for local_w in range(braille_config.width):
                for local_h in range(braille_config.height):
                    r, g, b, *rest = px[w + local_w, h + local_h]  # ignore alpha
                    if grayscale(r, g, b) > hex_threshold:
                        braille[local_w * braille_config.height + local_h] = True
            output = braille_config.base
            for idx, val in enumerate(braille):
                if val:
                    output += 2 ** idx
            answer += chr(output)
        answer += "\n"
    print(answer)
