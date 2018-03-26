import os

class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY", "some-super-duper-secret-key")
    UPLOAD_FOLDER = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), 
        "app",
        "tmp", 
        "ical_files")
    MAX_CONTENT_PATH = 100000