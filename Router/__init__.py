from utils import slog
from utils import get_session_code
session = {}

def session_get_user(Request):
    cookies = Request.get_cookies()
    session_code = cookies.get("session_code", None)
    user = session.get(session_code, None)
    return user


def user_get_session_code(user):
    session_code = get_session_code()
    session[session_code] = user
    return session_code


def redirect(path):
    header = {
        "Location": path,
    }
    slog("redirect: ", header["Location"])
    return get_response(None, code=302, extra_headers=header)


def Response_header_with_code(Header, code=200):
    header = "HTTP1.1 {} xxx\r\n".format(code)
    header += "\r\n".join(["{}: {}".format(k, v) for k, v in Header.items()])
    return header + "\r\n"


def error(Request, code=404):
    body = "<h1>NOT FOUND</h1>"
    code = 404
    return get_response(body,code=404)


def get_response(body, code=200, extra_headers={}):
    headers = {
        "Content-Type": "text/html",
    }
    if len(extra_headers) > 0:
        headers.update(extra_headers)
    header = Response_header_with_code(headers, code)
    if body is None:
        body = ""
    return (header + "\r\n" + body).encode("utf-8")



def check_login2(func):
    def f(Request):
        cook = Request.get_cookies()
        try:
            session_code = cook["session_code"]
            user = session[session_code]
        except KeyError:
            return redirect("/login")
        return func(Request)
    return f


