from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint
import speedtest
import aiohttp


def generate_captcha():
    # Generate one letter
    def gen_letter():
        return chr(randint(65, 90))

    def rndColor():
        return (randint(64, 255), randint(64, 255), randint(64, 255))

    def rndColor2():
        return (randint(32, 127), randint(32, 127), randint(32, 127))

    # Generate a 4 letter word
    def gen_wrong_answer():
        word = ""
        for _ in range(4):
            word += gen_letter()
        return word

    # Generate 8 wrong captcha answers
    wrong_answers = []
    for _ in range(8):
        wrong_answers.append(gen_wrong_answer())

    width = 80 * 4
    height = 100
    correct_answer = ""
    font = ImageFont.truetype("assets/arial.ttf", 55)
    file = f"assets/{randint(1000, 9999)}.jpg"
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)

    # Draw random points on image
    for x in range(width):
        for y in range(height):
            draw.point((x, y), fill=rndColor())

    for t in range(4):
        letter = gen_letter()
        correct_answer += letter
        draw.text(
            (60 * t + 50, 15),
            letter,
            font=font,
            fill=rndColor2()
        )
    image = image.filter(ImageFilter.BLUR)
    image.save(file, 'jpeg')
    return [file, correct_answer, wrong_answers]


async def test_speedtest():
    def speed_convert(size):
        power = 2 ** 10
        zero = 0
        units = {0: "", 1: "Kb/s", 2: "Mb/s", 3: "Gb/s", 4: "Tb/s"}
        while size > power:
            size /= power
            zero += 1
        return f"{round(size, 2)} {units[zero]}"
    speed = speedtest.Speedtest()
    info = speed.get_best_server()
    download = speed.download()
    upload = speed.upload()
    return [speed_convert(download), speed_convert(upload), info]


async def file_size_from_url(url: str) -> int:
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as resp:
            size = int(resp.headers['content-length'])
    return size


async def get_http_status_code(url: str)-> int:
    async with aiohttp.ClientSession() as session:
        async with session.head(url) as resp:
            return resp.status
