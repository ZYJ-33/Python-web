from Model.TW import TW
from Model.User import User
from utils import templates
from Router import get_response
from Router import session_get_user
from utils import json_resp
from utils import slog
from Router import redirect

def TW_index(Request):
    body = templates(Request)
    return get_response(body)


def TW_add(Request):
    user = session_get_user(Request)
    para = Request.get_para()
    para["userid"] = user.get_id()
    para["username"] = user.get_username()
    t = TW(para)
    t.save()
    para["id"] = t.get_id()
    body = json_resp(para)
    return get_response(body)

def TW_all(Request):
    ds = TW.find_all()
    for d in ds:
       user = User.find_by(id = d["userid"])[0]
       username = user["username"]
       d["username"] = username
    body = json_resp(ds)
    return get_response(body)


def TW_del(Request):
    para = Request.get_para()
    id = para["id"]
    id = id[5:]
    id = int(id)
    TW.todelete(id=id)
    body = json_resp(para)
    return get_response(body)


def TW_edit(Request):
    para = Request.get_para()
    id = para.get("id", None)
    if id is None:
        return redirect('/TW')
    '''
    if Request.get_method() == "GET":
        dl = TW.find_by(id=id)
        tw = dl[0].get("tw")
        body = templates(Request, tw=tw, id=id)
        return get_response(body)
    '''
    if Request.get_method() == "POST":
        tw = para.get("tw")
        slog("In edit", tw, id)
        TW.toupdate(tw=tw, id=id)
        body = json_resp(para)
        return get_response(body)



if __name__ == "__main__":
   pass