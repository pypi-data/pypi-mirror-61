import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

import requests
from prutils.pr_string import get_re_last
from prutils.pr_url import get_url_param_dict


class YDTK:
    def __init__(self, shared_url):
        self.shared_url = shared_url
        self.pre_init()

    def pre_init(self):
        pass

    def get_shared_id(self):
        return get_url_param_dict(self.shared_url)["id"]

    def get_last_img_url(self):
        url = "https://note.youdao.com/yws/public/note/" + self.get_shared_id()
        r = requests.get(url)
        j = r.json()
        return get_re_last('<img data-media-type="image" src="(.*?)".*?>', j["content"])


def ydtk():
    yd_tk_doc_url = sys.argv[1]
    ydtk = YDTK(yd_tk_doc_url)
    print(ydtk.get_last_img_url(), end="")

def main():
    ydtk()
    # os.system("pause")


if __name__ == '__main__':
    main()