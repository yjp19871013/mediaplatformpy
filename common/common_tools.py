import random

import time


def generate_validation_code():
    random.seed(int(time.time()))
    code = random.randint(0, 999999)
    return '%06d' % code

