import unittest
import os
import sys
sys.path.append(os.path.join(os.getcwd(),'..'))

from src.shorten_url import encode_url, is_valid_url, is_valid_id

class TestUrlBasics(unittest.TestCase):

    def test_encoded_length(self):
        """Test if the encoded hash value has the expected length"""

        urla = 'http://www.google.com'
        urlb = 'https://codesubmit.io/library/react'
        
        for _ in range(5):
            short_a = encode_url(urla,1)
            short_b = encode_url(urlb,1)

            self.assertEqual(4, len(short_a))
            self.assertEqual(4, len(short_b))
    
    def test_short_id_valid(self):
        """Test if the short id to be decoded is valid"""
        id1 = '4c90'
        id2 = '/324'

        self.assertTrue(is_valid_id(id1))
        self.assertFalse(is_valid_id(id2))

    def test_url_with_https_valid(self):
        url = 'https://codesubmit.io/library/react'

        self.assertTrue(is_valid_url(url))

    def test_url_without_protocol_not_valid(self):
        url = 'www.codesubmit.io/library/react'

        self.assertFalse(is_valid_url(url))

    def test_empty_url_not_valid(self):
        self.assertFalse(is_valid_url(''))

if __name__ == '__main__':
    unittest.main()