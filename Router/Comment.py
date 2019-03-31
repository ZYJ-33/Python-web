from utils import templates
from Router import get_response
from Router import session_get_user
from utils import json_resp
from utils import slog
from Router import redirect
from Model.Comment import Comment
from Model.TW import TW
'''
self.comment = para.get("comment", None)
        self.userid = para.get("userid", None)
        self.twid = para.get("twid", None)

        self.inittime = para.get("inittime", None)
        self.id = para.get("id", None)
'''

def TW_comment(Request):
    '''
    if Request.get_method() == "POST":
        user = session_get_user(Request)
        para["userid"] = user.get_id()
        para["username"] = user.get_username()
        c = Comment(para)
        c.save()
        body = json_resp(para)
        get_response(body)
    '''
    if Request.get_method() == "GET":
        para = Request.get_para()
        id = para.get("id", None)
        if id is not None:
            tw_list = TW.find_by(id=id)
            tw = tw_list[0]
            body = templates(Request, tw=tw.get("tw"), id = tw.get("id"))
            return get_response(body)
        else:
           return  redirect("/TW")


def TW_comment_all(Request):
    respdict={}
    paralist = Request.get_paralist()
    slog("TW_comment_all", paralist)
    for para in paralist:
        id = para.get("id")
        cl = Comment.find_by_twid(int(id[5:]))
        respdict[id] = cl
    body = json_resp(respdict)
    slog(body)
    return get_response(body)

def get_pack(para):
    li = []
    li.append(para)
    dl = {
        para["twid"]: li,
    }
    return dl


def TW_comment_add(Request):
    para = Request.get_para()
    user = session_get_user(Request)
    tem = ""
    para["userid"] = user.get_id()
    para["username"] = user.get_username()
    if para["twid"][0:5] == "span-":
        tem = para["twid"]
        para["twid"] = int(para["twid"][5:])
    c = Comment(para)
    c.save()
    para["id"] = c.get_id()
    para["twid"] = tem
    dl = get_pack(para)
    body = json_resp(dl)
    return get_response(body)


def TW_comment_del(Request):
    para = Request.get_para()
    id = para.get("id", None)
    if id is not None:
        Comment.todelete(id=int(id[8:]))
        body = json_resp(para)
        return get_response(body)
    return redirect('/TW')




