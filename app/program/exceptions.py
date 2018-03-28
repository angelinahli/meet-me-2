"""
desc: Define some exceptions to show
"""

class FlashException(Exception):
    """Class of exceptions that are flashed to user"""
    def __init__(self, message, category):
        self.message = message
        self.category = category