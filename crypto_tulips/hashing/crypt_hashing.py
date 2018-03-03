"""
Hashing Module
"""

import hashlib
import json


class Hashing:
    """
    The Hashing Class that has static methods to help with different type of hashing
    """

    @staticmethod
    def hashing_block(json_block):
        """ Generates and returns a sha256 hash

        Keyword arugments:
        json_block -- JSON string

        Returns:
        string -- Returns the sha256 hash of the JSON string provided
        """
        return hashlib.sha256((json.dumps(json_block)).encode('utf-8')).hexdigest()
