# -*- coding: UTF-8 -*-
# SPDX-License-Identifier: 0BSD

"""ElJef Data Encoding and Hashing Testing"""

import logging
import os
import tempfile
import unittest

from eljef.core import hash

logging.disable(logging.ERROR)


def _get_file() -> str:
    data = '''some data
    some more data
    even more data
    '''
    fd, path = tempfile.mkstemp(None, None, tempfile.gettempdir(), True)
    os.write(fd, data.encode('UTF-8'))
    os.close(fd)

    return path


class TestEncodeBase64(unittest.TestCase):
    def test_encode_base64(self):
        want = "c29tZSBkYXRhCiAgICBzb21lIG1vcmUgZGF0YQogICAgZXZlbiBtb3JlIGRhdGEKICAgIA=="

        path = _get_file()
        got = hash.encode_base64(path)
        os.remove(path)

        self.assertEqual(want, got)

    def test_encode_base64_file_does_not_exist(self):
        self.assertRaises(FileNotFoundError, hash.encode_base64,
                          os.path.join(tempfile.gettempdir(), "hopefully_this_file_does_not_exist"))

    def test_encode_base64_path_is_directory(self):
        self.assertRaises(IsADirectoryError, hash.encode_base64, tempfile.gettempdir())


class TestHashMD5(unittest.TestCase):
    def test_hash_md5(self):
        want = "6ab7331490715d56be198f0e0c6079cb"

        path = _get_file()
        got = hash.hash_md5(path)
        os.remove(path)

        self.assertEqual(want, got)

    def test_hash_md5_file_does_not_exist(self):
        self.assertRaises(FileNotFoundError, hash.hash_md5,
                          os.path.join(tempfile.gettempdir(), "hopefully_this_file_does_not_exist"))

    def test_hash_md5_path_is_directory(self):
        self.assertRaises(IsADirectoryError, hash.hash_md5, tempfile.gettempdir())


class TestHashSHA256(unittest.TestCase):
    def test_hash_sha256(self):
        want = "d94eb4cb7687832a9115cdfbea0bec0e0006dc2ec518531127d2426ac7d7c276"

        path = _get_file()
        got = hash.hash_sha256(path)
        os.remove(path)

        self.assertEqual(want, got)

    def test_hash_sha256_file_does_not_exist(self):
        self.assertRaises(FileNotFoundError, hash.hash_sha256,
                          os.path.join(tempfile.gettempdir(), "hopefully_this_file_does_not_exist"))

    def test_hash_sha256_path_is_directory(self):
        self.assertRaises(IsADirectoryError, hash.hash_sha256, tempfile.gettempdir())


class TestHashSHA512(unittest.TestCase):
    def test_hash_sha512(self):
        want = "d0dc6749ab8d63d5c1e3d19153150755beca1bec0b1ce14b6f8d1c36ceae4" \
               "ed9f0f398428187d7dbd17af7f72d27ad4fb83cc15270dec24c1a91444e9443402b"

        path = _get_file()
        got = hash.hash_sha512(_get_file())
        os.remove(path)

        self.assertEqual(want, got)

    def test_hash_sha512_file_does_not_exist(self):
        self.assertRaises(FileNotFoundError, hash.hash_sha512,
                          os.path.join(tempfile.gettempdir(), "hopefully_this_file_does_not_exist"))

    def test_hash_sha512_path_is_directory(self):
        self.assertRaises(IsADirectoryError, hash.hash_sha512, tempfile.gettempdir())


if __name__ == '__main__':
    unittest.main()
