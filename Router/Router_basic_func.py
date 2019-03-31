from utils import get_response
from utils import templates
from Router import session_get_user

def get_index(Request):
    user = session_get_user(Request)
    if user is not None:
        body = templates(Request, username=user.get_username())
    else:
        body = templates(Request, username="游客")
    return get_response(body)

