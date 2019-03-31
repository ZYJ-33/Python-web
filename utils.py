import time
from jinja2 import FileSystemLoader, Environment
from random import randint
import os.path
import json


def log(*args, **kargs):
    format = "%y\%m\%d %H:%M:%S"
    value = time.localtime(int(time.time()))
    ti_me = time.strftime(format, value)
    with open('log.txt', 'a+', encoding="utf-8") as f:
        print(ti_me+":  ", file=f, *args, **kargs)


def slog(*args, **kargs):
    format = "%y\%m\%d %H:%M:%S"
    value = time.localtime(int(time.time()))
    ti_me = time.strftime(format, value)
    print(ti_me+":  ", *args, **kargs)


path = "{}/templates".format(os.path.dirname(__file__))
loader = FileSystemLoader(path)
env = Environment(loader=loader)


def templates(Request, **kwargs):
    path = ""
    if Request.get_path() == "/":
        path += "/index.html"
    elif Request.get_path() == "/TW/edit":
        path += "TW_edit.html"
    elif Request.get_path() == "/TW/comment":
        path += "TW_comment.html"
    else:
        path += Request.get_path()
        if path[len(path) - 5:len(path)] != ".html":
            path += ".html"

    tmp = env.get_template(path)
    return tmp.render(**kwargs)


def get_session_code():
    seed = "vuhm6d9crd2oe3bx2cx1mxl3x2phc6701gcni3o"
    session_code = ""
    for i in range(16):
        index = randint(0, len(seed) - 1)
        session_code += seed[index]
    return session_code


def Response_header_with_code(Header, code=200):
    header = "HTTP1.1 {} xxx\r\n".format(code)
    header += "\r\n".join(["{}: {}".format(k, v) for k, v in Header.items()])
    log("the header" + header)
    return header + "\r\n"


def get_response(body, code=200, extra_headers={}):
    headers = {
        "Content-Type": "text/html",
    }
    if len(extra_headers) > 0:
        headers.update(extra_headers)
        log("In get_response ", extra_headers)
    header = Response_header_with_code(headers, code)
    if body is None:
        body = ""
    return (header + "\r\n" + body).encode("utf-8")


def redirect(path, extra_headers={}):
    header = {
        "Location": path,
    }
    if len(extra_headers) > 0:
        header.update(extra_headers)
    log("redirect: ", header["Location"])
    return get_response(None, code=302, extra_headers=header)


def json_resp(body):
    return json.dumps(body,ensure_ascii=False)

if __name__ == "__main__":
    pass
