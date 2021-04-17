from PIL import Image, ImageDraw, ImageFont, ImageFilter
from random import randint


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

    # Generate 7 wrong captcha answers
    wrong_answers = []
    for _ in range(7):
        wrong_answers.append(gen_wrong_answer())
    
    width = 120 * 4
    height = 120
    correct_answer = ""
    font = ImageFont.truetype("assets/arial.ttf", 90)
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
                (120 * t + 32, 3),
                letter,
                font=font,
                fill=rndColor2()
                )
    image = image.filter(ImageFilter.BLUR)
    image.save(file, 'jpeg')
    return [file, correct_answer, wrong_answers]
