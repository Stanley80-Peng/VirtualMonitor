import os


class File(object):
    def __init__(self, path):
        self.name = str(path).split('/')[-1]
        self.mtime = os.path.getmtime(path)
