import random


async def random_line(fname):
    return random.choice(open(fname).read().splitlines())
