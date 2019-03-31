from Model.User import User
from utils import slog
from utils import redirect
from Router import user_get_session_code
from utils import templates
from Router.Router_basic_func import get_response
import Router


def register(Request):
    para = Request.get_para()
    if Request.get_method() == 'POST':
        u = User(para)
        if u.register():
            return redirect("/login")
        return redirect("/register")
    elif Request.get_method() == 'GET':
        body = templates(Request)
        return get_response(body)

def login(Request):
    if Request.get_method() == 'POST':
        para = Request.get_para()
        li = User.login(para)
        if len(li)>0:
            u = User(li[0])
            session_code = user_get_session_code(u)
            headers = {
                "Set-Cookie":"session_code={}".format(session_code)
            }
            return redirect("/TW", extra_headers=headers)
        else:
            return redirect("/login")
    elif Request.get_method() == 'GET':
        body = templates(Request)
        return get_response(body)
