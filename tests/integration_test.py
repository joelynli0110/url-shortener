from base64 import encode
import unittest

import os
import sys
sys.path.append(os.path.join(os.getcwd(),'..'))

from src.shorten_url import encode_url,decode_url, get_server
from src.cache import get_from_cache, delete_from_cache
from src.app_server import AppServer

class TestUrlComplex(unittest.TestCase):

    def test_enc_doc_mapping(self):
        """Test if the same url is returned after encoding and decoding"""
        urla = 'http://www.google.com'
        urlb = 'https://codesubmit.io/library/react'

        short_a = encode_url(urla,1)
        short_b = encode_url(urlb,1)

        decode_a = decode_url(short_a)
        decode_b = decode_url(short_b)

        self.assertEqual(urla,decode_a)
        self.assertEqual(urlb,decode_b)

    def test_uniqueness_of_mapping(self):
        """Test if the same short id is returned once we start a second encoding phase"""
        url = 'https://codesubmit.io/library/react'
        short_a = encode_url(url,1)
        short_b = encode_url(url,1)

        self.assertEqual(short_a,short_b)

    def test_successful_storing(self):
        """Test if the mapping is stored into the cache after encoding"""
        url = 'https://codesubmit.io/library/react'
        short_id = encode_url(url,1)
        
        self.assertEqual(get_from_cache(url),short_id)
        self.assertEqual(get_from_cache(short_id),url)

    def test_counter_increment(self):
        """Test if the counter increases after a new encoding"""
        server = get_server(1)
        zk_counter = server.counter.zk_counter
        pre_value = zk_counter.value

        url = 'https://codesubmit.io/library/reactd'
        if get_from_cache(url) is not None:
            # ensure a new encoding as input: if the url already exists, then delete it
            delete_from_cache(url)
        encode_url(url,1) 
        value = zk_counter.value
        
        self.assertEqual(value, (pre_value + 1))

    def test_counter_no_increment(self):
        """Test if the counter will not increase after an encoding of an existing url"""
        server = get_server(1)
        zk_counter = server.counter.zk_counter

        url = 'https://codesubmit.io/library/reactqb'
        encode_url(url,1) 
        pre_value = zk_counter.value

        encode_url(url,1)
        value = zk_counter.value
        
        self.assertEqual(value, pre_value)



if __name__ == '__main__':
    unittest.main()