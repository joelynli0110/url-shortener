from src.base62_convert import base62_encode, base62_decode
from src.cache import add_to_cache, get_from_cache
from src.app_server import AppServer

import re

server_list = []

REGEX = re.compile(
        r'^(?:http)s?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)

BASE62 = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' 


def get_server(server_id):
    """Get the server with the given server id"""
    for server in server_list:
        if server.id == server_id:
            return server
    # create a new server
    server = AppServer(server_id)
    server_list.append(server)
    return server

def is_valid_url(url):
    """Test if the given url is valid"""
    return re.match(REGEX,url)

def is_valid_id(short_id):
    """Test if the given short id is valid (with Base62 encoding algorithm)"""
    if len(short_id) != 4:
        return False
    for c in short_id:
        if c not in BASE62:
            return False
    return True

def encode_url(long_url, server_id):
    """Encode the long url to short url and add them in the cache
    
    Arguments:
    - long_url (String): The given original url
    - server_id: The id of the server that requests a url-shorten service
    
    """
    # check if the long url is already stored in the memory
    if get_from_cache(long_url) is not None:
        return get_from_cache(long_url)
    app_server = get_server(server_id)
    # encode into Base62
    zk_counter = app_server.counter.zk_counter
    short_id = base62_encode(zk_counter.value)
    # update the counter value
    app_server.counter.add()
    # put the mapping into the cache
    add_to_cache(long_url, short_id)
    return short_id

def decode_url(short_id):
    """Decode the short url into long url, if long url does not exist in the cache
    
    Arguments:
    - short_id (String): The id of the short url to be decoded
    
    """
    # look up in the cache
    if get_from_cache(short_id) is None:
        # decode the url
        long_url = base62_decode(short_id)
        add_to_cache(long_url,short_id)
        return long_url
    else:
        return get_from_cache(short_id)
