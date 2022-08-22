import copy
import datetime
from random import Random, randint

visa_prefix = [
    ['4', '5', '3', '9'],
    ['4', '5', '5', '6'],
    ['4', '9', '1', '6'],
    ['4', '5', '3', '2'],
    ['4', '9', '2', '9'],
    ['4', '0', '2', '4', '0', '0', '7', '1'],
    ['4', '4', '8', '6'],
    ['4', '7', '1', '6'],
    ['4']]

mastercard_prefix = [
    ['5', '1'], ['5', '2'], ['5', '3'], ['5', '4'], ['5', '5']]

amex_prefix = [['3', '4'], ['3', '7']]


def expiration_date_generator() -> datetime.date:
    """
    Returns an expiration date of 5 years from now
    """
    today = datetime.date.today()
    expiration = today + datetime.timedelta(days=(365 * 5))
    return expiration


def completed_number(prefix, length) -> str:
    """
    'prefix' is the start of the CC number as a string, any number of digits.
    'length' is the length of the CC number to generate. Typically, 13 or 16
    """
    generator = Random()
    generator.seed()

    cc_number = prefix

    # generate digits

    while len(cc_number) < (length - 1):
        digit = str(generator.choice(range(0, 10)))
        cc_number.append(digit)

    # Calculate sum

    _sum = 0
    pos = 0

    reversed_cc_number = []
    reversed_cc_number.extend(cc_number)
    reversed_cc_number.reverse()

    while pos < length - 1:

        odd = int(reversed_cc_number[pos]) * 2
        if odd > 9:
            odd -= 9

        _sum += odd

        if pos != (length - 2):
            _sum += int(reversed_cc_number[pos + 1])

        pos += 2

    # Calculate check digit

    checkdigit = ((_sum / 10 + 1) * 10 - _sum) % 10

    cc_number.append(str(checkdigit))

    return ''.join(cc_number)


def generate_card_number(card_brand="VISA"):
    """
    Generates a credit card number of the given brand and length.
    """
    rd = Random()
    rd.seed()

    prefix_list = []
    length = 16

    match card_brand:
        case "AMEX":
            length = 15
            prefix_list = amex_prefix
        case "MASTERCARD":
            prefix_list = mastercard_prefix
        case "VISA":
            prefix_list = visa_prefix

    cc_number = copy.copy(rd.choice(prefix_list))
    number = str(int(float(completed_number(cc_number, length))))

    return number


def generate_cvv(length=3) -> str:
    """
    Generates a CVV of the given length.
    """
    cvv = ""
    i = 0

    while i < length:
        cvv = cvv + str(randint(0, 9))
        i += 1

    return cvv
