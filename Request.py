import json
import urllib.parse
from utils import slog



class Request(object):
    def __init__(self, request=''):
        self.method = "GET"
        self.path = ""
        self.raw_head = ""
        self.body = ""
        self.heads = {}
        self.para = {}
        self.cookies = {}
        self.para_list = []

        if request == '':
            return None

        line = request.split("\r\n", 1)
        method, path, version = line[0].split(" ", 2)
        self.method = method
        self.path = path

        self.raw_head, self.body = line[1].split("\r\n\r\n")
        self.set_heads()
        self.set_cookies()
        self.set_query()
        self.post_form()

    def set_cookies(self):
        cook = self.heads.get("Cookie", None)
        if cook is not None:
            kvs = cook.split("; ")
            for kv in kvs:
                try:
                    key, value = kv.split("=")
                except :
                    continue
                key = key.strip()
                value = value.strip()
                self.cookies[key] = value



    def set_query(self):
        if '?' in self.path:
            self.path, raw_query = self.path.split("?")
            query_list = raw_query.split("&")
            for query in query_list:
                key, value = query.split("=")
                key = urllib.parse.unquote(key)
                value = urllib.parse.unquote(value)
                self.para[key] = value

    def post_form(self):
        if len(self.body) > 0:
            content_type = self.heads['Content-Type']
            content_type = content_type.strip()
            if content_type == 'application/json':
                d = json.loads(self.body)
                if type(d) is dict:
                    self.para.update(d)
                elif type(d) is list:
                    self.para_list = d

                else:
                    raise Exception

            else:
                slog(self.heads['Content-Type'])
                key_value = self.body.split("&")
                for thing in key_value:
                    key, value = thing.split("=")
                    key = urllib.parse.unquote(key)
                    value = urllib.parse.unquote(value)
                    self.para[key] = value

    def set_heads(self):
        heads = self.raw_head.split("\r\n")
        for head in heads:
            key, value = head.split(":", 1)
            self.heads[key] = value

    def get_para(self):
        return self.para

    def get_paralist(self):
        return self.para_list

    def get_header(self):
        return self.heads

    def get_path(self):
        return self.path

    def get_method(self):
        return self.method

    def get_cookies(self):
        return self.cookies
