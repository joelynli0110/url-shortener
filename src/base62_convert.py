"""Encoding and decoding of BASE62"""

BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' 
BASE_LENGTH = len(BASE62)

def base62_encode(num):
    """Encode a positive number into a Base62 string

    Arguments:
    - num (int): The number to encode

    Returns:
    - str (String): The resulted string of Base62 encoding
    """
    str = ''
    while num > 0:
        num, idx = divmod(num,BASE_LENGTH)
        str = BASE62[idx] + str
    return str

def base62_decode(str):
    """Decode a Base62 encoded string into a positive number

    Arguments:
    - str (String): The Base62 string to decode
    
    Returns:
    - num: The value that decoded from a Base62 encoded string
    """
    num = 0
    for char in str:
        num = num * BASE_LENGTH + BASE62.find(char)
    return num