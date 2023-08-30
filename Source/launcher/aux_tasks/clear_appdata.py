import launcher.aux_tasks._logic
import urllib.request
import util.resource
import util.versions
import util.const
import os.path
import os


class obj_type(launcher.aux_tasks._logic.action):
    def check_host(path: str):
        with open(path, 'rb', newline='\0') as f:
            f.seek(12)
            return f.readline()

    def perform(self):
        os.listdir()
